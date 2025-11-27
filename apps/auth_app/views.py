"""Views for auth app."""
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from apps.auth_app.forms import CustomUserCreationForm, LoginForm
from apps.users.models import UserProfile


def _ensure_related(user):
    """Make sure profile exists for the user."""
    UserProfile.objects.get_or_create(user=user, defaults={'role': UserProfile.ROLE_USER})


def custom_login(request):
    """Vista de login personalizada."""
    if request.user.is_authenticated:
        return redirect('landing')
    
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                _ensure_related(user)
                remember = form.cleaned_data.get('remember_me')
                if not remember:
                    request.session.set_expiry(0)
                return redirect('landing')
            else:
                messages.error(request, 'Usuario o contrasena incorrectos.')
    else:
        form = LoginForm()
    
    return render(request, 'auth/login.html', {'form': form})


def register(request):
    """Vista de registro."""
    if request.user.is_authenticated:
        return redirect('landing')
    
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            _ensure_related(user)
            messages.success(request, 'Registro exitoso. Por favor, inicia sesion.')
            return redirect('login')
    else:
        form = CustomUserCreationForm()
    
    return render(request, 'auth/register.html', {'form': form})


@login_required(login_url='login')
def custom_logout(request):
    """Vista de logout."""
    logout(request)
    messages.success(request, 'Sesion cerrada correctamente.')
    return redirect('login')


@login_required(login_url='login')
def change_password(request):
    """Vista para cambiar contrasena."""
    if request.method == 'POST':
        current_password = request.POST.get('current_password')
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')
        
        if not request.user.check_password(current_password):
            messages.error(request, 'Contrasena actual incorrecta.')
        elif new_password != confirm_password:
            messages.error(request, 'Las contrasenas no coinciden.')
        elif len(new_password) < 8:
            messages.error(request, 'La contrasena debe tener al menos 8 caracteres.')
        else:
            request.user.set_password(new_password)
            request.user.save()
            messages.success(request, 'Contrasena actualizada correctamente.')
            return redirect('landing')
    
    return render(request, 'auth/change_password.html')
