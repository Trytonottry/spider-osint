FROM python:3.11-slim

WORKDIR /app

COPY backend/requirements.txt .
RUN apt-get update && \
    apt-get install -y build-essential && \
    pip install --no-cache-dir -r requirements.txt && \
    rm -rf /var/lib/apt/lists/*

COPY backend/ .

CMD ["python", "spider.py"]