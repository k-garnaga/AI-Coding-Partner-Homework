# How To Run - Homework 5 Task 4

## 1. Prerequisites

- Python 3.10+
- pip
- MCP-compatible client (Copilot, Claude Desktop, or another MCP client)

## 2. Install dependencies

From `homework-5/custom-mcp-server`:

```bash
python3 -m pip install -r requirements.txt
```

## 3. Start the custom MCP server

From `homework-5/custom-mcp-server`:

```bash
python3 server.py
```

If startup is successful, keep this process running while connecting from your MCP client.

## 4. MCP client configuration

Use `.mcp.json` from `homework-5` as a reference.

Example config in this project:

```json
{
  "mcpServers": {
    "custom-lorem-server": {
      "command": "python3",
      "args": [
        "custom-mcp-server/server.py"
      ],
      "cwd": "."
    }
  }
}
```

If your client uses a different MCP schema key, adapt `mcpServers` accordingly.

## 5. Validate Resource behavior

Try reading either resource:

- `lorem://ipsum` -> returns first 30 words
- `lorem://ipsum/12` -> returns first 12 words

## 6. Validate Tool behavior

Call tool `read` with no argument:

- Expected: first 30 words

Call tool `read` with argument:

- Input: `{ "word_count": 20 }`
- Expected: first 20 words

## 7. Verification checklist

- Server starts with `python3 server.py`
- `fastmcp` is listed in dependencies
- MCP configuration points to the custom server command
- Resource and tool both return word-limited content as requested
