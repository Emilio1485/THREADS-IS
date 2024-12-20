import unicodedata 

from django.db import models
from django.contrib.auth import get_user_model

from django.utils.crypto import get_random_string
from django.conf import settings



user = get_user_model()

class Producto(models.Model):
    codigo = models.CharField(max_length=12, primary_key=True, verbose_name='Código del producto' , unique=True, editable=False)
    nombre = models.CharField(max_length=100, verbose_name='Nombre del producto', blank=False, null=False)
    descripcion = models.TextField(verbose_name='Descripción del producto', blank=False, null=False)
    existencia = models.PositiveIntegerField(verbose_name='Existencia', blank=False, null=False)
    estado = models.CharField(max_length=1, choices=[('A', 'Disponible'), ('R', 'Rentado'), ('N', 'No disponible')], default='A', verbose_name='Estado del producto')
    pumapuntos = models.PositiveIntegerField(verbose_name='PumaPuntos requeridos', blank=False, null=False)
    dias_renta = models.PositiveIntegerField(verbose_name='Días de renta', blank=False, null=False, choices=[(i, f'{i} días') for i in range(3, 8)]) # Rango de 3 a 7 días
    propietario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='productos', verbose_name='Propietario')
    imagen = models.ImageField(upload_to='productos_imagenes/', verbose_name='Imagen del producto', blank=True, null=True)

    def generar_codigo(self):
        """
        Genera un código único para el producto.
        Utiliza los primeros 4 caracteres del nombre (sin acentos ni caracteres especiales)
        y genera una cadena aleatoria de 8 dígitos.
        """
        # Eliminar acentos y caracteres especiales del nombre del producto
        nombre_limpio = unicodedata.normalize('NFD', self.nombre).encode('ascii', 'ignore').decode('utf-8')

        # Generar los primeros 4 caracteres a partir del nombre limpio en mayúsculas
        letras = (nombre_limpio[:4].upper() + 'XXXX')[:4]

        # Generar una cadena aleatoria de 8 dígitos
        numeros = get_random_string(length=8, allowed_chars='0123456789')

        return f'{letras}{numeros}'
    
    def actualizar_estado(self):
        if self.existencia <= 0:
            self.estado = 'N'
        else:
            self.estado = 'A'
        self.save()

    def save(self, *args, **kwargs):
        self.actualizar_estado()
        super().save(*args, **kwargs)

    
    def save(self, *args, **kwargs):
        # Generar el código solo si es un producto nuevo y no tiene un código asignado
        if not self.codigo:
            self.codigo = self.generar_codigo()
        super(Producto, self).save(*args, **kwargs)
        
    def __str__(self):
        return f'{self.codigo} -> {self.nombre}'
    
    class Meta:
        ordering = ['nombre']
        verbose_name = 'Producto'
        verbose_name_plural = 'Productos'