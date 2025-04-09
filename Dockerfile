# Usa una imagen base completa que incluye herramientas necesarias
FROM python:3.10

# Establece entorno no interactivo para evitar bloqueos en instalaciones
ENV DEBIAN_FRONTEND=noninteractive

# Actualiza e instala librerías necesarias para face_recognition
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

# Directorio de trabajo
WORKDIR /app

# Copia archivos del proyecto
COPY . /app

# Instala dependencias de Python
RUN pip install --upgrade pip && pip install -r requirements.txt

# Expone puerto para Streamlit
EXPOSE 8501

# Comando para ejecutar Streamlit
CMD ["streamlit", "run", "streamlit_app.py", "--server.port=8501", "--server.enableCORS=false"]
