import os
import requests
from dotenv import load_dotenv
from datetime import datetime
import json

load_dotenv()
FRED_API_KEY = os.environ.get("FRED_API_KEY")
EXCHANGE_API_KEY = os.environ.get("EXCHANGE_API_KEY")
EXCHANGE_RATE_URL = os.environ.get("EXCHANGE_RATE_URL")
FRED_PRIME_RATE_URL = os.environ.get("FRED_BASE_URL")

os.environ["FRED_API_KEY"] = FRED_API_KEY
os.environ["EXCHANGE_API_KEY"] = EXCHANGE_API_KEY
os.environ["EXCHANGE_RATE_URL"] = EXCHANGE_RATE_URL
os.environ["FRED_BASE_URL"] = FRED_PRIME_RATE_URL

def convert_currency_service(currency_code: str, date_str: str) -> any:
    # Placeholder for currency conversion logic
    msg:str = ""

    if date_str == "latest":
        date_str = datetime.now().strftime("%Y-%m-%d")
    else:
        try:
            datetime.strptime(date_str, "%Y-%m-%d")
        except ValueError:
            return json.dumps({"error": "Invalid date format. Please use YYYY-MM-DD or 'latest'."})
        
        url = EXCHANGE_RATE_URL.format(date_str=date_str, currency_code=currency_code, EXCHANGE_API_KEY=EXCHANGE_API_KEY)

        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            if "rates" in data and "USD" in data["rates"]:
                exchange_rate = data["rates"]["USD"]
                msg = f"The exchange rate for {currency_code} to USD on {date_str} is {exchange_rate}."
            else:
                msg = f"Exchange rate data not available for {currency_code} on {date_str}."
        else:
            msg = f"Failed to retrieve exchange rate data. Status code: {response.status_code}"
        
    return json.dumps(
    {
        "currency" : currency_code,
        "date" : data["date"],
        "usd_rate" : data["rates"]["USD"],
        "message" : msg
    })

def prime_rates_service(date_str: str) -> any:
    if not FRED_API_KEY:
        return json.dumps({"error": "FRED API key is not set in environment variables."})
    
    prime_rate = None
    
    if date_str == "latest":
        date_str = datetime.now().strftime("%Y-%m-%d")
    else:
        try:
            datetime.strptime(date_str, "%Y-%m-%d")
        except ValueError:
            return json.dumps({"error": "Invalid date format. Please use YYYY-MM-DD or 'latest'."})     
        
    response = requests.get(FRED_PRIME_RATE_URL.format(FRED_API_KEY=FRED_API_KEY, start_date=date_str, end_date=date_str))
    if response.status_code == 200:
        data = response.json()
        if "observations" in data and len(data["observations"]) > 0:
            prime_rate = data["observations"][0]["value"]
            msg = f"The prime rate on {date_str} was {prime_rate}."
        else:
            msg = f"Prime rate data not available for {date_str}."
    else:
        msg = f"Failed to retrieve prime rate data. Status code: {response.status_code}"    

    return json.dumps(
    {
        "date" : date_str,
        "prime_rate" : prime_rate,
        "message" : msg
    })  