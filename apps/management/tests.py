from django.test import TestCase


class AdminEditLinkTagTests(TestCase):
    def setUp(self):
        self.response = self.client.get('/')

    def test_tag_returns_valid_href(self):
        """
        Looking if response contains valid link to admin edit object page
        """
        self.assertContains(self.response, '<a href="/admin/hello/profilemodel/1/change/">(admin)</a>', html=True)
