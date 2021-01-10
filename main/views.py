from django.shortcuts import render, redirect
from main.models import *
from operator import attrgetter
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from django.http import HttpResponse, Http404
from django.contrib import messages
from itertools import chain

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

def chat_view(request):
    return render(request, 'main/chat_view.html')

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
                if user.conversations.filter(user2=request.user):
                    g.users.add(user)
        g.save()

        return HttpResponseRedirect('/chat_view')
    
    context = {
        "conversations": request.user.conversations.all()
    }
    return render(request, 'main/new_group.html', context)

def settings(request):
    return render(request, 'main/new_group.html', {"settings": True})

def delete(request, id, type):
    if type == "group":
        try: 
            g = request.user.group_set.get(pk=id)
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
