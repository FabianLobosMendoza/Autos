"""Views for core app."""
from django.shortcuts import render
from django.contrib.auth.decorators import login_required


@login_required(login_url='login')
def landing(request):
    """Landing page - homepage despu\u0301s del login."""
    context = {
        'user': request.user,
        'role': 'admin' if request.user.is_staff else 'user',
    }
    return render(request, 'core/landing.html', context)
