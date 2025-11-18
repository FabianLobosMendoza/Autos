@echo off
REM Script de setup para Django app en Windows

echo 🚀 Configurando Concesionario Django...

REM 1. Crear entorno virtual
echo 1️⃣ Creando entorno virtual...
python -m venv venv
call venv\Scripts\activate.bat

REM 2. Instalar dependencias
echo 2️⃣ Instalando dependencias...
python -m pip install --upgrade pip
pip install -r requirements.txt

REM 3. Crear archivo .env
echo 3️⃣ Creando archivo .env...
if not exist .env (
    copy .env.example .env
    echo ✅ .env creado (edítalo si es necesario)
) else (
    echo ℹ️ .env ya existe
)

REM 4. Migraciones
echo 4️⃣ Ejecutando migraciones...
python manage.py migrate

REM 5. Inicializar datos
echo 5️⃣ Inicializando datos...
python init_data.py

REM 6. Crear carpeta de uploads
echo 6️⃣ Creando carpetas necesarias...
if not exist media mkdir media
if not exist staticfiles mkdir staticfiles

REM 7. Recolectar statics
echo 7️⃣ Recolectando archivos estáticos...
python manage.py collectstatic --noinput

echo.
echo ✅ ¡Setup completado!
echo.
echo Para ejecutar el servidor:
echo   venv\Scripts\activate.bat
echo   python manage.py runserver
echo.
echo Accede a: http://localhost:8000
pause
