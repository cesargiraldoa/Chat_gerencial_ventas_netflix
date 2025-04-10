FROM debian:bullseye

# Evita prompts interactivos
ENV DEBIAN_FRONTEND=noninteractive

# Instala Python manualmente + librerías del sistema necesarias
RUN apt-get update && apt-get install -y --no-install-recommends \
    python3.9 python3-pip python3.9-dev python3.9-venv \
    build-essential cmake libgtk-3-dev libboost-all-dev \
    libopenblas-dev liblapack-dev libx11-dev libjpeg-dev libpng-dev \
    libtbb2 libtbb-dev libavcodec-dev libavformat-dev libswscale-dev \
    libv4l-dev libx264-dev ffmpeg curl git \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Usar python3.9 como predeterminado
RUN ln -s /usr/bin/python3.9 /usr/bin/python && ln -s /usr/bin/pip3 /usr/bin/pip

# Crear carpeta de trabajo
WORKDIR /app

# Copiar archivos al contenedor
COPY . .

# Instalar dependencias Python
RUN pip install --upgrade pip && pip install -r requirements.txt

# Puerto para Streamlit
EXPOSE 8501

# Comando de arranque
CMD ["streamlit", "run", "streamlit_app.py"]
