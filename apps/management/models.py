from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models


class DataBaseActionModel(models.Model):
    class Action(models.IntegerChoices):
        CREATION = 0
        DELETION = 1
        EDITING = 2

    app = models.CharField(max_length=115)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, null=True)
    object_id = models.PositiveIntegerField(blank=True, null=True)
    content_object = GenericForeignKey()
    action = models.IntegerField(choices=Action.choices)
