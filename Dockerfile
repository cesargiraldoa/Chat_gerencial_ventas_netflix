# Imagen base ligera con Python 3.9
FROM python:3.9-slim

# Evitar prompts de configuración
ENV DEBIAN_FRONTEND=noninteractive

# Instalar dependencias del sistema necesarias para face_recognition y OpenCV
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
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

# Instalar dependencias Python desde requirements.txt
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el resto del proyecto
COPY . /app
WORKDIR /app

# Puerto para Streamlit
EXPOSE 8080

# Comando para ejecutar la app
CMD ["streamlit", "run", "streamlit_app.py", "--server.port=8080", "--server.address=0.0.0.0"]
