FROM python:3.10-slim

WORKDIR /app

# Copy requirements first for caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy app code and entrypoint
COPY . .
RUN chmod +x run.py

# Run the app using Python entrypoint (reads PORT env var, defaults to 8000)
CMD ["python", "run.py"]
