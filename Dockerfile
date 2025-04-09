# Dockerfile para Chat Gerencial V4 con reconocimiento facial
FROM python:3.9-slim

# Instalación de dependencias del sistema necesarias para dlib y face_recognition
RUN apt-get update && \
    apt-get install -y build-essential cmake \
    libgtk-3-dev libboost-all-dev libssl-dev \
    libx11-dev libatlas-base-dev \
    && rm -rf /var/lib/apt/lists/*

# Crear carpeta de trabajo
WORKDIR /app

# Copiar requirements e instalar dependencias Python
COPY requirements.txt ./
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copiar el resto del código de la app
COPY . .

# Exponer puerto (obligatorio para Streamlit en Render)
EXPOSE 8000

# Comando para ejecutar la app
CMD ["streamlit", "run", "streamlit_app.py", "--server.port=8000", "--server.address=0.0.0.0"]
