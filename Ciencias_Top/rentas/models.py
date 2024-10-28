from datetime import datetime, timedelta
from django.db import models
from django.conf import settings
import uuid

class Renta(models.Model):
    id_renta = models.CharField( max_length=10, primary_key=True, verbose_name='Identificador de renta', editable=False, unique=True)
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='rentas', verbose_name='Usuario')
    producto = models.ForeignKey('productos.producto', on_delete=models.CASCADE, related_name='rentas', verbose_name='Producto rentado')
    fecha_renta = models.DateTimeField(auto_now_add=True, verbose_name='Fecha de renta')
    fecha_devolucion_estimada = models.DateTimeField(verbose_name='Fecha de devolución estimada', editable=False, null=True ) # la fecha en la que el uyente debe devolver el producto debe devolver el producto
    fecha_devolucion = models.DateTimeField(blank=True, null=True, verbose_name='Fecha de devolución', editable=False) # este atributo registra cuando el usuario deolvio el producto (retardo)
    estado = models.CharField(max_length=20, choices=[('R', 'Rentado'), ('D', 'Devuelto'), ('T', 'Devuelto tarde'), ('P', 'Sin devolve aun')], default='R', verbose_name='Estado de la renta', editable=False)
    pumapuntos_obtenidos = models.PositiveIntegerField(default=0, verbose_name='PumaPuntos obtenidos de esta renta', editable=False)
    
    
    def puede_rentar(self):
        """Verifica si el usuario cumple con los requisitos para rentar."""
        # Verificar si el usuario tiene suficientes Puma Puntos
        if self.usuario.pumapuntos < self.producto.pumapuntos_requeridos:
            return False, "No tienes suficientes Puma Puntos."

        # Verificar el límite de 3 rentas diarias
        hoy = datetime.now().date()
        rentas_hoy = Renta.objects.filter(usuario=self.usuario, fecha_renta__date=hoy).count()
        if rentas_hoy >= 3:
            return False, "Ya has rentado el máximo de productos permitido para hoy."
        
        return True, "Puedes rentar este producto."
    
    def rentar(self):
        """Lógica de renta si cumple con los requisitos."""
        puede, mensaje = self.puede_rentar()
        if puede:
            # Descontar puntos del usuario y acumular la mitad del valor de puntos del producto
            self.usuario.pumapuntos -= self.producto.pumapuntos_requeridos
            puntos_acumulados = self.producto.pumapuntos_requeridos // 2
            self.usuario.pumapuntos += puntos_acumulados  # Acumular puntos al usuario
            self.pumapuntos_obtenidos = puntos_acumulados
            self.usuario.save()
            self.save()
            return True, "Renta completada con éxito."
        else:
            return False, mensaje
    
    
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
    
    
    