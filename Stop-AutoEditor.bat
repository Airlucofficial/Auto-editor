@echo off
title Stop AutoEditor
cd /d "%~dp0"

echo =======================================================
echo   Stopping AutoEditor & AI Engine Services...
echo =======================================================
echo.

if exist ".venv\Scripts\python.exe" (
    .venv\Scripts\python.exe service_manager.py stop
)

taskkill /F /IM AutoEditor.exe >nul 2>&1

echo.
echo =======================================================
echo   All AutoEditor and Python services have been stopped.
echo =======================================================
timeout /t 2 >nul
