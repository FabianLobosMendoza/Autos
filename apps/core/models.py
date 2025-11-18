"""Models for core app."""
from django.db import models
from django.contrib.auth.models import User

class ThemePreference(models.Model):
    """Preferencia de tema por usuario."""
    THEME_CHOICES = [('light', 'Claro'), ('dark', 'Oscuro')]
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='theme_pref')
    theme = models.CharField(max_length=10, choices=THEME_CHOICES, default='light')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username} - {self.theme}"

    class Meta:
        verbose_name_plural = "Theme Preferences"
