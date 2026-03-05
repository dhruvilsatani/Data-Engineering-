FROM python:3.11-slim

WORKDIR /app

# system deps for unzip + sqlite CLI (optional)
RUN apt-get update && apt-get install -y --no-install-recommends \
    unzip \
    sqlite3 \
  && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY src/ /app/src

# Default: show help
CMD ["python", "-m", "src.utils"]