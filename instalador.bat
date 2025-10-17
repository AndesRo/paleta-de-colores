@echo off
chcp 65001 >nul
echo 🎨 Instalador del Generador de Paletas IA Professional
echo ===================================================
echo.

echo 📦 Verificando Python...
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python no está instalado o no está en el PATH
    echo 💡 Descarga Python desde: https://python.org
    pause
    exit /b 1
)

echo ✅ Python encontrado

echo 📦 Instalando dependencias...
pip install -r requirements.txt

if errorlevel 1 (
    echo ❌ Error instalando dependencias
    pause
    exit /b 1
)

echo ✅ Dependencias instaladas correctamente

echo 🚀 Creando accesos directos...
echo @echo off > "Generador Paletas IA.bat"
echo chcp 65001 >> "Generador Paletas IA.bat"
echo cd /d "%~dp0" >> "Generador Paletas IA.bat"
echo python app.py >> "Generador Paletas IA.bat"
echo pause >> "Generador Paletas IA.bat"

echo 🎉 ¡Instalación completada!
echo.
echo 📱 Ahora puedes ejecutar la aplicación de dos formas:
echo    1. Doble clic en "Generador Paletas IA.bat"
echo    2. Ejecutar: python app.py
echo.
pause