@echo off
echo Uninstalling LogTracker Service...
echo.
echo This requires Administrator privileges.
echo Right-click and "Run as Administrator" if not already elevated.
echo.
pause

cd /d "%~dp0.."

echo Stopping service...
python -c "from logtracker.service import stop_service; stop_service()"

echo Removing service...
python -c "from logtracker.service import remove_service; remove_service()"

echo.
echo Service uninstalled!
pause