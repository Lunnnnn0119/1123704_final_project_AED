@echo off
chcp 65001 >nul
setlocal

where python >nul 2>nul
if errorlevel 1 (
    echo 找不到 Python。請先安裝 Python 3.11，或先啟用 Anaconda 環境。
    exit /b 1
)

if not exist "AED.v4i.yolov8\data.yaml" (
    if not exist "dataset\AED.v4i.yolov8.zip" (
        echo 找不到資料集壓縮檔：dataset\AED.v4i.yolov8.zip
        exit /b 1
    )
    echo 正在解壓 AED 資料集...
    powershell -NoProfile -Command "Expand-Archive -LiteralPath 'dataset\AED.v4i.yolov8.zip' -DestinationPath '.' -Force"
)

if not exist ".venv\Scripts\python.exe" (
    echo 正在建立虛擬環境...
    python -m venv .venv
)

echo 正在安裝套件...
".venv\Scripts\python.exe" -m ensurepip --upgrade
".venv\Scripts\python.exe" -m pip install --upgrade pip
".venv\Scripts\python.exe" -m pip install -r requirements.txt

echo 正在檢查安裝結果...
".venv\Scripts\python.exe" -c "import torch, ultralytics; print('PyTorch:', torch.__version__); print('CUDA available:', torch.cuda.is_available()); print('Ultralytics:', ultralytics.__version__)"
echo 環境建立完成。
