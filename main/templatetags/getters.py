from django import template

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