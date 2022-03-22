from django.conf.urls import url
from main.consumers import ChatConsumer, GroupChatConsumer

websocket_urlpatterns = [
    url(r'^ws/conversation/(?P<id>\w+)/$', ChatConsumer.as_asgi()),
    url(r'^ws/group/(?P<id>\w+)/$', GroupChatConsumer.as_asgi())
]
