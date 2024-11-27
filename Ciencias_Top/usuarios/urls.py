from django.urls import path
from .views import *

urlpatterns = [
    path('', inicar_sesion_vista, name='iniciar_sesion'),
    path('cerrar_sesion/', cerrar_sesion_vista, name='cerrar_sesion'),
    path('inicio/', inicio_vista, name='inicio'),  # Esta es la vista que quieres mostrar después de iniciar sesión
    path('agregar_usuario/', agregar_usuario_vista, name='agregar_usuario'),
    path('usuarios/',usuarios_vista, name='usuarios'),
    path('eliminar_usuario/<str:numero_cuenta>/', eliminar_usuario_vista, name='eliminar_usuario'),
    path('detalles_usuario/<str:numero_cuenta>/', vista_detallada_usuario, name='vista_detallada_usuario'),  
    path('editar_usuario/<str:numero_cuenta>/', editar_usuario_vista, name='editar_usuario'),
    path('generar_contrasena/<str:numero_cuenta>/', generar_contrasena_vista, name='generar_contrasena_vista'),
    path('perfil/', ver_perfil, name='ver_perfil'),
    ]

