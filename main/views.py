from django.shortcuts import render, redirect
from main.models import *
from operator import attrgetter

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
    context = {
        "conversations": sorted(request.user.conversation_set.all(), key=attrgetter('last_message_date'), reverse=True)
    }
    return render(request, 'main/new_group.html', context)

def settings(request):
    return render(request, 'main/new_group.html', {"settings": True})