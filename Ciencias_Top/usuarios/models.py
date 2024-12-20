# models.py

from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.conf import settings
from django.utils.crypto import get_random_string
import string
import re
from django.utils.timezone import now



class SuperUsuarioManager(BaseUserManager):
    def create_superuser(self, numero_cuenta, password=None, **extra_fields):
        """
        Crea y devuelve un superusuario con el número de cuenta y contraseña dados.
        """
        if not numero_cuenta:
            raise ValueError('El número de cuenta debe ser establecido')
        superuser = self.model(numero_cuenta=numero_cuenta, **extra_fields)
        superuser.set_password(password)  # Configura la contraseña
        superuser.is_staff = True
        superuser.is_superuser = True
        superuser.save(using=self._db)
        return superuser
    
    
class SuperUsuario(AbstractUser):
    """
    Modelo de usuario personalizado extendiendo el usuario estándar de Django.
    Utiliza los campos estándar de Django, como username, password, email.
    """
    # Definir el administrador de objetos para el modelo
    objects = SuperUsuarioManager()
    
    
     # Evitar conflictos en las relaciones inversas
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='superusuario_groups', 
        blank=True
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='superusuario_permissions',  
        blank=True
    )
    # Lista de opciones de roles
    ROLES = [
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
        ('academico', 'Acádemico Ciencias'),
    ]
    
    # Opciones para tipo de usuario
    TIPO_USUARIO = [
        ('estudiante', 'Estudiante'),
        ('trabajador', 'Trabajador'),
    ]

    # Atributos adicionales para el modelo de usuario
    numero_cuenta = models.CharField(max_length=12, unique=True, primary_key=True, verbose_name='Número de cuenta')
    contrasenia_temp = models.CharField(max_length=128, blank=True, null=True)
    nombre = models.CharField(max_length=50, verbose_name='Nombre(s)')
    apellido_paterno = models.CharField(max_length=50, verbose_name='Apellido paterno')
    apellido_materno = models.CharField(max_length=50, blank=True, null=True, verbose_name='Apellido materno')
    celular = models.CharField(max_length=10, verbose_name='Número de celular')
    correo = models.EmailField(unique=True, default='ejemplo@unam.mx') 
    carrera = models.CharField(max_length=100, choices=CARRERAS, verbose_name='Carrera')
    rol = models.CharField(max_length=20, choices=ROLES, verbose_name='Rol')
    tipo_usuario = models.CharField(max_length=20, choices=TIPO_USUARIO, verbose_name='Tipo de usuario')
    
    
    
    # Definir el número de cuenta como el campo principal para autenticación
    USERNAME_FIELD = 'numero_cuenta'
    REQUIRED_FIELDS = ['nombre', 'apellido_paterno', 'correo', 'rol']
    
    
    def save(self, *args, **kwargs):
        """
        Guarda el usuario en la base de datos.
        """
        if not self.pk:
            self.username = self.numero_cuenta # Establecer el nombre de usuario como el número de cuenta
        super().save(*args, **kwargs)
        
    def generar_contraseña(self):
        """
        Genera una contraseña segura para el usuario.
        """
        caracteres = string.ascii_letters + string.digits + '!@#$%^&*()'
        while True:
            contraseña = get_random_string(12, caracteres)
            # Validar que la contraseña tenga al menos una mayúscula, una minúscula, un número y un carácter especial
            if (re.search(r'[A-Z]', contraseña) and
                    re.search(r'[a-z]', contraseña) and
                    re.search(r'[0-9]', contraseña) and
                    re.search(r'[!@#$%^&*()]', contraseña)):
                return contraseña

    def __str__(self):
        return f'{self.numero_cuenta} -> {self.rol}'

    
    class Meta:
        permissions = [
            ("ver_productos", "Puede ver productos"),
            ("agregar_producto", "Puede agregar productos"),
            ("editar_producto", "Puede editar productos"),
            ("eliminar_producto", "Puede eliminar productos"),
            ("agregar_usuario", "Puede añadir usuarios"),
            ("editar_usuario", "Puede editar usuarios"),
            ("eliminar_usuario", "Puede eliminar usuarios"),
            ("ver_usuarios", "Puede ver usuarios"),
            ("sumar_pumapuntos", "Puede sumar puma puntos"),
            ("rentar_producto", "Puede rentar productos"),
            
        ] 
        
    


class Usuario(models.Model):
    """
    Modelo de perfil para los usuarios normales, que incluye los pumapuntos.
    Cada usuario tendrá un perfil único asociado.
    """
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    pumapuntos = models.IntegerField(default=0)
    fecha_ultimo_reinicio = models.DateField(default=now)
    
    def reiniciar_pumapuntos(self):
        self.pumapuntos = 0
        self.fecha_ultimo_reinicio = now()
        self.save()

    def __str__(self):

        return f'Perfil de {self.user.username} - Puma Puntos: {self.pumapuntos}'


