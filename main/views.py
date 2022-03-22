from django.shortcuts import render, redirect
from main.models import *
from users.models import UserChoices
from operator import attrgetter
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from django.http import HttpResponse, Http404
from django.contrib import messages
from itertools import chain
from main.auxiliary import *
from django.db.models import Q
from django.db.models import Count
import json
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required
def home(request):
    # If user searches for something send him search results
    if request.GET.get('search'):
        search = request.GET.get('search')
        # Get other users that match the search and remove from the list current user
        data = User.objects.filter(username__contains=search).exclude(username=request.user.username)

        context = {
            'title': 'Home',
            "users": data
        }
        return render(request,'main/home_search.html', context)
        
    context = {
        'title': 'Home',
        "conversations": list(chain(request.user.conversations.all(), request.user.group_set.all()))  
    }
    return render(request,'main/home.html', context)

def landing_page(request):
    if request.user.is_authenticated:
        return redirect('home')
    return render(request, 'main/landing_page.html')

@login_required
def conversation(request, id):
    # Get messages list and mark them as read by the user
    messages_list = get_messages(request, "conversation", id)
    for i in range(1, len(messages_list)+1):
        if request.user in messages_list[-i].read_by.all():
            break
        else:
            messages_list[-i].read_by.add(request.user)

    conv = get_object_or_404(Conversation, pk=id)
    conversation_list = sorted(chain(request.user.conversations.all(), request.user.group_set.all()), key=attrgetter('last_message.date_sent'), reverse=True)[:8]
    if conv in conversation_list:
        conversation_list.remove(conv)

    context = {
        'messages': messages_list,
        'first_conversation': conv,
        'last_conversations': conversation_list
    }

    return render(request, 'main/chat_view.html', context)

@login_required
def group(request, id):
    if request.method == "POST":
        # Check if request if automatic (Browser checks every 2 seconds for new messages)
        if request.POST.get('check'):
            c = request.user.group_set.get(id=id)
            messages = c.messages.filter(~Q(read_by__in=[request.user]))
            data = []

            # Mark all of the messages to send as read by the user
            for message in messages:
                message.read_by.add(request.user)
                message.save()
                data.append({'text':message.text, 'id':message.id, 'author':message.author.username})
            
            data = json.dumps(data)
            return HttpResponse(data, status=200)

        text = request.POST.get('message_text')
        
        check = check_text(text)
        if check:
            return HttpResponse(check, status=400)

        m = Message()
        m.author = request.user
        m.text = text
        m.save()
        m.read_by.add(request.user)
        
        send_message(request.user.group_set, id, m)
        return HttpResponse(m.id, status=200)
    
    # Get messages list and mark them as read by the user
    messages_list = get_messages(request, "group", id)
    for i in range(1, len(messages_list)):
        if request.user in messages_list[-i].read_by.all():
            break
        else:
            messages_list[-i].read_by.add(request.user)

    # Get groups with latest messages
    group = get_object_or_404(Group, pk=id)
    conversation_list = sorted(chain(request.user.conversations.all(), request.user.group_set.all()), key=attrgetter('last_message.date_sent'), reverse=True)[:8]
    if group in conversation_list:
        conversation_list.remove(group)  # Current group is passed separately as first_conversation

    context = {
        'messages': messages_list,
        'first_conversation': group,
        'last_conversations': conversation_list,
        'is_group': True
    }


    return render(request, 'main/chat_view.html', context)

@login_required
def new_conversation(request, id):
    user = get_object_or_404(User, pk=id)

    # Check if conversation doesn't already exists
    if not Conversation.objects.filter(users__in=[request.user]).filter(users__in=[user]):
        new_conversation = Conversation()
        new_conversation.save()
        new_conversation.users.add(request.user)
        new_conversation.users.add(user)

        m = Message()
        m.save()

        new_conversation.last_message = m        # Conversation must have a last message

        new_conversation.save()
    else:
        new_conversation = Conversation.objects.filter(users__in=[request.user]).filter(users__in=[user])[0]

    return HttpResponseRedirect('/conversation/'+str(new_conversation.id))
    
@login_required
def new_group(request):
    if request.method == "POST":
        name = request.POST.get('group_name')
        g = Group()

        # Check and save group name
        if "<script>" not in name.lower() and name:
            g.name = name
            g.save()

            # Check the group photo
            try:
                allowed = ['jpg', 'jpeg', 'png']            
                if request.FILES['file_in'].name.split('.')[-1] in allowed:
                    g.image = request.FILES['file_in']
            except Exception:
                pass

            # Add user who created group to its members
            g.users.add(request.user)
        else:
            messages.error(request, "Wrong group name")
            context = {
                "conversations": request.user.conversations.all()
            }
            return render(request, 'main/new_group.html', context)

        ids = request.POST.get('ids').split(',')
        # Add users who user selected to the group
        for user_id in ids:
            if user_id != '':
                user = get_object_or_404(User, pk=user_id)
                # if check_if_connected(user, request.user):        When creating profile do something with it
                g.users.add(user)

        server_message = Message.objects.create(text="Group was created", is_server_message=True)
        g.last_message = server_message
        g.messages.add(server_message)
        g.save()

        return HttpResponseRedirect('/group/'+str(g.id))
    
    # If user was searching for additional users pass search results to front-end
    if request.GET.get('search'):
        search = request.GET.get('search')
        context = {
            "title": "New group",
            "search": True,
            "members": User.objects.filter(username__contains=search).exclude(userchoices__everyone_can_add_to_group=False)
        }
    else:                
        context = {
            "title": "New group",
            "conversations": request.user.conversations.annotate(num_messages=Count('messages')).filter(num_messages__gte=2)
        }
    return render(request, 'main/new_group.html', context)

