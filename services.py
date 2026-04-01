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
    # Main conversion service that returns USD exchange rate info for a given currency and date.
    # It supports a literal "latest" date translation and strict YYYY-MM-DD validation.
    msg: str = ""

    if date_str == "latest":
        # Normalize to today's date for the API call
        date_str = datetime.now().strftime("%Y-%m-%d")

    # Ensure date format is strictly correct before hitting the API
    try:
        datetime.strptime(date_str, "%Y-%m-%d")
    except ValueError:
        return json.dumps({"error": "Invalid date format. Please use YYYY-MM-DD or 'latest'."})

    url = EXCHANGE_RATE_URL.format(date_str=date_str, currency_code=currency_code, EXCHANGE_API_KEY=EXCHANGE_API_KEY)

    response = requests.get(url)
    data = None
    if response.status_code == 200:
        # Parse JSON safely, with error fallback
        try:
            data = response.json()
        except ValueError:
            return json.dumps({"error": "Invalid JSON response from exchange rate provider."})

        # The API may include many fields; target USD rate from nested rates object
        if "rates" in data and "USD" in data["rates"]:
            exchange_rate = data["rates"]["USD"]
            msg = f"The exchange rate for {currency_code} to USD on {date_str} is {exchange_rate}."
        else:
            msg = f"Exchange rate data not available for {currency_code} on {date_str}."
    else:
        msg = f"Failed to retrieve exchange rate data. Status code: {response.status_code}"

    # Attempt to read optional quote field; keep payload stable even when missing.
    two_codes = f"USD{currency_code}"
    usd_rate = None
    if isinstance(data, dict) and "quotes" in data and two_codes in data["quotes"]:
        usd_rate = data["quotes"][two_codes]

    return json.dumps(
        {
            "source": "USD",
            "currency": currency_code,
            "date": date_str,
            "usd_rate": usd_rate,
            "message": msg
        }
    )

def prime_rates_service(date_str: str) -> any:
    # Return prime rate data for a specific date, using FRED API (Federal Reserve Economic Data).
    # Handles missing API key, date validation, and API transport/format robustness.
    if not FRED_API_KEY:
        return json.dumps({"error": "FRED API key is not set in environment variables."})

    if date_str == "latest":
        # Convert latest to today, so we can query FRED using a date range
        date_str = datetime.now().strftime("%Y-%m-%d")

    try:
        datetime.strptime(date_str, "%Y-%m-%d")
    except ValueError:
        return json.dumps({"error": "Invalid date format. Please use YYYY-MM-DD or 'latest'."})

    # Query FRED for prime rate series for the desired date range (start_date=end_date=date_str)
    response = requests.get(FRED_PRIME_RATE_URL.format(FRED_API_KEY=FRED_API_KEY, start_date=date_str, end_date=date_str))

    if response.status_code != 200:
        return json.dumps({"error": f"Failed to retrieve prime rate data. Status code: {response.status_code}"})

    try:
        data = response.json()
    except ValueError:
        return json.dumps({"error": "Invalid JSON response from FRED API."})

    if not isinstance(data, dict):
        return json.dumps({"error": "Unexpected FRED API response format."})

    # Build cleaned observation list. Ignore entries without the expected keys.
    observations_raw = data.get("observations", [])
    observations_list = []
    for obs in observations_raw:
        if isinstance(obs, dict) and "date" in obs and "value" in obs:
            observations_list.append({"date": obs["date"], "value": obs["value"]})

    # Determine message to give user visibility into whether we found data.
    if observations_list:
        prime_rate = observations_list[0]["value"]
        msg = f"The prime rate on {date_str} was {prime_rate}."
    else:
        msg = f"Prime rate data not available for {date_str}."

    result = {
        "observation_start": data.get("observation_start"),
        "observation_end": data.get("observation_end"),
        "observations": observations_list,
        "message": msg
    }

    return json.dumps(result)  