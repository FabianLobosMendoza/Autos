"""URLs for audit app."""
from django.urls import path
from . import views

urlpatterns = [
    path('', views.audit_log_list, name='audit_log_list'),
    path('export/', views.export_audit_csv, name='export_audit_csv'),
]
