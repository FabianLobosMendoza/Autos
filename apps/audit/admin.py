"""Admin for audit app."""
from django.contrib import admin
from .models import AuditLog

@admin.register(AuditLog)
class AuditLogAdmin(admin.ModelAdmin):
    list_display = ('timestamp', 'actor', 'action', 'target_user', 'ip_address')
    list_filter = ('action', 'timestamp', 'actor')
    search_fields = ('actor__username', 'target_user__username', 'details')
    readonly_fields = ('timestamp', 'actor', 'action', 'target_user', 'details', 'ip_address', 'user_agent')
    
    def has_add_permission(self, request):
        return False
    
    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser
