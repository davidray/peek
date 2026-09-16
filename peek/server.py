"""MCP server exposing a single `peek` tool that photographs with the camera."""

from __future__ import annotations

import subprocess
import sys
import time
from pathlib import Path

from mcp.server.mcpserver import Image, MCPServer

mcp = MCPServer("peek", instructions="Call the peek tool when you need to see a physical object; the user positions it and presses space.")

PHOTO_DIR = Path.home() / "Pictures" / "Peek"


@mcp.tool()
def peek(max_side: int = 1500, device: int = 0) -> list:
    """Open a live camera preview so the user can position an item, then wait
    for them to press space to take the photo (or Escape to cancel).

    Returns the photo as an image plus the path where it was saved.
    Call this when you need to see a physical object, document, or scene.

    Args:
        max_side: longest edge in pixels for the returned image (default 1500).
        device: camera index if the user has more than one (default 0).
    """
    PHOTO_DIR.mkdir(parents=True, exist_ok=True)
    out = PHOTO_DIR / time.strftime("peek-%Y%m%d-%H%M%S.jpg")

    proc = subprocess.run(
        [sys.executable, "-m", "peek.camera", str(out), "--max-side", str(max_side), "--device", str(device)],
        capture_output=True,
        text=True,
        check=False,
    )
    if proc.returncode == 1:
        return ["The user cancelled the photo (pressed Escape or closed the window)."]
    if proc.returncode != 0 or not out.exists():
        return [f"Camera capture failed: {proc.stderr.strip() or 'unknown error'}"]

    return [f"Photo saved to {out}", Image(path=str(out))]


def main() -> None:
    mcp.run()


if __name__ == "__main__":
    main()
