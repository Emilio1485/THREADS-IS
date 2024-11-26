from django.contrib import messages
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test , permission_required

from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from django.shortcuts import render, redirect
from django.db.models import Q

from datetime import datetime
from rentas.models import Renta

from productos.models import Producto  
from .models import SuperUsuario , Usuario
from .forms import UsuarioForm 
from django.db.models import Sum
#import logging

#Permisos

def is_admin(user):
    return user.groups.filter(name='Administradores').exists()

def is_prov(user):
    return user.groups.filter(name='Proveedores').exists()

def is_admin_or_prov(user):
    return is_admin(user) or is_prov(user)


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

    if request.user.is_authenticated:
        return redirect('inicio')
    
    return render(request, 'login.html')





@login_required
@user_passes_test(is_admin,login_url='iniciar_sesion')
def usuarios_vista(request):
    usuarios = SuperUsuario.objects.all()
    return render(request, 'usuario/ver_usuarios.html', {'usuarios': usuarios})

def cerrar_sesion_vista(request):
    logout(request)  # Cerrar sesión del usuario
    #messages.success(request, "Has cerrado sesión correctamente.")  # Mensaje de confirmación
    return redirect('iniciar_sesion')  # Redirigir a la página de inicio de sesión 


@login_required
@user_passes_test(is_admin,login_url='iniciar_sesion')
def agregar_usuario_vista(request):
    if request.method == 'POST':
        form = UsuarioForm(request.POST)
        if form.is_valid():
            try:
                usuario = form.save()
                
                messages.success(
                    request, 
                    f'Usuario creado exitosamente.'
                    f'\n Número de cuenta: {usuario.numero_cuenta}, '
                    f'Contraseña: {usuario.contrasenia_temp}'
                )
                
                return render(request, 'inicioV/AnadirUsuario.html', {
                    'titulo': 'Agregar Usuario',
                    'form': form
                })
                
            except Exception as e:
                messages.error(request, f'Error al crear el usuario: {str(e)}')
        else:
            for field, error_list in form.errors.items():
                for error in error_list:
                    messages.error(request, f'Error en {field}: {error} <br>')
    else:
        form = UsuarioForm()
    
    return render(request, 'inicioV/AnadirUsuario.html', {
        'titulo': 'Agregar Usuario',
        'form': form
    })

@login_required
def ver_perfil(request):
    usuario = request.user
    perfil, created = Usuario.objects.get_or_create(user=usuario)  # Obtener o crear el perfil del usuario

    # Inicializar variables para el historial de rentas
    rentas_rentadas = []
    rentas_devueltas = []
    puma_puntos_mes = 0
    puma_puntos_totales = None
    puede_rentar = usuario.has_perm('usuarios.rentar_producto')

    # Solo obtener el historial de rentas y Puma Puntos para usuarios normales
    if puede_rentar:
        rentas_rentadas = Renta.objects.filter(usuario=usuario, estado='R').order_by('-fecha_renta')
        rentas_devueltas = Renta.objects.filter(usuario=usuario, estado__in=['D', 'T']).order_by('-fecha_renta')
        puma_puntos_mes = usuario.rentas.filter(fecha_renta__month=datetime.now().month).aggregate(Sum('pumapuntos_obtenidos'))['pumapuntos_obtenidos__sum'] or 0
        puma_puntos_totales = perfil.pumapuntos  # Obtener los Puma Puntos totales del perfil del usuario

    context = {
        'usuario': usuario,
        'perfil': perfil,
        'rentas_rentadas': rentas_rentadas,
        'rentas_devueltas': rentas_devueltas,
        'puma_puntos_mes': puma_puntos_mes,
        'puma_puntos_totales': puma_puntos_totales,  # Incluir los Puma Puntos totales en el contexto si aplica
        'rol': usuario.get_rol_display(),  # Incluir el rol del usuario en el contexto
        'puede_rentar': puede_rentar,  # Incluir si el usuario puede rentar productos
    }
    return render(request, 'usuario/ver_perfil.html', context)