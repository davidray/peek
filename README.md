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
- [uv](https://docs.astral.sh/uv/) — used both to run the server and as the
  install mechanism below.
- A camera. Developed and tested on macOS; should work anywhere OpenCV can
  open a camera, but the "keep window on top" behavior is macOS-specific.

## Install

Peek isn't published to PyPI (the name's taken), so the easiest install is
to run it straight from GitHub with `uv` — no clone, no local checkout:

```bash
uvx --from git+https://github.com/davidray/peek.git peek
```

`uv` caches the build after the first run, so subsequent launches are fast.
Every config below uses this form. If you'd rather work from a local clone
(e.g. to hack on it), see [Local development](#local-development).

The first capture triggers a camera permission prompt for whichever process
launched the server (your terminal, or the app hosting your agent). On
macOS, grant it under System Settings > Privacy & Security > Camera if you
dismiss the prompt.

### GitHub Copilot (VS Code)

[![Install in VS Code](https://img.shields.io/badge/VS_Code-Install_Peek-0098FF?logo=visualstudiocode&logoColor=white)](https://vscode.dev/redirect/mcp/install?name=peek&config=%7B%22command%22%3A%20%22uvx%22%2C%20%22args%22%3A%20%5B%22--from%22%2C%20%22git%2Bhttps%3A//github.com/davidray/peek.git%22%2C%20%22peek%22%5D%7D)

Or run **MCP: Add Server** from the Command Palette, or add it from the
command line:

```bash
code --add-mcp "{\"name\":\"peek\",\"command\":\"uvx\",\"args\":[\"--from\",\"git+https://github.com/davidray/peek.git\",\"peek\"]}"
```

Or edit `mcp.json` yourself (**MCP: Open User Configuration**, or
`.vscode/mcp.json` for a single workspace):

```json
{
  "servers": {
    "peek": {
      "type": "stdio",
      "command": "uvx",
      "args": ["--from", "git+https://github.com/davidray/peek.git", "peek"]
    }
  }
}
```

For the Copilot coding agent / Agent Host (which doesn't read
`.vscode/mcp.json`), use a workspace `.mcp.json` or user
`~/.copilot/mcp-config.json` with the same `mcpServers` shape shown under
[Generic MCP clients](#generic-mcp-clients) below.

### Claude

**Claude Code:**

```bash
claude mcp add --scope user peek -- uvx --from git+https://github.com/davidray/peek.git peek
```

**Claude Desktop:** add this to your config
(`~/Library/Application Support/Claude/claude_desktop_config.json` on macOS):

```json
{
  "mcpServers": {
    "peek": {
      "command": "uvx",
      "args": ["--from", "git+https://github.com/davidray/peek.git", "peek"]
    }
  }
}
```

### ChatGPT

ChatGPT's MCP connectors (Settings > Apps & Connectors, with Developer Mode
enabled) only talk to a server over HTTPS — it can't launch a local stdio
process the way Claude or VS Code can. To use Peek there:

1. Run Peek in HTTP mode on your machine:

   ```bash
   uvx --from git+https://github.com/davidray/peek.git peek --transport http --port 8931
   ```

2. Expose it with an HTTPS tunnel, e.g. [`cloudflared`](https://developers.cloudflare.com/cloudflare-one/connections/connect-networks/downloads/)
   or [`ngrok`](https://ngrok.com/):

   ```bash
   cloudflared tunnel --url http://127.0.0.1:8931
   ```

3. In ChatGPT, add a custom connector pointing at `https://<tunnel-host>/mcp`.

Since this puts a local, unauthenticated server on a public URL for as long
as the tunnel runs, only do this on a trusted network and shut the tunnel
down when you're done.

### Generic MCP clients

Most other clients (Cursor, Windsurf, etc.) use the same `mcpServers` shape:

```json
{
  "mcpServers": {
    "peek": {
      "command": "uvx",
      "args": ["--from", "git+https://github.com/davidray/peek.git", "peek"]
    }
  }
}
```

## Local development

```bash
git clone git@github.com:davidray/peek.git
cd peek && uv sync
```

Then point any of the configs above at your checkout instead of the git URL:

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

## Try it without an agent

```bash
uv run python -m peek.camera /tmp/test.jpg
```

## Tool

`peek(max_side: int = 1500, device: int = 0)`

- `max_side`: longest edge of the returned image in pixels (default 1500).
- `device`: camera index if you have more than one (default 0).

The server itself takes `--transport {stdio,http}` (default `stdio`), plus
`--host`/`--port` for HTTP mode. Stdio is what every desktop MCP client
uses; HTTP is only needed for clients (like ChatGPT above) that require a
reachable URL instead of a local process.

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
