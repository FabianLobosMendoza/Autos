"""Models for users app."""
from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    """Perfil extendido de usuario."""
    ROLE_ADMIN = 'admin'
    ROLE_USER = 'usuario'
    ROLE_VENDOR = 'vendedor'
    ROLE_SUPERVISOR = 'supervisor'
    ROLE_CHOICES = [
        (ROLE_ADMIN, 'Administrador'),
        (ROLE_USER, 'Usuario'),
        (ROLE_VENDOR, 'Vendedor oficial de cuentas'),
        (ROLE_SUPERVISOR, 'Supervisor'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default=ROLE_USER)
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
