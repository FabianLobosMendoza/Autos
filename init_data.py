#!/usr/bin/env python
"""
Script de inicialización para la aplicación Django.
Ejecutar después de las migraciones para poblar datos iniciales.
"""
import os
import django
from django.contrib.auth.models import User

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'concesionario_project.settings')
django.setup()

from apps.users.models import UserProfile
from apps.core.models import ThemePreference

def create_default_user():
    """Crea el usuario por defecto Arkangel."""
    if not User.objects.filter(username='Arkangel').exists():
        user = User.objects.create_user(
            username='Arkangel',
            email='arkangel@concesionario.com',
            password='Arkangel_01',
            first_name='Arkangel',
            last_name='Admin',
            is_staff=True,
            is_superuser=True
        )
        print(f"✅ Usuario '{user.username}' creado exitosamente")
        
        # Crear perfil
        profile, _ = UserProfile.objects.get_or_create(user=user)
        print(f"✅ Perfil de '{user.username}' creado")
        
        # Crear preferencia de tema
        theme_pref, _ = ThemePreference.objects.get_or_create(user=user)
        print(f"✅ Preferencia de tema para '{user.username}' creada")
    else:
        print("ℹ️ Usuario 'Arkangel' ya existe")

def create_test_users():
    """Crea usuarios de prueba."""
    test_users = [
        {
            'username': 'usuario1',
            'email': 'usuario1@concesionario.com',
            'password': 'Password123',
            'first_name': 'Juan',
            'last_name': 'García',
        },
        {
            'username': 'usuario2',
            'email': 'usuario2@concesionario.com',
            'password': 'Password123',
            'first_name': 'María',
            'last_name': 'López',
        }
    ]
    
    for user_data in test_users:
        if not User.objects.filter(username=user_data['username']).exists():
            user = User.objects.create_user(**user_data)
            UserProfile.objects.get_or_create(user=user)
            ThemePreference.objects.get_or_create(user=user)
            print(f"✅ Usuario '{user.username}' creado")
        else:
            print(f"ℹ️ Usuario '{user_data['username']}' ya existe")

if __name__ == '__main__':
    print("🚀 Inicializando datos de la aplicación...")
    create_default_user()
    create_test_users()
    print("✅ Inicialización completada")
