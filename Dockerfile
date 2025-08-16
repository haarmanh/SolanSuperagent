FROM python:3.11-slim

# Security: Create non-root user
RUN groupadd -r solan && useradd -r -g solan solan

# Install system dependencies
RUN apt-get update && apt-get install -y \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create logs directory
RUN mkdir -p logs && chown -R solan:solan logs

# Security: Remove unnecessary files
RUN rm -rf tests/ *.md .git/ .env.example

# Switch to non-root user
USER solan

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# Default command (can be overridden)
CMD ["python", "main.py"]
