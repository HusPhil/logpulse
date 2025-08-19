@echo off
echo Installing LogTracker Service...
echo.
echo This requires Administrator privileges.
echo Right-click and "Run as Administrator" if not already elevated.
echo.
pause

cd /d "%~dp0.."
python -c "from logtracker.service import install_service; install_service()"

if %ERRORLEVEL% EQU 0 (
    echo.
    echo Service installed successfully!
    echo Starting service...
    python -c "from logtracker.service import start_service; start_service()"
) else (
    echo.
    echo Installation failed!
)

pause