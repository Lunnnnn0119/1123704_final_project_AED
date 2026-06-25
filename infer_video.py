"""使用訓練好的 YOLO 權重，對影片或攝影機畫面進行 AED 偵測。

範例（Windows CMD）：
    .\.venv\Scripts\python.exe infer_video.py --source input.mp4
    .\.venv\Scripts\python.exe infer_video.py --source 0 --show
"""

from __future__ import annotations

import argparse
import time
from pathlib import Path

import cv2
import torch
from ultralytics import YOLO


ROOT = Path(__file__).resolve().parent
DEFAULT_WEIGHTS = ROOT / "runs" / "aed_yolov8n" / "weights" / "best.pt"
DEFAULT_OUTPUT = ROOT / "outputs" / "aed_detection.mp4"


def parse_source(value: str) -> int | str:
    """數字字串視為攝影機編號，其餘視為影片路徑。"""
    return int(value) if value.isdigit() else value


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="使用 YOLOv8 偵測影片中的 AED。")
    parser.add_argument("--source", required=True, help="輸入影片路徑，或攝影機編號，例如 0。")
    parser.add_argument("--weights", type=Path, default=DEFAULT_WEIGHTS, help="YOLO .pt 權重檔路徑。")
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT, help="標註後輸出影片路徑。")
    parser.add_argument("--conf", type=float, default=0.35, help="信心門檻，範圍 0 到 1。")
    parser.add_argument("--imgsz", type=int, default=640, help="YOLO 推論影像尺寸。")
    parser.add_argument("--device", default=None, help="GPU 編號，例如 0；也可填 cpu；留空則自動選擇。")
    parser.add_argument("--show", action="store_true", help="顯示即時預覽，按 Q 或 Esc 結束。")
    parser.add_argument("--no-save", action="store_true", help="不輸出影片，常搭配 --show 使用。")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    if not 0.0 <= args.conf <= 1.0:
        raise ValueError("--conf 必須介於 0 到 1。")

    weights = args.weights.resolve()
    if not weights.is_file():
        raise FileNotFoundError(f"找不到模型權重：{weights}")

    source = parse_source(args.source)
    capture = cv2.VideoCapture(source)
    if not capture.isOpened():
        raise RuntimeError(f"無法開啟影片來源：{args.source}")

    width = int(capture.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(capture.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = capture.get(cv2.CAP_PROP_FPS)
    fps = fps if fps and fps > 0 else 30.0
    total_frames = int(capture.get(cv2.CAP_PROP_FRAME_COUNT))
    device = args.device if args.device is not None else (0 if torch.cuda.is_available() else "cpu")

    print(f"載入模型：{weights}")
    print(f"來源：{args.source}（{width}x{height}, {fps:.2f} FPS）")
    print(f"使用裝置：{device}")
    model = YOLO(str(weights))

    writer: cv2.VideoWriter | None = None
    output = args.output.resolve()
    if not args.no_save:
        output.parent.mkdir(parents=True, exist_ok=True)
        writer = cv2.VideoWriter(str(output), cv2.VideoWriter_fourcc(*"mp4v"), fps, (width, height))
        if not writer.isOpened():
            raise RuntimeError(f"無法建立輸出影片：{output}")

    frame_index = 0
    started_at = time.perf_counter()
    try:
        while True:
            success, frame = capture.read()
            if not success:
                break

            result = model.predict(frame, conf=args.conf, imgsz=args.imgsz, device=device, verbose=False)[0]
            annotated = result.plot()
            frame_index += 1
            elapsed = time.perf_counter() - started_at
            current_fps = frame_index / elapsed if elapsed else 0.0

            cv2.putText(
                annotated,
                f"推論速度：{current_fps:.1f} FPS",
                (12, 30),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.8,
                (0, 255, 0),
                2,
                cv2.LINE_AA,
            )

            if writer is not None:
                writer.write(annotated)
            if args.show:
                cv2.imshow("AED 偵測（Q/Esc 結束）", annotated)
                if cv2.waitKey(1) & 0xFF in (ord("q"), 27):
                    break

            if total_frames > 0 and (frame_index % 30 == 0 or frame_index == total_frames):
                print(f"已處理 {frame_index}/{total_frames} 幀", end="\r")
    finally:
        capture.release()
        if writer is not None:
            writer.release()
        cv2.destroyAllWindows()

    print()
    print(f"完成：共處理 {frame_index} 幀，耗時 {time.perf_counter() - started_at:.1f} 秒。")
    if writer is not None:
        print(f"已儲存標註影片：{output}")


if __name__ == "__main__":
    main()
