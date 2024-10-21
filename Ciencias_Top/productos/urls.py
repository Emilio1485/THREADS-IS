from django.urls import path
from . import views

urlpatterns = [
    path('', views.inicioAdmin, name = 'inicioAdmin')
]
