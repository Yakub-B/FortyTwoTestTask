from django.contrib.auth import get_user_model
from django.test import TestCase


# models tests
from apps.requests.models import RequestModel


class RequestsModelTests(TestCase):

    @classmethod
    def setUpTestData(cls):
        """
        Creating request instance
        """
        # creating user to link with request
        user_model = get_user_model()
        cls.user_instance = user_model.objects.create_user(
            username='test', password='test'
        )
        # creating request instance
        cls.request = RequestModel.objects.create(
            method='POST', url='http://localhos:8000/test',
            encoding='utf-8', user=cls.user_instance, content_type='text/html'
        )

    def test_request_creation(self):
        """
        Testing creation of request instance
        """
        self.assertEqual('http://localhos:8000/test', self.request.url)
        self.assertEqual('POST', self.request.method)
        self.assertEqual('utf-8', self.request.encoding)
        self.assertEqual('text/html', self.request.content_type)
        self.assertEqual(self.user_instance, self.request.user)
