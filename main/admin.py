from django.contrib import admin
from main.models import *

# Register your models here.
admin.site.register(Message)
admin.site.register(Group)
admin.site.register(Conversation)
admin.site.register(Unread_messages)
