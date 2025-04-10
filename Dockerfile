FROM python:3.9-slim

# Evita prompts interactivos
ENV DEBIAN_FRONTEND=noninteractive

# Instala dependencias del sistema necesarias para face_recognition y OpenCV
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    cmake \
    libgtk-3-dev \
    libboost-all-dev \
    libopenblas-dev \
    liblapack-dev \
    libx11-dev \
    libjpeg-dev \
    libpng-dev \
    libtbb2 \
    libtbb-dev \
    libavcodec-dev \
    libavformat-dev \
    libswscale-dev \
    libv4l-dev \
    libx264-dev \
    ffmpeg \
    curl \
    git \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Copia todo el contenido del repo al contenedor
COPY . /app
WORKDIR /app

# Instala dependencias Python
RUN pip install --upgrade pip && pip install -r requirements.txt

# Expone puerto usado por Streamlit
EXPOSE 8501

# Comando de arranque
CMD ["streamlit", "run", "streamlit_app.py"]
