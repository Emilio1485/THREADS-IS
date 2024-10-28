from django.urls import path
from . import views

urlpatterns = [
    # Otras rutas
    path('rentas/rentar/<int:producto_id>/', views.rentar_producto, name='rentar_producto'),
]
