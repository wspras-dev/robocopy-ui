@echo off
REM Build otomatis PyInstaller untuk rbcopy-plus
REM Pastikan sudah install pyinstaller dan Pillow dan pystray

set SCRIPT=rbcopy-plus.py
set LOGO=logo.png
set FAVICON=favicon.ico
set INI=config.conf
set OUTDIR=dist

REM Build dengan logo.png dan config.conf ikut dibundle
pyinstaller --onefile --windowed --add-data "%FAVICON%;." --add-data "%LOGO%;." --add-data "%INI%;." "%SCRIPT%"

REM Selesai
pause