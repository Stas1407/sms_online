from django.urls import path
from . import views

urlpatterns = [
    path('', views.landing_page, name='landing_page'),
    path('home', views.home, name='home'),
    path('chat_view', views.chat_view, name="chat_view"),
    path('new_group', views.new_group, name="new_group"),
    path('settings', views.settings, name="settings")
]
