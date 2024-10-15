from django.urls import path
from . import views

urlpatterns = [
    path('inicioAdmin', views.inicioAdmin, name = 'inicioAdmin')
]
