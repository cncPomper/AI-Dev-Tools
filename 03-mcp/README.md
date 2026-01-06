# 03-mcp: Model Context Protocol Tools

## What is this?

This folder demonstrates building custom MCP (Model Context Protocol) tools that allow AI assistants like Claude, ChatGPT, and GitHub Copilot to access external functionality. MCP is a standardized protocol for AI assistants to interact with tools and services.

## Quick Start

```bash
# Install dependencies
cd /workspaces/AI-Dev-Tools/03-mcp
uv sync

# Run the MCP server
uv run python main.py

# Or run tests
python test_datatalks.py
python search.py
```

## What's Inside

**MCP Tools (`main.py`):**
- `download_web_content()` - Downloads web pages as markdown using Jina Reader
- `count_word_occurrences()` - Counts words in text (case-insensitive)
- `add()` - Simple demo tool for adding numbers

**Search Implementation (`search.py`):**
- Downloads FastMCP docs from GitHub
- Extracts `.md` and `.mdx` files from ZIP archives
- Indexes documents with minsearch for full-text search
- Searches and retrieves top-K relevant documents

**Tests:**
- `test.py` - Tests web content download
- `test_datatalks.py` - Tests word counting on real websites
- `search.py` - Tests document indexing and search

## How to Use with AI Assistants

Add to `.vscode/mcp.json`:
```json
{
  "servers": {
    "ai-dev-tools": {
      "type": "stdio",
      "command": "uv",
      "args": ["--directory", "/workspaces/AI-Dev-Tools/03-mcp", "run", "python", "main.py"]
    }
  }
}
```

Then ask your AI assistant: *"Count how many times 'data' appears on https://datatalks.club/"*

## Key Technologies

- **FastMCP** - Framework for building MCP tools
- **Jina Reader** - Converts web pages to markdown (`r.jina.ai`)
- **Minsearch** - Lightweight Python search library
- **uv** - Fast Python package manager

## Learn More

- [FastMCP Docs](https://github.com/jlowin/fastmcp)
- [Minsearch](https://github.com/alexeygrigorev/minsearch)
- [MCP Specification](https://modelcontextprotocol.io/)