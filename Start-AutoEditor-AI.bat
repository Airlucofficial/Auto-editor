@echo off
title AutoEditor (v2 + AI Studio)
cd /d "%~dp0"

echo =======================================================
echo   Starting TryAIToday AutoEditor + AI Studio
echo   - Audio-to-Transcript Engine (Local Whisper)
echo   - TXT and PDF Export
echo   - CapCut Multi-Style Caption Generator
echo   - In-Editor Canvas Caption Sync
echo =======================================================
echo.

:: Check for virtual environment
if not exist ".venv\Scripts\python.exe" (
    echo [ERROR] Virtual environment not found in .venv.
    pause
    exit /b 1
)

:: Start Background AI Service silently without opening extra console windows
echo [1/2] Starting AutoEditor AI Engine background service...
.venv\Scripts\python.exe service_manager.py start

:: Start Main AutoEditor on port 4000
echo [2/2] Launching AutoEditor Desktop Server on port 4000...
echo.
echo =======================================================
echo   AutoEditor is running at http://localhost:4000
echo   To stop the app and all background AI services:
echo   simply close this window or press Ctrl+C.
echo =======================================================
echo.
set RENDER_ZOOM_SS=1
AutoEditor.exe

:: AutoEditor has exited - clean up background services immediately
echo.
echo [Cleanup] Stopping AutoEditor AI Engine background service...
if exist ".venv\Scripts\python.exe" (
    .venv\Scripts\python.exe service_manager.py stop
)
echo Done! All processes stopped cleanly.
