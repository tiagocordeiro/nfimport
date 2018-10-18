from django.contrib.auth.models import AnonymousUser, User, Group
from django.test import RequestFactory, TestCase

from .views import product_list, product_create


class NotasViewsTest(TestCase):
    def setUp(self):
        # Every test needs access to the request factory.
        self.factory = RequestFactory()
        self.user = User.objects.create_user(username='jacob', email='jacob@…', password='top_secret')
        self.group = Group.objects.create(name='Testes')
        self.group.user_set.add(self.user)

    def test_product_list_anonimo(self):
        request = self.factory.get('/products')
        request.user = AnonymousUser()

        response = product_list(request)
        self.assertEqual(response.status_code, 302)

    def test_product_list_logado(self):
        request = self.factory.get('/products')
        request.user = self.user

        response = product_list(request)
        self.assertEqual(response.status_code, 200)

    def test_product_create_anonimo(self):
        request = self.factory.get('/products')
        request.user = AnonymousUser()

        response = product_create(request)
        self.assertEqual(response.status_code, 302)

    def test_product_create_logado(self):
        request = self.factory.get('/products')
        request.user = self.user

        response = product_create(request)
        self.assertEqual(response.status_code, 200)
