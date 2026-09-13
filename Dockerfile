FROM python:3.9-slim

# Set working directory to /app to match your mounting strategy
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    unzip \
    wget \
    cron \
    python3 \
    python3-pip \
    && rm -rf /var/lib/apt/lists/*


# Copy entire project root
COPY . /app

#RUN pip install --upgrade pip           # to upgrade pip

RUN pip install -r requirements.txt
