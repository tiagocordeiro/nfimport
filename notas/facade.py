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
