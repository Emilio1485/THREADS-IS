# Usar la imagen de Python
FROM python:3.11

# Establecer el directorio de trabajo
WORKDIR /app

# Copiar los archivos de requisitos
COPY requirements.txt .

# Instalar las dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el resto del código
COPY . .

# Copiar el script de espera
COPY wait-for-it.sh /wait-for-it.sh

# Dar permisos de ejecución al script de espera
RUN chmod +x /wait-for-it.sh

# Exponer el puerto
EXPOSE 8000

# Comando para ejecutar la aplicación
CMD ["/wait-for-it.sh", "db", "5432", "--", "python", "manage.py", "runserver", "0.0.0.0:8000"]