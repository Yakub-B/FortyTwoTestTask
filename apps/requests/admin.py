from django.contrib import admin

from apps.requests.models import RequestModel, UrlPriority

admin.site.register(RequestModel)

admin.site.register(UrlPriority)
