from mcp.server import Server
from services import convert_currency_service, prime_rates_service

server = Server("currency_mcp_server")

@server.tool() 
def convert_currency_tool(currency_code: str = "INR", date_str: str = "latest") -> any:
    return convert_currency_service(currency_code, date_str)

@server.tool() 
def prime_rates_tool(date_str: str = "latest") -> any:
    return prime_rates_service(date_str)


if __name__ == "__main__":
    server.run()

