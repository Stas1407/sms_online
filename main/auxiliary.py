from django.http import Http404

def get_messages(request, type, id):
    if type == "group":
        if len(request.user.group_set.filter(pk=id)) != 0:
            group = request.user.group_set.get(pk=id)
            messages_list = group.messages.all()
        else:
            raise Http404()
    elif type == "conversation":
        if len(request.user.conversations.filter(pk=id)) != 0:
            conv = request.user.conversations.get(pk=id)
            messages_list = conv.messages.all()
        else:
            raise Http404()

    return messages_list

def check_text(text):
    if len(text) == 0:
        return 'Please type in the message'
    elif "<script>" in text:
        return "Wrong message"
    return 0

def send_message(object, id, message):
    if len(object.filter(pk=id)) != 0:
        o = object.get(pk=id)
        o.messages.add(message)
        o.save()
    else:
        raise Http404()