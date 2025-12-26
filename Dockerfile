# Use Python 3.11 slim image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies for Pygame
# Note: For GUI display, you'll need X11 forwarding or VNC
RUN apt-get update && apt-get install -y \
    libsdl1.2debian \
    libsdl-image1.2debian \
    libsdl-mixer1.2debian \
    libsdl-ttf2.0debian \
    libsmpeg0 \
    libportmidi0 \
    libswscale-extra2 \
    libavformat-extra56 \
    libjpeg62-turbo \
    libpng16-16 \
    libtiff5 \
    libwebp5 \
    libfreetype6 \
    fonts-freefont-ttf \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application files
COPY main.py .
COPY game.py .
COPY front.py .
COPY config.py .

# Set the entry point
CMD ["python", "main.py"]

# Metadata
LABEL maintainer="Alexsandr"
LABEL description="Galactic Connect 4 - Space-themed Connect 4 game with AI opponent"
LABEL version="1.0"
