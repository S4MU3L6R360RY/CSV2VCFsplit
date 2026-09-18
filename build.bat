@echo off

echo ==========================================
echo       CSV to VCF Converter Builder
echo ==========================================
echo.

echo Installing PyInstaller...
python -m pip install --upgrade pyinstaller

echo.
echo Building standalone EXE...
echo.

python -m PyInstaller ^
    --onefile ^
    --windowed ^
    --name CSV-to-VCF ^
    csv_to_vcf.py

echo.
echo ==========================================
echo Build completed.
echo ==========================================
echo.
echo EXE location:
echo dist\CSV-to-VCF.exe
echo.

pause