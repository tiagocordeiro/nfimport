from django.contrib.auth.models import User, Group, AnonymousUser
from django.contrib.messages.storage.fallback import FallbackStorage
from django.forms.models import inlineformset_factory
from django.test import RequestFactory, TestCase, Client
from django.urls import reverse
from django.utils import timezone

from .forms import ProductForm, NotaItensForm, NotaForm
from .models import Nota, Product, NotaItens
from .views import product_list, product_create, nota_list, nota_create, nota_update, product_update, \
    nota_export_csv, nota_export_xls, nota_export_xlsx, nota_export_pdf


class NotasViewsTest(TestCase):
    def setUp(self):
        # Every test needs access to the request factory.
        self.factory = RequestFactory()
        self.client = Client()
        self.user = User.objects.create_user(username='jacob', email='jacob@…', password='top_secret')
        self.group = Group.objects.create(name='Testes')
        self.group.user_set.add(self.user)

        # Nota
        self.nota = Nota.objects.create(description='Nota Teste', date=timezone.now(), dolar_dia=3.33)

        # Produto
        self.product = Product.objects.create(maquina_pt='Maquina teste',
                                              tipo_pt='tipo teste',
                                              modelo_pt='ZM-Teste',
                                              area_trabalho_pt='66x66',
                                              eixo_z_pt='22',
                                              cor_pt='Azul',
                                              faz_pt='Faz testes',
                                              voltagem_pt='110v',
                                              ncm='111.222.333')

        # Nota Itens
        self.nota_itens = NotaItens.objects.create(item=self.product,
                                                   nota=self.nota,
                                                   quantidade=1,
                                                   valor_usd=3.33)

        # Nota Itens FormSet
        self.item_nota_formset = inlineformset_factory(Nota, NotaItens, form=NotaItensForm,
                                                       extra=0, can_delete=True, min_num=1, validate_min=True, )

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

    def test_product_create_form_is_valid(self):
        form_data = {'maquina_pt': 'Maquina teste',
                     'tipo_pt': 'tipo teste',
                     'modelo_pt': 'ZM-Teste',
                     'area_trabalho_pt': '66x66',
                     'eixo_z_pt': '22',
                     'cor_pt': 'Azul',
                     'faz_pt': 'Faz testes',
                     'voltagem_pt': '110v',
                     'ncm': '111.222.333'}
        form = ProductForm(data=form_data)
        self.assertEqual(form.is_valid(), True)

    def test_product_create_form_invalid(self):
        form_data = {'maquina_pt': '',
                     'tipo_pt': 'tipo teste'}

        form = ProductForm(data=form_data)
        self.assertEqual(form.is_valid(), False)

    def test_product_view_create(self):
        produtos = Product.objects.all()
        self.assertEqual(len(produtos), 1)

        form_data = {'maquina_pt': 'Maquina teste',
                     'tipo_pt': 'tipo teste',
                     'modelo_pt': 'ZM-Teste',
                     'area_trabalho_pt': '66x66',
                     'eixo_z_pt': '22',
                     'cor_pt': 'Azul',
                     'faz_pt': 'Faz testes',
                     'voltagem_pt': '110v',
                     'ncm': '111.222.333'}

        request = self.factory.post(reverse('product_create'), data=form_data)
        request.user = self.user

        response = product_create(request)
        self.assertEqual(response.status_code, 302)

        produtos = Product.objects.all()
        self.assertEqual(len(produtos), 2)

    def test_product_view_update(self):
        product = self.product
        new_data = {'maquina_pt': 'Maquina teste',
                    'tipo_pt': 'tipo teste',
                    'modelo_pt': 'ZM-Teste',
                    'area_trabalho_pt': '77x77',
                    'eixo_z_pt': '22',
                    'cor_pt': 'Verde',
                    'faz_pt': 'Faz testes',
                    'voltagem_pt': '110v',
                    'ncm': '111.222.333'}

        request = self.factory.post(reverse('product_update', kwargs={'pk': product.id}), data=new_data)
        request.user = self.user
        setattr(request, 'session', 'session')
        messages = FallbackStorage(request)
        setattr(request, '_messages', messages)

        response = product_update(request, pk=product.pk)
        self.assertEqual(response.status_code, 302)
        product.refresh_from_db()
        self.assertEqual(product.area_trabalho_pt, '77x77')
        self.assertEqual(product.cor_pt, 'Verde')

    def test_product_view_update_invalid(self):
        product = self.product
        new_erro_data = {'maquina_pt': ''}

        request = self.factory.post(reverse('product_update', kwargs={'pk': product.id}), data=new_erro_data)
        request.user = self.user
        setattr(request, 'session', 'session')
        messages = FallbackStorage(request)
        setattr(request, '_messages', messages)

        response = product_update(request, pk=product.pk)

        self.assertEqual(response.status_code, 200)
        product.refresh_from_db()
        self.assertEqual(product.maquina_pt, 'Maquina teste')

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

    def test_retorno_nota_model(self):
        nota = self.nota
        self.assertTrue(nota.__str__(), nota.description)

    def test_nota_view_create(self):
        notas = Nota.objects.all()
        self.assertEqual(len(notas), 1)

        data = {'main-description': 'Teste',
                'main-date_day': 8,
                'main-date_month': 1,
                'main-date_year': 2019,
                'main-dolar_dia': 3.12,
                'product-TOTAL_FORMS': 1,
                'product-INITIAL_FORMS': 0,
                'product-MIN_NUM_FORMS': 1,
                'product-MAX_NUM_FORMS': 1000,
                'product-0-item': self.product.pk,
                'product-0-quantidade': 1,
                'product-0-valor_usd': 1000}

        nota_forms = Nota()
        item_nota_formset = inlineformset_factory(Nota, NotaItens, form=NotaItensForm, min_num=1, validate_min=True, )
        forms = NotaForm(data, instance=nota_forms, prefix='main')
        formset = item_nota_formset(data, instance=nota_forms, prefix='product')

        request = self.factory.post(reverse('nota_create'), data=data)
        request.user = self.user
        setattr(request, 'session', 'session')
        messages = FallbackStorage(request)
        setattr(request, '_messages', messages)

        self.assertEqual(forms.is_valid(), True)
        self.assertEqual(formset.is_valid(), True)

        response = nota_create(request)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/notas/')

        notas = Nota.objects.all()
        self.assertEqual(len(notas), 2)

    def test_nota_view_update(self):
        nota = self.nota
        data_edited = {'main-description': 'Teste Editado',
                       'main-date_day': 8,
                       'main-date_month': 1,
                       'main-date_year': 2019,
                       'main-dolar_dia': 3.12,
                       'product-TOTAL_FORMS': 1,
                       'product-INITIAL_FORMS': 0,
                       'product-MIN_NUM_FORMS': 1,
                       'product-MAX_NUM_FORMS': 1000,
                       'product-0-item': self.product.pk,
                       'product-0-quantidade': 2,
                       'product-0-valor_usd': 2000}

        request = self.factory.post(reverse('nota_update', kwargs={'pk': nota.pk}), data=data_edited)
        request.user = self.user
        setattr(request, 'session', 'session')
        messages = FallbackStorage(request)
        setattr(request, '_messages', messages)

        response = nota_update(request, pk=nota.pk)

        self.assertEqual(response.status_code, 302)
        nota.refresh_from_db()
        self.assertEqual(nota.description, 'Teste Editado')
        self.assertTrue(nota.notaitens_set.values().last()['valor_usd'], 2000)

    def test_nota_export_csv_statuscode(self):
        nota = self.nota
        request = self.factory.get('/nota/export/csv/' + str(nota.pk))
        request.user = self.user

        response = nota_export_csv(request, pk=nota.pk)
        self.assertEqual(response.status_code, 200)

    def test_nota_export_xls_statuscode(self):
        nota = self.nota
        request = self.factory.get('/nota/export/xls/' + str(nota.pk))
        request.user = self.user

        response = nota_export_xls(request, pk=nota.pk)
        self.assertEqual(response.status_code, 200)

    def test_nota_export_xlsx_statuscode(self):
        nota = self.nota
        request = self.factory.get('/nota/export/xlsx/' + str(nota.pk))
        request.user = self.user

        response = nota_export_xlsx(request, pk=nota.pk)
        self.assertEqual(response.status_code, 200)

    def test_nota_export_pdf_statuscode(self):
        nota = self.nota
        request = self.factory.get('/nota/export/pdf/' + str(nota.pk))
        request.user = self.user

        response = nota_export_pdf(request, pk=nota.pk)
        self.assertEqual(response.status_code, 200)
