FROM python:3.11-slim

WORKDIR /app

COPY ./requirements.txt .

RUN pip install --upgrade pip setuptools && \
    pip install --no-cache-dir -r requirements.txt

COPY . .