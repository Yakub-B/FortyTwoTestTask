from django.conf import settings
from django.db import models


class RequestModel(models.Model):
    """
    Model for storing requests into db
    """
    method = models.CharField(max_length=10)
    encoding = models.CharField(max_length=10, null=True)
    content_type = models.CharField(max_length=50)

    timestamp = models.DateTimeField(auto_now_add=True)

    url_priority = models.ForeignKey("UrlPriority", on_delete=models.CASCADE, null=True)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True
    )

    class Meta:
        ordering = ('-timestamp',)
        get_latest_by = 'id'


class UrlPriority(models.Model):
    """
    Model for storing request priority linked to request path
    """
    priority = models.IntegerField(default=1, blank=True)
    path = models.URLField(max_length=300)
