@echo off
title AutoEditor (v2 + AI Studio)
cd /d "%~dp0"

echo =======================================================
echo   Starting TryAIToday AutoEditor + AI Studio
echo   - Audio-to-Transcript Engine (Local Whisper)
echo   - TXT and PDF Export
echo   - CapCut Multi-Style Caption Generator
echo =======================================================
echo.

:: Check for virtual environment
if not exist ".venv\Scripts\python.exe" (
    echo [ERROR] Virtual environment not found in .venv.
    pause
    exit /b 1
)

:: Start Persistent Background Service via service_manager.py
echo [1/2] Starting AutoEditor AI Engine background service...
.venv\Scripts\python.exe service_manager.py start

:: Start Main AutoEditor on port 4000
echo [2/2] Launching AutoEditor Desktop Server on port 4000...
set RENDER_ZOOM_SS=1
AutoEditor.exe
