"""Admin for core app."""
from django.contrib import admin
from .models import ThemePreference

@admin.register(ThemePreference)
class ThemePreferenceAdmin(admin.ModelAdmin):
    list_display = ('user', 'theme', 'updated_at')
    search_fields = ('user__username',)
    readonly_fields = ('created_at', 'updated_at')
