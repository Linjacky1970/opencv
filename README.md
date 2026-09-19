
# OpenCV Vision

以 `uv` 管理的 Python 3.12 影像與影片辨識專案，使用 OpenCV 處理媒體，使用 Ultralytics YOLO 執行物件偵測。

## 開始使用

```powershell
uv sync
uv run opencv-vision --source .\data\image.jpg --output .\runs\image.jpg
uv run opencv-vision --source .\data\video.mp4 --output .\runs\video_detected.mp4
```

第一次執行會自動下載 `yolo26n.pt` 模型。若要預覽視窗，加上 `--show`；若要指定其他模型，可使用 `--model`。

## 常用參數

```text
--source  輸入圖片或影片路徑
--output  標註結果路徑；未指定時寫入 runs/
--model   YOLO 模型路徑或名稱，預設 yolo26n.pt
--conf    信心閾值，預設 0.25
--show    顯示即時預覽視窗
```

## 開發

```powershell
uv run python -m compileall src
uv run opencv-vision --help
```
