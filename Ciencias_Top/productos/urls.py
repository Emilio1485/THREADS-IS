from django.urls import path
from .views import *


urlpatterns = [
    #path('', views.inicioAdmin, name = 'inicioAdmin'),
    path('agregar_producto/', agregarProductoVista, name='agregar_producto'),
    path('eliminar_producto/<str:codigo>/', eliminar_producto, name='eliminar_producto'),
    path('buscar_productos/', buscar_productos, name='buscar_productos'),
]


