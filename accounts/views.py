from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import RegistrationForm, ProviderRegistrationForm, LoginForm

def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_service_provider = False  # Regular user
            user.save()
            login(request, user)
            return redirect('homepage')
    else:
        form = RegistrationForm()
    return render(request, 'registration/register.html', {'form': form})

def provider_register(request):
    if request.method == 'POST':
        form = ProviderRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_service_provider = True  # Service provider
            user.save()
            login(request, user)
            return redirect('provider_home')
    else:
        form = ProviderRegistrationForm()
    return render(request, 'registration/provider_register.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        form = LoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            if user.is_service_provider:
                messages.error(request, 'Please use the Service Provider Login.')
                return redirect('login')
            login(request, user)
            return redirect('homepage')
    else:
        form = LoginForm()
    return render(request, 'registration/login.html', {'form': form})

def provider_login(request):
    if request.method == 'POST':
        form = LoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            if not user.is_service_provider:
                messages.error(request, 'Please use the Regular Login.')
                return redirect('provider_login')
            login(request, user)
            return redirect('provider_home')
    else:
        form = LoginForm()
    return render(request, 'registration/provider_login.html', {'form': form})

@login_required
def provider_home(request):
    if not request.user.is_service_provider:
        return redirect('homepage')
    return render(request, 'provider_home.html', {'user': request.user})

@login_required
def user_logout(request):
    logout(request)
    return redirect('login')