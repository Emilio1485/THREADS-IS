from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.contrib import messages

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
    productos = Producto.objects.filter(nombre__icontains=query)  # Filtra por nombre del producto
    return render(request, 'inicioV/inicio.html', {
        'titulo': 'Resultados de la búsqueda',
        'productos': productos,
        'query': query
    })

@login_required
def agregarProductoView(request):
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
