Exit code: 0
Wall time: 0.2 seconds
Output:
param(
    [int]$Epochs = 100,
    [int]$ImageSize = 640,
    [int]$Batch = -1,
    [string]$Model = 'yolov8n.pt'
)

$ErrorActionPreference = 'Stop'
$Python = Join-Path $PSScriptRoot '.venv\\Scripts\\python.exe'
if (-not (Test-Path $Python)) {
    throw 'Environment not found. Run .\\setup.ps1 first.'
}

& $Python (Join-Path $PSScriptRoot 'train.py') --epochs $Epochs --imgsz $ImageSize --batch $Batch --model $Model