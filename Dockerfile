FROM python:3.12-slim

WORKDIR /
COPY . .

# Install system dependencies
RUN apt-get update && apt-get install -y wget gnupg curl ca-certificates fonts-liberation libasound2 libatk1.0-0 libatk-bridge2.0-0 libgtk-3-0 libnss3 libxss1 libx11-xcb1 libxcomposite1 libxdamage1 libxrandr2 libgbm-dev libxshmfence-dev libxext6 libxfixes3 libxrender1 libxinerama1 libxcursor1 libglib2.0-0 libsm6 libice6 xvfb && \
    pip install --no-cache-dir playwright && \
    playwright install && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir -r requirements.txt

CMD ["python", "app.py"]
