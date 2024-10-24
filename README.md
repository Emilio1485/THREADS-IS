# THREADS-IS
Repositorio para el equipo 2 THREADS



## Instrucciones para levantar el proyecto

### Prerrequisitos

Tener Docker y Docker Compose instalados.

### Paso 1: Clonar el repositorio

Clona el repositorio desde GitHub y navega al directorio del proyecto:


### Paso 2: Construir y ejecutar los contenedores Docker

Construye y ejecuta los contenedores Docker:

docker-compose up --build


### Paso 3: Migrar la base de datos
En otra terminal, migra la base de datos:

docker-compose exec web python manage.py migrate

### Paso 4: Crear un superusuario (opcional)
Si  se desea crear un superusuario para acceder al panel de administración de Django, ejecuta:


docker-compose exec web python manage.py createsuperuser



### Paso 5: Acceder a la aplicación
Abrir el navegador web y acceder  a la aplicación en
http://localhost:8000.