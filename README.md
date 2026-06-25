# 1123704_期末專題-AED偵測

本專題使用 YOLOv8 訓練 AED（自動體外心臟電擊去顫器）物件偵測模型，可對圖片資料集訓練、測試集評估，以及影片/攝影機即時推論。

## 檔案快速摘要

| 項目 | 位置 |
| --- | --- |
| 訓練程式 | `train.py` |
| 評估程式 | `evaluate.py` |
| 影片推論程式 | `infer_video.py` |
| 資料集 | `dataset/AED.v4i.yolov8.zip` |
| 訓練完成權重 | `runs/aed_yolov8n/weights/best.pt` |
| 訓練結果 | `runs/aed_yolov8n/` |
| 測試集推論結果 | `runs/detect/val/` |
| Demo 影片 | `outputs/aed_detection.mp4` |
| AI 協作紀錄 | `AI_COLLABORATION.md` |
| 第三方套件/授權 | `THIRD_PARTY_NOTICES.md` |

## 環境安裝

請先安裝 Python 3.11 或使用 Anaconda Prompt。進入專案根目錄後執行：

```bat
.\setup.bat
```

此指令會：
1. 建立 `.venv` 虛擬環境。
2. 解壓 `dataset/AED.v4i.yolov8.zip` 到 `AED.v4i.yolov8/`。
3. 安裝 `requirements.txt` 內的套件。

## 執行方式

### 1. 評估已訓練模型

```bat
.\.venv\Scripts\python.exe .\evaluate.py
```

### 2. 對影片進行 AED 偵測(本次主要)

```bat
.\run_infer_video.bat input.mp4
```

輸出影片預設存到：

```text
outputs/aed_detection.mp4
```

### 3. 使用攝影機即時偵測

```bat
.\.venv\Scripts\python.exe .\infer_video.py --source 0 --show --no-save
```

按 `Q` 或 `Esc` 可結束視窗。

### 4. 重新訓練

```bat
.\.venv\Scripts\python.exe .\train.py --epochs 200 --model yolov8n.pt
```

## 模型成果

- 模型：YOLOv8 Nano
- 類別數：1 類（AED）
- 資料集：train 219 張、valid 22 張、test 10 張
- Validation：Precision 0.998、Recall 1.000、mAP@0.5 0.995、mAP@0.5:0.95 0.964
- Test：Precision 0.988、Recall 0.909、mAP@0.5 0.905、mAP@0.5:0.95 0.815

訓練曲線、混淆矩陣與推論範例圖已放在 `runs/` 資料夾中。
