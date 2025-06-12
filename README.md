# Gemini MCP Server

A Model Context Protocol (MCP) server that enables Claude to interact with Google's Gemini AI models.

## Setup

1. **Get a Gemini API key** from [Google AI Studio](https://aistudio.google.com/apikey)

2. **Add to Claude Desktop config** (`~/Library/Application Support/Claude/claude_desktop_config.json`):

```json
{
  "mcpServers": {
    "gemini": {
      "command": "uvx",
      "args": ["--from", "/path/to/gemini-mcp", "gemini-mcp"],
      "env": {
        "GEMINI_API_KEY": "your_api_key_here",
        "MODEL_NAME": "gemini-2.5-flash-preview-05-20"
      }
    }
  }
}
```

Replace `/path/to/gemini-mcp` with the actual path to this directory.

## Usage

### `ask_gemini`
Ask Gemini questions directly from Claude.

- `prompt`: Your question for Gemini
- `temperature`: Response creativity (0.0-1.0, default: 0.5)
- `context`: Additional context
- `persona`: Role for Gemini (e.g., "senior architect", "security expert")

### `server_info`
Check server status and Gemini availability.

## Examples

```
Ask Gemini: What are the latest trends in machine learning?

Ask Gemini to review this code as a senior developer: [code]

Ask Gemini about Python best practices with context that I'm building a web API
```

## Troubleshooting

- **API key error**: Set `GEMINI_API_KEY` in your environment
- **Rate limit**: Wait and try again
- **Content filtered**: Rephrase your request
- **Server issues**: Use `server_info` tool to check status