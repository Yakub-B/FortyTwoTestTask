from django.apps import AppConfig


class ManagementConfig(AppConfig):
    name = 'apps.management'

    def ready(self):
        from apps.management.signals import connect
        connect()
