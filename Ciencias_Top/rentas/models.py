from datetime import datetime, timedelta , timezone
from django.db import models
from django.conf import settings
import uuid

class Renta(models.Model):
    id_renta = models.CharField(max_length=10, primary_key=True, verbose_name='Identificador de renta', editable=False, unique=True)
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='rentas', verbose_name='Usuario')
    producto = models.ForeignKey('productos.Producto', on_delete=models.CASCADE, related_name='rentas', verbose_name='Producto rentado')
    fecha_renta = models.DateTimeField(auto_now_add=True, verbose_name='Fecha de renta')
    fecha_devolucion_estimada = models.DateTimeField(verbose_name='Fecha de devolución estimada', editable=False, null=True)
    fecha_devolucion = models.DateTimeField(blank=True, null=True, verbose_name='Fecha de devolución', editable=False)
    estado = models.CharField(max_length=20, choices=[('R', 'Rentado'), ('D', 'Devuelto'), ('T', 'Devuelto tarde'), ('P', 'Sin devolución aún')], default='R', verbose_name='Estado de la renta', editable=False)
    pumapuntos_obtenidos = models.PositiveIntegerField(default=0, verbose_name='PumaPuntos obtenidos de esta renta', editable=False)

    def puede_rentar(self):
        """Verifica si el usuario cumple con los requisitos para rentar."""
        # Verificar si el usuario tiene suficientes Puma Puntos
        if self.usuario.usuario.pumapuntos < self.producto.pumapuntos:
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
            self.usuario.usuario.pumapuntos -= self.producto.pumapuntos
            puntos_acumulados = self.producto.pumapuntos // 2
            self.usuario.usuario.pumapuntos += puntos_acumulados  # Acumular puntos al usuario
            self.pumapuntos_obtenidos = puntos_acumulados
            self.usuario.usuario.save()
            self.estado = 'R'  # Estado 'Rentado' al momento de rentar
            self.save()
            return True, "Renta completada con éxito."
        else:
            return False, mensaje

    def save(self, *args, **kwargs):
        if not self.id_renta:
            self.id_renta = self.generar_id()
            # Establecer fecha de devolución estimada según los días de renta
            self.fecha_devolucion_estimada = self.fecha_renta + timedelta(days=self.producto.dias_renta)
            self.pumapuntos_obtenidos = self.producto.pumapuntos // 2
        super(Renta, self).save(*args, **kwargs)

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

        # Asegurarse de que ambos objetos datetime sean del mismo tipo
        if self.fecha_devolucion.tzinfo is None:
            self.fecha_devolucion = self.fecha_devolucion.replace(tzinfo=timezone.utc)
        if self.fecha_devolucion_estimada.tzinfo is None:
            self.fecha_devolucion_estimada = self.fecha_devolucion_estimada.replace(tzinfo=timezone.utc)

        # Si la devolución es después de la fecha estimada, se marca como "Devuelto tarde"
        if self.fecha_devolucion > self.fecha_devolucion_estimada:
            self.estado = 'T'  # Devuelto tarde
            # Penalizar al usuario restando 20 Puma Puntos
            self.usuario.usuario.pumapuntos -= 20
        else:
            self.estado = 'D'  # Devuelto a tiempo

        self.usuario.usuario.save()
        self.save()
        
    def _str_(self):
        return f'{self.id_renta} -> {self.usuario} -> {self.producto}'