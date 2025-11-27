"""Views for core app."""
from django.shortcuts import render
from django.contrib.auth.decorators import login_required


@login_required(login_url='login')
def landing(request):
    """Landing page - homepage despu\u0301s del login."""
    profile = getattr(request.user, 'profile', None)
    role_value = getattr(profile, 'role', 'usuario') if profile else 'usuario'
    context = {
        'user': request.user,
        'role': role_value,
    }
    return render(request, 'core/landing.html', context)
