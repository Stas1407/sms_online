from django.shortcuts import render, redirect
from main.models import *
from operator import attrgetter
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from django.http import HttpResponse, Http404
from django.contrib import messages
from itertools import chain
from main.auxiliary import *
from django.db.models import Q
import json

# Create your views here.
def home(request):
    context = {
        'title': 'home',
        "conversations": chain(request.user.conversations.all(), request.user.group_set.all())
    }
    return render(request,'main/home.html', context)

def landing_page(request):
    if request.user.is_authenticated:
        return redirect('home')
    return render(request, 'main/landing_page.html')

def conversation(request, id):
    if request.method == "POST":
        if request.POST.get('check'):
            c = request.user.conversations.filter(id=id)[0]
            if not c:
                raise Http404()
            messages = c.messages.filter(~Q(read_by__in=[request.user]))
            data = []

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
        send_message(request.user.conversations, id, m)

        return HttpResponse(m.id, status=200)
    
    messages_list = get_messages(request, "conversation", id)
    for i in range(1, len(messages_list)):
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

def group(request, id):
    if request.method == "POST":
        if request.POST.get('check'):
            c = request.user.group_set.get(id=id)
            messages = c.messages.filter(~Q(read_by__in=[request.user]))
            data = []

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
    
    messages_list = get_messages(request, "group", id)
    for i in range(1, len(messages_list)):
        if request.user in messages_list[-i].read_by.all():
            break
        else:
            messages_list[-i].read_by.add(request.user)

    group = get_object_or_404(Group, pk=id)
    conversation_list = sorted(chain(request.user.conversations.all(), request.user.group_set.all()), key=attrgetter('last_message.date_sent'), reverse=True)[:8]
    if group in conversation_list:
        conversation_list.remove(group)

    context = {
        'messages': messages_list,
        'first_conversation': group,
        'last_conversations': conversation_list,
        'is_group': True
    }


    return render(request, 'main/chat_view.html', context)

def new_group(request):
    if request.method == "POST":
        name = request.POST.get('group_name')
        g = Group()
        if "<script>" not in name.lower() and name:
            g.name = name
            g.save()
            try:
                allowed = ['jpg', 'jpeg', 'png']            
                if request.FILES['file_in'].name.split('.')[-1] in allowed:
                    g.image = request.FILES['file_in']
            except Exception:
                pass
            g.users.add(request.user)
        else:
            messages.error(request, "Wrong group name")
            context = {
                "conversations": request.user.conversations.all()
            }
            return render(request, 'main/new_group.html', context)

        ids = request.POST.get('ids').split(',')
        for user_id in ids:
            if user_id != '':
                user = get_object_or_404(User, pk=user_id)
                if check_if_connected(user, request.user):
                    g.users.add(user)

        server_message = Message.objects.create(text="Group was created", is_server_message=True)
        g.last_message = server_message
        g.messages.add(server_message)
        g.save()

        return HttpResponseRedirect('/home')
    
    context = {
        "conversations": request.user.conversations.all()
    }
    return render(request, 'main/new_group.html', context)

def settings(request, id):
    if request.method == "POST": 
        name = request.POST.get('group_name')
        g = request.user.group_set.get(pk=id)

        if "<script>" not in name.lower() and name:
            g.name = name
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
        for user_id in ids:
            if user_id != '':
                user = get_object_or_404(User, pk=user_id)
                g.users.remove(user)
        g.save()

        return HttpResponseRedirect('/home')

    if request.user.group_set.filter(pk=id).count() != 0:
        group = get_object_or_404(Group, pk=id)
        context = {
            "settings":True,
            "name": group.name,
            "image": group.image.url,
            "members": group.users.all()
        }
        return render(request, 'main/new_group.html', context)
    else:
        raise Http404()

def delete(request, id, type):
    if type == "group":
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

def delete_message(request, id):
    message = get_object_or_404(Message, pk=id)
    if message.author == request.user:
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
