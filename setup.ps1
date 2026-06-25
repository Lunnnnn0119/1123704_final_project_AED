<#
建立專案虛擬環境，並安裝 CUDA PyTorch 與 Ultralytics。
執行一次即可：.\\setup.ps1
#>

$ErrorActionPreference = 'Stop'
$ProjectRoot = $PSScriptRoot
$VenvPython = Join-Path $ProjectRoot '.venv\\Scripts\\python.exe'

if (-not (Get-Command uv -ErrorAction SilentlyContinue)) {
    throw "找不到 uv。請從 https://docs.astral.sh/uv/ 安裝，或執行：pip install uv"
}

if (-not (Test-Path $VenvPython)) {
    Write-Host '正在建立 Python 3.11 虛擬環境...'
    uv venv --python 3.11 "$ProjectRoot\\.venv"
}

Write-Host '正在安裝 CUDA 版本 PyTorch（CUDA 12.6）...'
uv pip install --python $VenvPython torch torchvision --index-url https://download.pytorch.org/whl/cu126

Write-Host '正在安裝 Ultralytics YOLO...'
uv pip install --python $VenvPython -r "$ProjectRoot\\requirements.txt"

Write-Host '正在檢查 GPU 是否可用...'
& $VenvPython -c "import torch, ultralytics; print('PyTorch:', torch.__version__); print('CUDA available:', torch.cuda.is_available()); print('CUDA version:', torch.version.cuda); print('GPU:', torch.cuda.get_device_name(0) if torch.cuda.is_available() else 'not available'); print('Ultralytics:', ultralytics.__version__)"
