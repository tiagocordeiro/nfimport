import os

import quandl
from django.contrib.auth.models import AnonymousUser, User, Group
from django.test import RequestFactory, TestCase

from .forms import ProfileForm
from .views import dashboard, profile, profile_update


class CoreViewsTest(TestCase):
    def setUp(self):
        # Every test needs access to the request factory.
        self.factory = RequestFactory()
        self.user = User.objects.create_user(username='jacob', email='jacob@…', password='top_secret')
        self.group = Group.objects.create(name='Testes')
        self.group.user_set.add(self.user)

    def test_dashboard_anonimo(self):
        quandl.ApiConfig.api_key = os.environ.get('QUANDL_KEY')
        request = self.factory.get('/')
        request.user = AnonymousUser()

        response = dashboard(request)
        self.assertEqual(response.status_code, 302)

    def test_dashboard_logado(self):
        request = self.factory.get('/')
        request.user = self.user

        response = dashboard(request)
        self.assertEqual(response.status_code, 200)

    def test_profile_anonimo(self):
        request = self.factory.get('/profile')
        request.user = AnonymousUser()

        response = profile(request)
        self.assertEqual(response.status_code, 302)

    def test_profile_logado(self):
        request = self.factory.get('/profile')
        request.user = self.user

        response = profile(request)
        self.assertEqual(response.status_code, 200)

    def test_profile_update_anonimo(self):
        request = self.factory.get('/profile/update')
        request.user = AnonymousUser()

        response = profile_update(request)
        self.assertEqual(response.status_code, 302)

    def test_profile_update_logado(self):
        request = self.factory.get('/profile/update')
        request.user = self.user

        response = profile_update(request)
        self.assertEqual(response.status_code, 200)

    # Valid Form Data
    def test_ProfileForm_valid(self):
        form = ProfileForm(data={'email': "jacob@mg.com", 'password': "top_secret", 'first_name': "jacob"})
        self.assertTrue(form.is_valid())

    # Invalid Form Data
    def test_ProfileForm_invalid(self):
        form = ProfileForm(data={'email': "jacob@...", 'password': "123", 'first_name': ""})
        self.assertFalse(form.is_valid())

    def test_ProfileForm_change_first_name(self):
        request = self.factory.get('/profile/update')
        request.user = self.user

        response = profile_update(request)
        self.assertEqual(response.status_code, 200)

        self.assertEqual(self.user.first_name, '')

        self.user.first_name = 'Jacob'
        self.user.save()

        self.assertEqual(self.user.first_name, 'Jacob')
