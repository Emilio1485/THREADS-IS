from django.urls import path
from .views import *

urlpatterns = [
    path('', inicar_sesion_vista, name='login'),
    path('logout/', cerrar_sesion_vista, name='logout'),
    path('inicio/', inicio_vista, name='inicio'),  # Esta es la vista que quieres mostrar después de iniciar sesión
    path('agregarUsuario/', agregarUsuarioVista, name='agregarUsuario'),
    path('vistaUsuarios/',usuarios_vista, name='vistaUsuarios'),
    ]

