# Gyrobot MCP Adapter (Client Distribution)

## Overview
This folder is a client-side MCP adapter package. It exposes two tools via FastMCP and proxies calls to a backend MCP server (e.g., `server.py` service in top-level repo).

- `mcp_adapter/server.py` runs a local MCP server and exposes:
  - `convert_currency_tool(currency_code, date_str)`
  - `prime_rates_tool(date_str)`

## System requirements
- Python 3.11+ installed and on PATH
- `pip` available
- Network access to the backend API (API_BASE)

## Install locally
1. Clone (mock repo URL):
```bash
git clone https://github.com/example/gyrobot.git
cd gyrobot/mcp_adapter
```

2. Create and activate virtual environment:
```bash
python -m venv .venv
# macOS/Linux:
source .venv/bin/activate
# Windows:
.venv\Scripts\activate
```

3. Install dependencies (from root requirements):
```bash
pip install -r ../requirements.txt
```

## Configure environment variables
Create `.env` or export vars directly:
```bash
export API_BASE=http://localhost:8000              # backend service endpoint
export FRED_API_KEY=<your_fred_api_key>            # optional
```

## Running adapter server
```bash
cd gyrobot/mcp_adapter
python server.py
```

- Default listen endpoint: (as configured by FastMCP) `http://localhost:8000` (or changed by your setup)
- Confirm tool availability by requesting:
  - `/tool/convert_currency_tool?currency_code=EUR&date_str=2026-01-01`
  - `/tool/prime_rates_tool?date_str=2026-01-01`

## `mcp.json` example (client workspace)
Create `mcp.json` in your workspace root to connect an MCP client to this adapter:
```json
{
  "tools": [
    {
      "name": "currency_mcp_server",
      "type": "http",
      "url": "http://localhost:8000",
      "api_key": "<optional>",
      "timeout": 120000
    }
  ]
}
```

## VS Code integration
1. Install MCP extension or any LLM tool extension that supports HTTP tool integration.
2. In `.vscode/settings.json`:
```json
{
  "mcp.serverUrl": "http://localhost:8000",
  "mcp.apiKey": "<your_api_key_if_needed>",
  "mcp.timeout": 120000,
  "mcp.tools": [
    {
      "name": "convert_currency_tool",
      "command": "GET",
      "url": "http://localhost:8000/tool/convert_currency_tool"
    },
    {
      "name": "prime_rates_tool",
      "command": "GET",
      "url": "http://localhost:8000/tool/prime_rates_tool"
    }
  ]
}
```
3. Start adapter server:
```bash
python mcp_adapter/server.py
```
4. Use command palette or product-specific tool panel to invoke these endpoints.

## Claude integration
Create `claude_tools.json` for Claude agent config:
```json
[
  {
    "name": "convert_currency_tool",
    "description": "Get conversion from given currency to USD on given date",
    "url": "http://localhost:8000/tool/convert_currency_tool",
    "method": "GET",
    "headers": {"Content-Type": "application/json"}
  },
  {
    "name": "prime_rates_tool",
    "description": "Get FRED prime rate observation for one day",
    "url": "http://localhost:8000/tool/prime_rates_tool",
    "method": "GET",
    "headers": {"Content-Type": "application/json"}
  }
]
```

Import the JSON in Claude config and call by name.

## Examples
```bash
curl "http://localhost:8000/tool/convert_currency_tool?currency_code=EUR&date_str=2026-01-01"
curl "http://localhost:8000/tool/prime_rates_tool?date_str=2026-01-01"
```

## Notes and troubleshooting
- Check `.env` for correct `API_BASE`
- If `convert_currency_tool` fails, verify backend `convert_currency` endpoint and keys
- If `prime_rates_tool` returns no observations, confirm FRED API key and correct date range
