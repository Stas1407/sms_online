from django.shortcuts import render

# Create your views here.
def home(request):
    context = {'title': 'home'}
    return render(request,'main/home.html', context)

def landing_page(request):
    return render(request, 'main/landing_page.html')
