from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.contrib import messages
from django.db.models import Q

from .forms import ProductoForm
from .models import Producto 

#import productos

# Create your views here.

def inicioAdmin(request):
    print("Llamando a inicioAdmin")
    return render(request, 'inicioV\inicioAdmin.html',{'titulo':'Inicio Administrador'}) 

def inicio(request):
    print("Llamando a inicio")
    return render(request, 'inicioV\inicio.html',{'titulo':'Inicio'})

def buscar_productos(request):
    query = request.GET.get('query', '')
    productos = Producto.objects.filter(Q(nombre__icontains=query) | Q(codigo__icontains=query))  # Filtra por nombre del producto
    return render(request, 'inicioV/inicio.html', {
        'titulo': 'Resultados de la búsqueda',
        'productos': productos,
        'query': query
    })

@login_required
def agregarProductoVista(request):
    if request.method == 'POST':
        form = ProductoForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                producto = form.save(commit=False)
                producto.propietario = request.user
                
                if 'imagen' in request.FILES:
                    producto.imagen = request.FILES['imagen']
                else:
                    messages.error(request, 'Se requiere una imagen para el producto.')
                    return render(request, 'inicioV/AnadirProducto.html', {
                        'titulo': 'Agregar Producto',
                        'form': ProductoForm()
                    })
                
                producto.save()
                messages.success(request, 'Producto agregado exitosamente.')
                return redirect('inicio')
            except Exception as e:
                messages.error(request, f'Error al crear el producto: {str(e)}')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'Error en {field}: {error}')
            
            form = ProductoForm()
    else:
        form = ProductoForm()

    return render(request, 'inicioV/AnadirProducto.html', {
        'titulo': 'Agregar Producto',
        'form': form
    })


def eliminar_producto(request, codigo):
    producto = get_object_or_404(Producto, codigo=codigo)
    
    if request.method == "POST":
        if request.user.has_perm('usuarios.eliminar_producto'):
            producto.delete()
            messages.success(request, f'Producto "{producto.nombre}" eliminado con éxito.')
        else:
            messages.error(request, "No tienes permiso para eliminar este producto.")
    
    return redirect('inicio')  # Cambia esto al nombre de la vista que muestra la lista de productos
