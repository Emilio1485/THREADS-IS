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


### Ejecutar Comandos de Django
Para trabajar se necesitan 2 consolas: en una estará corriendo Docker y en la otra se ejecutarán los comandos de Django utilizando docker-compose exec.

- docker-compose exec web python manage.py makemigrations
- docker-compose exec web python manage.py migrate
- docker-compose exec web python manage.py shell
- docker-compose exec web python manage.py loaddata data.json
- docker-compose exec web python manage.py tu_comando_personalizado
- docker-compose exec web python manage.py runserver 0.0.0.0:8000


**Detener y eliminar los contenedores actuales:**

   
   docker-compose down
