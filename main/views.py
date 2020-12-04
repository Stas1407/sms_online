from django.shortcuts import render, redirect

# Create your views here.
def home(request):
    context = {'title': 'home'}
    return render(request,'main/home.html', context)

def landing_page(request):
    if request.user.is_authenticated:
        return redirect('home')
    return render(request, 'main/landing_page.html')
