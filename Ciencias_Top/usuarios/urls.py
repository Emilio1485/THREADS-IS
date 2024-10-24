from django.urls import path
from .views import inicio_view, login_view, logout_view

urlpatterns = [
    path('', login_view, name='login'),
    path('inicio/', inicio_view, name='inicio'),  # Esta es la vista que quieres mostrar después de iniciar sesión
    ]
