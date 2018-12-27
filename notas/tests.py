from django.contrib.auth.models import AnonymousUser, User, Group
from django.test import RequestFactory, TestCase
from django.utils import timezone

from .views import product_list, product_create, nota_list, nota_create, nota_update
from .models import Nota


class NotasViewsTest(TestCase):
    def setUp(self):
        # Every test needs access to the request factory.
        self.factory = RequestFactory()
        self.user = User.objects.create_user(username='jacob', email='jacob@…', password='top_secret')
        self.group = Group.objects.create(name='Testes')
        self.group.user_set.add(self.user)

        # Nota
        self.nota = Nota.objects.create(description='Nota Teste', date=timezone.now(), dolar_dia=3.33)

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

    def test_notas_list_anonimo(self):
        request = self.factory.get('/notas')
        request.user = AnonymousUser()

        response = nota_list(request)
        self.assertEqual(response.status_code, 302)

    def test_notas_list_logado(self):
        request = self.factory.get('/notas')
        request.user = self.user

        response = nota_list(request)
        self.assertEqual(response.status_code, 200)

    def test_nota_create_anonimo(self):
        request = self.factory.get('/nota/add')
        request.user = AnonymousUser()

        response = nota_create(request)
        self.assertEqual(response.status_code, 302)

    def test_nota_create_logado(self):
        request = self.factory.get('/nota/add')
        request.user = self.user

        response = nota_create(request)
        self.assertEqual(response.status_code, 200)

    def test_nota_update_anonimo(self):
        request = self.factory.get('/nota/edit/')
        request.user = AnonymousUser()

        response = nota_update(request, pk=self.nota.pk)
        self.assertEqual(response.status_code, 302)

    def test_nota_update_logado(self):
        request = self.factory.get('/nota/edit/')
        request.user = self.user

        response = nota_update(request, pk=self.nota.pk)
        self.assertEqual(response.status_code, 200)
