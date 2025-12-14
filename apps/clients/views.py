"""Views for clients app."""
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import get_object_or_404, redirect, render
from django.db import transaction
from django.db.models import Q
from .forms import ClientForm, CoHolderForm, ClientEventForm
from .models import Client, ClientNote, ClientEvent
from apps.users.models import UserProfile
from apps.audit.models import AuditLog


def is_admin(user):
    """Control de acceso al módulo de clientes."""
    profile = getattr(user, 'profile', None)
    role = getattr(profile, 'role', UserProfile.ROLE_VENDOR) if profile else UserProfile.ROLE_VENDOR
    return user.is_superuser or role in (
        UserProfile.ROLE_ADMIN,
        UserProfile.ROLE_SUPERVISOR,
        UserProfile.ROLE_VENDOR,
        UserProfile.ROLE_NEGOTIATOR,
    )


def is_full_admin(user):
    """Admin/supervisor (no restringido a sus propios clientes)."""
    profile = getattr(user, 'profile', None)
    role = getattr(profile, 'role', UserProfile.ROLE_VENDOR) if profile else UserProfile.ROLE_VENDOR
    return user.is_superuser or role in (UserProfile.ROLE_ADMIN, UserProfile.ROLE_SUPERVISOR)


@login_required(login_url='login')
@user_passes_test(is_admin, login_url='landing')
def client_list(request):
    """Listado simple de clientes con filtro basico."""
    full_admin = is_full_admin(request.user)
    query = request.GET.get('q', '').strip()
    clients = Client.objects.all()
    if not full_admin:
        clients = clients.filter(owner=request.user)
    if query:
        clients = clients.filter(
            Q(company_name__icontains=query)
            | Q(last_name__icontains=query)
            | Q(first_name__icontains=query)
            | Q(cuit__icontains=query)
            | Q(phone__icontains=query)
            | Q(coholder__phone__icontains=query)
        )
    return render(request, 'clients/client_list.html', {'clients': clients, 'query': query})


@login_required(login_url='login')
@user_passes_test(is_admin, login_url='landing')
@transaction.atomic
def client_create(request):
    """Crear cliente y opcionalmente cotitular."""
    if request.method == 'POST':
        client_form = ClientForm(request.POST, user=request.user)
        coholder_form = CoHolderForm(request.POST, prefix='co')

        coholder_has_data = any(
            request.POST.get(f'co-{field}', '').strip()
            for field in coholder_form.fields.keys()
        )

        client_valid = client_form.is_valid()
        coholder_valid = coholder_form.is_valid() if coholder_has_data else True
        forms_valid = client_valid and coholder_valid

        if forms_valid:
            client = client_form.save(commit=False)
            client.owner = client_form.cleaned_data.get('owner') or request.user
            client.save()
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
    full_admin = is_full_admin(request.user)
    if not full_admin and client.owner != request.user:
        messages.error(request, 'No tienes permiso para editar este cliente.')
        return redirect('client_list')

    if request.method == 'POST':
        data = request.POST
        # Si no envían fecha, conserva la existente para evitar sobreescribirla.
        if not request.POST.get('birth_date') and client.birth_date:
            data = request.POST.copy()
            data['birth_date'] = client.birth_date.isoformat()

        co_data = data
        if coholder_instance and not request.POST.get('co-birth_date') and coholder_instance.birth_date:
            co_data = data.copy()
            co_data['co-birth_date'] = coholder_instance.birth_date.isoformat()

        client_form = ClientForm(data, instance=client, user=request.user)
        coholder_form = CoHolderForm(co_data, prefix='co', instance=coholder_instance)

        coholder_has_data = any(
            (co_data.get(f'co-{field}', '') or '').strip()
            for field in coholder_form.fields.keys()
        )

        client_valid = client_form.is_valid()
        if coholder_instance and not coholder_has_data:
            # No sobrescribir datos del cotitular si no se envió nada.
            coholder_valid = True
        else:
            coholder_valid = coholder_form.is_valid() if coholder_has_data or coholder_instance else True
        forms_valid = client_valid and coholder_valid

        if forms_valid:
            client = client_form.save(commit=False)
            if full_admin:
                client.owner = client_form.cleaned_data.get('owner') or client.owner
            client.save()
            if coholder_has_data:
                coholder = coholder_form.save(commit=False)
                coholder.client = client
                coholder.save()
            
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
        client_form = ClientForm(instance=client, user=request.user)
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
    full_admin = is_full_admin(request.user)
    if not full_admin and client.owner != request.user:
        messages.error(request, 'No tienes permiso para ver este cliente.')
        return redirect('client_list')
    coholder = getattr(client, 'coholder', None)
    if request.method == 'POST':
        note_text = request.POST.get('note', '').strip()
        if note_text:
            ClientNote.objects.create(
                client=client,
                content=note_text,
                author=request.user if request.user.is_authenticated else None,
            )
            messages.success(request, 'Nota agregada.')
            return redirect('client_detail', client_id=client.id)
        messages.error(request, 'Ingresa una nota antes de guardar.')

    notes = ClientNote.objects.filter(client=client).select_related('author')
    return render(request, 'clients/client_detail.html', {
        'client': client,
        'coholder': coholder,
        'notes': notes,
    })


