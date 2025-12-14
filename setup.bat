@echo off
REM Script de setup para Django app en Windows

echo 🚀 Configurando Concesionario Django...

REM 1. Crear entorno virtual
echo 1️⃣ Creando entorno virtual...
if not exist venv python -m venv venv
call venv\Scripts\activate.bat

REM 2. Instalar dependencias
echo 2️⃣ Instalando dependencias...
python -m pip install --upgrade pip setuptools wheel
pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo ❌ Error instalando dependencias.
    pause
    exit /b
)

REM 3. Crear archivo .env
echo 3️⃣ Creando archivo .env...
if not exist .env (
    if exist .env.example (
        copy .env.example .env
        echo ✅ .env creado (edítalo si es necesario)
    ) else (
        echo ⚠️ .env.example no encontrado. Creando .env vacio...
        type nul > .env
    )
) else (
    echo ℹ️ .env ya existe
)

REM 4. Migraciones
echo 4️⃣ Ejecutando migraciones...
python manage.py migrate
if %errorlevel% neq 0 (
    echo ❌ Error ejecutando migraciones.
    pause
    exit /b
)

REM 5. Inicializar datos
echo 5️⃣ Inicializando datos...
if exist init_data.py (
    python init_data.py
) else (
    echo ⚠️ init_data.py no encontrado. Saltando carga de datos.
)

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
