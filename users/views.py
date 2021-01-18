from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import UserRegisterForm
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from django.http import HttpResponse, Http404

# Create your views here.
def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Your acount has been created! You are now able to login.')
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'form': form})

def profile(request):
    return render(request, 'users/profile.html')

def change_username(request):
    if request.method == "POST" and request.POST.get('username'):
        name = request.POST.get('username')
        if len(User.objects.filter(username=name)) == 0 and "<script>" not in name.lower() and len(name) < 20:
            request.user.username = name
            request.user.save()
            return HttpResponse()
        else:
            return HttpResponse("Username is taken or wrong (max username length is 20 characters)", status=400)
    else:
        raise Http404()

def change_email(request):
    if request.method == "POST" and request.POST.get('email'):
        email = request.POST.get('email')
        if '@' in email and "<script>" not in email.lower():
            request.user.email = email
            request.user.save()
            return HttpResponse()
        else:
            return HttpResponse("Wrong email", status=400)
    else:
        raise Http404()