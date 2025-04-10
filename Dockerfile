# Imagen base
FROM python:3.10-slim

# Evita problemas de input
ENV DEBIAN_FRONTEND=noninteractive

# Instala dependencias del sistema
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
    libavcodec-dev \
    libavformat-dev \
    libswscale-dev \
    libv4l-dev \
    libx264-dev \
    ffmpeg \
    git \
    curl \
 && apt-get clean \
 && rm -rf /var/lib/apt/lists/*

# Copia archivos
WORKDIR /app
COPY . .

# Instala librerías Python
RUN pip install --no-cache-dir -r requirements.txt

# Puerto
EXPOSE 8501

# Comando de arranque
CMD ["streamlit", "run", "streamlit_app.py"]
