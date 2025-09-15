# Gaming Workforce Observatory - Enterprise Dockerfile
# Multi-stage build for production optimization

FROM python:3.11-slim as base

# Set gaming app metadata
LABEL maintainer="remichenouri"
LABEL description="Gaming Workforce Observatory Enterprise Edition"
LABEL version="2.0.0"

# Gaming environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV STREAMLIT_SERVER_PORT=8501
ENV STREAMLIT_SERVER_ADDRESS=0.0.0.0
ENV GAMING_ENV=production

# Create gaming app user for security
RUN useradd --create-home --shell /bin/bash gaming_user

# Set gaming app directory
WORKDIR /app

# Install system gaming dependencies
RUN apt-get update && apt-get install -y \
    curl \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy gaming requirements first for better caching
COPY requirements.txt .

# Install gaming Python dependencies
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# Copy gaming application code
COPY . .

# Copy gaming configuration
COPY streamlit-config.toml /app/.streamlit/config.toml

# Create gaming data directories
RUN mkdir -p /app/data /app/logs /app/cache

# Set gaming permissions
RUN chown -R gaming_user:gaming_user /app

# Switch to gaming user
USER gaming_user

# Gaming health check
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8501/_stcore/health || exit 1

# Expose gaming port
EXPOSE 8501

# Gaming application startup
CMD ["streamlit", "run", "app.py", "--server.address", "0.0.0.0", "--server.port", "8501"]

# === PRODUCTION STAGE ===
FROM base as production

# Additional gaming production optimizations
ENV STREAMLIT_BROWSER_GATHER_USAGE_STATS=false
ENV STREAMLIT_CLIENT_CACHING=true
ENV STREAMLIT_SERVER_ENABLE_CORS=false

# Gaming production entrypoint
ENTRYPOINT ["streamlit", "run", "app.py"]

# === DEVELOPMENT STAGE ===
FROM base as development

# Gaming development dependencies
RUN pip install --no-cache-dir \
    pytest \
    black \
    flake8 \
    jupyter

# Gaming development mode
ENV STREAMLIT_SERVER_RUN_ON_SAVE=true
ENV GAMING_ENV=development

# Development gaming entrypoint with hot reload
CMD ["streamlit", "run", "app.py", "--server.runOnSave", "true"]