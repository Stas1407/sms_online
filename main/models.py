from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from PIL import Image
from django.urls import reverse

# Create your models here.

def check_path(instance, filename):
    return 'web-private/groups/{0}/{1}'.format(instance.id, filename.split('/')[-1])


class Message(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, default=None,null=True)
    text = models.CharField(max_length=200)
    date_sent = models.DateTimeField(default=timezone.now)
    is_server_message = models.BooleanField(default=False)
    read_by = models.ManyToManyField(User, related_name="read_message")

    def __str__(self):
        return "{}".format(self.text)    # Change before production

class Unread_messages(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    count = models.IntegerField()
 
class Conversation(models.Model):
    messages = models.ManyToManyField(Message, default=None)
    last_message = models.OneToOneField(Message, on_delete=models.PROTECT, default=None, null=True, related_name="last_message_conversation")
    unread_messages = models.ForeignKey(Unread_messages, on_delete=models.DO_NOTHING, default=None, null=True)
    users = models.ManyToManyField(User, related_name="conversations")
    is_group = False

    def __str__(self):
        return "{0} - {1}".format(self.users.all()[0], self.users.all()[1])

    def get_absolute_url(self):
        return reverse('chat_view', kwargs={'pk': self.pk})
    
    def get_second_user(self, user):
        for u in self.users.all():
            if u != user:
                return u
    
    def get_image(self, user):
        for u in self.users.all():
            if u != user:
                return u.profile.image.url
    
    def get_name(self, user):
        for u in self.users.all():
            if u != user:
                return u.username
    
    def get_id(self, user):
        for u in self.users.all():
            if u != user:
                return u.id
    
    def send_message(self, message):
        self.messages.add(message)
        self.last_message = message
        self.save()
    
    def delete(self):
        for message in self.messages.all():
            message.delete()
        super().delete()
        

class Group(models.Model):
    name = models.CharField(max_length=40)
    messages = models.ManyToManyField(Message, default=None)
    last_message = models.OneToOneField(Message, on_delete=models.PROTECT, default=None, null=True, related_name="last_message_group")
    unread_messages = models.ForeignKey(Unread_messages, on_delete=models.CASCADE, default=None, null=True)
    image = models.ImageField(upload_to=check_path, default="default.jpg")
    users = models.ManyToManyField(User)
    is_group = True

    def __str__(self):
        return "{}".format(self.name)

    def get_absolute_url(self):
        return reverse('chat_view', kwargs={'pk': self.pk})

    def save(self):
        super().save()

        img = Image.open(self.image.path)
        if img.height > 500 or img.width > 500:
            output_size = (500, 500)
            img.thumbnail(output_size)
            img.save(self.image.path)
    
    def delete(self):
        for message in self.messages.all():
            message.delete()
        super().delete()