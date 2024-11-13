from django.contrib import admin

from .models import SuperUsuario, Usuario


class UsuarioInline(admin.StackedInline): # inline  para mostrar el perfil de usuario en el admin
    model = Usuario
    can_delete = False
    verbose_name_plural = 'Perfil Usuario'
    fk_name = 'user'

#@admin.register(Usuario)
class SuperUsuarioAdmin(admin.ModelAdmin):
    list_display = ('numero_cuenta', 'contrasenia_temp','nombre', 'apellido_paterno', 'apellido_materno', 'celular', 'correo', 'carrera', 'rol', 'is_active')
    list_filter = ('carrera', 'rol')
    search_fields = ('numero_cuenta', 'nombre', 'apellido_paterno', 'apellido_materno', 'correo', 'celular')
    
    
    inlines = [UsuarioInline]
    
    def get_queryset(self, request):
        queryset = super().get_queryset(request) 
        queryset =  queryset.prefetch_related('usuario') # prefetch_related para evitar el problema de n+1
        return queryset
    
    def pumapuntos(self, obj):
        return obj.usuario.pumapuntos if hasattr(obj, 'usuario') else 'N/A'
    
    pumapuntos.short_description = 'Pumapuntos'


class UsuarioAdmin(admin.ModelAdmin):
    list_display = ('user', 'pumapuntos')
    search_fields = ('user__numero_cuenta',)



# Registrar los modelos en el admin
admin.site.register(SuperUsuario, SuperUsuarioAdmin)
admin.site.register(Usuario, UsuarioAdmin)