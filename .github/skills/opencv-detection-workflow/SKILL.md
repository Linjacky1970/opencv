---
name: opencv-detection-workflow
description: 'Use when implementing or debugging Python OpenCV image recognition, video recognition, object detection, YOLO inference, frame processing, codecs, or computer-vision tests in this project.'
argument-hint: 'Describe the image or video recognition behavior to implement or debug.'
user-invocable: true
---

# OpenCV Detection Workflow

## Goal

Deliver a focused, verifiable image or video recognition change using the repository's Python 3.12 and uv environment.

## Procedure

1. Inspect the owning code path under `src/opencv_vision` and identify whether the input is an image, video file, or camera stream.
2. Confirm the expected input and output formats, model name or weight path, confidence threshold, and whether GUI preview is allowed.
3. Use `uv run` for all Python commands. Add missing packages with `uv add`; do not install into the global interpreter.
4. For images, validate `cv2.imread` and write the annotated result with `cv2.imwrite`.
5. For videos, validate `VideoCapture.isOpened()`, preserve width, height, and FPS when practical, and release capture and writer resources in `finally` blocks.
6. Keep model inference explicit and injectable where tests need to avoid downloading weights or using a GPU.
7. Run `uv run python -m compileall src`, then the narrowest relevant test or CLI command.
8. Report generated output paths and note whether model weights were downloaded or hardware acceleration was used.

## Project commands

```powershell
uv sync
uv run opencv-vision --source .\data\image.jpg --output .\runs\image.jpg
uv run opencv-vision --source .\data\video.mp4 --output .\runs\video_detected.mp4
uv run python -m compileall src
```

## Failure checklist

- `Unable to read image`: verify the path, extension, and file permissions.
- `Unable to open video`: verify the codec and try a local MP4 or camera index.
- Empty output video: check writer dimensions, FPS, codec support, and release order.
- Slow inference: use a smaller model, reduce input size, or configure a supported GPU.
- Headless environment: omit `--show` and validate the saved output instead.
