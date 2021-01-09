from django.shortcuts import render, redirect
from main.models import *
from operator import attrgetter
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from django.http import HttpResponse

# Create your views here.
def home(request):
    context = {
        'title': 'home'
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
        if request.POST.get('group_name'):
            name = request.POST.get('group_name')
            g = Group()
            if "<script>" not in name.lower():
                g.name = name
                g.users.add(request.user)
                g.save()
            else:
                return HttpResponse("Wrong group name", status=406)

        if request.POST.getlist('ids[]'):
           ids = request.POST.getlist('ids[]')
           for user_id in ids:
                user = get_object_or_404(User, pk=user_id)
                if user.conversations.filter(user2=request.user):
                    print('check')

        return HttpResponseRedirect('/chat_view')
    
    context = {
        "conversations": sorted(request.user.conversations.all(), key=attrgetter('last_message_date'), reverse=True)
    }
    return render(request, 'main/new_group.html', context)

def settings(request):
    return render(request, 'main/new_group.html', {"settings": True})