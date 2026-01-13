FROM python:3.12.8-slim AS base

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and setup files
COPY requirements.txt setup.py pyproject.toml ./

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy source code
COPY src /app/src

# Install the project as a package
RUN pip install -e .

# Expose port
EXPOSE 8000

# PYTHONUNBUFFERED=1 to disable output buffering
ENV PYTHONUNBUFFERED=1
ARG VERSION=0.1.0
ENV APP_VERSION=$VERSION

# Run the application
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "4"] 