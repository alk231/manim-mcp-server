# ---- Base Image ----
FROM python:3.11-slim

# ---- Install System Dependencies for Manim ----
RUN apt-get update && apt-get install -y \
    ffmpeg \
    libcairo2 \
    libcairo2-dev \
    libpango-1.0-0 \
    libpangoft2-1.0-0 \
    libfreetype6 \
    libfreetype6-dev \
    libgl1 \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# ---- Install Manim ----
RUN pip install --no-cache-dir manim

# ---- Set Work Directory ----
WORKDIR /app

# ---- Copy Your MCP Server Code ----
COPY . .

# ---- Environment Variables ----
ENV MANIM_EXECUTABLE="manim"
ENV PYTHONUNBUFFERED=1

# ---- Expose Port for Streamable HTTP MCP ----
EXPOSE 8000

# ---- Start the MCP Server ----
CMD ["python", "manim_server.py"]
