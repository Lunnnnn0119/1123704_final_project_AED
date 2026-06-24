@echo off
setlocal

if "%~1"=="" (
    echo Usage: %~nx0 ^<input-video^> [output-video]
    echo Example: %~nx0 input.mp4 outputs\aed_detection.mp4
    exit /b 1
)

set "PYTHON=%~dp0.venv\Scripts\python.exe"
if not exist "%PYTHON%" (
    echo Environment not found. Run setup.ps1 first.
    exit /b 1
)

if "%~2"=="" (
    "%PYTHON%" "%~dp0infer_video.py" --source "%~1"
) else (
    "%PYTHON%" "%~dp0infer_video.py" --source "%~1" --output "%~2"
)