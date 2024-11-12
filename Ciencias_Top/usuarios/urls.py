from django.urls import path
from .views import *

urlpatterns = [
    path('', inicar_sesion_vista, name='login'),
    path('cerrar_sesion/', cerrar_sesion_vista, name='cerrar_sesion'),
    path('inicio/', inicio_vista, name='inicio'),  # Esta es la vista que quieres mostrar después de iniciar sesión
    path('agregar_usuario/', agregar_usuario_vista, name='agregar_usuario'),
    path('usuarios/',usuarios_vista, name='usuarios'),
    ]

