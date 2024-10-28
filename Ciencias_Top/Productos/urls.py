from django.urls import path
from . import views  # Import the views module



urlpatterns = [
    #path('', views.inicioAdmin, name = 'inicioAdmin'),
    path('inicio/', views.inicio_vista, name='inicio'),  # Esta es la vista que quieres mostrar después de iniciar sesión
    
]
