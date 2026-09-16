# Peek

Let an AI agent take a photo with your camera.

Peek is an MCP server with one tool, `peek`. When an agent calls it, a live
camera preview opens. Position the item, press **space** to capture, or
**Escape** to cancel. The photo is returned to the agent as an image and
saved under `~/Pictures/Peek/`.

## Setup

```bash
cd ~/code/peek && uv sync
```

Register with Claude Code (user scope, so every project has it):

```bash
claude mcp add --scope user peek -- uv --directory ~/code/peek run peek
```

The first capture triggers a macOS camera permission prompt for whichever app
launched the server (the Claude desktop app or your terminal). Grant it in
System Settings > Privacy & Security > Camera if you dismissed the prompt.

## Try it without an agent

```bash
uv run python -m peek.camera /tmp/test.jpg
```

## Tool

`peek(max_side: int = 1500, device: int = 0)`

- `max_side`: longest edge of the returned image in pixels.
- `device`: camera index if you have more than one.
