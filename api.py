from fastapi import FastAPI
from services import convert_currency_service, get_prime_rate_service

app = FastAPI(title="Currency Bot API", description="API for currency conversion and prime rate retrieval.", version="1.0")

@app.get("/convert_currency")
def convert_currency(currency_code: str = "INR", date_str: str = "latest"):
    return convert_currency_service(currency_code, date_str)

@app.get("/prime_rate")
def prime_rate(date_str: str = "latest"):
    return get_prime_rate_service(date_str)