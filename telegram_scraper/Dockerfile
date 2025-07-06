# Usa una imagen base de Python ligera
FROM python:3.9-slim-buster

# Establece el directorio de trabajo dentro del contenedor
WORKDIR /app

# Copia los archivos de requerimientos e instala las dependencias
# ¡CAMBIO CLAVE AQUÍ! Usa la ruta completa desde la raíz del contexto de construcción
COPY telegram_scraper/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt --break-system-packages

# Copia el código de tu aplicación
# ¡CAMBIO CLAVE AQUÍ! Usa la ruta completa desde la raíz del contexto de construcción
COPY telegram_scraper/app.py . 

# Comando para ejecutar la aplicación
# Usa la ruta absoluta, es más seguro.
CMD ["python3", "/app/app.py"]