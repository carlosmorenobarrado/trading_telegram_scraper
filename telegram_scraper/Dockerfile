# Usa una imagen base de Python ligera
FROM python:3.9-slim-buster

# Establece el directorio de trabajo dentro del contenedor
WORKDIR /app

# Copia los archivos de requerimientos e instala las dependencias
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt --break-system-packages

# Copia el código de tu aplicación
COPY app.py .

# --- ¡CAMBIO CLAVE AQUÍ! ---
# ENTRYPOINT es el binario de Python. Lo ejecutamos en formato "exec" para que sea el proceso principal.
ENTRYPOINT ["python3"] 

# CMD son los argumentos que se le pasan al ENTRYPOINT.
# Aquí, le pasamos la ruta ABSOLUTA de tu script.
CMD ["/app/app.py"]