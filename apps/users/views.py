"""Views for users app."""
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from django.contrib import messages
from django.db.models import Q
from apps.users.models import UserProfile


def is_admin(user):
    """Verifica si el usuario tiene rol administrador o supervisor."""
    profile = getattr(user, 'profile', None)
    role = getattr(profile, 'role', UserProfile.ROLE_USER) if profile else UserProfile.ROLE_USER
    return user.is_superuser or role in (UserProfile.ROLE_ADMIN, UserProfile.ROLE_SUPERVISOR)


def ensure_user_related(user):
    """Garantiza que el usuario tenga perfil."""
    UserProfile.objects.get_or_create(user=user, defaults={'role': UserProfile.ROLE_USER})


@login_required(login_url='login')
@user_passes_test(is_admin, login_url='landing')
def user_list(request):
    """Lista de usuarios (solo admins)."""
    query = request.GET.get('q', '')
    if query:
        users = User.objects.filter(Q(username__icontains=query) | Q(email__icontains=query))
    else:
        users = User.objects.all()
    
    context = {'users': users, 'query': query}
    return render(request, 'users/user_list.html', context)


@login_required(login_url='login')
@user_passes_test(is_admin, login_url='landing')
def user_detail(request, user_id):
    """Detalle de usuario."""
    user = get_object_or_404(User, id=user_id)
    ensure_user_related(user)
    profile = user.profile
    
    context = {'user': user, 'profile': profile}
    return render(request, 'users/user_detail.html', context)


@login_required(login_url='login')
@user_passes_test(is_admin, login_url='landing')
def edit_user_profile(request, user_id):
    """Editar perfil de usuario."""
    user = get_object_or_404(User, id=user_id)
    ensure_user_related(user)
    profile = user.profile
    
    if request.method == 'POST':
        user.first_name = request.POST.get('first_name', '')
        user.last_name = request.POST.get('last_name', '')
        user.email = request.POST.get('email', '')
        role_value = request.POST.get('role', UserProfile.ROLE_USER)
        user.is_staff = role_value in (UserProfile.ROLE_ADMIN, UserProfile.ROLE_SUPERVISOR)
        user.save()
        
        profile.phone = request.POST.get('phone', '')
        profile.address = request.POST.get('address', '')
        profile.notes = request.POST.get('notes', '')
        birthdate_value = request.POST.get('birthdate')
        profile.birthdate = birthdate_value or None
        profile.role = role_value
        profile.save()
        
        messages.success(request, 'Perfil actualizado.')
        return redirect('user_detail', user_id=user.id)
    
    context = {'user': user, 'profile': profile}
    return render(request, 'users/edit_profile.html', context)


@login_required(login_url='login')
@user_passes_test(is_admin, login_url='landing')
def change_user_password(request, user_id):
    """Cambiar contrasena de un usuario (admin)."""
    user = get_object_or_404(User, id=user_id)
    ensure_user_related(user)
    
    if request.method == 'POST':
        new_password = request.POST.get('new_password', '')
        confirm_password = request.POST.get('confirm_password', '')
        
        if not new_password:
            messages.error(request, 'Ingresa la nueva contrasena.')
        elif new_password != confirm_password:
            messages.error(request, 'Las contrasenas no coinciden.')
        else:
            user.set_password(new_password)
            user.save()
            messages.success(request, f'Contrasena de {user.username} actualizada.')
            return redirect('user_detail', user_id=user.id)
    
    context = {'user': user}
    return render(request, 'users/change_password.html', context)


@login_required(login_url='login')
@user_passes_test(is_admin, login_url='landing')
def toggle_admin(request, user_id):
    """Cambiar estado de admin del usuario."""
    user = get_object_or_404(User, id=user_id)
    ensure_user_related(user)
    user.is_staff = not user.is_staff
    user.save()
    user.profile.role = UserProfile.ROLE_ADMIN if user.is_staff else UserProfile.ROLE_USER
    user.profile.save()
    status = "administrador" if user.is_staff else "usuario"
    messages.success(request, f'{user.username} ahora es {status}.')
    return redirect('user_detail', user_id=user.id)


