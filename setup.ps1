Exit code: 0
Wall time: 0.2 seconds
Output:
<#
Creates the project virtual environment and installs CUDA PyTorch + Ultralytics.
Run once: .\\setup.ps1
#>

$ErrorActionPreference = 'Stop'
$ProjectRoot = $PSScriptRoot
$VenvPython = Join-Path $ProjectRoot '.venv\\Scripts\\python.exe'

if (-not (Get-Command uv -ErrorAction SilentlyContinue)) {
    throw "uv was not found. Install it from https://docs.astral.sh/uv/ or use: pip install uv"
}

if (-not (Test-Path $VenvPython)) {
    Write-Host 'Creating Python 3.11 virtual environment...'
    uv venv --python 3.11 "$ProjectRoot\\.venv"
}

Write-Host 'Installing CUDA-enabled PyTorch (CUDA 12.6)...'
uv pip install --python $VenvPython torch torchvision --index-url https://download.pytorch.org/whl/cu126

Write-Host 'Installing Ultralytics YOLO...'
uv pip install --python $VenvPython -r "$ProjectRoot\\requirements.txt"

Write-Host 'Verifying GPU access...'
& $VenvPython -c "import torch, ultralytics; print('PyTorch:', torch.__version__); print('CUDA available:', torch.cuda.is_available()); print('CUDA version:', torch.version.cuda); print('GPU:', torch.cuda.get_device_name(0) if torch.cuda.is_available() else 'not available'); print('Ultralytics:', ultralytics.__version__)"