from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from .forms import CustomerRegistrationForm, ProviderRegistrationForm


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


def logout_view(request):
    logout(request)
    return redirect('home')
