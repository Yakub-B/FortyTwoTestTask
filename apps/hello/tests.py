from django.test import TestCase
from django.urls import reverse, resolve

from apps.hello.views import IndexView


class IndexViewTests(TestCase):
    """
    Test case for index view
    """
    def setUp(self):
        """
        making request to test view
        """
        # creating profile instance
        self.response = self.client.get(reverse('hello:index'))

    def test_status_code(self):
        """
        testing status code returned by view
        """
        self.assertEqual(200, self.response.status_code)

    def test_template_used(self):
        """
        testing if the right template is used in view
        """
        self.assertTemplateUsed(
            template_name='index.html', response=self.response
        )

    def test_index_view_resolves_index_page(self):
        """
        testing if the right view resolves '/' url
        """
        view = resolve('/')
        self.assertEqual(
            view.func.__name__,
            IndexView.as_view().__name__
        )
