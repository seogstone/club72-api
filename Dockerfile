FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Install Playwright dependencies and browsers
RUN apt-get update && apt-get install -y wget gnupg unzip libglib2.0-0 libnss3 libatk1.0-0 libatk-bridge2.0-0 libcups2 libdrm2 libxkbcommon0 libxcomposite1 libxrandr2 libgbm1 libgtk-3-0 libasound2
RUN pip install playwright
RUN playwright install --with-deps

COPY . .

EXPOSE 10000
CMD ["sh", "start.sh"]
