from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static 

urlpatterns = [
    path('', views.landing_page, name='landing_page'),
    path('home', views.home, name='home'),
    path('chat_view', views.chat_view, name="chat_view"),
    path('new_group', views.new_group, name="new_group"),
    path('settings/<int:id>', views.settings, name="settings"),
    path('delete/<str:type>/<int:id>', views.delete, name="delete")
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)