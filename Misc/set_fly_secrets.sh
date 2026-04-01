echo "Setting up secrets for the application..."

fly secrets set FREFRED_API_KEY="06c73d0a311e793c2b08989ee10b5352"
echo "Done adding FRED_API_KEY"
fly secrets set FRED_BASE_URL="https://api.stlouisfed.org/fred/series/observations?series_id=MPRIME&api_key={FRED_API_KEY}&file_type=json&observation_start={start_date}&observation_end={end_date}"
echo "Done adding FRED_BASE_URL"
fly secrets set EXCHANGE_API_KEY="a72202fa18e8f2d6e43d782685c90e6b"
echo "Done adding EXCHANGE_API_KEY"
fly secrets set EXCHANGE_RATE_URL="https://api.exchangerate.host/historical?date={date_str}&access_key={EXCHANGE_API_KEY}"D
echo "Done adding EXCHANGE_RATE_URL"

echo "All secrets added successfully!"