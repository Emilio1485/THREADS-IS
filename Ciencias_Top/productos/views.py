from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import HttpResponse
from django.contrib import messages
from django.db.models import Q


from .forms import ProductoForm
from .models import Producto 

#Permisos

def is_admin(user):
    return user.groups.filter(name='Administradores').exists()

def is_prov(user):
    return user.groups.filter(name='Proveedores').exists()

def is_admin_or_prov(user):
    return is_admin(user) or is_prov(user)


# Create your views here.

def inicioAdmin(request):
    print("Llamando a inicioAdmin")
    return render(request, 'inicioV\inicioAdmin.html',{'titulo':'Inicio Administrador'}) 

@login_required
def inicio_vista(request):
    query = request.GET.get('q', '')
    user = request.user

    # Inicializar productos como un queryset vacío
    productos = Producto.objects.none()

    if user.groups.filter(name='Administradores').exists():
        # Si es administrador, mostrar todos los productos
        if query:
            productos = Producto.objects.filter(
                Q(nombre__icontains=query) | Q(codigo__icontains=query)
            )
        else:
            productos = Producto.objects.all()
    elif user.groups.filter(name='Proveedores').exists():
        # Si es proveedor, mostrar solo sus productos
        if query:
            productos = Producto.objects.filter(
                Q(propietario=user) & (Q(nombre__icontains=query) | Q(codigo__icontains=query))
            )
        else:
            productos = Producto.objects.filter(propietario=user)
    else:
        # Para otros tipos de usuarios, mostrar todos los productos
        if query:
            productos = Producto.objects.filter(
                Q(nombre__icontains=query) | Q(codigo__icontains=query)
            )
        else:
            productos = Producto.objects.all()

    # Manejar el caso en que no hay productos
    if not productos.exists():
        messages.warning(request, 'No se encontraron productos que coincidan con tu búsqueda.')

    return render(request, 'inicioV/inicio.html', {
        'titulo': 'Inicio',
        'user': user,
        'productos': productos,
        'query': query
    })

@login_required
@user_passes_test(is_admin_or_prov,login_url='iniciar_sesion')
def agregar_producto_vista(request):
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
                return redirect('agregar_producto')
            except Exception as e:
                messages.error(request, f'Error al crear el producto: {str(e)}')
                return render(request, 'inicioV/AnadirProducto.html', {
                    'titulo': 'Agregar Producto',
                    'form': form
                })
                
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'Error en {field}: {error}')
                    return render(request, 'inicioV/AnadirProducto.html', {
        '               titulo': 'Agregar Producto',
                        'form': form
                    })
            
            form = ProductoForm()
    else:
        form = ProductoForm()

    return render(request, 'inicioV/AnadirProducto.html', {
        'titulo': 'Agregar Producto',
        'form': form
    })


@login_required
def editar_producto(request, codigo):
    print(f"Editando producto con código: {codigo}")
    print("Método de solicitud:", request.method)
    
    producto = get_object_or_404(Producto, codigo=codigo)
    
    if request.method == "POST":
        form = ProductoForm(request.POST, request.FILES, instance=producto)
        
        print("Datos del formulario:", request.POST)
        print("Archivos:", request.FILES)
        
        if form.is_valid():
            try:
                producto = form.save(commit=False)
                
                # Manejar la imagen
                if 'imagen' in request.FILES:
                    producto.imagen = request.FILES['imagen']
                
                producto.save()
                messages.success(request, f'Producto "{producto.nombre}" editado con éxito.')
                print(f"Producto {producto.nombre} editado exitosamente")
            except Exception as e:
                print(f"Error al editar el producto: {str(e)}")
                messages.error(request, f'Error al editar el producto: {str(e)}')
        else:
            print("Errores del formulario:", form.errors)
            # Si el formulario no es válido, mostrar errores
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'Error en {field}: {error}')
    
    return redirect('inicio')


@login_required
def eliminar_producto(request, codigo):
    producto = get_object_or_404(Producto, codigo=codigo)
    
    if request.method == "POST":
        if request.user.has_perm('usuarios.eliminar_producto'):
            producto.delete()
            #messages.success(request, f'Producto "{producto.nombre}" eliminado con éxito.')
        else:
            messages.error(request, "No tienes permiso para eliminar este producto.")
        return redirect('inicio')  # Redirigir a la vista de inicio después de eliminar

    # Si no es un POST, redirigir a la vista de inicio
    return redirect('inicio')