from django.contrib import messages
from django.shortcuts import render
from django.contrib.auth.decorators import login_required, permission_required

from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from django.shortcuts import render, redirect, get_object_or_404

from django.http import JsonResponse
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
    return render(request, 'inicioV/inicio.html', {
    'titulo': 'Inicio',
    'user': request.user,
    'productos': productos
})
    
@login_required    
def cerrar_sesion_vista(request):
    logout(request)  # Cerrar sesión del usuario
    messages.success(request, "Has cerrado sesión correctamente.")  # Mensaje de confirmación
    return redirect('iniciar_sesion')  # Redirigir a la página de inicio de sesión 



@login_required
@permission_required('usuarios.ver_usuarios', raise_exception=True)
def usuarios_vista(request):
    #  Obtener la consulta de búsqueda
    query = request.GET.get('q', '') # Obtener el valor de la consulta de búsqueda
    mensaje = None
    
    es_busqueda_usuario = request.GET.get('tipo', '') == 'usuario'
    if es_busqueda_usuario:
        if query and not query.isdigit():
            mensaje = "El número de cuenta/trabajador sólo esta compuesto de números."
            usuarios = SuperUsuario.objects.none()
        else:
            usuarios = SuperUsuario.objects.filter(numero_cuenta__contains=query, is_active = True)
            if not usuarios:
                mensaje = f"No se encontró usuario con el número de cuenta/trabajador '{query}'."
    else:
        usuarios = SuperUsuario.objects.filter(is_active = True)
    
    return render(request, 'usuario/ver_usuarios.html', {'usuarios': usuarios, 'query': query, 'mensaje': mensaje, 'es_busqueda_usuario': es_busqueda_usuario})



@login_required
@permission_required('usuarios.eliminar_usuario', raise_exception=True)
def eliminar_usuario_vista(request, numero_cuenta): # inhabilitar usuario
    usuario =  get_object_or_404(SuperUsuario, numero_cuenta=numero_cuenta)
    if usuario == request.user:
        messages.error(request, "No puedes eliminar tu propia cuenta.")
        return redirect('usuarios')
    if usuario.is_active:
        usuario.is_active = False
        usuario.save()
        messages.success(request, f'Usuario {numero_cuenta} ha sido inhabilitado.')
    else:
        messages.warning(request, f'Usuario {numero_cuenta} ya está inhabilitado.')
    return redirect('usuarios')

@login_required
@permission_required('usuarios.agregar_usuario', raise_exception=True)
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

