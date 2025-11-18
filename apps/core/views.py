"""Views for core app."""
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from apps.core.models import ThemePreference

@login_required(login_url='login')
def landing(request):
    """Landing page - homepage después del login."""
    context = {
        'user': request.user,
        'role': 'admin' if request.user.is_staff else 'user',
    }
    return render(request, 'core/landing.html', context)

@login_required(login_url='login')
def toggle_theme(request):
    """Alterna el tema del usuario."""
    theme_pref, _ = ThemePreference.objects.get_or_create(user=request.user)
    theme_pref.theme = 'dark' if theme_pref.theme == 'light' else 'light'
    theme_pref.save()
    return redirect(request.META.get('HTTP_REFERER', 'landing'))
