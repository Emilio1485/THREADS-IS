from django.contrib import admin
from .models import Renta

@admin.register(Renta)
class RentaAdmin(admin.ModelAdmin):
    list_display = ('id_renta', 'usuario', 'producto', 'fecha_renta', 'fecha_devolucion_estimada', 'fecha_devolucion', 'estado', 'pumapuntos_obtenidos')
    list_filter = ('estado', 'fecha_renta', 'fecha_devolucion')
    search_fields = ('id_renta', 'numero_cuenta', 'codigo')