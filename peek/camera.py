"""Live camera preview. Space captures a frame, Escape cancels.

Runs as its own process because OpenCV's window loop must own the main
thread on macOS. Usage: python -m peek.camera OUT.jpg [--max-side N] [--device N]
"""

from __future__ import annotations

import argparse
import sys

import cv2

WINDOW = "Peek  -  space: capture   esc: cancel"


def _resize(frame, max_side: int):
    h, w = frame.shape[:2]
    scale = max_side / max(h, w)
    if scale >= 1:
        return frame
    return cv2.resize(frame, (int(w * scale), int(h * scale)), interpolation=cv2.INTER_AREA)


def _overlay(frame):
    out = frame.copy()
    text = "SPACE to capture   ESC to cancel"
    cv2.putText(out, text, (16, 34), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 0), 4, cv2.LINE_AA)
    cv2.putText(out, text, (16, 34), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2, cv2.LINE_AA)
    return out


def capture(out_path: str, max_side: int = 1500, device: int = 0) -> int:
    cap = cv2.VideoCapture(device)
    if not cap.isOpened():
        print(f"peek: could not open camera {device}", file=sys.stderr)
        return 2

    cv2.namedWindow(WINDOW, cv2.WINDOW_AUTOSIZE)
    cv2.setWindowProperty(WINDOW, cv2.WND_PROP_TOPMOST, 1)

    frame = None
    code = 1
    try:
        while True:
            ok, frame = cap.read()
            if not ok:
                print("peek: camera read failed", file=sys.stderr)
                code = 2
                break
            cv2.imshow(WINDOW, _overlay(frame))
            key = cv2.waitKey(16) & 0xFF
            if key == 32:  # space
                cv2.imwrite(out_path, _resize(frame, max_side), [cv2.IMWRITE_JPEG_QUALITY, 88])
                code = 0
                break
            if key == 27:  # escape
                code = 1
                break
            if cv2.getWindowProperty(WINDOW, cv2.WND_PROP_VISIBLE) < 1:
                code = 1
                break
    finally:
        cap.release()
        cv2.destroyAllWindows()
        cv2.waitKey(1)
    return code


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("out")
    p.add_argument("--max-side", type=int, default=1500)
    p.add_argument("--device", type=int, default=0)
    a = p.parse_args()
    sys.exit(capture(a.out, a.max_side, a.device))


if __name__ == "__main__":
    main()
