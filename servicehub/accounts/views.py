from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import CustomerRegistrationForm, ProviderRegistrationForm, ProfileForm, ProviderProfileForm


def choose_role(request):
    """Role selection page — user picks Customer or Service Provider."""
    return render(request, 'registration/choose_role.html')


def register_customer(request):
    if request.method == 'POST':
        form = CustomerRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = CustomerRegistrationForm()
    return render(request, 'registration/register.html', {
        'form': form,
        'role_label': 'Customer',
        'role_icon': '🛒',
    })


def register_provider(request):
    if request.method == 'POST':
        form = ProviderRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = ProviderRegistrationForm()
    return render(request, 'registration/register.html', {
        'form': form,
        'role_label': 'Service Provider',
        'role_icon': '🔧',
    })


@login_required
def profile_view(request):
    user = request.user
    provider_form = None

    if request.method == 'POST':
        user_form = ProfileForm(request.POST, instance=user)
        if user.role == 'provider' and hasattr(user, 'providerprofile'):
            provider_form = ProviderProfileForm(request.POST, instance=user.providerprofile)
            if user_form.is_valid() and provider_form.is_valid():
                user_form.save()
                provider_form.save()
                messages.success(request, 'Profile updated successfully!')
                return redirect('profile')
        else:
            if user_form.is_valid():
                user_form.save()
                messages.success(request, 'Profile updated successfully!')
                return redirect('profile')
    else:
        user_form = ProfileForm(instance=user)
        if user.role == 'provider' and hasattr(user, 'providerprofile'):
            provider_form = ProviderProfileForm(instance=user.providerprofile)

    return render(request, 'profile.html', {
        'user_form': user_form,
        'provider_form': provider_form,
    })


def logout_view(request):
    logout(request)
    return redirect('home')

