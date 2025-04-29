FROM python:3.12-slim

WORKDIR /

COPY . .

RUN apt-get update && \
    apt-get install -y wget gnupg libnss3 libatk-bridge2.0-0 libxcomposite1 libxdamage1 libxrandr2 \
    libasound2 libatk1.0-0 libcups2 libdbus-1-3 libdrm2 libxkbcommon0 libxshmfence1 \
    libgbm1 libgtk-3-0 libx11-xcb1 libxcomposite-dev libxdamage-dev libxrandr-dev && \
    rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir -r requirements.txt

RUN pip install playwright && playwright install --with-deps

CMD ["python", "app.py"]
