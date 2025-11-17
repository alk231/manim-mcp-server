FROM python:3.11-slim

# Install system libs required by Manim
RUN apt-get update && apt-get install -y \
    libcairo2 \
    libcairo2-dev \
    libpango1.0-dev \
    libglib2.0-dev \
    ffmpeg \
    pkg-config \
    python3-dev \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Create app directory
WORKDIR /app

# Copy requirements
COPY requirements.txt /app/

# Install Python dependencies
RUN pip install --no-cache-dir -r /app/requirements.txt

# Copy project
COPY . /app/

# MCP server runs on port 8000
ENV PORT=8000

# Expose port
EXPOSE 8000

# Run MCP server
CMD ["python", "src/manim_server.py"]