@login_required(login_url='login')
@user_passes_test(is_admin, login_url='landing')
def update_user_role(request, user_id):
    """Actualizar rol del usuario desde el detalle."""
    user = get_object_or_404(User, id=user_id)
    ensure_user_related(user)

    if request.method != 'POST':
        messages.error(request, 'Método no permitido.')
        return redirect('user_detail', user_id=user.id)

    new_role = request.POST.get('role', UserProfile.ROLE_USER)
    valid_roles = [choice[0] for choice in UserProfile.ROLE_CHOICES]
    if new_role not in valid_roles:
        messages.error(request, 'Rol inválido.')
        return redirect('user_detail', user_id=user.id)

    user.is_staff = new_role in (UserProfile.ROLE_ADMIN, UserProfile.ROLE_SUPERVISOR)
    user.save()
    profile = user.profile
    profile.role = new_role
    profile.save(update_fields=['role'])

    messages.success(request, f'Rol de {user.username} actualizado a {profile.get_role_display()}.')
    return redirect('user_detail', user_id=user.id)


@login_required(login_url='login')
@user_passes_test(is_admin, login_url='landing')
def delete_user(request, user_id):
    """Eliminar usuario."""
    user = get_object_or_404(User, id=user_id)
    ensure_user_related(user)
    if user == request.user:
        messages.error(request, 'No puedes eliminar tu propio usuario.')
        return redirect('user_list')
    
    if request.method == 'POST':
        user.delete()
        messages.success(request, f'Usuario {user.username} eliminado.')
        return redirect('user_list')
    
    context = {'user': user}
    return render(request, 'users/delete_confirm.html', context)


@login_required(login_url='login')
def profile_view(request):
    """Perfil del usuario actual."""
    ensure_user_related(request.user)
    profile = request.user.profile
    
    context = {'profile': profile}
    return render(request, 'users/profile_view.html', context)


@login_required(login_url='login')
def profile_edit(request):
    """Editar perfil del usuario actual."""
    ensure_user_related(request.user)
    profile = request.user.profile
    
    if request.method == 'POST':
        request.user.first_name = request.POST.get('first_name', '')
        request.user.last_name = request.POST.get('last_name', '')
        request.user.email = request.POST.get('email', '')
        request.user.save()
        
        profile.phone = request.POST.get('phone', '')
        profile.address = request.POST.get('address', '')
        profile.notes = request.POST.get('notes', '')
        birthdate_value = request.POST.get('birthdate')
        profile.birthdate = birthdate_value or None
        profile.save()
        
        messages.success(request, 'Perfil actualizado.')
        return redirect('profile_view')
    
    context = {'profile': profile}
    return render(request, 'users/profile_edit.html', context)


@login_required(login_url='login')
@user_passes_test(is_admin, login_url='landing')
def create_user(request):
    """Crear un nuevo usuario (solo admins)."""
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        email = request.POST.get('email', '').strip()
        first_name = request.POST.get('first_name', '').strip()
        last_name = request.POST.get('last_name', '').strip()
        password = request.POST.get('password', '')
        confirm_password = request.POST.get('confirm_password', '')
        role_value = request.POST.get('role', UserProfile.ROLE_USER)
        phone = request.POST.get('phone', '').strip()
        address = request.POST.get('address', '').strip()
        notes = request.POST.get('notes', '').strip()
        birthdate_value = request.POST.get('birthdate')

        if not username or not email or not password:
            messages.error(request, 'Usuario, email y contrasena son obligatorios.')
            return render(request, 'users/create_user.html')

        if password != confirm_password:
            messages.error(request, 'Las contrasenas no coinciden.')
            return render(request, 'users/create_user.html')

        if User.objects.filter(username=username).exists():
            messages.error(request, 'El nombre de usuario ya existe.')
            return render(request, 'users/create_user.html')

        if User.objects.filter(email=email).exists():
            messages.error(request, 'El email ya esta registrado.')
            return render(request, 'users/create_user.html')

        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name,
            is_staff=role_value in (UserProfile.ROLE_ADMIN, UserProfile.ROLE_SUPERVISOR),
        )
        UserProfile.objects.get_or_create(
            user=user,
            defaults={
                'role': role_value,
                'phone': phone,
                'address': address,
                'notes': notes,
                'birthdate': birthdate_value or None,
            }
        )

        messages.success(request, f'Usuario {user.username} creado correctamente.')
        return redirect('user_detail', user_id=user.id)

    return render(request, 'users/create_user.html')
