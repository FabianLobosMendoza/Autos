"""URLs for core app."""
from django.urls import path
from . import views

urlpatterns = [
    path('', views.landing, name='landing'),
    path('toggle-theme/', views.toggle_theme, name='toggle_theme'),
]
