FROM python:3.11-slim

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

# Install required Python packages
COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

# Copy your code
COPY src /app/src

WORKDIR /app/src

ENV MANIM_EXECUTABLE="manim"

EXPOSE 8000

CMD ["python", "manim_server.py"]
