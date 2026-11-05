FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    ENV=test

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    curl unzip wget gnupg \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["pytest", "-m", "api", "--alluredir=reports/allure-results", "--clean-alluredir"]
