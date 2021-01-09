from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from PIL import Image
from django.urls import reverse

# Create your models here.

def check_path(instance, filename):
    return 'web-private/{0}/{1}'.format(instance.id, filename.split('/')[-1])


class Message(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.CharField(max_length=200)
    date_sent = models.DateTimeField(default=timezone.now)

class Unread_messages(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    count = models.IntegerField()

class Conversation(models.Model):
    last_message = models.OneToOneField(Message, on_delete=models.CASCADE, default=None, null=True)
    last_message_date = models.DateTimeField(default=None, null=True)
    unread_messages = models.ForeignKey(Unread_messages, on_delete=models.CASCADE, default=None, null=True)
    user1 = models.ForeignKey(User, on_delete=models.CASCADE, related_name="conversations", null=True)
    user2 = models.ForeignKey(User, on_delete=models.CASCADE, related_name="c", null=True)

    def get_absolute_url(self):
        return reverse('chat_view', kwargs={'pk': self.pk})

class Group(models.Model):
    name = models.CharField(max_length=40)
    last_message = models.OneToOneField(Message, on_delete=models.CASCADE, default=None, null=True)
    last_message_date = models.DateTimeField(default=None, null=True)
    unread_messages = models.ForeignKey(Unread_messages, on_delete=models.CASCADE, default=None, null=True)
    image = models.ImageField(upload_to=check_path, default="default.jpg")
    users = models.ManyToManyField(User)

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