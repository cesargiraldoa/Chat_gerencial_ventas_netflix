FROM python:3.9-slim

ENV DEBIAN_FRONTEND=noninteractive

# Instalar dependencias necesarias para face_recognition y opencv-python-headless
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    cmake \
    libgtk-3-dev \
    libboost-all-dev \
    libopenblas-dev \
    liblapack-dev \
    libx11-dev \
    libtbb2 \
    libtbb-dev \
    libjpeg-dev \
    libpng-dev \
    libavcodec-dev \
    libavformat-dev \
    libswscale-dev \
    libv4l-dev \
    libx264-dev \
    ffmpeg \
    curl \
    git && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Copiar e instalar dependencias Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar todo el proyecto
COPY . /app
WORKDIR /app

EXPOSE 8080

CMD ["streamlit", "run", "streamlit_app.py", "--server.port=8080", "--server.address=0.0.0.0"]
