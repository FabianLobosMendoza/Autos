# Quick Start - Concesionario (Django)

## Que incluye
- Aplicacion Django con apps: `core` (landing), `auth_app` (login/registro), `users` (gestion de usuarios), `audit` (logs).
- Templates base con Bootstrap 5.
- Script `init_data.py` para crear usuarios de prueba.

## Instalacion rapida
```bash
python -m venv venv
source venv/bin/activate        # En Windows: venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python init_data.py
python manage.py runserver
```

## Rutas principales
- `/` landing (requiere login)
- `/auth/login/`, `/auth/register/`, `/auth/logout/`, `/auth/change-password/`
- `/users/` CRUD de usuarios (admin)
- `/users/profile/` ver/editar mi perfil
- `/audit/` y `/audit/export/` (admin)
- `/admin/` panel de Django

## Credenciales de prueba
- Usuario: `Arkangel`
- Contrasena: `Arkangel_01`
- Rol: Administrador

## Funcionalidades
- Autenticacion (login, registro, logout, cambio de contrasena, remember me)
- Gestion de usuarios (admin): listar, ver, editar, cambiar rol, resetear contrasena, eliminar
- Auditoria: registro automatico, filtros, exportacion CSV

## Notas
- Los archivos originales de Tkinter siguen en la raiz por referencia (`main.py`, `database.py`, etc.).
- Personaliza las variables de entorno copiando `.env.example` si lo necesitas.
