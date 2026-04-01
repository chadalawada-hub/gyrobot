from fastapi import FastAPI
from services import convert_currency_service, prime_rates_service

app = FastAPI(title="Currency Bot API", description="API for currency conversion and prime rate retrieval.", version="1.0")

@app.get("/convert_currency")
def convert_currency(currency_code: str = "INR", date_str: str = "latest"):
    return convert_currency_service(currency_code, date_str)

@app.get("/prime_rate")
def prime_rate(date_str: str = "latest"):
    return prime_rates_service(date_str)