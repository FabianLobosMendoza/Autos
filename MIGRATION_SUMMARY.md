# Migracion Tkinter -> Django (Resumen)

## Estado
- Migracion completada. Django 4.2.x, Python 3.10+.

## Estructura Django
- `concesionario_project/` configuracion y urls globales.
- `apps/core/`: landing simple.
- `apps/auth_app/`: login, registro, logout, cambio de contrasena.
- `apps/users/`: perfiles y administracion de usuarios.
- `apps/audit/`: modelo y vistas de auditoria, export CSV.
- `templates/`: base con navbar, vistas para auth, landing y usuarios.
- `static/`: colocar CSS/JS/imagenes.

## Modelos clave
- `users.UserProfile`: datos extra (telefono, direccion, notas, nacimiento).
- `audit.AuditLog`: registro de acciones con actor, objetivo, detalles, IP, user agent, timestamp.

## Funcionalidad portada desde Tkinter
- Autenticacion completa con mensajes de error y recordar sesion.
- Gestion de usuarios (CRUD, toggle admin, cambio de contrasena).
- Auditoria automatica y exportable.
- Landing post-login y plantilla base con navbar.

## Operaciones basicas
```bash
python manage.py migrate
python init_data.py
python manage.py runserver
```

## Notas
- Los archivos originales de Tkinter se mantienen en la raiz por referencia.
- El tema oscuro claro se removio; la interfaz usa un tema claro fijo.
