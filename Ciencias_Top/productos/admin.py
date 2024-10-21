from django.contrib import admin
from .models import Producto

class ProductoAdmin(admin.ModelAdmin):
    list_display = ('codigo', 'nombre', 'existencia', 'pumapuntos', 'dias_renta', 'propietario')
    search_fields = ('nombre', 'codigo')
    list_filter = ('dias_renta', 'propietario')

admin.site.register(Producto, ProductoAdmin)