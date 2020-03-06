from notas.models import NotaItens, Nota


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
