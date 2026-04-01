# Gyrobot MCP Server

## Overview
This repository provides a small MCP-based currency and prime-rate service:

- `services.py` contains business logic:
  - `convert_currency_service(currency_code, date_str)`
  - `prime_rates_service(date_str)`
- `server.py` exposes the tools with FastMCP
- `mcp_adapter/server.py` wraps a remote/base API as an MCP tool and includes binding logic for agents

## Local setup

### 1. System prerequisites
- macOS/Linux/Windows with a shell
- Python 3.11+ recommended
- `pip` (Python package manager)

### 2. Clone repository
```bash
git clone https://github.com/<username>/gyrobot.git
cd gyrobot
```

### 3. Create virtual environment and install deps
```bash
python -m venv .venv
source .venv/bin/activate   # macOS/Linux
.venv\Scripts\activate     # Windows
pip install -r requirements.txt
```

### 4. Configure environment variables
Create `.env` with values (or use `export` / `set`):
```
FRED_API_KEY=<your_fred_api_key>
EXCHANGE_API_KEY=<your_exchange_api_key>
EXCHANGE_RATE_URL=https://api.exchangerate.host/{date_str}?base={currency_code}&symbols=USD&access_key={EXCHANGE_API_KEY}
FRED_BASE_URL=https://api.stlouisfed.org/fred/series/observations?series_id=MPRIME&api_key={FRED_API_KEY}&file_type=json&observation_start={start_date}&observation_end={end_date}
API_BASE=http://localhost:8000
```

### 5. Run the service
```bash
python server.py
```

Then visit:
- `http://localhost:8000/tool/convert_currency_tool?currency_code=EUR&date_str=2026-01-01`
- `http://localhost:8000/tool/prime_rates_tool?date_str=2026-01-01`

## MCP config (mcp.json)

Create a `mcp.json` in user workspace with a tool entry:
```json
{
  "tools": [
    {
      "name": "currency_mcp_server",
      "type": "http",
      "url": "http://localhost:8000",
      "api_key": "<your_api_key_optional>",
      "timeout": 120000
    }
  ]
}
```

> For Claude Agent usage, point the tool endpoint to local `mcp_adapter/server.py` or proxied API (see MCA docs).

## Configuring in VS Code (using MCP extension / custom tooling)

1. Install MCP extension or Claude integration extension.
2. Create `.vscode/settings.json` (or use extension GUI):
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

3. Start the server:
```bash
python mcp_adapter/server.py
```

4. Use tool calls from VS Code tool side panel (as per extension docs).

## Claude config

Claude expects a JSON or YAML tool definition in its app settings:

### Example `claude_tools.json`:
```json
[
  {
    "name": "convert_currency_tool",
    "description": "Get conversion from given currency to USD on given date",
    "url": "http://localhost:8000/tool/convert_currency_tool",
    "method": "GET",
    "headers": {
      "Content-Type": "application/json",
      "Authorization": "Bearer <CLAUDE_API_TOKEN_IF_NEEDED>"
    }
  },
  {
    "name": "prime_rates_tool",
    "description": "Get FRED prime rate observation for one day",
    "url": "http://localhost:8000/tool/prime_rates_tool",
    "method": "GET",
    "headers": {
      "Content-Type": "application/json"
    }
  }
]
```

Then in Claude UI/agent config: attach this tool file and invoke by name.

## Using the tools

1. `convert_currency_tool` - supported currency_code + date (YYYY-MM-DD or latest)
2. `prime_rates_tool` - returns a time-series observation list from FRED for a single day

Example:
```bash
curl "http://localhost:8000/tool/convert_currency_tool?currency_code=EUR&date_str=2026-01-01"
curl "http://localhost:8000/tool/prime_rates_tool?date_str=2026-01-01"
```

## Troubleshooting
- If `FRED_API_KEY` missing: service returns error JSON
- If rate is not available, `usd_rate` may be null and message will indicate unavailable
- If `date_str` invalid: returns JSON with format error

## Additional notes
- `mcp_adapter/server.py` has improved comments and tight error propagation in requests.
- The `services.py` has input validation and handling for missing observation fields.

