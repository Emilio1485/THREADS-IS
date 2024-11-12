from django.urls import path
from .views import *


urlpatterns = [
    #path('', views.inicioAdmin, name = 'inicioAdmin'),
    path('agregar_producto/', agregarProductoVista, name='agregar_producto'),
]


