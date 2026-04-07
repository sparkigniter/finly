# ---- Base image ----
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy and install Python dependencies first (layer caching)
COPY app/backend/requirements.txt ./requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire app source
COPY app/ ./app/

# Cloud Run sets PORT env var (default 8080)
ENV PORT=8000

# Run the FastAPI app with uvicorn
CMD ["sh", "-c", "uvicorn app.backend.apis:app --host 0.0.0.0 --port $PORT --workers 2"]
