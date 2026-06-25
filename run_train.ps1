param(
    [int]$Epochs = 100,
    [int]$ImageSize = 640,
    [int]$Batch = -1,
    [string]$Model = 'yolov8n.pt'
)

$ErrorActionPreference = 'Stop'
$Python = Join-Path $PSScriptRoot '.venv\\Scripts\\python.exe'
if (-not (Test-Path $Python)) {
    throw '找不到虛擬環境。請先執行 .\\setup.bat 或 .\\setup.ps1。'
}

& $Python (Join-Path $PSScriptRoot 'train.py') --epochs $Epochs --imgsz $ImageSize --batch $Batch --model $Model
