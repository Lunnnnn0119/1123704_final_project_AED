@echo off
setlocal

where python >nul 2>nul
if errorlevel 1 (
    echo Python was not found. Install Python 3.11 or activate an Anaconda environment first.
    exit /b 1
)

if not exist "AED.v4i.yolov8\data.yaml" (
    if not exist "dataset\AED.v4i.yolov8.zip" (
        echo Dataset archive not found: dataset\AED.v4i.yolov8.zip
        exit /b 1
    )
    echo Extracting AED dataset...
    powershell -NoProfile -Command "Expand-Archive -LiteralPath 'dataset\AED.v4i.yolov8.zip' -DestinationPath '.' -Force"
)

if not exist ".venv\Scripts\python.exe" (
    echo Creating virtual environment...
    python -m venv .venv
)

echo Installing dependencies...
".venv\Scripts\python.exe" -m ensurepip --upgrade
".venv\Scripts\python.exe" -m pip install --upgrade pip
".venv\Scripts\python.exe" -m pip install -r requirements.txt

echo Verifying installation...
".venv\Scripts\python.exe" -c "import torch, ultralytics; print('PyTorch:', torch.__version__); print('CUDA available:', torch.cuda.is_available()); print('Ultralytics:', ultralytics.__version__)"
echo Setup complete.
