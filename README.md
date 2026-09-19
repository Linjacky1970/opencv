
# OpenCV Vision

以 `uv` 管理的 Python 3.12 OpenCV 影片處理專案。主程式 `main.py` 會播放範例影片，並提供原始畫面、灰階與 Canny 邊緣偵測三種模式，支援暫停、截圖、即時 FPS 與影片時間顯示。

## 環境安裝

請先安裝 Python 3.12 與 [uv](https://docs.astral.sh/uv/)，再在專案根目錄執行：

```powershell
uv python install 3.12
uv sync
```

啟動互動式影片播放程式：

```powershell
uv run python main.py
```

程式會開啟 OpenCV 視窗。若使用遠端或無 GUI 的環境，無法使用互動式播放視窗。

## 操作說明

程式會在同一個視窗中將原始畫面與處理後畫面水平並排顯示。右側畫面會顯示目前模式、影片時間與即時 FPS。

| 按鍵 | 功能 |
| --- | --- |
| `1` | 切換至模式 1：原始畫面 |
| `2` | 切換至模式 2：灰階 |
| `3` | 切換至模式 3：Canny 邊緣偵測 |
| `Space` | 暫停／繼續播放；暫停時仍可切換模式與截圖 |
| `s` | 儲存目前的左右並排畫面 |
| `q` | 離開播放 |
| `Esc` | 離開播放 |

影片播放結束或離開後，終端機會輸出總播放幀數、平均處理 FPS、影片總時長與本次截圖數量。

## 輸出檔案位置

- 截圖會自動儲存到 `captures/`。
- 截圖檔名格式為 `capture_YYYYMMDD_HHMMSS_microseconds.jpg`。
- `captures/` 不存在時，程式會自動建立資料夾。
- YOLO CLI 的輸出預設寫入 `runs/`，也可以使用 `--output` 指定其他路徑。

## 範例影片來源

`main.py` 預設讀取專案內的本地影片：

```text
videos/people02.mp4
```

這是隨專案提供的範例輸入檔，不需要另外下載。若要使用其他影片，請將影片放入 `videos/`，並將 `main.py` 中的 `cv2.VideoCapture("videos/people02.mp4")` 改成對應的檔案路徑。

## YOLO CLI

本專案也提供使用 Ultralytics YOLO 的命令列工具：

```powershell
uv run opencv-vision --source .\data\image.jpg --output .\runs\image.jpg
uv run opencv-vision --source .\data\video.mp4 --output .\runs\video_detected.mp4
```

常用參數：

```text
--source  輸入圖片或影片路徑
--output  標註結果路徑；未指定時寫入 runs/
--model   YOLO 模型路徑或名稱，預設 yolo26n.pt
--conf    信心閾值，預設 0.25
--show    顯示即時預覽視窗
```

## 開發檢查

```powershell
uv run python -m compileall src
uv run python -m py_compile main.py
uv run opencv-vision --help
```
