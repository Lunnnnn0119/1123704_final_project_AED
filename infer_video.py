"""Run AED detection on a video or webcam stream using trained YOLO weights.

Examples (Windows CMD):
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
    """Treat values such as '0' as webcam indexes; all other values are paths."""
    return int(value) if value.isdigit() else value


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Detect AEDs in a video with YOLOv8.")
    parser.add_argument("--source", required=True, help="Input video path, or webcam index such as 0.")
    parser.add_argument("--weights", type=Path, default=DEFAULT_WEIGHTS, help="Path to YOLO .pt weights.")
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT, help="Annotated output .mp4 path.")
    parser.add_argument("--conf", type=float, default=0.35, help="Minimum confidence threshold (0 to 1).")
    parser.add_argument("--imgsz", type=int, default=640, help="YOLO inference image size.")
    parser.add_argument("--device", default=None, help="GPU index (e.g. 0), cpu, or empty for automatic selection.")
    parser.add_argument("--show", action="store_true", help="Show a live preview. Press Q or Esc to stop.")
    parser.add_argument("--no-save", action="store_true", help="Do not create an output video (useful with --show).")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    if not 0.0 <= args.conf <= 1.0:
        raise ValueError("--conf must be between 0 and 1.")

    weights = args.weights.resolve()
    if not weights.is_file():
        raise FileNotFoundError(f"Model weights not found: {weights}")

    source = parse_source(args.source)
    capture = cv2.VideoCapture(source)
    if not capture.isOpened():
        raise RuntimeError(f"Cannot open video source: {args.source}")

    width = int(capture.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(capture.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = capture.get(cv2.CAP_PROP_FPS)
    fps = fps if fps and fps > 0 else 30.0
    total_frames = int(capture.get(cv2.CAP_PROP_FRAME_COUNT))
    device = args.device if args.device is not None else (0 if torch.cuda.is_available() else "cpu")

    print(f"Loading model: {weights}")
    print(f"Source: {args.source} ({width}x{height}, {fps:.2f} FPS)")
    print(f"Device: {device}")
    model = YOLO(str(weights))

    writer: cv2.VideoWriter | None = None
    output = args.output.resolve()
    if not args.no_save:
        output.parent.mkdir(parents=True, exist_ok=True)
        writer = cv2.VideoWriter(str(output), cv2.VideoWriter_fourcc(*"mp4v"), fps, (width, height))
        if not writer.isOpened():
            raise RuntimeError(f"Cannot create output video: {output}")

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
                f"Inference: {current_fps:.1f} FPS",
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
                cv2.imshow("AED detection (Q/Esc to quit)", annotated)
                if cv2.waitKey(1) & 0xFF in (ord("q"), 27):
                    break

            if total_frames > 0 and (frame_index % 30 == 0 or frame_index == total_frames):
                print(f"Processed {frame_index}/{total_frames} frames", end="\r")
    finally:
        capture.release()
        if writer is not None:
            writer.release()
        cv2.destroyAllWindows()

    print()
    print(f"Finished: {frame_index} frames in {time.perf_counter() - started_at:.1f} seconds.")
    if writer is not None:
        print(f"Saved annotated video: {output}")


if __name__ == "__main__":
    main()