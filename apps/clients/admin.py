"""Admin registration for clients."""
from django.contrib import admin
from .models import Client, CoHolder


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'doc_type', 'doc_number', 'tax_condition', 'cuit', 'phone', 'email')
    search_fields = ('first_name', 'last_name', 'company_name', 'cuit', 'doc_number')
    list_filter = ('tax_condition', 'marital_status', 'nationality', 'sex')


@admin.register(CoHolder)
class CoHolderAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'dni', 'client')
    search_fields = ('full_name', 'dni', 'client__cuit')
