from pyexpat.errors import messages
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
    logout(request)
    return redirect('login')  # Redirigir a la página de inicio de sesión

def agregarUsuarioView(request):

    if request.method == 'POST':
        form = UsuarioForm(request.POST)
        if form.is_valid():
            # Crear una instancia del modelo SuperUsuario
            superusuario = SuperUsuario(
                numero_cuenta=form.cleaned_data['numero_cuenta'],
                nombre=form.cleaned_data['nombre'],
                apellido_paterno=form.cleaned_data['apellido_paterno'],
                apellido_materno=form.cleaned_data['apellido_materno'],
                celular=form.cleaned_data['celular'],
                correo=form.cleaned_data['correo'],
                carrera=form.cleaned_data['carrera'],
                rol=form.cleaned_data['rol'],
                tipo_usuario=form.cleaned_data['tipo_usuario'],
            )

            # Generar y establecer una contraseña segura
            contrasena = superusuario.generar_contraseña()
            superusuario.set_password(contrasena)  # Almacenar la contraseña de forma segura

            # Guardar el superusuario en la base de datos
            superusuario.save()

            messages.success(request, f"Usuario registrado exitosamente. La contraseña generada es: {contrasena}")
            return redirect('inicio')  # Redirigir a la página de inicio o a donde desees
        else:
            messages.error(request, "Error en el registro. Por favor, revisa los datos.")
    else:
        form = UsuarioForm()
    return render(request, 'inicioV/AnadirUsuario.html',{
        'titulo':'Agregar Producto'
})


