from PIL import Image
from django.db import models

from apps.hello.utils import resize_image


class ProfileModel(models.Model):
    """
    Model for profile info
    """
    name = models.CharField(max_length=55)
    last_name = models.CharField(max_length=55)
    birthday_date = models.DateField()
    bio = models.TextField(verbose_name='Biography')
    profile_photo = models.ImageField(null=True, blank=True)

    email = models.EmailField(max_length=115)
    jabber = models.CharField(max_length=115)
    skype = models.CharField(max_length=115)

    other_contacts = models.TextField(blank=True, null=True)

    def save(self, *args, **kwargs):
        """
        Resizing profile photo
        """
        if self.profile_photo:    # checking if the image needs to be resized
            img = Image.open(self.profile_photo)
            if img.height > 200 or img.width > 200:
                self.profile_photo = resize_image((200, 200), self.profile_photo)
        super().save(*args, **kwargs)
