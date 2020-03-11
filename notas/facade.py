import csv
import io

from notas.models import NotaItens, Nota, Product


def copy_nfi(pk):
    nf_copy = Nota.objects.get(pk=pk)
    nf_itens = NotaItens.objects.select_related().filter(nota=nf_copy)

    nf_copy.pk = None
    nf_copy.description = nf_copy.description + ' (copy)'
    nf_copy.save()

    for item in nf_itens.select_related():
        item.pk = None
        item.nota = nf_copy
        item.save()

    return nf_copy


def make_full_description_ci(fields: tuple):
    fields = fields
    full_description = ''
    fields_total_len = len(fields)
    field_item_position = 1

    for field in fields:
        if field:
            if field_item_position == fields_total_len:
                full_description += field
            else:
                full_description += field + ' '
        field_item_position += 1

    return full_description


def translate_from_csv(csv_file):
    csv_file = io.TextIOWrapper(csv_file)
    dialect = csv.Sniffer().sniff(csv_file.read(1024), delimiters=";,")
    csv_file.seek(0)
    reader = csv.reader(csv_file, dialect)
    return list(reader)


def update_translations(lista: list):
    products_for_update = []

    for product in lista:
        codigo_sku = str(product[0]).replace('\t', '')
        try:
            product_for_update = Product.objects.get(codigo_sku=codigo_sku)
            product_for_update.modelo_en = product[3]
            product_for_update.modelo_ch = product[4]
            products_for_update.append(product_for_update)
        except Product.DoesNotExist:
            pass

    Product.objects.bulk_update(products_for_update, [
        'modelo_en',
        'modelo_ch'
    ])
