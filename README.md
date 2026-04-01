# gyrobot

curl -L httosL//fly.io/install.sh | sh
fly auth login

fly launch
fly secrets set 

fly deploy


FRED_API_KEY="06c73d0a311e793c2b08989ee10b5352"
FRED_BASE_URL="https://api.stlouisfed.org/fred/series/observations?series_id=DPRIME&api_key=06c73d0a311e793c2b08989ee10b5352&file_type=json&observation_start=2026-01-01&observation_end=2026-01-01"
EXCHANGE_RATE_URL="https://api.exchangerate.host/2026-01-01?base=EUR&symbols=USD&access_key=a72202fa18e8f2d6e43d782685c90e6b"