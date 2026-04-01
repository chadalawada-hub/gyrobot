from mcp.server import FastMCP
import requests
import os

# MCP client adapter: this file is meant to be distributed to client installations
# that need to expose a stable MCP interface to tools and agents while calling a
# backend service. It should be installed as part of the mcp_adapter package.

# Optional environment variable for local adapter usage.
# Typically the secrets for data source API keys live in the backend service.
GREA_FRED_API_KEY = os.environ.get("FRED_API_KEY")

# API_BASE is the backend endpoint that this adapter proxies.
# Defaults to deployed service URL, but can be set to local service for dev/test.
API_BASE = os.environ.get("API_BASE", "http://localhost:8000")

# FastMCP server wraps tool functions for agents (Claude, VS Code MCP extensions, etc.).
server = FastMCP("currency_mcp_server")

@server.tool()
def convert_currency_tool(currency_code: str = "EUR", date_str: str = "latest") -> any:
    """Client-side MCP tool: proxy request to currency conversion backend."""
    # Request structure should match the backend API. We use explicit timeout.
    response = requests.get(
        f"{API_BASE}/convert_currency",
        params={"currency_code": currency_code, "date_str": date_str},
        timeout=10,
    )
    response.raise_for_status()  # Make failures obvious to agents
    return response.json()


@server.tool()
def prime_rates_tool(date_str: str = "latest") -> any:
    """Client-side MCP tool: proxy request to prime rate backend."""
    response = requests.get(
        f"{API_BASE}/prime_rate",
        params={"date_str": date_str},
        timeout=10,
    )
    response.raise_for_status()
    return response.json()


if __name__ == "__main__":
    # Start the adapter server. The MCP agent tooling calls this process.
    # Example: `python mcp_adapter/server.py`
    server.run()
