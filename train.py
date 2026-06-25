"""使用 Ultralytics YOLOv8 訓練 AED 偵測模型。

執行方式：.\\.venv\\Scripts\\python.exe train.py
"""

from __future__ import annotations

import argparse
from pathlib import Path

import torch
from ultralytics import YOLO

ROOT = Path(__file__).resolve().parent
DEFAULT_DATA = ROOT / "AED.v4i.yolov8" / "data.yaml"

def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="訓練 YOLOv8 AED 偵測模型。")
    parser.add_argument("--model", default="yolov8n.pt", help="預訓練模型或本機 .pt 權重檔。")
    parser.add_argument("--data", type=Path, default=DEFAULT_DATA, help="資料集 data.yaml 路徑。")
    parser.add_argument("--epochs", type=int, default=100, help="最大訓練 epoch 數。")
    parser.add_argument("--imgsz", type=int, default=640, help="訓練影像尺寸。")
    parser.add_argument("--batch", type=int, default=-1, help="batch size；-1 代表自動選擇。")
    parser.add_argument("--device", default=None, help="GPU 編號，例如 0；也可填 cpu；留空則自動選擇。")
    parser.add_argument("--name", default="aed_yolov8n", help="訓練結果資料夾名稱。")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    data_path = args.data.resolve()
    if not data_path.is_file():
        raise FileNotFoundError(f"找不到資料集設定檔：{data_path}")

    device = args.device if args.device is not None else (0 if torch.cuda.is_available() else "cpu")
    print(f"使用裝置：{device}")
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
