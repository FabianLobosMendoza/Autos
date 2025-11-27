"""Views for audit app."""
from django.shortcuts import render
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import HttpResponse
from django.db.models import Q
from datetime import datetime
import csv
from apps.audit.models import AuditLog
from apps.users.models import UserProfile

def is_admin(user):
    profile = getattr(user, 'profile', None)
    role = getattr(profile, 'role', UserProfile.ROLE_USER) if profile else UserProfile.ROLE_USER
    return user.is_superuser or role in (UserProfile.ROLE_ADMIN, UserProfile.ROLE_SUPERVISOR)

@login_required(login_url='login')
@user_passes_test(is_admin, login_url='landing')
def audit_log_list(request):
    """Lista de auditoría con filtros."""
    actor_filter = request.GET.get('actor', '')
    action_filter = request.GET.get('action', '')
    date_from = request.GET.get('date_from', '')
    date_to = request.GET.get('date_to', '')
    
    logs = AuditLog.objects.all()
    
    if actor_filter:
        logs = logs.filter(actor__username__icontains=actor_filter)
    if action_filter:
        logs = logs.filter(action__icontains=action_filter)
    if date_from:
        logs = logs.filter(timestamp__gte=date_from)
    if date_to:
        logs = logs.filter(timestamp__lte=date_to)
    
    logs = logs.select_related('actor', 'target_user')[:500]
    
    actions = [action[0] for action in AuditLog.ACTION_CHOICES]
    
    context = {
        'logs': logs,
        'actor_filter': actor_filter,
        'action_filter': action_filter,
        'date_from': date_from,
        'date_to': date_to,
        'actions': actions,
    }
    return render(request, 'audit/audit_list.html', context)

@login_required(login_url='login')
@user_passes_test(is_admin, login_url='landing')
def export_audit_csv(request):
    """Exportar auditoría a CSV."""
    actor_filter = request.GET.get('actor', '')
    action_filter = request.GET.get('action', '')
    date_from = request.GET.get('date_from', '')
    date_to = request.GET.get('date_to', '')
    
    logs = AuditLog.objects.all()
    
    if actor_filter:
        logs = logs.filter(actor__username__icontains=actor_filter)
    if action_filter:
        logs = logs.filter(action__icontains=action_filter)
    if date_from:
        logs = logs.filter(timestamp__gte=date_from)
    if date_to:
        logs = logs.filter(timestamp__lte=date_to)
    
    logs = logs.select_related('actor', 'target_user')[:10000]
    
    response = HttpResponse(content_type='text/csv; charset=utf-8-sig')
    response['Content-Disposition'] = 'attachment; filename="audit_log.csv"'
    
    writer = csv.writer(response)
    writer.writerow(['Fecha/Hora', 'Actor', 'Acción', 'Objetivo', 'Detalles', 'IP', 'User Agent'])
    
    for log in logs:
        writer.writerow([
            log.timestamp.strftime('%Y-%m-%d %H:%M:%S'),
            log.actor.username if log.actor else '',
            log.get_action_display(),
            log.target_user.username if log.target_user else '',
            log.details,
            log.ip_address or '',
            log.user_agent[:50] if log.user_agent else '',
        ])
    
    return response
