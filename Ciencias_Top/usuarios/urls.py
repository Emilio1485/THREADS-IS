from django.urls import path
}
from . import views  # Import the views module

urlpatterns = [
    path('', views.iniciar_sesion_vista, name='iniciar_sesion'),
    path('salir/', views.cerrar_sesion_vista, name='cerrar_sesion'),
    path('usuarios/', views.usuarios_vista, name='ver_usuarios'),
  
    ]

