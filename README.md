# Autos

Proyecto Django 4.2 para un concesionario, con autenticación, perfiles de usuario, auditoría y personalización de tema. Usa REST Framework, CORS y Crispy (Bootstrap 5).

## Requisitos
- Python 3.10+ (virtualenv recomendado)
- Pip

## Configuración rápida
1) Crear entorno: `python -m venv venv` y activarlo.  
2) Instalar dependencias: `pip install -r requirements.txt`.  
3) Copiar el ejemplo de variables: `cp .env.example .env` (o duplicarlo en Windows) y ajustar:
   - `SECRET_KEY` (cambia esta clave)
   - `DEBUG` (`True` en local, `False` en prod)
   - `ALLOWED_HOSTS` (dominios o IPs separados por coma)
   - `CORS_ALLOWED_ORIGINS` (orígenes permitidos para frontend)
4) Aplicar migraciones: `python manage.py migrate`.  
5) Datos de ejemplo (usuarios y preferencias): `python init_data.py` después de las migraciones.  
6) (Opcional) Crea un superusuario: `python manage.py createsuperuser`.  
7) Levantar el servidor: `python manage.py runserver` y abre http://localhost:8000/.

## Estructura útil
- `concesionario_project/`: configuración base de Django.
- `apps/`: módulos principales (`core`, `auth_app`, `users`, `audit`).
- `templates/`: plantillas HTML.
- `init_data.py`: script para crear usuarios de demo (incluye admin “Arkangel”).

## Comandos rápidos
- Formato/cambios estáticos: `python manage.py collectstatic` (para despliegue).
- Pruebas y linting: agrega los comandos que uses en tu entorno de CI.

## Despliegue
- Configura `DEBUG=False`, `ALLOWED_HOSTS` y `CORS_ALLOWED_ORIGINS`.
- Ajusta la base de datos en `concesionario_project/settings.py` si usas Postgres u otro motor.
- Sirve estáticos desde `staticfiles/` y media desde `media/` según tu servidor web.
