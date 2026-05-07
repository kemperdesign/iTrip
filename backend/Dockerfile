FROM python:3.10-slim

WORKDIR /app

# Copy requirements first for caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy app code and entrypoint
COPY . .
RUN chmod +x run.py

# Run the app on port 8000 (Railway will handle port mapping via environment)
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
