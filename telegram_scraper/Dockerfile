# Usa una imagen base de Python ligera
FROM python:3.9-slim-buster

# Establece el directorio de trabajo dentro del contenedor
WORKDIR /app

# Copia los archivos de requerimientos e instala las dependencias
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt --break-system-packages

# Copia el código de tu aplicación
COPY app.py .

# ¡CAMBIO CLAVE AQUÍ! Define ENTRYPOINT y CMD en "exec form"
# Esto sobrescribe cualquier ENTRYPOINT preexistente de la imagen base
# El comando final será /usr/local/bin/python /app/app.py
ENTRYPOINT ["/usr/local/bin/python"] # Ruta absoluta al binario de Python
CMD ["/app/app.py"]                   # Ruta absoluta a tu script como argumento