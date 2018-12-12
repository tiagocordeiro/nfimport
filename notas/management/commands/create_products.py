from django.core.management.base import BaseCommand

from notas.models import Product
from utils.products_populate import create_products


class Command(BaseCommand):
    help = '''Pupula banco com produtos do utils/csv_data/products.csv'''

    def handle(self, *args, **options):
        produtos = create_products()
        new_products = []
        for product in produtos:
            maquina_pt = product['maquina']
            maquina_en = product['maquina_en']
            maquina_ch = product['maquina_ch']
            tipo_pt = product['tipo']
            tipo_en = product['tipo_en']
            tipo_ch = product['tipo_ch']
            modelo_pt = product['modelo']
            modelo_en = product['modelo_en']
            modelo_ch = product['modelo_ch']
            area_trabalho_pt = product['area_trabalho']
            area_trabalho_en = product['area_trabalho_en']
            area_trabalho_ch = product['area_trabalho_ch']
            eixo_z_pt = product['eixo_z']
            eixo_z_en = product['eixo_z_en']
            eixo_z_ch = product['eixo_z_ch']
            cor_pt = product['cor']
            cor_en = product['cor_en']
            cor_ch = product['cor_ch']
            faz_pt = product['o_que_ela_faz']
            faz_en = product['o_que_ela_faz_en']
            faz_ch = product['o_que_ela_faz_ch']
            voltagem_pt = product['voltagem']
            voltagem_en = product['voltagem_en']
            voltagem_ch = product['voltagem_ch']
            ncm = product['ncm']
            nome_classificacao = product['nome_da_classificacao']
            caixa_lateral_base = product['caixa_lateral_e_base']
            opcionais = product['opcionais']

            new_product = Product(
                maquina_pt=maquina_pt,
                maquina_en=maquina_en,
                maquina_ch=maquina_ch,
                tipo_pt=tipo_pt,
                tipo_en=tipo_en,
                tipo_ch=tipo_ch,
                modelo_pt=modelo_pt,
                modelo_en=modelo_en,
                modelo_ch=modelo_ch,
                area_trabalho_pt=area_trabalho_pt,
                area_trabalho_en=area_trabalho_en,
                area_trabalho_ch=area_trabalho_ch,
                eixo_z_pt=eixo_z_pt,
                eixo_z_en=eixo_z_en,
                eixo_z_ch=eixo_z_ch,
                cor_pt=cor_pt,
                cor_en=cor_en,
                cor_ch=cor_ch,
                faz_pt=faz_pt,
                faz_en=faz_en,
                faz_ch=faz_ch,
                voltagem_pt=voltagem_pt,
                voltagem_en=voltagem_en,
                voltagem_ch=voltagem_ch,
                ncm=ncm,
                nome_classificacao=nome_classificacao,
                caixa_lateral_base=caixa_lateral_base,
                opcionais=opcionais,
            )
            new_products.append(new_product)
        Product.objects.bulk_create(new_products)
