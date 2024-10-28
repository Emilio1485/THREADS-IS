from django.contrib import admin

from .models import SuperUsuario, Usuario 

#@admin.register(Usuario)
class UsuarioAdmin(admin.ModelAdmin):
    list_display = ('numero_cuenta', 'contrasenia_temp','nombre', 'apellido_paterno', 'apellido_materno', 'celular', 'correo', 'carrera', 'rol', 'is_active')
    list_filter = ('carrera', 'rol')
    search_fields = ('numero_cuenta', 'nombre', 'apellido_paterno', 'apellido_materno', 'correo', 'celular')

# Solo registrar una vez
admin.site.register(SuperUsuario, UsuarioAdmin)