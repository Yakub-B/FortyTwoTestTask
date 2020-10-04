from apps.management.models import DataBaseActionModel
from django.db.models import signals


def deletion_handler(sender, instance, **kwargs):
    if sender.__name__ in ['DataBaseActionModel', 'Migrations', 'Session', 'ContentType']:
        return

    app = sender.__module__

    DataBaseActionModel.objects.create(
        app=app, action=DataBaseActionModel.Action.DELETION, content_object=instance
    )


def post_save_handler(sender, instance, created, **kwargs):
    if sender.__name__ in ['DataBaseActionModel', 'Migration', 'Session', 'ContentType']:
        return

    app = sender.__module__

    db_action = DataBaseActionModel(app=app, content_object=instance)
    if created:
        db_action.action = DataBaseActionModel.Action.CREATION
    else:
        db_action.action = DataBaseActionModel.Action.EDITING
    db_action.save()


def connect():
    signals.post_delete.connect(deletion_handler)
    signals.post_save.connect(post_save_handler)
