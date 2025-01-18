# Build stage for Python dependencies
FROM python:3.10-slim as python-builder

WORKDIR /app
COPY requirements.txt .

RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --user --no-cache-dir -r requirements.txt

# Build stage for Node.js frontend
FROM node:16-slim as node-builder

WORKDIR /app
COPY frontend/package*.json ./
RUN npm install

COPY frontend/ .
RUN npm run build

# Final stage
FROM python:3.10-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    chromium \
    chromium-driver \
    curl \
    libgomp1 \
    && rm -rf /var/lib/apt/lists/*

# Copy Python packages from builder
COPY --from=python-builder /root/.local /root/.local
ENV PATH=/root/.local/bin:$PATH

# Copy frontend build
COPY --from=node-builder /app/build /app/static

# Copy application code
COPY . .

# Set environment variables
ENV PYTHONPATH=/app
ENV PYTHONUNBUFFERED=1
ENV CHROME_BIN=/usr/bin/chromium
ENV CHROMEDRIVER_PATH=/usr/bin/chromedriver

# Create necessary directories
RUN mkdir -p /app/data /app/logs /app/models

# Create non-root user
RUN useradd -m -u 1000 appuser && \
    chown -R appuser:appuser /app
USER appuser

# Health check
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# Expose ports for API, Prometheus, and Grafana
EXPOSE 8000 9090 3000

# Create volumes for persistence
VOLUME ["/app/data", "/app/logs", "/app/models"]

# Default command
CMD ["python", "-m", "uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]
