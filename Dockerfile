FROM python:3.10-slim

# Evitar prompts en instalaciones
ENV DEBIAN_FRONTEND=noninteractive

# Instala dependencias necesarias del sistema
RUN apt-get update && apt-get install -y \
    build-essential \
    cmake \
    libgtk-3-dev \
    libboost-all-dev \
    libopenblas-dev \
    liblapack-dev \
    libx11-dev \
    libjpeg-dev \
    libtbb2 \
    libtbb-dev \
    libpng-dev \
    libavcodec-dev \
    libavformat-dev \
    libswscale-dev \
    libv4l-dev \
    libx264-dev \
    ffmpeg \
    curl \
    git && \
    rm -rf /var/lib/apt/lists/*

# Instalar dlib antes de face_recognition
RUN pip install --no-cache-dir dlib

# Establece directorio de trabajo
WORKDIR /app

# Copia archivos
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Ejecuta la app
CMD ["streamlit", "run", "streamlit_app.py", "--server.port=8080", "--server.address=0.0.0.0"]
