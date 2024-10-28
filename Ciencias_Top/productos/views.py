
from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Producto

from .forms import ProductoForm 

#import productos

# Create your views here.

def inicioAdmin(request):
    print("Llamando a inicioAdmin")
    return render(request, 'inicioV\inicioAdmin.html',{'titulo':'Inicio Administrador'}) 

def inicio(request):
    print("Llamando a inicio")
    return render(request, 'inicioV\inicio.html',{'titulo':'Inicio'})
  
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

def agregarProductoView(request):
    if request.method == 'POST':
        form_data = {
            'nombre': request.POST.get('nombre'),
            'descripcion': request.POST.get('descripcion'),
            'existencia': request.POST.get('existencia'),
            'pumapuntos': request.POST.get('pumapuntos'),
            'dias_renta': request.POST.get('dias_renta'),
            'imagen': request.FILES.get('imagen'),
        }

        form = ProductoForm(form_data, request.FILES)

        if form.is_valid():
            try:
                producto = form.save(commit=False)
                producto.propietario = request.user
                producto.save()
                
                messages.success(
                    request, 
                    f'Producto agregdo exitosamente. Nombre: {producto.nombre}, '
                    f'Puntos: {producto.pumapuntos}'
                )
                
                return redirect('inicio')
                
            except Exception as e:
                messages.error(request, f'Error al crear el producto: {str(e)}')
        else:
            # Manejo correcto de errores del formulario
            for field, error_list in form.errors.items():
                for error in error_list:
                    messages.error(request, f'Error en {field}: {error}')

    return render(request, 'inicioV/AnadirProducto.html',{
        'titulo':'Agregar Producto'
    })

