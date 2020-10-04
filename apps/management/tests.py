from django.contrib.auth import get_user_model
from django.test import TestCase

from apps.hello.models import ProfileModel
from apps.management.models import DataBaseActionModel


class AdminEditLinkTagTests(TestCase):
    def setUp(self):
        ProfileModel.objects.create(
            id=1, name='Bohdan', last_name='Yakubovskyi',
            birthday_date='2000-10-18', bio='Lalala test',
            email='test@test.com', jabber='test@cc.co',
            skype='124519222asd',
        )
        self.response = self.client.get('/')

    def test_tag_returns_valid_href(self):
        """
        Looking if response contains valid link to admin edit object page
        """
        self.assertContains(self.response, '<a href="/admin/hello/profilemodel/1/change/">(admin)</a>', html=True)


class DataBaseActionModelTests(TestCase):
    def setUp(self):
        # getting user created by data migration
        user_model = get_user_model()
        user = user_model.objects.first()
        # making some changes with user
        user.username = 'test'
        user.save()
        self.entry = DataBaseActionModel.objects.first()

    def test_entries_from_data_migration(self):
        """
        Testing creation of action entry
        """
        self.assertEqual('django.contrib.auth.models', self.entry.app)
        self.assertEqual(DataBaseActionModel.Action.EDITING, self.entry.action)

    def test_entry_does_not_created_for_db_action_model(self):
        """
        Testing if listeners don`t create entries about DataBaseActionModel actions
        """
        # 2 entries created with data migration (ProfileModel, User)
        self.assertEqual(1, DataBaseActionModel.objects.count())
