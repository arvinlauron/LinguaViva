# Use a slim Python image
FROM python:3.12-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Install system dependencies if needed
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential && \
    rm -rf /var/lib/apt/lists/*

# Install python dependencies
COPY requirements.txt .
RUN pip install --default-timeout=1000 --retries 5 --no-cache-dir -r requirements.txt

# Copy your application files and model folders
COPY . .

# Expose standard Cloud Run port
EXPOSE 8080

# Shell format forces Gunicorn to read Cloud Run's dynamic $PORT
CMD exec gunicorn --bind :$PORT --workers 1 --threads 8 --timeout 0 app:app