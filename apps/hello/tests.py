from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse, resolve

from apps.hello.forms import EditProfileDataForm
from apps.hello.models import ProfileModel
from apps.hello.views import IndexView, EditProfileDataView


User = get_user_model()


class ProfileModelTests(TestCase):
    """
    Test case for Profile model
    """
    @classmethod
    def setUp(cls):
        # creating profile instance
        cls.profile = ProfileModel(
            name='Bohdan', last_name='Yakubovskyi',
            birthday_date='18.10.2000', bio='Lalala test',
            email='test@test.com', jabber='test@cc.co',
            skype='124519222asd', other_contacts='telegram: @grey_five_9'
        )

    def test_profile_creation(self):
        """
        testing creation of profile instance
        """
        self.assertEqual('Bohdan', self.profile.name)
        self.assertEqual('Yakubovskyi', self.profile.last_name)
        self.assertEqual('18.10.2000', self.profile.birthday_date)
        self.assertEqual('Lalala test', self.profile.bio)
        self.assertEqual('test@test.com', self.profile.email)
        self.assertEqual('test@cc.co', self.profile.jabber)
        self.assertEqual('124519222asd', self.profile.skype)
        self.assertEqual('telegram: @grey_five_9', self.profile.other_contacts)


# Tests for views____________________________________________________


class IndexViewTests(TestCase):
    """
    Test case for index view
    """
    def setUp(self):
        """
        making request to test view
        """
        # creating profile instance
        self.profile = ProfileModel(
            name='Bohdan', last_name='Yakubovskyi',
            birthday_date='18.10.2000', bio='Lalala test',
            email='test@test.com', jabber='test@cc.co',
            skype='124519222asd',
        )
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


class EditProfileDataPageTests(TestCase):
    def setUp(self):
        user = User.objects.create_user(username='admin', password='admin')
        self.client.force_login(user)
        self.get_response = self.client.get(reverse('hello:edit'))
        self.post_response = self.client.post(reverse('hello:edit'), {'name': 'New', 'bio': 'New interesting bio'})

    def test_status_code(self):
        """
        testing status code returned by view
        """
        self.assertEqual(200, self.get_response.status_code)

    def test_template_used(self):
        """
        testing if the right template is used in view
        """
        self.assertTemplateUsed(
            template_name='edit_profile.html', response=self.get_response
        )

    def test_context_form(self):
        """
        Test form in page context
        """
        self.assertIsInstance(self.get_response.context['form'], EditProfileDataForm)

    def test_index_view_resolves_index_page(self):
        """
        testing if the right view resolves '/edit-profile/' url
        """
        view = resolve('/edit-profile/')
        self.assertEqual(
            view.func.__name__,
            EditProfileDataView.as_view().__name__
        )

    def test_post_request_status_code(self):
        """
        testing status code returned by view
        """
        self.assertEqual(200, self.post_response.status_code)
