"""Models for users app."""
from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    """Perfil extendido de usuario."""
    ROLE_ADMIN = 'admin'
    ROLE_VENDOR = 'vendedor'
    ROLE_NEGOTIATOR = 'negociador'
    ROLE_SUPERVISOR = 'supervisor'
    ROLE_MANAGER = 'gestor'
    ROLE_ACCOUNTANT = 'contable'
    ROLE_MARKETING = 'marqueting'
    ROLE_CHOICES = [
        (ROLE_ADMIN, 'Administrador'),
        (ROLE_VENDOR, 'Vendedor'),
        (ROLE_NEGOTIATOR, 'Negociador oficial de cuenta'),
        (ROLE_SUPERVISOR, 'Supervisor'),
        (ROLE_MANAGER, 'Gestor'),
        (ROLE_ACCOUNTANT, 'Contable'),
        (ROLE_MARKETING, 'Marqueting'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default=ROLE_VENDOR)
    phone = models.CharField(max_length=20, blank=True)
    birthdate = models.DateField(null=True, blank=True)
    address = models.CharField(max_length=255, blank=True)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Profile de {self.user.username}"

    class Meta:
        verbose_name = "User Profile"
        verbose_name_plural = "User Profiles"
