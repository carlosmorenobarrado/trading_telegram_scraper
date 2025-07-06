# Usa una imagen base de Python ligera
FROM python:3.9-slim-buster

# Establece el directorio de trabajo dentro del contenedor
WORKDIR /app

# Copia los archivos de requerimientos e instala las dependencias
# Las rutas son RELATIVAS al contexto (telegram_scraper/)
COPY requirements.txt . 
RUN pip install --no-cache-dir -r requirements.txt --break-system-packages

# Copia el código de tu aplicación
# Las rutas son RELATIVAS al contexto (telegram_scraper/)
COPY app.py .

# Comando para ejecutar la aplicación
CMD ["python", "app/app.py"]