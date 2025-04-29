FROM ghcr.io/microsoft/playwright-python:v1.43.1

WORKDIR /

COPY . .

RUN pip install --no-cache-dir -r requirements.txt

RUN playwright install --with-deps

# Run your bot
CMD ["python", "app.py"]
