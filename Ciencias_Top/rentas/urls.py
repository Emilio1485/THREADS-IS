from django.urls import path
from . import views

app_name = 'rentas'

urlpatterns = [
    path('rentar/', views.rentar_producto_vista, name='rentar_producto_vista'),
    path('renta/<str:producto_codigo>/', views.renta_producto, name='renta_producto'),
    path('lista/', views.lista_rentas, name='lista_rentas'),
    path('devolver/<str:renta_id>/', views.devolver_producto, name='devolver_producto'),
    path('historial/<int:usuario_id>/', views.historial_rentas_usuario, name='historial_rentas_usuario'),
]