@login_required(login_url='login')
@user_passes_test(is_admin, login_url='landing')
def client_contract(request, client_id):
    """Vista imprimible del contrato del cliente."""
    client = get_object_or_404(Client, id=client_id)
    full_admin = is_full_admin(request.user)
    if not full_admin and client.owner != request.user:
        messages.error(request, 'No tienes permiso para ver este contrato.')
        return redirect('client_list')
    coholder = getattr(client, 'coholder', None)
    return render(request, 'clients/client_contract.html', {
        'client': client,
        'coholder': coholder,
    })


@login_required(login_url='login')
@user_passes_test(is_admin, login_url='landing')
def client_pdf(request, client_id):
    """Vista exportable (para imprimir/guardar como PDF) con datos completos del cliente."""
    client = get_object_or_404(Client, id=client_id)
    full_admin = is_full_admin(request.user)
    if not full_admin and client.owner != request.user:
        messages.error(request, 'No tienes permiso para ver este PDF.')
        return redirect('client_list')
    coholder = getattr(client, 'coholder', None)
    notes = ClientNote.objects.filter(client=client).select_related('author')
    return render(request, 'clients/client_pdf.html', {
        'client': client,
        'coholder': coholder,
        'notes': notes,
    })


@login_required(login_url='login')
@user_passes_test(is_admin, login_url='landing')
def client_calendar(request):
    """Calendario simple para agendar reuniones con clientes."""
    # Admin ve todos; otros roles permitidos solo ven sus propios eventos.
    profile = getattr(request.user, 'profile', None)
    role = getattr(profile, 'role', UserProfile.ROLE_VENDOR) if profile else UserProfile.ROLE_VENDOR
    is_admin_user = request.user.is_superuser or role == UserProfile.ROLE_ADMIN

    qs = ClientEvent.objects.select_related('client', 'owner', 'owner__profile').order_by('starts_at')
    show_owner = is_admin_user or role == UserProfile.ROLE_SUPERVISOR
    events = qs if is_admin_user else qs.filter(owner=request.user)
    form = ClientEventForm(request.POST or None, user=request.user)

    if request.method == 'POST':
        if form.is_valid():
            event = form.save(commit=False)
            if not is_admin_user:
                event.owner = request.user
            event.save()
            messages.success(request, 'Evento agendado.')
            return redirect('client_calendar')
        else:
            messages.error(request, 'Revisa los datos del evento.')

    return render(request, 'clients/client_calendar.html', {
        'events': events,
        'form': form,
        'show_owner': show_owner,
    })


@login_required(login_url='login')
@user_passes_test(is_admin, login_url='landing')
def client_event_edit(request, event_id):
    """Editar un evento existente."""
    event = get_object_or_404(ClientEvent.objects.select_related('owner'), id=event_id)
    profile = getattr(request.user, 'profile', None)
    role = getattr(profile, 'role', UserProfile.ROLE_VENDOR) if profile else UserProfile.ROLE_VENDOR
    is_admin_user = request.user.is_superuser or role == UserProfile.ROLE_ADMIN
    if not is_admin_user and event.owner != request.user:
        messages.error(request, 'No tienes permiso para editar este evento.')
        return redirect('client_calendar')

    form = ClientEventForm(request.POST or None, instance=event, user=request.user)
    if request.method == 'POST' and form.is_valid():
        ev = form.save(commit=False)
        if not is_admin_user:
            ev.owner = request.user
        ev.save()
        messages.success(request, 'Evento actualizado.')
        return redirect('client_calendar')
    elif request.method == 'POST':
        messages.error(request, 'Revisa los datos del evento.')

    return render(request, 'clients/client_event_form.html', {
        'form': form,
        'event': event,
    })


@login_required(login_url='login')
@user_passes_test(is_admin, login_url='landing')
def client_event_delete(request, event_id):
    """Eliminar un evento."""
    event = get_object_or_404(ClientEvent, id=event_id)
    profile = getattr(request.user, 'profile', None)
    role = getattr(profile, 'role', UserProfile.ROLE_VENDOR) if profile else UserProfile.ROLE_VENDOR
    is_admin_user = request.user.is_superuser or role == UserProfile.ROLE_ADMIN
    if not is_admin_user and event.owner != request.user:
        messages.error(request, 'No tienes permiso para eliminar este evento.')
        return redirect('client_calendar')
    if request.method == 'POST':
        event.delete()
        messages.success(request, 'Evento eliminado.')
    return redirect('client_calendar')
