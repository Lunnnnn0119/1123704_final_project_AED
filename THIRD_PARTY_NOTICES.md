Exit code: 0
Wall time: 0.2 seconds
Output:
# 第三方軟體與資料來源

## Ultralytics YOLO

- 專案：[ultralytics/ultralytics](https://github.com/ultralytics/ultralytics)
- 使用範圍：載入 YOLOv8 預訓練權重、訓練偵測模型、驗證與逐幀推論。
- 授權：AGPL-3.0（或依 Ultralytics 提供的商業授權）。本專題為課程公開展示用途；公開或再散布前應自行確認授權義務。
- 本專題的工作：建立 AED 資料集流程、設定訓練參數、撰寫訓練／評估／影片推論的整合程式、驗證輸出與整理說明文件。

## OpenCV

- 專案：[OpenCV](https://opencv.org/)
- 使用範圍：讀取影片與攝影機影像、繪製偵測結果、輸出標註影片。
- 授權：Apache License 2.0。

## Roboflow 資料集匯出

- 平台：[Roboflow](https://roboflow.com/)
- 使用範圍：將 AED 影像與標註匯出為 YOLOv8 目錄結構。
- 資料集授權：CC BY 4.0；完整匯出資訊保留於 `AED.v4i.yolov8/README.dataset.txt` 與 `README.roboflow.txt`。

本檔僅記錄第三方來源與本專題整合範圍，並不取代各專案的原始授權條款。