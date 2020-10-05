from django.conf import settings
from django.db import models


class RequestModel(models.Model):
    """
    Model for storing requests into db
    """
    url = models.URLField(max_length=300)
    method = models.CharField(max_length=10)
    encoding = models.CharField(max_length=10, null=True)
    content_type = models.CharField(max_length=50)
    priority = models.IntegerField(default=1)

    timestamp = models.DateTimeField(auto_now_add=True)

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True
    )

    class Meta:
        ordering = ('-priority', '-timestamp')
        get_latest_by = 'id'
