import re

from django.core.management.base import BaseCommand

from notas.models import Product
from utils.products_from_bling import update_from_bling


class Command(BaseCommand):
    help = '''Adiciona ou atualiza produtos do Bling'''

    def handle(self, *args, **options):
        products = update_from_bling()
        print('Total de itens encontrados no Bling: ', len(products))

        new_products = []  # create if it doesn't exist
        old_products = []  # update if product with `codigo` exist

        for product in products:
            if product['produto']['tipo'] == 'P':
                imagem = None
                try:
                    imagens = product['produto']['imagem']
                    if imagens:
                        imagem = imagens[0]['link']
                except KeyError:
                    imagem = None

                modelo_pt = product['produto']['descricao']

                TAG_RE = re.compile(r'<[^>]+>')
                faz_pt = TAG_RE.sub('', product['produto']['descricaoCurta'].replace('S&amp;A', 'S&A'))

                ncm = product['produto']['class_fiscal']
                codigo_sku = product['produto']['codigo']
                preco_custo = product['produto']['precoCusto']
                preco_federal = product['produto']['preco']

                try:
                    peso_liquido = product['produto']['pesoLiq']
                    if peso_liquido == '':
                        peso_liquido = 0
                except KeyError:
                    peso_liquido = 0
                try:
                    peso_bruto = product['produto']['pesoBruto']
                    if peso_bruto == '':
                        peso_bruto = 0
                except KeyError:
                    peso_bruto = 0
                try:
                    largura = product['produto']['larguraProduto']
                    if largura == '':
                        largura = 0
                except KeyError:
                    largura = 0
                try:
                    altura = product['produto']['alturaProduto']
                    if altura == '':
                        altura = 0
                except KeyError:
                    altura = 0
                try:
                    profundidade = product['produto']['profundidadeProduto']
                    if profundidade == '':
                        profundidade = 0
                except KeyError:
                    profundidade = 0

                try:
                    old_product = Product.objects.get(codigo_sku=codigo_sku)
                    old_product.modelo_pt = modelo_pt
                    old_product.faz_pt = faz_pt
                    old_product.ncm = ncm
                    old_product.codigo_sku = codigo_sku
                    old_product.preco_custo = preco_custo
                    old_product.preco_federal = preco_federal
                    old_product.peso_liquido = peso_liquido
                    old_product.peso_bruto = peso_bruto
                    old_product.largura = largura
                    old_product.altura = altura
                    old_product.profundidade = profundidade
                    old_product.imagem = imagem

                    old_products.append(old_product)

                except Product.DoesNotExist:
                    new_product = Product(
                        modelo_pt=modelo_pt,
                        faz_pt=faz_pt,
                        ncm=ncm,
                        codigo_sku=codigo_sku,
                        preco_custo=preco_custo,
                        preco_federal=preco_federal,
                        peso_liquido=float(peso_liquido),
                        peso_bruto=float(peso_bruto),
                        largura=float(largura),
                        altura=float(altura),
                        profundidade=float(profundidade),
                        imagem=imagem,
                    )
                    new_products.append(new_product)

        print(len(new_products), 'novos produtos')
        print(len(old_products), 'produtos para atualizar')

        Product.objects.bulk_create(new_products)
        Product.objects.bulk_update(old_products, [
            'modelo_pt',
            'faz_pt',
            'ncm',
            'codigo_sku',
            'preco_custo',
            'preco_federal',
            'peso_liquido',
            'peso_bruto',
            'largura',
            'altura',
            'profundidade',
            'imagem',
        ])
