FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV PYTHONBUFFERED=1

CMD ["sh", "-c", "uvicorn api:app & python server.py --host 0.0.0.0 --port 8080"]
