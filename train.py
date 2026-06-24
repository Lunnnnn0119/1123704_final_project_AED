Exit code: 0
Wall time: 0.2 seconds
Output:
"""Train an AED detector with Ultralytics YOLOv8.

Run from PowerShell with: .\\.venv\\Scripts\\python.exe train.py
"""

from __future__ import annotations

import argparse
from pathlib import Path

import torch
from ultralytics import YOLO


ROOT = Path(__file__).resolve().parent
DEFAULT_DATA = ROOT / "AED.v4i.yolov8" / "data.yaml"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Train a YOLOv8 AED detector.")
    parser.add_argument("--model", default="yolov8n.pt", help="Pretrained model or local .pt file.")
    parser.add_argument("--data", type=Path, default=DEFAULT_DATA, help="Dataset data.yaml path.")
    parser.add_argument("--epochs", type=int, default=100, help="Maximum training epochs.")
    parser.add_argument("--imgsz", type=int, default=640, help="Training image size.")
    parser.add_argument("--batch", type=int, default=-1, help="Batch size; -1 selects it automatically.")
    parser.add_argument("--device", default=None, help="GPU index (for example 0), cpu, or leave empty for auto.")
    parser.add_argument("--name", default="aed_yolov8n", help="Experiment folder name.")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    data_path = args.data.resolve()
    if not data_path.is_file():
        raise FileNotFoundError(f"Dataset config not found: {data_path}")

    device = args.device if args.device is not None else (0 if torch.cuda.is_available() else "cpu")
    print(f"Using device: {device}")
    if torch.cuda.is_available():
        print(f"GPU: {torch.cuda.get_device_name(0)}")

    model = YOLO(args.model)
    model.train(
        data=str(data_path),
        epochs=args.epochs,
        imgsz=args.imgsz,
        batch=args.batch,
        device=device,
        project=str(ROOT / "runs"),
        name=args.name,
        exist_ok=True,
        patience=20,
        pretrained=True,
        seed=42,
        workers=4,
    )


if __name__ == "__main__":
    main()