#!/bin/bash
# Script de setup para Django app en Linux/Mac

echo "🚀 Configurando Concesionario Django..."

# 1. Crear entorno virtual
echo "1️⃣ Creando entorno virtual..."
python3 -m venv venv
source venv/bin/activate

# 2. Instalar dependencias
echo "2️⃣ Instalando dependencias..."
pip install --upgrade pip
pip install -r requirements.txt

# 3. Crear archivo .env
echo "3️⃣ Creando archivo .env..."
if [ ! -f .env ]; then
    cp .env.example .env
    echo "✅ .env creado (edítalo si es necesario)"
else
    echo "ℹ️ .env ya existe"
fi

# 4. Migraciones
echo "4️⃣ Ejecutando migraciones..."
python manage.py migrate

# 5. Crear superusuario (opcional)
echo "5️⃣ Inicializando datos..."
python init_data.py

# 6. Crear carpeta de uploads
echo "6️⃣ Creando carpetas necesarias..."
mkdir -p media
mkdir -p staticfiles

# 7. Recolectar statics
echo "7️⃣ Recolectando archivos estáticos..."
python manage.py collectstatic --noinput

echo "✅ ¡Setup completado!"
echo ""
echo "Para ejecutar el servidor:"
echo "  source venv/bin/activate"
echo "  python manage.py runserver"
echo ""
echo "Accede a: http://localhost:8000"
