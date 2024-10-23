from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

def inicioAdmin(request):
    print("Llamando a inicioAdmin")
    return render(request, 'inicioV\inicioAdmin.html',{'titulo':'Inicio Administrador'}) 

def inicio(request):
    print("Llamando a inicio")
    return render(request, 'inicioV\inicio.html',{'titulo':'Inicio'})
