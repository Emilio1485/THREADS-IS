from django.urls import path
from .views import *


urlpatterns = [
    #path('', views.inicioAdmin, name = 'inicioAdmin'),
    path('agregarProducto/', agregarProductoVista, name='agregarProducto'),
]


