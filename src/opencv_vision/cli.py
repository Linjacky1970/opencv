"""Command-line image and video object detection."""

from __future__ import annotations

import argparse
from pathlib import Path

import cv2
from ultralytics import YOLO

IMAGE_SUFFIXES = {".bmp", ".jpeg", ".jpg", ".png", ".tif", ".tiff", ".webp"}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Detect objects in an image or video with OpenCV and YOLO.")
    parser.add_argument("--source", type=Path, required=True, help="Input image or video path.")
    parser.add_argument("--output", type=Path, help="Output path. Defaults to runs/<source>_detected.")
    parser.add_argument("--model", default="yolo26n.pt", help="YOLO model path or model name.")
    parser.add_argument("--conf", type=float, default=0.25, help="Minimum detection confidence.")
    parser.add_argument("--show", action="store_true", help="Show a live preview window.")
    return parser.parse_args()


def default_output(source: Path) -> Path:
    suffix = source.suffix.lower()
    output_suffix = ".jpg" if suffix in IMAGE_SUFFIXES else ".mp4"
    return Path("runs") / f"{source.stem}_detected{output_suffix}"


def detect_image(model: YOLO, source: Path, output: Path, confidence: float, show: bool) -> None:
    image = cv2.imread(str(source))
    if image is None:
        raise ValueError(f"Unable to read image: {source}")

    result = model.predict(source=image, conf=confidence, verbose=False)[0]
    annotated = result.plot()
    output.parent.mkdir(parents=True, exist_ok=True)
    if not cv2.imwrite(str(output), annotated):
        raise OSError(f"Unable to write image: {output}")
    if show:
        cv2.imshow("OpenCV Vision", annotated)
        cv2.waitKey(0)
        cv2.destroyAllWindows()


def detect_video(model: YOLO, source: Path, output: Path, confidence: float, show: bool) -> None:
    capture = cv2.VideoCapture(str(source))
    if not capture.isOpened():
        raise ValueError(f"Unable to open video: {source}")

    width = int(capture.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(capture.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = capture.get(cv2.CAP_PROP_FPS) or 30.0
    output.parent.mkdir(parents=True, exist_ok=True)
    writer = cv2.VideoWriter(
        str(output),
        cv2.VideoWriter_fourcc(*"mp4v"),
        fps,
        (width, height),
    )
    if not writer.isOpened():
        capture.release()
        raise OSError(f"Unable to create video: {output}")

    try:
        while True:
            success, frame = capture.read()
            if not success:
                break
            result = model.predict(source=frame, conf=confidence, verbose=False)[0]
            annotated = result.plot()
            writer.write(annotated)
            if show:
                cv2.imshow("OpenCV Vision", annotated)
                if cv2.waitKey(1) & 0xFF == ord("q"):
                    break
    finally:
        capture.release()
        writer.release()
        if show:
            cv2.destroyAllWindows()


def run(source: Path, output: Path, model_name: str, confidence: float, show: bool) -> None:
    if not source.is_file():
        raise FileNotFoundError(f"Source does not exist: {source}")
    if not 0.0 <= confidence <= 1.0:
        raise ValueError("--conf must be between 0 and 1")

    model = YOLO(model_name)
    if source.suffix.lower() in IMAGE_SUFFIXES:
        detect_image(model, source, output, confidence, show)
    else:
        detect_video(model, source, output, confidence, show)
    print(f"Saved detection result to {output}")


def main() -> None:
    args = parse_args()
    run(args.source, args.output or default_output(args.source), args.model, args.conf, args.show)


if __name__ == "__main__":
    main()
