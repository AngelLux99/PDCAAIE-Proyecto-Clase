# Descargar imagen oficial de python
FROM python:3.9.6

# Ingresamos a un entorno de trabajo
WORKDIR /usr/src/app

# Seteamos variables de entorno obligatorio para python
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Actualizar comando pip
RUN pip install --upgrade pip

# Copiar el archivo requirements a nuestro entorno de trabajo
COPY ./requirements.txt /usr/src/app

# Instalamos dependencias
RUN pip install -r requirements.txt

# Hacer migraciones de nuestros modelos a postgres
CMD ["python", "manage.py", "makemigrations", "usuario"]
CMD ["python", "manage.py", "migrate", "usuario"]

# Copiamos el proyecto actual hacia nuestro entorno de trabajo
COPY . /usr/src/app

# Exponemos el puerto 8000
EXPOSE 8000

# Ejecución de la aplicación
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]