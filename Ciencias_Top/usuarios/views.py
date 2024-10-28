
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from django.shortcuts import render, redirect
from django.contrib import messages


from productos.models import Producto  
from usuarios.models import SuperUsuario




def iniciar_sesion_vista(request):
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





@login_required
def usuarios_vista(request):
    usuarios = SuperUsuario.objects.all()
    return render(request, 'usuarios/ver_usuarios.html', {'usuarios': usuarios})

@login_required
def cerrar_sesion_vista(request):
    logout(request)  # Cerrar sesión del usuario
    messages.success(request, "Has cerrado sesión correctamente.")  # Mensaje de confirmación
    return redirect('iniciar_sesion')  # Redirigir a la página de inicio de sesión 
