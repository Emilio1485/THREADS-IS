from django.shortcuts import render
from django.http import HttpResponse
from .models import Producto
from django.contrib.auth.decorators import login_required

# Create your views here.

@login_required  # Esto requiere que el usuario esté autenticado para acceder a esta vista
def inicio_vista(request):
    #buscar
    query = request.GET.get('q') # Obtener la consulta de búsqueda
    if query:
        productos = Producto.objects.filter(nombre__icontains=query )  | Producto.objects.filter(codigo__icontains=query) # Filtrar los productos que contienen la consulta de búsqueda
    else:
        productos = Producto.objects.all()
    return render(request, 'inicioV/inicio.html', {
    'titulo': 'Inicio',
    'user': request.user,
    'productos': productos,
    'query':query
})
