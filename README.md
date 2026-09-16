# Peek

Let an AI agent take a photo with your camera.

Peek is an [MCP](https://modelcontextprotocol.io) server with one tool,
`peek`. When an agent calls it, a live camera preview opens. Position the
item, press **space** to capture, or **Escape** to cancel. The photo is
returned to the agent as an image and saved under `~/Pictures/Peek/`.

Handy for showing an agent a physical object, a document, a whiteboard, a
part number, or anything else it can't otherwise see.

## Requirements

- Python 3.12+
- [uv](https://docs.astral.sh/uv/)
- A camera. Developed and tested on macOS; should work anywhere OpenCV can
  open a camera, but the "keep window on top" behavior is macOS-specific.

## Setup

```bash
git clone git@github.com:davidray/peek.git
cd peek && uv sync
```

Register with Claude Code (user scope, so every project has it):

```bash
claude mcp add --scope user peek -- uv --directory /path/to/peek run peek
```

Or add it by hand to your MCP client's config:

```json
{
  "mcpServers": {
    "peek": {
      "command": "uv",
      "args": ["--directory", "/path/to/peek", "run", "peek"]
    }
  }
}
```

The first capture triggers a camera permission prompt for whichever process
launched the server (your terminal, or the app hosting your agent). On
macOS, grant it under System Settings > Privacy & Security > Camera if you
dismiss the prompt.

## Try it without an agent

```bash
uv run python -m peek.camera /tmp/test.jpg
```

## Tool

`peek(max_side: int = 1500, device: int = 0)`

- `max_side`: longest edge of the returned image in pixels (default 1500).
- `device`: camera index if you have more than one (default 0).

## How it works

- [`peek/server.py`](peek/server.py) — the MCP server. Its `peek` tool
  shells out to the capture window and returns the resulting photo as an
  MCP image content block plus the saved path.
- [`peek/camera.py`](peek/camera.py) — the live preview, run as its own
  process since OpenCV's window/event loop needs the main thread.

## Contributing

Issues and pull requests welcome. Keep it small: one tool, one job.

## License

MIT — see [LICENSE](LICENSE).
