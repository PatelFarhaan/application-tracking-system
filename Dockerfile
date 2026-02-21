FROM python:3.7-slim

RUN apt-get update && apt-get install -y --no-install-recommends \
    default-libmysqlclient-dev gcc \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY "DB-Application directory/requirements.txt" .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

WORKDIR /app/DB-Application directory

EXPOSE 5000

CMD ["python", "app.py"]
