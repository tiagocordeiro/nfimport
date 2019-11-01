import csv
import io
import os
import ssl
from io import BytesIO
from urllib.request import urlopen

import xlsxwriter
import xlwt
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.staticfiles.storage import staticfiles_storage
from django.forms.models import inlineformset_factory
from django.shortcuts import render, redirect, get_object_or_404, HttpResponse
from django.template.loader import get_template
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from xhtml2pdf import pisa
from xhtml2pdf.default import DEFAULT_FONT

from core.models import UserProfile
from .forms import ProductForm, NotaForm, NotaItensForm
from .models import Product, Nota, NotaItens


@login_required
def product_list(request):
    try:
        usuario = UserProfile.objects.get(user=request.user)
    except UserProfile.DoesNotExist:
        usuario = None
    products = Product.objects.all()
    return render(request, 'products/list.html', {'produtos': products,
                                                  'usuario': usuario, })


@login_required
def product_create(request):
    try:
        usuario = UserProfile.objects.get(user=request.user)
    except UserProfile.DoesNotExist:
        usuario = None

    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            product = form.save(commit=False)
            product.added_by = request.user
            product.save()
            return redirect(product_list)

    else:
        form = ProductForm()

    return render(request, 'products/create.html', {'usuario': usuario,
                                                    'form': form, })


@login_required
def product_update(request, pk):
    try:
        usuario = UserProfile.objects.get(user=request.user)
    except UserProfile.DoesNotExist:
        usuario = None

    product = get_object_or_404(Product, pk=pk)

    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)

        try:
            if form.is_valid():
                form.save()
                messages.success(request, "O produto foi atualizado")
                return redirect(product_list)

        except Exception as e:
            messages.warning(request, 'Ocorreu um erro ao atualizar: {}'.format(e))

    else:
        form = ProductForm(instance=product)

    contex = {
        'form': form,
        'usuario': usuario,
        'product': product,
    }

    return render(request, 'products/edit.html', contex)


@login_required
def nota_list(request):
    try:
        usuario = UserProfile.objects.get(user=request.user)
    except UserProfile.DoesNotExist:
        usuario = None
    notas = Nota.objects.all()
    return render(request, 'notas/list.html', {'notas': notas,
                                               'usuario': usuario, })


@login_required
def nota_create(request):
    nota_forms = Nota()
    item_nota_formset = inlineformset_factory(
        Nota, NotaItens, form=NotaItensForm, extra=0, can_delete=True,
        min_num=1, validate_min=True,
    )
    try:
        usuario = UserProfile.objects.get(user=request.user)
    except UserProfile.DoesNotExist:
        usuario = None

    if request.method == 'POST':
        forms = NotaForm(request.POST, instance=nota_forms, prefix='main')
        formset = item_nota_formset(request.POST, instance=nota_forms, prefix='product')

        if forms.is_valid() and formset.is_valid():
            forms = forms.save(commit=False)
            forms.added_by = request.user
            forms.save()
            formset.save()
            return redirect(nota_list)

    else:
        forms = NotaForm(instance=nota_forms, prefix='main')
        formset = item_nota_formset(instance=nota_forms, prefix='product')

    context = {
        'forms': forms,
        'formset': formset,
        'usuario': usuario,
    }

    return render(request, 'notas/add.html', context)


@login_required
def nota_update(request, pk):
    try:
        usuario = UserProfile.objects.get(user=request.user)
    except UserProfile.DoesNotExist:
        usuario = None

    nota = get_object_or_404(Nota, pk=pk)

    item_nota_formset = inlineformset_factory(
        Nota, NotaItens, form=NotaItensForm, extra=0, can_delete=True,
        min_num=1, validate_min=True,
    )

    if request.method == 'POST':
        forms = NotaForm(request.POST, instance=nota, prefix='main')
        formset = item_nota_formset(request.POST, instance=nota, prefix='product')

        try:
            if forms.is_valid() and formset.is_valid():
                forms.save()
                formset.save()
                messages.success(request, "A nota foi atualizada")
                return redirect(nota_list)

        except Exception as e:
            messages.warning(request, 'Ocorreu um erro ao atualizar: {}'.format(e))

    else:
        forms = NotaForm(instance=nota, prefix='main')
        formset = item_nota_formset(instance=nota, prefix='product')

    context = {
        'nota': nota,
        'forms': forms,
        'formset': formset,
        'usuario': usuario,
    }

    return render(request, 'notas/edit.html', context)


@login_required
def nota_export_csv(request, pk):
    nota = get_object_or_404(Nota, pk=pk)
    nota_itens = nota.notaitens_set.all()

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="notaImportacao.csv"'

    writer = csv.writer(response)
    writer.writerow(['maquina_pt', 'tipo_pt', 'modelo_pt', 'area_trabalho_pt', 'eixo_z_pt',
                     'cor_pt', 'faz_pt', 'voltagem_pt', 'ncm', 'nome_classificacao',
                     'caixa_lateral_base', 'opcionais', 'imagem', 'Quantidade', 'Valor USD'])

    for item in nota_itens:
        colunas = [item.item.maquina_pt, item.item.tipo_pt, item.item.modelo_pt, item.item.area_trabalho_pt,
                   item.item.eixo_z_pt, item.item.cor_pt, item.item.faz_pt, item.item.voltagem_pt,
                   item.item.ncm, item.item.nome_classificacao, item.item.caixa_lateral_base,
                   item.item.opcionais, item.item.imagem, item.quantidade, item.valor_usd]
        writer.writerow(colunas)

    return response


