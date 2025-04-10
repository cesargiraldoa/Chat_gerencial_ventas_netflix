FROM python:3.10-slim

# Evitar interacciones en la instalación
ENV DEBIAN_FRONTEND=noninteractive

# Actualiza y corrige paquetes del sistema
RUN apt-get update --fix-missing && apt-get install -y \
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
    curl && \
    rm -rf /var/lib/apt/lists/* && \
    apt-get clean

# Establece el directorio de trabajo
WORKDIR /app

# Copia requirements e instala
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copia el resto de archivos
COPY . .

# Comando por defecto para ejecutar la app
CMD ["streamlit", "run", "streamlit_app.py", "--server.port=8080", "--server.address=0.0.0.0"]
