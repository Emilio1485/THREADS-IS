from django.urls import path
from .views import *

urlpatterns = [
    path('', inicar_sesion_vista, name='iniciar_sesion'),
    path('cerrar_sesion/', cerrar_sesion_vista, name='cerrar_sesion'),
    
    path('agregar_usuario/', agregar_usuario_vista, name='agregar_usuario'),
    path('usuarios/',usuarios_vista, name='usuarios'),
    ]

