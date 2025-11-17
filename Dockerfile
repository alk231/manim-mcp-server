# Dockerfile (Railway - lightweight Manim)
FROM python:3.11-slim

# Install lightweight system libs required by Manim (no LaTeX)
RUN apt-get update && apt-get install -y --no-install-recommends \
    libcairo2 libcairo2-dev \
    libpango1.0-0 libpango1.0-dev \
    libglib2.0-0 libglib2.0-dev \
    ffmpeg pkg-config \
    build-essential python3-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# copy requirements and install
COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

# copy project
COPY . /app

ENV PORT=8000
EXPOSE 8000

# entrypoint (run the server)
CMD ["python", "src/manim_server.py"]
