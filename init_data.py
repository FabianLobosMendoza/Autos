#!/usr/bin/env python
"""
Script de inicializacion para la aplicacion Django.
Ejecutar despues de las migraciones para poblar datos iniciales.
"""
import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "concesionario_project.settings")

import django  # noqa: E402  # importa Django luego de setear DJANGO_SETTINGS_MODULE

django.setup()  # inicializa Django antes de tocar modelos

from django.contrib.auth.models import User  # noqa: E402
from apps.users.models import UserProfile  # noqa: E402


def create_default_user():
    """Crea el usuario administrador por defecto."""
    if User.objects.filter(username="Arkangel").exists():
        print("Usuario 'Arkangel' ya existe")
        return

    user = User.objects.create_user(
        username="Arkangel",
        email="arkangel@concesionario.com",
        password="Arkangel_01",
        first_name="Arkangel",
        last_name="Admin",
        is_staff=True,
        is_superuser=True,
    )
    print(f"Usuario '{user.username}' creado")
    UserProfile.objects.get_or_create(user=user)
    print(f"Perfil de '{user.username}' creado")


def create_test_users():
    """Crea usuarios de prueba."""
    test_users = [
        {
            "username": "usuario1",
            "email": "usuario1@concesionario.com",
            "password": "Password123",
            "first_name": "Juan",
            "last_name": "Garcia",
        },
        {
            "username": "usuario2",
            "email": "usuario2@concesionario.com",
            "password": "Password123",
            "first_name": "Maria",
            "last_name": "Lopez",
        },
    ]

    for user_data in test_users:
        if User.objects.filter(username=user_data["username"]).exists():
            print(f"Usuario '{user_data['username']}' ya existe")
            continue
        user = User.objects.create_user(**user_data)
        UserProfile.objects.get_or_create(user=user)
        print(f"Usuario '{user.username}' creado")


if __name__ == "__main__":
    print("Inicializando datos de la aplicacion...")
    create_default_user()
    create_test_users()
    print("Inicializacion completada")