@login_required
def nota_export_xls(request, pk):
    nota = get_object_or_404(Nota, pk=pk)
    nota_itens = nota.notaitens_set.all()

    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="notaImportacao.xls"'

    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('Itens da Nota')

    # Sheet header, first row
    row_num = 0

    font_style = xlwt.XFStyle()
    font_style.font.bold = True

    columns = ['maquina_pt', 'tipo_pt', 'modelo_pt', 'area_trabalho_pt', 'eixo_z_pt',
               'cor_pt', 'faz_pt', 'voltagem_pt', 'ncm', 'nome_classificacao',
               'caixa_lateral_base', 'opcionais', 'imagem', 'Quantidade', 'Valor USD']

    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style)

    # Sheet body, remaining rows
    font_style = xlwt.XFStyle()

    rows = nota_itens.values_list('item__maquina_pt', 'item__tipo_pt', 'item__modelo_pt', 'item__area_trabalho_pt',
                                  'item__eixo_z_pt', 'item__cor_pt', 'item__faz_pt', 'item__voltagem_pt',
                                  'item__ncm', 'item__nome_classificacao', 'item__caixa_lateral_base',
                                  'item__opcionais', 'item__imagem', 'quantidade', 'valor_usd')

    for row in rows:
        row_num += 1
        for col_num in range(len(row)):
            ws.write(row_num, col_num, row[col_num], font_style)

    wb.save(response)
    return response


@login_required
def nota_export_xlsx(request, pk):
    nota = get_object_or_404(Nota, pk=pk)
    nota_itens = nota.notaitens_set.all()

    ssl._create_default_https_context = ssl._create_unverified_context
    output = io.BytesIO()

    wb = xlsxwriter.Workbook(output)
    ws = wb.add_worksheet()

    # Sheet header, first row
    row_num = 0

    columns = ['maquina_pt', 'tipo_pt', 'modelo_pt', 'area_trabalho_pt', 'eixo_z_pt',
               'cor_pt', 'faz_pt', 'voltagem_pt', 'ncm', 'nome_classificacao',
               'caixa_lateral_base', 'opcionais', 'imagem', 'Quantidade', 'Valor USD']

    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num])

    rows = nota_itens.values_list('item__maquina_pt', 'item__tipo_pt', 'item__modelo_pt', 'item__area_trabalho_pt',
                                  'item__eixo_z_pt', 'item__cor_pt', 'item__faz_pt', 'item__voltagem_pt',
                                  'item__ncm', 'item__nome_classificacao', 'item__caixa_lateral_base',
                                  'item__opcionais', 'item__imagem', 'quantidade', 'valor_usd')

    for row in rows:
        try:
            imagem = nota.notaitens_set.all()[row_num].item.imagem.url
        except ValueError:
            imagem = ''

        row_num += 1
        for col_num in range(len(row)):
            ws.set_row(row_num, 80)
            ws.write(row_num, col_num, row[col_num])

        if row[12] != '':
            image_data = BytesIO(urlopen(imagem).read())
            ws.insert_image(row_num, 16, imagem, {'image_data': image_data,
                                                  'positioning': 1,
                                                  'x_scale': 0.1,
                                                  'y_scale': 0.1})

    # Close the workbook before sending the data.
    wb.close()

    # Rewind the buffer.
    output.seek(0)

    filename = 'notaImportacao.xlsx'
    response = HttpResponse(
        output,
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
    response['Content-Disposition'] = 'attachment; filename=%s' % filename

    return response


def link_callback(uri, rel):
    """
    Convert HTML URIs to absolute system paths so xhtml2pdf can access those
    resources
    """
    # use short variable names
    s_url = settings.STATIC_URL  # Typically /static/
    s_root = settings.STATIC_ROOT  # Typically /home/userX/project_static/
    m_url = settings.MEDIA_URL  # Typically /static/media/
    m_root = settings.MEDIA_ROOT  # Typically /home/userX/project_static/media/

    # convert URIs to absolute system paths
    if uri.startswith(m_url):
        path = os.path.join(m_root, uri.replace(m_url, ""))
    elif uri.startswith(s_url):
        path = os.path.join(s_root, uri.replace(s_url, ""))
    else:
        return uri  # handle absolute uri (ie: http://some.tld/foo.png)

    # make sure that file exists
    if not os.path.isfile(path):
        raise Exception(
            'media URI must start with %s or %s' % (s_url, m_url)
        )
    return path


def nota_export_pdf(request, pk):
    pdfmetrics.registerFont(
        TTFont('yh', request.build_absolute_uri(staticfiles_storage.url('assets/minutafonts/msyh.ttf'))))
    DEFAULT_FONT['helvetica'] = 'yh'

    nota = get_object_or_404(Nota, pk=pk)
    nota_itens = nota.notaitens_set.all()

    ssl._create_default_https_context = ssl._create_unverified_context

    template_path = 'notas/pdf.html'
    context = {
        'nota': nota,
        'nota_itens': nota_itens,
    }
    # Create a Django response object, and specify content_type as pdf
    response = HttpResponse(content_type='application/pdf;charset=utf-8')
    response['Content-Disposition'] = 'attachment; filename="report.pdf"'
    # find the template and render it.
    template = get_template(template_path)
    html = template.render(context)

    # create a pdf
    pisa_status = pisa.CreatePDF(html, dest=response, encoding='utf8', link_callback=link_callback)
    # if error then show some funy view
    if pisa_status.err:
        return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response
