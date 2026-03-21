# Homework 5: MCP Servers (GitHub, Filesystem, Jira, Custom)

Author: Your Name

## Deliverables summary

This homework contains configuration and evidence for:

- Task 1: GitHub MCP
- Task 2: Filesystem MCP
- Task 3: Jira MCP
- Task 4: Custom MCP server built with FastMCP

## Custom MCP server implementation

The custom server is located in `custom-mcp-server/` and provides:

- Resource URIs:
	- `lorem://ipsum`
	- `lorem://ipsum/{word_count}`
- Tool:
	- `read(word_count=30)`

The resource and tool both read from `lorem-ipsum.md` and return exactly the requested number of words (default: `30`).

## Resource vs Tool (short explanation)

- Resources are URI-based data endpoints that the AI can read (for example files or API-style data sources).
- Tools are callable actions that the AI can execute with arguments (for example reading content with a specific `word_count`).

## Included files

- `HOWTORUN.md`: install, run, MCP config, and validation steps.
- `.mcp.json`: example MCP client configuration for the custom server.
- `custom-mcp-server/server.py`: FastMCP server implementation.
- `custom-mcp-server/requirements.txt`: dependencies including `fastmcp`.
- `custom-mcp-server/lorem-ipsum.md`: source content for resource/tool output.

## Screenshots

Screenshots are stored in `docs/screenshots/`:

- `github-mcp-result.png`
- `filesystem-mcp-result.png`
- `custom-mcp-read-tool-result.png`

## Task 3 (Jira MCP) note

Jira MCP was configured and validated, but result screenshots/details are not included because this is a corporate MCP environment and the data is under NDA restrictions.
