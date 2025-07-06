# Usa una imagen base de Python ligera
FROM python:3.9-slim-buster

# Establece el directorio de trabajo dentro del contenedor
WORKDIR /app

# Copia los archivos de requerimientos e instala las dependencias
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt --break-system-packages

# Copia el código de tu aplicación
COPY app.py .

# ¡CAMBIO CLAVE AQUÍ! Usa ENTRYPOINT para el intérprete y CMD para los argumentos
ENTRYPOINT ["python"] # El intérprete de Python
CMD ["/app/app.py"]   # Los argumentos para el intérprete (la ruta absoluta de tu script)