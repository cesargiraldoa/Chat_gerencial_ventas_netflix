# Usa una imagen base oficial de Python
FROM python:3.11-slim

# Evita que Python genere archivos pyc
ENV PYTHONDONTWRITEBYTECODE=1
# Asegura que se muestren los logs
ENV PYTHONUNBUFFERED=1

# Instala dependencias necesarias del sistema para face_recognition
RUN apt-get update && apt-get install -y \
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
    git \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Crea directorio de trabajo
WORKDIR /app

# Copia los archivos del proyecto al contenedor
COPY . .

# Instala las dependencias de Python
RUN pip install --no-cache-dir -r requirements.txt

# Expone el puerto que Streamlit usará
EXPOSE 8501

# Comando para ejecutar la app
CMD ["streamlit", "run", "streamlit_app.py", "--server.port=8501", "--server.enableCORS=false"]
