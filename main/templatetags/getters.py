from django import template
from django.db.models import Q

register = template.Library()

@register.filter(name="get_name")
def get_name(conversation, user):
    return conversation.get_name(user)

@register.filter(name="get_image")
def get_image(conversation, user):
    return conversation.get_image(user)

@register.filter(name="get_id")
def get_id(conversation, user):
    return conversation.get_id(user)

@register.filter(name="get_unread_messages")
def get_unread_messages(conversation, user):
    uunread_messages_count = conversation.messages.filter(~Q(read_by__in=[user])).count()
    return uunread_messages_count