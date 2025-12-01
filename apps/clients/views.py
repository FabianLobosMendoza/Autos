"""Views for clients app."""
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import get_object_or_404, redirect, render
from django.db import transaction
from django.db.models import Q
from .forms import ClientForm, CoHolderForm
from .models import Client
from apps.users.models import UserProfile
from apps.audit.models import AuditLog


def is_admin(user):
    """Control de acceso al módulo de clientes."""
    profile = getattr(user, 'profile', None)
    role = getattr(profile, 'role', UserProfile.ROLE_USER) if profile else UserProfile.ROLE_USER
    return user.is_superuser or role in (
        UserProfile.ROLE_ADMIN,
        UserProfile.ROLE_SUPERVISOR,
        UserProfile.ROLE_VENDOR,
    )


@login_required(login_url='login')
@user_passes_test(is_admin, login_url='landing')
def client_list(request):
    """Listado simple de clientes con filtro basico."""
    query = request.GET.get('q', '').strip()
    clients = Client.objects.all()
    if query:
        clients = clients.filter(
            Q(company_name__icontains=query)
            | Q(last_name__icontains=query)
            | Q(first_name__icontains=query)
            | Q(cuit__icontains=query)
        )
    return render(request, 'clients/client_list.html', {'clients': clients, 'query': query})


@login_required(login_url='login')
@user_passes_test(is_admin, login_url='landing')
@transaction.atomic
def client_create(request):
    """Crear cliente y opcionalmente cotitular."""
    if request.method == 'POST':
        client_form = ClientForm(request.POST)
        coholder_form = CoHolderForm(request.POST, prefix='co')

        coholder_has_data = any(
            request.POST.get(f'co-{field}', '').strip()
            for field in coholder_form.fields.keys()
        )

        client_valid = client_form.is_valid()
        coholder_valid = coholder_form.is_valid() if coholder_has_data else True
        forms_valid = client_valid and coholder_valid

        if forms_valid:
            client = client_form.save()
            if coholder_has_data:
                coholder = coholder_form.save(commit=False)
                coholder.client = client
                coholder.save()
            
            # Registrar en auditoría
            client_name = client.company_name if client.company_name else f"{client.first_name} {client.last_name}"
            AuditLog.objects.create(
                actor=request.user,
                action='create_client',
                details=f'Cliente creado: {client_name} (CUIT: {client.cuit})',
                ip_address=request.META.get('REMOTE_ADDR'),
                user_agent=request.META.get('HTTP_USER_AGENT', '')[:255]
            )
            
            messages.success(request, 'Cliente guardado correctamente.')
            return redirect('client_detail', client_id=client.id)
        messages.error(request, 'Revisa los datos obligatorios.')
    else:
        client_form = ClientForm()
        coholder_form = CoHolderForm(prefix='co')

    return render(request, 'clients/client_form.html', {
        'client_form': client_form,
        'coholder_form': coholder_form,
        'is_edit': False,
    })


@login_required(login_url='login')
@user_passes_test(is_admin, login_url='landing')
@transaction.atomic
def client_edit(request, client_id):
    """Editar cliente y cotitular existente."""
    client = get_object_or_404(Client, id=client_id)
    coholder_instance = getattr(client, 'coholder', None)

    if request.method == 'POST':
        client_form = ClientForm(request.POST, instance=client)
        coholder_form = CoHolderForm(request.POST, prefix='co', instance=coholder_instance)

        coholder_has_data = any(
            request.POST.get(f'co-{field}', '').strip()
            for field in coholder_form.fields.keys()
        )

        client_valid = client_form.is_valid()
        coholder_needed = coholder_has_data or coholder_instance
        coholder_valid = coholder_form.is_valid() if coholder_needed else True
        forms_valid = client_valid and coholder_valid

        if forms_valid:
            client = client_form.save()
            if coholder_needed:
                coholder = coholder_form.save(commit=False)
                coholder.client = client
                coholder.save()
            elif coholder_instance:
                coholder_instance.delete()
            
            # Registrar en auditoría
            client_name = client.company_name if client.company_name else f"{client.first_name} {client.last_name}"
            AuditLog.objects.create(
                actor=request.user,
                action='update_client',
                details=f'Cliente actualizado: {client_name} (CUIT: {client.cuit})',
                ip_address=request.META.get('REMOTE_ADDR'),
                user_agent=request.META.get('HTTP_USER_AGENT', '')[:255]
            )
            
            messages.success(request, 'Cliente actualizado.')
            return redirect('client_detail', client_id=client.id)
        messages.error(request, 'Revisa los datos obligatorios.')
    else:
        client_form = ClientForm(instance=client)
        coholder_form = CoHolderForm(prefix='co', instance=coholder_instance)

    return render(request, 'clients/client_form.html', {
        'client_form': client_form,
        'coholder_form': coholder_form,
        'client': client,
        'is_edit': True,
    })


@login_required(login_url='login')
@user_passes_test(is_admin, login_url='landing')
def client_detail(request, client_id):
    """Detalle de cliente y cotitular."""
    client = get_object_or_404(Client, id=client_id)
    coholder = getattr(client, 'coholder', None)
    return render(request, 'clients/client_detail.html', {'client': client, 'coholder': coholder})


@login_required(login_url='login')
@user_passes_test(is_admin, login_url='landing')
def client_contract(request, client_id):
    """Vista imprimible del contrato del cliente."""
    client = get_object_or_404(Client, id=client_id)
    coholder = getattr(client, 'coholder', None)
    return render(request, 'clients/client_contract.html', {
        'client': client,
        'coholder': coholder,
    })
