from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.views.generic import CreateView
from django.forms.models import inlineformset_factory

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
        Nota, NotaItens, form=NotaItensForm, extra=0, can_delete=False,
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
