from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static 

urlpatterns = [
    path('', views.landing_page, name='landing_page'),
    path('home', views.home, name='home'),
    path('conversation/<int:id>', views.conversation, name="conversation"),
    path('new_conversation/<int:id>', views.new_conversation, name="new_conversation"),
    path('group/<int:id>', views.group, name="group"),
    path('new_group', views.new_group, name="new_group"),
    path('settings/<int:id>', views.settings, name="settings"),
    path('delete/<str:type>/<int:id>', views.delete, name="delete"),
    path('delete_message/<int:id>', views.delete_message, name="delete_message")
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)