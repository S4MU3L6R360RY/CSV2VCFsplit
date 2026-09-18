@echo off

echo ==========================================
echo       CSV to VCF Converter Builder
echo ==========================================
echo.

echo Installing PyInstaller...
python -m pip install --upgrade pyinstaller

echo.
echo Cleaning previous build...

if exist build rmdir /s /q build
if exist dist rmdir /s /q dist

echo.
echo Building standalone EXE...
echo.

python -m PyInstaller ^
    --onefile ^
    --windowed ^
    --name CSV-to-VCF ^
    src\app.py

echo.
echo ==========================================
echo Build completed.
echo ==========================================
echo.
echo EXE location:
echo dist\CSV-to-VCF.exe
echo.

pause
