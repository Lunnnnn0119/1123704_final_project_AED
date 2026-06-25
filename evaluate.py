"""Evaluate a trained AED YOLO model on the held-out test split."""

from __future__ import annotations

import argparse
from pathlib import Path

import torch
from ultralytics import YOLO


ROOT = Path(__file__).resolve().parent
DEFAULT_WEIGHTS = ROOT / "runs" / "aed_yolov8n" / "weights" / "best.pt"
DEFAULT_DATA = ROOT / "AED.v4i.yolov8" / "data.yaml"


def main() -> None:
    parser = argparse.ArgumentParser(description="Evaluate AED YOLO weights.")
    parser.add_argument("--weights", type=Path, default=DEFAULT_WEIGHTS)
    parser.add_argument("--data", type=Path, default=DEFAULT_DATA)
    parser.add_argument("--imgsz", type=int, default=640)
    args = parser.parse_args()

    weights = args.weights.resolve()
    if not weights.is_file():
        raise FileNotFoundError(f"Weights not found: {weights}")

    device = 0 if torch.cuda.is_available() else "cpu"
    model = YOLO(str(weights))
    model.val(data=str(args.data.resolve()), split="test", imgsz=args.imgsz, device=device)


if __name__ == "__main__":
    main()
