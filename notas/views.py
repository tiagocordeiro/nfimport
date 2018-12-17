import csv

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.forms.models import inlineformset_factory
from django.shortcuts import render, redirect, get_object_or_404, HttpResponse
from django.views.generic import CreateView

from core.models import UserProfile
from .forms import ProductForm, NotaForm, NotaItensFormSet, NotaItensForm
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
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save(commit=False)
            product.added_by = request.user
            product.save()
            return redirect(product_list)

    else:
        form = ProductForm()

    return render(request, 'products/create.html', {'usuario': usuario,
                                                    'form': form, })


def product_update(request, pk):
    try:
        usuario = UserProfile.objects.get(user=request.user)
    except UserProfile.DoesNotExist:
        usuario = None

    product = get_object_or_404(Product, pk=pk)

    if request.method == 'POST':
        form = ProductForm(request.POST, instance=product)

        try:
            if form.is_valid():
                form.save()
                messages.success(request, "O produto foi atualizado")

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
    # nota_itens = get_list_or_404(NotaItens, nota_id=nota)

    item_nota_formset = inlineformset_factory(
        Nota, NotaItens, form=NotaItensForm, extra=0, can_delete=True,
        min_num=1, validate_min=True,
    )

    if request.method == 'POST':
        forms = NotaForm(request.POST, instance=nota, prefix='main')
        formset = item_nota_formset(request.POST, instance=nota, prefix='product')

        try:
            if forms.is_valid() and formset.is_valid():
                # forms = forms.save(commit=False)
                # forms.added_by = request.user
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


class NotaView(CreateView):
    template_name = 'notas/nota_view.html'
    form_class = NotaForm

    def get_context_data(self, **kwargs):
        context = super(NotaView, self).get_context_data(**kwargs)
        if self.request.POST:
            context['forms'] = NotaForm(self.request.POST)
            context['formset'] = NotaItensFormSet(self.request.POST)
            try:
                context['usuario'] = UserProfile.objects.get(user=self.request.user)
            except UserProfile.DoesNotExist:
                context['usuario'] = None
        else:
            context['forms'] = NotaForm()
            context['formset'] = NotaItensFormSet()
            try:
                context['usuario'] = UserProfile.objects.get(user=self.request.user)
            except UserProfile.DoesNotExist:
                context['usuario'] = None
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        forms = context['forms']
        formset = context['formset']
        if forms.is_valid() and formset.is_valid():
            self.object = form.save()
            forms.instance = self.object
            formset.instance = self.object
            forms.save()
            formset.save()
            return redirect('nota_list')
        else:
            return self.render_to_response(self.get_context_data(form=form))
