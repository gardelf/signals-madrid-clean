FROM python:3.11-slim

WORKDIR /app

# Forzar salida sin buffer
ENV PYTHONUNBUFFERED=1

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python", "-u", "web_app.py"]
