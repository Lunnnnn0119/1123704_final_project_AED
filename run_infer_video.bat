@echo off
chcp 65001 >nul
setlocal

if "%~1"=="" (
    echo 用法：%~nx0 ^<輸入影片^> [輸出影片]
    echo 範例：%~nx0 input.mp4 outputs\aed_detection.mp4
    exit /b 1
)

set "PYTHON=%~dp0.venv\Scripts\python.exe"
if not exist "%PYTHON%" (
    echo 找不到虛擬環境。請先執行 setup.bat。
    exit /b 1
)

if "%~2"=="" (
    "%PYTHON%" "%~dp0infer_video.py" --source "%~1"
) else (
    "%PYTHON%" "%~dp0infer_video.py" --source "%~1" --output "%~2"
)
