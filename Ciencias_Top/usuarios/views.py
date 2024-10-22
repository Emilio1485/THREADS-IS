from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login
from django.contrib import messages
from .models import SuperUsuario

def login(request):
    if request.method == 'POST':
        numero_cuenta = request.POST.get('numero_cuenta')
        password = request.POST.get('password')
        
        try:
            # Intentamos autenticar usando el modelo SuperUsuario
            user = authenticate(username=numero_cuenta, password=password)
            
            if user is not None:
                auth_login(request, user)
                # Redirigir según el rol del usuario
                if user.rol == 'admin':
                    return redirect('inicioAdmin')
                elif user.rol == 'proveedor':
                    return redirect('inicioProveedor')
                else:
                    return redirect('inicioUsuario')
            else:
                messages.error(request, 'Número de cuenta o contraseña incorrectos')
        except SuperUsuario.DoesNotExist:
            messages.error(request, 'Usuario no encontrado')
        except Exception as e:
            messages.error(request, 'Error en el inicio de sesión')
            
    return render(request, 'login.html')