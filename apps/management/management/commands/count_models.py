from django.core.management import BaseCommand

from django.apps import apps


class Command(BaseCommand):
    help = 'Prints all project models and the count of instances in every model'

    def handle(self, *args, **options):
        for model in apps.get_models():
            output = f'App: {model.__module__}, model:{model.__name__}, objects count = {model.objects.count()}'
            self.stdout.write(output)
            self.stderr.write(f'error: {output}')
