from django.shortcuts import render,redirect
from django.http import HttpResponse
from pyexpat.errors import messages

#import productos

# Create your views here.

def inicioAdmin(request):
    print("Llamando a inicioAdmin")
    return render(request, 'inicioV\inicioAdmin.html',{'titulo':'Inicio Administrador'}) 

def inicio(request):
    print("Llamando a inicio")
    return render(request, 'inicioV\inicio.html',{'titulo':'Inicio'})

def agregarProductoView(request):
    return render(request, 'inicioV/AnadirProducto.html',{'titulo':'Agregar Producto'})
