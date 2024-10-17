import string
import re
from django.contrib.auth.models import AbstractUser
from django.utils.crypto import get_random_string
from django.db import models

"""

class Usuario(AbstractUser):
    ROLES =[
        ('admin', 'Administrador'),
        ('proveedor', 'Proveedor'),
        ('usuario', 'Usuario'),
    ]
    
    # Lista de opciones de carreras
    CARRERAS = [
        ('actuaria', 'Actuaría'),
        ('biologia', 'Biología'),
        ('computacion', 'Ciencias de la Computación'),
        ('ciencias_de_la_tierra', 'Ciencias de la Tierra'),
        ('fisica', 'Física'),
        ('fisica_biomedica', 'Física Biomédica'),
        ('manejo_zonas_costeras', 'Manejo Sustentable de Zonas Costeras'),
        ('matematicas', 'Matemáticas'),
        ('matematicas_aplicadas', 'Matemáticas Aplicadas'),
    
    ]
    
    def generar_contraseña(self):
        caracteres = string.ascii_letters + string.digits + '!@#$%^&*()'
        while True:
            contraseña = get_random_string(12, caracteres)
            # Validar que la contraseña tenga al menos una mayúscula, una minúscula, un número y un carácter especial
            if (re.search(r'[A-Z]', contraseña) and
                re.search(r'[a-z]', contraseña) and
                re.search(r'[0-9]', contraseña) and
                re.search(r'[!@#$%^&*()]', contraseña)):
                return contraseña
    

    
    nombre  = models.CharField(max_length=100)
    apellido_paterno = models.CharField(max_length=100) 
    apellido_materno = models.CharField(max_length=100, blank=True, null=True)  
    numero_cuenta = models.CharField(max_length=12, unique=True)
    celular = models.CharField(max_length=10)
    correo = models.EmailField(unique=True)
    carrera = models.CharField(max_length=100, choices=CARRERAS)
    rol = models.CharField(max_length=20, choices=ROLES) # Campo para el rol del usuario
    def __str__(self):
        return f'{self.nombre} {self.apellido_paterno} {self.apellido_materno} -> {self.rol}'
        
        
        
"""