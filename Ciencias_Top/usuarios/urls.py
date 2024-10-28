from django.urls import path
from .views import *

urlpatterns = [
    path('', login_view, name='login'),
    path('inicio/', inicio_view, name='inicio'),  # Esta es la vista que quieres mostrar después de iniciar sesión
    path('agregarUsuario/', agregarUsuarioView, name='agregarUsuario'),
    ]