from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.forms.models import inlineformset_factory
from django.shortcuts import render, redirect

from notas.models import Nota
from notas.models import NotaItens
from notas.models import Product
from .facade import get_usd_cny_exchange
from .forms import ProfileForm
from .models import UserProfile


@login_required
def dashboard(request):
    try:
        usuario = UserProfile.objects.get(user=request.user)
    except UserProfile.DoesNotExist:
        usuario = None

    produtos = Product.objects.all()
    notas = Nota.objects.all()
    notas_total = 0
    for nota in notas:
        itens = NotaItens.objects.filter(nota=nota)
        for item in itens:
            if item.valor_usd and item.quantidade:
                notas_total += item.valor_usd * item.quantidade
            else:
                pass

    cotacao = get_usd_cny_exchange()
    cotacao_brl = cotacao[0]
    cotacao_cny = cotacao[1]

    last_cny = cotacao_cny[-1]
    last_cny_data = last_cny['data']
    last_cny_valor = last_cny['valor']

    last_brl = cotacao_brl[-1]
    last_brl_data = last_brl['data']
    last_brl_valor = last_brl['valor']

    context = {
        'usuario': usuario,
        'produtos_qt': produtos.count(),
        'notas_qt': notas.count(),
        'notas_total': notas_total,
        'cotacao_cny': cotacao_cny,
        'cotacao_brl': cotacao_brl,
        'last_cny_data': last_cny_data,
        'last_cny_valor': last_cny_valor,
        'last_brl_data': last_brl_data,
        'last_brl_valor': last_brl_valor,
    }

    return render(request, 'dashboard.html', context=context)


@login_required
def profile(request):
    try:
        usuario = UserProfile.objects.get(user=request.user)
    except UserProfile.DoesNotExist:
        usuario = None

    return render(request, 'profile.html', {'usuario': usuario})


@login_required
def profile_update(request):
    try:
        usuario = UserProfile.objects.get(user=request.user)
    except UserProfile.DoesNotExist:
        usuario = None

    ProfileInlineFormset = inlineformset_factory(User, UserProfile, fields=('avatar',))
    formset = ProfileInlineFormset(instance=request.user)

    if request.method == 'POST':
        form = ProfileForm(data=request.POST, instance=request.user)
        formset = ProfileInlineFormset(request.POST, request.FILES, instance=request.user)

        if form.is_valid():
            perfil = form.save(commit=False)
            formset = ProfileInlineFormset(request.POST, request.FILES, instance=perfil)

            if formset.is_valid():
                perfil.save()
                formset.save()
                # return HttpResponseRedirect('/accounts/profile/')
                return redirect('dashboard')

    else:
        form = ProfileForm(instance=request.user)
        formset = ProfileInlineFormset(instance=request.user)

    return render(request, 'profile_update.html', {'form': form,
                                                   'formset': formset,
                                                   'usuario': usuario, })
