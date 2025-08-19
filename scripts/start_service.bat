@echo off
cd /d "%~dp0.."
echo Starting LogTracker Service...
python -c "from logtracker.service import start_service; start_service()"
pause