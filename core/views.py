from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.forms.models import inlineformset_factory
from django.shortcuts import render, redirect

from .forms import UserProfileForm, ProfileForm, SignUpForm
from .models import UserProfile


@login_required
def dashboard(request):
    try:
        usuario = UserProfile.objects.get(user=request.user)
    except UserProfile.DoesNotExist:
        usuario = None
    return render(request, 'dashboard.html', {'usuario': usuario, })


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


@login_required
def avatar_update(request):
    try:
        usuario = get_object_or_404(UserProfile)
    except UserProfile.DoesNotExist:
        usuario = None

    perfil = get_object_or_404(UserProfile, user=request.user)

    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=perfil)
        if form.is_valid():
            form.save()
            return redirect('dashboard')

    else:
        form = UserProfileForm(instance=perfil)

    return render(request, 'avatar_update.html', {'form': form,
                                                  'usuario': usuario, })


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('dashboard')
    else:
        form = SignUpForm()
    return render(request, 'registration/signup.html', {'form': form})
