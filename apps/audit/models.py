"""Models for audit app."""
from django.db import models
from django.contrib.auth.models import User

class AuditLog(models.Model):
    """Registro de auditoría."""
    ACTION_CHOICES = [
        ('login', 'Login'),
        ('logout', 'Logout'),
        ('create_user', 'Crear usuario'),
        ('update_profile', 'Actualizar perfil'),
        ('change_password', 'Cambiar contraseña'),
        ('set_role', 'Cambiar rol'),
        ('delete_user', 'Eliminar usuario'),
        ('reset_password', 'Resetear contraseña'),
        ('create_client', 'Crear cliente'),
        ('update_client', 'Actualizar cliente'),
        ('delete_client', 'Eliminar cliente'),
    ]
    
    actor = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='audit_logs')
    action = models.CharField(max_length=50, choices=ACTION_CHOICES)
    target_user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='audit_targets')
    details = models.TextField(blank=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.TextField(blank=True)
    timestamp = models.DateTimeField(auto_now_add=True, db_index=True)

    def __str__(self):
        return f"{self.actor} - {self.action} - {self.timestamp}"

    class Meta:
        verbose_name = "Audit Log"
        verbose_name_plural = "Audit Logs"
        ordering = ['-timestamp']
        indexes = [
            models.Index(fields=['actor', '-timestamp']),
            models.Index(fields=['action', '-timestamp']),
        ]
