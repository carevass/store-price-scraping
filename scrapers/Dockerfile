FROM python:3.11-slim

# Set working directory to /app to match your mounting strategy
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    cron \
    python3 \
    python3-pip \
    #gconf-service \
    chromium \
    chromium-driver \
    wget \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/*

# Copy entire project root
COPY . /app

#RUN pip install --upgrade pip           # to upgrade pip

RUN pip install -r requirements.txt
