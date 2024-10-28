from django.contrib import messages
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from django.shortcuts import render, redirect


from productos.models import Producto  
from .models import SuperUsuario 
from .forms import UsuarioForm 

import logging



def login_view(request):
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
def inicio_view(request):
    productos = Producto.objects.all()
    return render(request, 'inicioV/inicio.html', {
    'titulo': 'Inicio',
    'user': request.user,
    'productos': productos
})



def logout_view(request):
    logout(request)  # Cerrar sesión del usuario
    messages.success(request, "Has cerrado sesión correctamente.")  # Mensaje de confirmación
    return redirect('login')  # Redirigir a la página de inicio de sesión 

def agregarUsuarioView(request):
    if request.method == 'POST':
        # Crear un diccionario con los datos del formulario
        form_data = {
            'numero_cuenta': request.POST.get('numero_cuenta'),
            'nombre': request.POST.get('nombre'),
            'apellido_paterno': request.POST.get('apellido_paterno'),
            'apellido_materno': request.POST.get('apellido_materno'),
            'celular': request.POST.get('celular'),
            'correo': request.POST.get('correo_institucional'),
            'carrera': request.POST.get('carrera'),
            'rol': request.POST.get('tipo_usuario').lower(),
        }

        form = UsuarioForm(form_data)
        
        if form.is_valid():
            try:
                usuario = form.save(commit=False)
                # Generar contraseña automáticamente
                contraseña = usuario.generar_contraseña()
                usuario.set_password(contraseña)
                usuario.contrasenia_temp = contraseña
                usuario.save()
                
                messages.success(
                    request, 
                    f'Usuario creado exitosamente. Número de cuenta: {usuario.numero_cuenta}, '
                    f'Contraseña: {usuario.contrasenia_temp}'
                )
                
                return redirect('inicio')
                
            except Exception as e:
                messages.error(request, f'Error al crear el usuario: {str(e)}')
        else:
            # Manejo correcto de errores del formulario
            for field, error_list in form.errors.items():
                for error in error_list:
                    messages.error(request, f'Error en {field}: {error}')
    
    # Si es GET o si hubo errores en el POST
    return render(request, 'inicioV/AnadirUsuario.html', {
        'titulo': 'Agregar Usuario'
    })




