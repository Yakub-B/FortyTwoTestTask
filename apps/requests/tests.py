from django.contrib.auth import get_user_model
from django.test import TestCase, Client

from django.urls import resolve, reverse

from apps.requests.models import RequestModel
from apps.requests.views import LastTenRequestsView

# models tests


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


# middleware tests


class RequestLoggerMiddlewareTests(TestCase):
    """
    Tests for RequestLoggerMiddleware
    """
    @classmethod
    def setUpTestData(cls):
        user_model = get_user_model()
        cls.user_instance = user_model.objects.create_user(
            username='test', password='test'
        )
        client = Client()
        client.force_login(cls.user_instance)
        cls.response = client.get('/requests/')

    def test_request_logging(self):
        """
        Testing if request is saved into db
        """
        request_instance = RequestModel.objects.get(user=self.user_instance)
        self.assertEqual('http://testserver/requests/', request_instance.url)
        self.assertEqual('GET', request_instance.method)
        self.assertEqual(None, request_instance.encoding)
        self.assertEqual('', request_instance.content_type)
        self.assertEqual(1, request_instance.priority)


# views tests


class LastTenRequestsViewTests(TestCase):

    def setUp(self):
        self.response = self.client.get('/requests/')

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
            template_name='requests.html', response=self.response
        )

    def test_template_contains_info_about_client_get_request(self):
        """
        testing if template contains info about request made in setUp method
        """
        self.assertContains(self.response, 'http://testserver')
        self.assertContains(self.response, 'GET')

    def test_last_ten_requests_view_resolves_requests_page(self):
        """
        testing if the right view resolves '/requests/' url
        """
        view = resolve('/requests/')
        self.assertEqual(
            view.func.__name__,
            LastTenRequestsView.as_view().__name__
        )


class EditRequestPriorityViewTests(TestCase):

    def setUp(self):
        RequestModel.objects.create(
            method='POST', url='http://localhos:8000/test',
            encoding='utf-8', content_type='text/html'
        )
        self.response = self.client.post(
            path=reverse('requests:edit_priority'), data={'id': 1, 'priority': 2}
        )

    def test_status_code(self):
        """
        testing status code returned by view
        """
        self.assertEqual(301, self.response.status_code)

    def test_request_change_priority(self):
        """
        testing if priority of request changed by view
        """
        request = RequestModel.objects.get(id=1)
        self.assertEqual(2, request.priority)
