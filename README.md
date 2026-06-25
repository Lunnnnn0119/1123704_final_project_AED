# Yuan Ze University AED Object Detection

This final project detects Automated External Defibrillators (AEDs) on the Yuan Ze University campus. It uses a custom AED image dataset exported in YOLOv8 format and a YOLOv8 Nano object detector. The included application supports training, test-set evaluation, video inference, and live webcam inference.

## Repository contents

```text
dataset/AED.v4i.yolov8.zip      # Full YOLOv8 dataset: 219 train, 22 val, 10 test images
runs/aed_yolov8n/weights/best.pt # Trained best model
runs/aed_yolov8n/results.*     # Training log and result curves
runs/detect/val/                # Held-out test prediction and confusion matrix
outputs/aed_detection.mp4       # Recorded inference demonstration
train.py                        # Model training
evaluate.py                     # Test-set evaluation
infer_video.py                  # Video and webcam inference
setup.bat                       # Windows CMD / Anaconda Prompt setup
run_infer_video.bat             # Video-inference shortcut
```

`setup.bat` extracts the included dataset archive to `AED.v4i.yolov8/`, so the project is runnable immediately after setup.

## Installation (Windows)

Install Python 3.11 (or a compatible version). In CMD or Anaconda Prompt at the repository root, run:

```bat
.\setup.bat
```

The script creates a virtual environment, extracts the data, and installs the required packages. CUDA is used automatically when an NVIDIA GPU and compatible driver are available; CPU inference also works.

## Run the project

### Evaluate the supplied best model

```bat
.\.venv\Scripts\python.exe .\evaluate.py
```

### Run inference on a video

```bat
.\run_infer_video.bat input.mp4
```

The annotated video is saved to `outputs/aed_detection.mp4`. To choose a different output file:

```bat
.\run_infer_video.bat input.mp4 outputs\my_result.mp4
```

### Live webcam inference

```bat
.\.venv\Scripts\python.exe .\infer_video.py --source 0 --show --no-save
```

Press `Q` or `Esc` in the preview window to stop.

### Retrain the detector

```bat
.\.venv\Scripts\python.exe .\train.py --epochs 200 --model yolov8n.pt
```

## Results

The model was trained with YOLOv8 Nano, 640x640 images, a maximum of 200 epochs, and early stopping at epoch 82. Its best validation metrics were Precision 0.998, Recall 1.000, mAP@0.5 0.995, and mAP@0.5:0.95 0.964. Training plots and validation samples are in `runs/aed_yolov8n/`.

On the held-out test set (10 images), the supplied `best.pt` achieved Precision 0.988, Recall 0.909, mAP@0.5 0.905, and mAP@0.5:0.95 0.815. The held-out predictions and normalized confusion matrix are in `runs/detect/val/`.

The small dataset contains augmented images that may be visually similar. These results should be validated further in new campus locations and with real camera footage.

## Demonstration video

The repository includes [`outputs/aed_detection.mp4`](outputs/aed_detection.mp4), a recorded inference demonstration. You can also reproduce it using the video and webcam commands above.

## Data, open source, and AI collaboration

- Dataset: AED images and annotations prepared for this project and exported with Roboflow in YOLOv8 format. The export is marked [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/) and is included in [`dataset/AED.v4i.yolov8.zip`](dataset/AED.v4i.yolov8.zip).
- Model framework: [Ultralytics YOLO](https://github.com/ultralytics/ultralytics), AGPL-3.0.
- Image/video I/O: [OpenCV](https://opencv.org/), Apache-2.0.

See [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md) for usage and licensing information, and [AI_COLLABORATION.md](AI_COLLABORATION.md) for the required AI-assistance summary.