@login_required
def settings(request, id):
    if request.method == "POST":
        try:
            name = request.POST.get('group_name')
            g = request.user.group_set.get(pk=id)

            # Check group name and save it
            if "<script>" not in name.lower() and name:
                g.name = name

                # Check group image
                try:
                    allowed = ['jpg', 'jpeg', 'png']            
                    if request.FILES['file_in'].name.split('.')[-1] in allowed:
                        g.image = request.FILES['file_in']
                except Exception:
                    pass
            elif "<script>" in name.lower():
                messages.error(request, "Wrong group name")
                group = get_object_or_404(Group, pk=id)
                context = {
                    "settings":True,
                    "name": group.name,
                    "image": group.image.url,
                    "members": group.users.all()
                }
                return render(request, 'main/new_group.html', context)

            ids = request.POST.get('ids').split(',')
            # If user searched for new users he wants to add them to the group
            if request.GET.get('search'):
                for user_id in ids:
                    if user_id != '':
                        user = get_object_or_404(User, pk=user_id)
                        sMessage = Message()
                        sMessage.text = "User {} was added to the group".format(user.username)
                        sMessage.is_server_message = True
                        sMessage.save() 
                        g.users.add(user)
                        g.messages.add(sMessage)
            # else remove selected user from the group
            else:
                for user_id in ids:
                    if user_id != '':
                        user = get_object_or_404(User, pk=user_id)
                        sMessage = Message()
                        sMessage.text = "User {} was deleted from the group".format(user.username)
                        sMessage.is_server_message = True
                        sMessage.save() 
                        g.users.remove(user)
                        g.messages.add(sMessage)
            # If there aren't any users left in the group delete it
            if g.users.all().count() == 0:
                g.delete()
                return HttpResponseRedirect('/home')
            g.save()
        except Exception:
            context = {
                'title': 'Home',
                "conversations": list(chain(request.user.conversations.all(), request.user.group_set.all()))  
            }
            return render(request, "main/home.html", context)

        return HttpResponseRedirect('/group/'+str(g.id))

    # If the group exists pass to the front-end it's current settings
    if request.user.group_set.filter(pk=id).count() != 0:
        group = get_object_or_404(Group, pk=id)
        
        if request.GET.get('search'):
            search = request.GET.get('search')
            context = {
                "title": "Group settings",
                "settings":True,
                "search": True,
                "name": group.name,
                "image": group.image.url,
                "members": User.objects.filter(username__contains=search).exclude(userchoices__everyone_can_add_to_group=False).difference(group.users.all())
            }
        else:                
            context = {
                "title": "Group settings",
                "settings":True,
                "name": group.name,
                "image": group.image.url,
                "members": group.users.all()
            }
        return render(request, 'main/new_group.html', context)
    else:
        raise Http404()

@login_required
def delete(request, id, type):
    if type == "group":
        # User can't delete a group he can only leave it
        try: 
            g = request.user.group_set.get(pk=id)
            g.users.remove(request.user)
            g.save()
            if g.users.count() == 0:
                g.delete()
        except Exception:
            raise Http404()
    elif type == "conversation":
        try:
            c = request.user.conversations.get(pk=id)
            c.delete()
        except Exception:
            raise Http404()
    return HttpResponseRedirect('/home')

@login_required
def delete_message(request, id):
    message = get_object_or_404(Message, pk=id)

    # User can't delete other users messages
    if message.author == request.user:
        # if message is a latest message replace it to the older one
        if hasattr(message, "last_message_conversation"):
            c = message.last_message_conversation
            messages_list = c.messages.all().order_by('-date_sent')
            if len(messages_list) > 1:
                new_last_message = messages_list[1]
            else:
                new_last_message = None
            c.last_message = new_last_message
            c.save()
        if hasattr(message, "last_message_group"):
            g = message.last_message_group
            messages_list = g.messages.all().order_by('-date_sent')
            if len(messages_list) > 1:
                new_last_message = messages_list[1]
            else:
                new_last_message = None
            g.last_message = new_last_message
            g.save()
        message.delete()
    else:
        raise Http404()

    return HttpResponse("Deleted", status=200)
