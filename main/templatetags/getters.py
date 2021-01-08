from django import template

register = template.Library()

@register.filter(name="get_name")
def get_name(conversation, user):
    try:
        return conversation.name
    except AttributeError:
        for u in conversation.users.all():
            if u != user:
                return u.username

@register.filter(name="get_image")
def get_image(conversation, user):
    try:
        return conversation.image.url
    except AttributeError:
        for u in conversation.users.all():
            if u != user:
                return u.profile.image.url