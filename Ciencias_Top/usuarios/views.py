from django.contrib import messages
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from django.shortcuts import render, redirect
from django.db.models import Q

from productos.models import Producto  
from .models import SuperUsuario 
from .forms import UsuarioForm 

#import logging



def inicar_sesion_vista(request):
    if request.method == 'POST':
        numero_cuenta = request.POST.get('numero_cuenta')
        password = request.POST.get('password')

        user = authenticate(request, username=numero_cuenta, password=password)

        if user is not None:
            login(request, user)
            return redirect('inicio')  # Redirigir a la página de inicio
        else:
            error_message = "Número de cuenta o contraseña incorrectos."
            return render(request, 'login.html', {'error_message': error_message})

    return render(request, 'login.html')



@login_required  # Esto requiere que el usuario esté autenticado para acceder a esta vista
def inicio_vista(request):
    productos = Producto.objects.all()
    query = request.GET.get('q', '')

    if query:
        productos = productos.filter(Q(nombre__icontains=query) | Q(codigo__icontains=query))
    else:
        productos = Producto.objects.all()

    return render(request, 'inicioV/inicio.html',{
        'titulo':'Inicio',
        'user': request.user,
        'productos': productos,
        'query': query
})

@login_required
def usuarios_vista(request):
    usuarios = SuperUsuario.objects.all()
    return render(request, 'usuario/ver_usuarios.html', {'usuarios': usuarios})

def cerrar_sesion_vista(request):
    logout(request)  # Cerrar sesión del usuario
    messages.success(request, "Has cerrado sesión correctamente.")  # Mensaje de confirmación
    return redirect('iniciar_sesion')  # Redirigir a la página de inicio de sesión 


@login_required
def agregar_usuario_vista(request):
    if request.method == 'POST':
        form = UsuarioForm(request.POST)
        if form.is_valid():
            try:
                usuario = form.save()
                
                messages.success(
                    request, 
                    f'Usuario creado exitosamente.\n Número de cuenta: {usuario.numero_cuenta}, '
                    f'Contraseña: {usuario.contrasenia_temp}'
                )
                
                return redirect('inicio')
                
            except Exception as e:
                messages.error(request, f'Error al crear el usuario: {str(e)}')
        else:
            for field, error_list in form.errors.items():
                for error in error_list:
                    messages.error(request, f'Error en {field}: {error}')
    else:
        form = UsuarioForm()
    
    return render(request, 'inicioV/AnadirUsuario.html', {
        'titulo': 'Agregar Usuario',
        'form': form
    })

