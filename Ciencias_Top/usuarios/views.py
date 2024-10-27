
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from django.shortcuts import render, redirect
from django.contrib import messages


from productos.models import Producto  




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
    # Obtener permisos de todos los grupos a los que pertenece el usuario
    return render(request, 'inicioV/inicio.html', {
    'titulo': 'Inicio',
    'user': request.user,
    'productos': productos,
})


def logout_view(request):
    logout(request)  # Cerrar sesión del usuario
    messages.success(request, "Has cerrado sesión correctamente.")  # Mensaje de confirmación
    return redirect('login')  # Redirigir a la página de inicio de sesión 
