#!/bin/bash

# Script para configurar y ejecutar la API en Linux/Mac

echo "================================================"
echo "API Biblioteca Universitaria - Configuracion"
echo "================================================"
echo ""

# Verificar si Python está instalado
if ! command -v python3 &> /dev/null; then
    echo "Error: Python 3 no está instalado"
    echo "Instálalo usando: sudo apt-get install python3 python3-pip"
    exit 1
fi

# Crear entorno virtual si no existe
if [ ! -d "venv" ]; then
    echo "Creando entorno virtual..."
    python3 -m venv venv
    echo "✓ Entorno virtual creado"
    echo ""
fi

# Activar entorno virtual
echo "Activando entorno virtual..."
source venv/bin/activate

# Instalar dependencias
echo "Instalando dependencias..."
pip install -r requirements.txt
echo "✓ Dependencias instaladas"
echo ""

# Iniciar servidor
echo "================================================"
echo "Iniciando API en http://localhost:8000"
echo "================================================"
echo ""
echo "Presiona Ctrl+C para detener el servidor"
echo ""
echo "Documentación interactiva disponible en:"
echo "  - Swagger UI: http://localhost:8000/docs"
echo "  - ReDoc: http://localhost:8000/redoc"
echo ""

python main.py
