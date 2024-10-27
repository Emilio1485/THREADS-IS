from datetime import timedelta
from django.db import models
from django.conf import settings
import uuid

class Renta(models.Model):
    id_renta = models.CharField( max_length=10, primary_key=True, verbose_name='Identificador de renta', editable=False, unique=True)
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='rentas', verbose_name='Usuario')
    producto = models.ForeignKey('productos.Producto', on_delete=models.CASCADE, related_name='rentas', verbose_name='Producto rentado')
    fecha_renta = models.DateTimeField(auto_now_add=True, verbose_name='Fecha de renta')
    fecha_devolucion_estimada = models.DateTimeField(verbose_name='Fecha de devolución estimada', editable=False, null=True ) # la fecha en la que el uyente debe devolver el producto debe devolver el producto
    fecha_devolucion = models.DateTimeField(blank=True, null=True, verbose_name='Fecha de devolución', editable=False) # este atributo registra cuando el usuario deolvio el producto (retardo)
    estado = models.CharField(max_length=20, choices=[('R', 'Rentado'), ('D', 'Devuelto'), ('T', 'Devuelto tarde'), ('P', 'Sin devolve aun')], default='R', verbose_name='Estado de la renta', editable=False)
    pumapuntos_obtenidos = models.PositiveIntegerField(default=0, verbose_name='PumaPuntos obtenidos de esta renta', editable=False)
    
    def save(self, *args, **kwargs):
        if not self.id_renta:
            self.id_renta = self.generar_id()
            self.pumapuntos_obtenidos = self.producto.pumapuntos // 2
        super(Renta, self).save(*args, **kwargs)
        # Asegurarse de que dias_renta sea un valor válido
        
    
    def generar_id(self):
        """
        Genera un identificador único para la renta.
        """
        return f'R-{uuid.uuid4().hex[:5].upper()}'
    
    
    
    def registrar_devolucion(self, fecha_devolucion_real):
        """
        Registra la fecha en la que el producto es devuelto y actualiza el estado.
        """
        self.fecha_devolucion = fecha_devolucion_real
        if self.fecha_devolucion > self.fecha_devolucion_estimada:
            self.estado = 'Tarde'
        else:
            self.estado = 'Devuelto'
        self.save()
    
    def __str__(self):
        return f'{self.id_renta} -> {self.usuario} -> {self.producto}'
    
    
    