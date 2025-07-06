# Usa una imagen base de Python ligera
FROM python:3.9-slim-buster

# Establece el directorio de trabajo dentro del contenedor
WORKDIR /app

# Copia los archivos de requerimientos e instala las dependencias
# Se usa --no-cache-dir para ahorrar espacio
# Se usa --break-system-packages para evitar advertencias en Python 3.9+ si no usas un virtualenv
COPY telegram_scraper/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt --break-system-packages

# Copia el código de tu aplicación
COPY telegram_scraper/app.py .

# Comando para ejecutar la aplicación
# Si tu script requiere el archivo .session, necesitarás un PV o manejar la sesión
CMD ["python", "app.py"]