from pyexpat.errors import messages
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from django.shortcuts import render, redirect

import logging

logger = logging.getLogger(__name__)

def login_view(request):
    if request.method == 'POST':
        numero_cuenta = request.POST.get('numero_cuenta')
        password = request.POST.get('password')

        logger.debug(f'Intentando autenticar: {numero_cuenta}')  # Añade esto para depuración

        user = authenticate(request, username=numero_cuenta, password=password)

        if user is not None:
            logger.debug(f'Usuario autenticado: {user}')  # Usuario autenticado
            login(request, user)
            logger.debug('Redirigiendo a la página de inicio')  # Mensaje de depuración de redirección
            return redirect('inicio')  # Redirigir a la página de inicio
        else:
            error_message = "Número de cuenta o contraseña incorrectos."
            logger.debug('Autenticación fallida')  # Mensaje en caso de fallo
            return render(request, 'login.html', {'error_message': error_message})

    return render(request, 'login.html')



@login_required  # Esto requiere que el usuario esté autenticado para acceder a esta vista
def inicio_view(request):
    return render(request, 'inicioV/inicio.html', {'titulo': 'Inicio', 'user': request.user})




def logout_view(request):
    logout(request)
    return redirect('login')  # Redirigir a la página de inicio de sesión


