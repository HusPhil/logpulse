@echo off
cd /d "%~dp0.."
echo Stopping LogTracker Service...
python -c "from logtracker.service import stop_service; stop_service()"
pause