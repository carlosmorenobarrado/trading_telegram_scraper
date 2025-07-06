# Usa una imagen base de Python ligera
FROM python:3.9-slim-buster

# Establece el directorio de trabajo dentro del contenedor
WORKDIR /app

# Copia TODA la carpeta 'telegram_scraper' (que está en la raíz de tu CONTEXTO)
# a un directorio temporal dentro del contenedor
# Con text: telegram_scraper/ en GH Actions, esto copia el contenido de telegram_scraper/ a /temp_source
COPY . /temp_source/ 

# Mueve el contenido de la carpeta temporal a tu WORKDIR /app
RUN mv /temp_source/* /app/ && rm -rf /temp_source

# Instala las dependencias desde el archivo en /app
RUN pip install --no-cache-dir -r requirements.txt --break-system-packages

# Define el punto de entrada y el comando para ejecutar tu script
ENTRYPOINT ["python3"]   
CMD ["/app/app.py"]