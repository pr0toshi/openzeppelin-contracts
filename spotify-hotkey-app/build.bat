@echo off
echo Building Spotify Hotkey App...
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.8 or higher from python.org
    pause
    exit /b 1
)

echo Installing dependencies...
pip install -r requirements.txt

echo.
echo Building executable with PyInstaller...
pyinstaller build.spec --clean

echo.
if exist "dist\SpotifyHotkey.exe" (
    echo ========================================
    echo SUCCESS! Executable created at:
    echo dist\SpotifyHotkey.exe
    echo ========================================
    echo.
    echo You can now run the .exe file!
) else (
    echo ERROR: Build failed. Check the output above for errors.
)

echo.
pause
