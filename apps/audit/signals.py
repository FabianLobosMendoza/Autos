"""Signals for audit app."""
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.contrib.auth.models import User
from apps.audit.models import AuditLog
from apps.users.models import UserProfile

def get_client_ip(request):
    """Obtiene la IP del cliente."""
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

@receiver(post_save, sender=UserProfile)
def log_profile_update(sender, instance, created, **kwargs):
    """Registra actualizaciones de perfil."""
    if not created:
        AuditLog.objects.create(
            action='update_profile',
            target_user=instance.user,
            details=f'Perfil actualizado: {instance.user.username}'
        )

@receiver(post_delete, sender=User)
def log_user_delete(sender, instance, **kwargs):
    """Registra eliminación de usuarios."""
    AuditLog.objects.create(
        action='delete_user',
        target_user=instance,
        details=f'Usuario eliminado: {instance.username}'
    )
