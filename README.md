# Autos

Proyecto Django 4.2 para un concesionario, con autenticacion, perfiles de usuario y auditoria. Usa REST Framework, CORS y Crispy (Bootstrap 5).

## Requisitos
- Python 3.10+ (virtualenv recomendado)
- Pip

## Configuracion rapida
1) Crear entorno: `python -m venv venv` y activarlo.  
2) Instalar dependencias: `pip install -r requirements.txt`.  
3) Copiar el ejemplo de variables: `cp .env.example .env` (o duplicarlo en Windows) y ajustar:
   - `SECRET_KEY` (cambia esta clave)
   - `DEBUG` (`True` en local, `False` en prod)
   - `ALLOWED_HOSTS` (dominios o IPs separados por coma)
   - `CORS_ALLOWED_ORIGINS` (origenes permitidos para frontend)
4) Aplicar migraciones: `python manage.py migrate`.  
5) Datos de ejemplo (usuarios): `python init_data.py` despues de las migraciones.  
6) (Opcional) Crea un superusuario: `python manage.py createsuperuser`.  
7) Levantar el servidor: `python manage.py runserver` y abre http://localhost:8000/.

## Estructura util
- `concesionario_project/`: configuracion base de Django.
- `apps/`: modulos principales (`core`, `auth_app`, `users`, `audit`).
- `templates/`: plantillas HTML.
- `init_data.py`: script para crear usuarios de demo (incluye admin "Arkangel").

## Comandos rapidos
- Formato/cambios estaticos: `python manage.py collectstatic` (para despliegue).
- Pruebas y linting: agrega los comandos que uses en tu entorno de CI.

## Despliegue
- Configura `DEBUG=False`, `ALLOWED_HOSTS` y `CORS_ALLOWED_ORIGINS`.
- Ajusta la base de datos en `concesionario_project/settings.py` si usas Postgres u otro motor.
- Sirve estaticos desde `staticfiles/` y media desde `media/` segun tu servidor web.
