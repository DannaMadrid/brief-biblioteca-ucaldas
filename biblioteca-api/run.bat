@echo off
REM Script para configurar y ejecutar la API en Windows

echo ================================================
echo API Biblioteca Universitaria - Configuracion
echo ================================================
echo.

REM Verificar si Python está instalado
python --version >nul 2>&1
if errorlevel 1 (
    echo Error: Python no está instalado o no está en el PATH
    echo Descárgalo desde: https://www.python.org/
    pause
    exit /b 1
)

REM Crear entorno virtual si no existe
if not exist "venv" (
    echo Creando entorno virtual...
    python -m venv venv
    echo ✓ Entorno virtual creado
    echo.
)

REM Activar entorno virtual
echo Activando entorno virtual...
call venv\Scripts\activate.bat

REM Instalar dependencias
echo Instalando dependencias...
pip install -r requirements.txt
echo ✓ Dependencias instaladas
echo.

REM Iniciar servidor
echo ================================================
echo Iniciando API en http://localhost:8000
echo ================================================
echo.
echo Presiona Ctrl+C para detener el servidor
echo.
echo Documentación interactiva disponible en:
echo   - Swagger UI: http://localhost:8000/docs
echo   - ReDoc: http://localhost:8000/redoc
echo.

python main.py

pause
