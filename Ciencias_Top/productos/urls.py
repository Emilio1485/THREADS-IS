from django.urls import path
from .views import *


urlpatterns = [
    #path('', views.inicioAdmin, name = 'inicioAdmin'),
    path('inicio/', inicio_vista, name='inicio'),  # Esta es la vista que quieres mostrar después de iniciar sesión
    path('agregar_producto/', agregar_producto_vista, name='agregar_producto'),
    path('eliminar_producto/<str:codigo>/', eliminar_producto, name='eliminar_producto'),
    path('editar_producto/<str:codigo>/', editar_producto, name='editar_producto'),

]


