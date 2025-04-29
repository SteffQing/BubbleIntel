FROM mcr.microsoft.com/playwright/python:v1.43.1-jammy

WORKDIR /

COPY . .

RUN pip install --no-cache-dir -r requirements.txt

RUN playwright install --with-deps

# Run your bot
CMD ["python", "app.py"]
