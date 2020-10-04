from django.test import TestCase

from apps.hello.models import ProfileModel


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
