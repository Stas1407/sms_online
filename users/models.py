from django.db import models
from django.contrib.auth.models import User
from PIL import Image

# Create your models here.
def check_profile_path(instance, filename):
    return 'web-private/profiles/{0}/{1}'.format(instance.user.id, filename.split('/')[-1])

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='default.jpg', upload_to=check_profile_path)
    everybody_can_add_to_group = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.user.username} Profile'

    def save(self):
        super().save()

        img = Image.open(self.image.path)
        if img.height > 500 or img.width > 500:
            output_size = (500, 500)
            img.thumbnail(output_size)
            img.save(self.image.path)