from django.db import models


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
