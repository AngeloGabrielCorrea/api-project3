FROM python:3.10-slim

RUN apt-get update && apt-get install -y \
    curl wget unzip fonts-liberation libnss3 libatk-bridge2.0-0 libgtk-3-0 libxss1 libasound2 libgbm1 libxshmfence1 \
    && pip install --no-cache-dir playwright flask \
    && playwright install chromium

WORKDIR /app

COPY . .

ENV PORT=5000

CMD ["gunicorn", "app:app", "--bind", "0.0.0.0:5000"]
