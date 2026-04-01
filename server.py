from mcp.server import FastMCP
from services import convert_currency_service, prime_rates_service

server = FastMCP("currency_mcp_server")

@server.tool() #"convert_currency", "Convert a currency to USD based on a specific date or the latest rate.")
def convert_currency_tool(currency_code: str = "INR", date_str: str = "latest") -> any:
    return convert_currency_service(currency_code, date_str)

@server.tool() #"prime_rates", "Get the prime rate for a specific date or the latest rate.")
def prime_rates_tool(date_str: str = "latest") -> any:
    return prime_rates_service(date_str)


if __name__ == "__main__":
    server.run()


"""
    from mcp.server import FastMCP
    from services import convert_currency_service, prime_rates_service

    server = FastMCP("currency_bot", "1.0", "A bot that provides currency conversion rates and prime rates based on user queries.")

    @server.tool("convert_currency", "Convert a currency to USD based on a specific date or the latest rate.")
    def convert_currency_tool(currency_code: str = "INR", date_str: str = "latest") -> any:
        return convert_currency_service(currency_code, date_str)

    @server.tool("prime_rates", "Get the prime rate for a specific date or the latest rate.")
    def prime_rates_tool(date_str: str = "latest") -> any:
        return prime_rates_service(date_str)


    if __name__ == "__main__":
        server.run()

"""
