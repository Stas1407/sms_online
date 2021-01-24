from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import UserRegisterForm
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.contrib.auth import authenticate, login

# Create your views here.
def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid() and len(User.objects.filter(email=form.cleaned_data.get('email'))) == 0:
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
        if '@' in email and "<script>" not in email.lower() and len(User.objects.filter(email=email)) == 0:
            request.user.email = email
            request.user.save()
            return HttpResponse()
        else:
            return HttpResponse("Wrong email", status=400)
    else:
        raise Http404()

def change_image(request):
    if request.method == "POST" and request.FILES['img_input']:
        image = request.FILES['img_input']
        allowed = ['jpg', 'jpeg', 'png']
        if image.name.split('.')[-1] in allowed:
            request.user.profile.image = image
            request.user.profile.save()
            print(request.user.profile.image)
            return HttpResponseRedirect('/profile')
        else:
            return HttpResponse("Wrong image", status=400)
    else:
        raise Http404()

def change_password(request):
    if request.method == "POST":
        if request.POST.get('new_password') and request.POST.get('old_password'):
            old_password = request.POST.get('old_password')
            if request.user.check_password(old_password):
                username = request.user.username
                new_password = request.POST.get('new_password')
                request.user.set_password(new_password)
                request.user.save()
                
                user = authenticate(request, username=username, password=new_password)
                if user is not None:
                    login(request, user)
                return HttpResponse()
            else:
                return HttpResponse("Wrong password", status=400)
        elif request.POST.get('old_password'):
            old_password = request.POST.get('old_password')
            if request.user.check_password(old_password):
                return HttpResponse()
            else:
                return HttpResponse("Wrong password", status=400)
        else:
            raise Http404()
    else:
        raise Http404()

def change_adding_to_groups(request):
    if request.method == "POST" and request.POST.get('switch'):
        setting = request.user.userchoices.everyone_can_add_to_group
        request.user.userchoices.everyone_can_add_to_group = not setting
        request.user.userchoices.save() 
        return HttpResponse()
    else:
        raise Http404()
