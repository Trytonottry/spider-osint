# workers/Dockerfile
FROM python:3.11-slim
WORKDIR /app/workers
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY workers/ .
CMD ["celery", "-A", "worker", "worker", "--loglevel=info"]
RUN pip install python-telegram-bot