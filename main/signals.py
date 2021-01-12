# from django.db.models.signals import post_save
# from main.models import Conversation
# from django.dispatch import receiver

# @receiver(post_save, sender=Conversation)
# def create_second_side_of_conversation(sender, instance, created, **kwargs):
#     if created and len(Conversation.objects.filter(user1=instance.user2, user2=instance.user1)) == 0:
#         c = Conversation()
#         c.user1=instance.user2
#         c.user2=instance.user1 
#         c.last_message=instance.last_message
#         c.unread_messages=instance.unread_messages
#         c.save()
#         c.messages.set(instance.messages.all())
#         c.save()

