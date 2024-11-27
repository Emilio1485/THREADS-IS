from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required ,user_passes_test

from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from django.shortcuts import render, redirect, get_object_or_404
from datetime import datetime
from django.urls import reverse
from rentas.models import Renta

from productos.models import Producto  
from .models import SuperUsuario, Usuario
from .forms import UsuarioForm, UsuarioEditForm
from django.db.models import Q, Sum
from django.http import JsonResponse
from django.contrib.auth.models import Group, Permission
from django.utils.timezone import now

import logging

# Configure logger
logger = logging.getLogger(__name__)

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
            return redirect(reverse('inicio'))   # Redirigir a la página de inicio
        else:
            error_message = "Número de cuenta o contraseña incorrectos."
            return render(request, 'login.html', {'error_message': error_message})
        
    if request.user.is_authenticated:
        return redirect(reverse('inicio'))

    return render(request, 'login.html')




    
@login_required    
def cerrar_sesion_vista(request):
    logout(request)  # Cerrar sesión del usuario
    print("Sesión cerrada con éxito")
    return redirect('iniciar_sesion')  # Redirigir a la página de inicio de sesión 



@login_required
@user_passes_test(is_admin,login_url='iniciar_sesion')
def usuarios_vista(request):
    
    #  Obtener la consulta de búsqueda
    query = request.GET.get('q', '') # Obtener el valor de la consulta de búsqueda
    mensaje = None
    if query:
        usuarios = SuperUsuario.objects.filter(
            Q(numero_cuenta__icontains=query) |
            Q(nombre__icontains=query) |
            Q(apellido_paterno__icontains=query) |
            Q(apellido_materno__icontains=query) |
            Q(tipo_usuario__icontains=query) |
            Q(rol__icontains=query) |
            Q(carrera__icontains=query) |
            Q(correo__icontains=query)
    )
        if not usuarios:
            mensaje = 'No se encontraron usuarios con los criterios de búsqueda proporcionados.'
    else:
        usuarios = SuperUsuario.objects.all()
        
        
    return render(request, 'usuario/ver_usuarios.html', {'usuarios': usuarios, 'query': query, 'mensaje': mensaje, 'search_type': 'usuarios'})



@login_required
@permission_required('usuarios.eliminar_usuario', raise_exception=True)
def eliminar_usuario_vista(request, numero_cuenta):
    if request.method == 'POST':
        try:
            usuario = get_object_or_404(SuperUsuario, numero_cuenta=numero_cuenta)
            
            # No permitir deshabilitar tu propia cuenta
            if usuario == request.user:
                messages.error(request, "No puedes inhabilitar tu propia cuenta.")
                return redirect('vista_detallada_usuario', numero_cuenta=numero_cuenta)

            # Deshabilitar usuario si está activo
            if usuario.is_active:
                usuario.is_active = False
                usuario.save()
                messages.success(request, f'Usuario {numero_cuenta} inhabilitado exitosamente.')
                return redirect('vista_detallada_usuario', numero_cuenta=numero_cuenta)
        
            # Ya está deshabilitado
            messages.error(request, "Este usuario ya está inhabilitado.")
            return redirect('vista_detallada_usuario', numero_cuenta=numero_cuenta)
        except Exception as e:
            messages.error(request, f'Error al inhabilitar el usuario: {str(e)}')
    # Si no es POST
    return JsonResponse({'success': False, 'message': 'Método no permitido.'}, status=405)


@login_required
def vista_detallada_usuario(request, numero_cuenta):
    # Obtener usuario con el número de cuenta proporcionado
    usuario = get_object_or_404(SuperUsuario, numero_cuenta=numero_cuenta)
    # Obtener los roles disponibles
    roles = SuperUsuario.ROLES
    permisos = usuario.user_permissions.all()
    # Convertir los mensajes a una lista
    messages_list = [message.message for message in messages.get_messages(request)]
    return render(request, 'usuario/vista_detallada_usuario.html', {'usuario': usuario, 'roles': roles, 'permisos': permisos,'messages': messages_list})




@login_required
@permission_required('usuarios.editar_usuario', raise_exception=True)
def editar_usuario_vista(request, numero_cuenta):
    usuario = get_object_or_404(SuperUsuario, numero_cuenta=numero_cuenta)
    rol_actual = usuario.rol  # Guardar el rol actual del usuario
    if request.method == 'POST':
        form = UsuarioEditForm(request.POST, instance=usuario)
        if form.is_valid():
            try:
                usuario = form.save(commit=False)
                nuevo_rol = form.cleaned_data['rol']
                
                # Solo actualizar permisos y pumapuntos si el rol ha cambiado
                if rol_actual != nuevo_rol:
                    actualizar_permisos_y_pumapuntos(usuario, nuevo_rol)
                    
                    # Si el nuevo rol no es 'usuario', eliminar el perfil de pumapuntos si existe
                    if nuevo_rol != 'usuario':
                        Usuario.objects.filter(user=usuario).delete()

                # Actualizar la contraseña si se ha generado una nueva
                nueva_contrasena = request.POST.get('hidden_password')
                if nueva_contrasena:
                    usuario.set_password(nueva_contrasena)
                usuario.save()
                
                # Sumar pumapuntos si se ha proporcionado y el rol es 'usuario'
                if nuevo_rol == 'usuario':
                    pumapuntos = request.POST.getlist('puma_puntos[]')
                    total_pumapuntos = sum(int(punto) for punto in pumapuntos)
                    puntos_sumados, mensaje = sumar_pumapuntos(usuario, total_pumapuntos)
                    if puntos_sumados > 0:
                        messages.success(request, f'Usuario {numero_cuenta} actualizado exitosamente. {mensaje}')
                    else:
                        messages.warning(request, f'Usuario {numero_cuenta} actualizado exitosamente. {mensaje}')
                else:
                    messages.success(request, f'Usuario {numero_cuenta} actualizado exitosamente.')
                
                return redirect('vista_detallada_usuario', numero_cuenta=numero_cuenta)
            except Exception as e:
                messages.error(request, f'Error al actualizar el usuario: {str(e)}')
        else:
            messages.error(request, 'Error al actualizar el usuario. Por favor, revise los datos ingresados.')
    return redirect('vista_detallada_usuario', numero_cuenta=numero_cuenta)

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


@login_required
@permission_required('usuarios.editar_usuario', raise_exception=True)
def generar_contrasena_vista(request, numero_cuenta):
    if request.method == 'POST':
        try:
            usuario = get_object_or_404(SuperUsuario, numero_cuenta=numero_cuenta)
            nueva_contrasena = usuario.generar_contraseña()
            usuario.set_password(nueva_contrasena)
            return JsonResponse({'nueva_contrasena': nueva_contrasena}, status=200)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    return JsonResponse({'error': 'Método no permitido'}, status=405)




def sumar_pumapuntos(usuario, puntos_a_sumar):
    try:
        # Obtener el perfil de usuario
        usuario_perfil  = Usuario.objects.get(user=usuario)
        
        fecha_actual = now()
        mes_actual = fecha_actual.month
        anio_actual = fecha_actual.year
        dia_actual = fecha_actual.day
        fecha_ultimo_reinicio = usuario_perfil.fecha_ultimo_reinicio
        # Reiniciar los pumapuntos si es el primer día del mes y no se ha reiniciado ya
        if dia_actual == 1 and (fecha_ultimo_reinicio.month != mes_actual or fecha_ultimo_reinicio.year != anio_actual):
            usuario_perfil.reiniciar_pumapuntos()
            logger.debug(f'Pumapuntos reiniciados para {usuario.numero_cuenta}.')
        
        puntos_mes_actual = usuario_perfil.pumapuntos
        logger.debug(f'Pumapuntos actuales: {puntos_mes_actual}')
        # Calcular los puntos a sumar sin exceder el límite de 500 puntos
        puntos_permitidos = max(0,500-puntos_mes_actual)
        puntos_a_sumar= min(puntos_a_sumar, puntos_permitidos)
        logger.debug(f'Puntos permitidos a sumar: {puntos_permitidos}')
        logger.debug(f'Puntos a sumar: {puntos_a_sumar}')
        
        if puntos_a_sumar > 0:
            # Actualizar los puntos del usuario
            usuario_perfil.pumapuntos += puntos_a_sumar
            usuario_perfil.save()
            mensaje = f'Se han sumado {puntos_a_sumar} Puma Puntos a {usuario.numero_cuenta}.'
            
            
        else:
            mensaje = f'No se han sumado puntos extras a {usuario.numero_cuenta}.'
        return puntos_a_sumar, mensaje
    except Exception as e:
        logger.error(f'Error al sumar pumapuntos: {str(e)}')
        return 0, f'Error al sumar pumapuntos: {str(e)}'






def actualizar_permisos_y_pumapuntos(usuario, nuevo_rol):
    # Limpiar grupos y permisos actuales del usuario
    usuario.groups.clear()
    usuario.user_permissions.clear()
    
    if nuevo_rol == 'admin':
        admin_group, _ = Group.objects.get_or_create(name='Administradores')
        usuario.groups.add(admin_group)
        permisos_admin = [
            'ver_productos', 'agregar_producto', 'editar_producto', 
            'eliminar_producto', 'agregar_usuario', 'editar_usuario', 
            'eliminar_usuario', 'ver_usuarios'
        ]
        for perm in permisos_admin:
            try:
                permission = Permission.objects.get(codename=perm)
                usuario.user_permissions.add(permission)
            except Permission.DoesNotExist:
                continue

    elif nuevo_rol == 'proveedor':
        proveedor_group, _ = Group.objects.get_or_create(name='Proveedores')
        usuario.groups.add(proveedor_group)
        permisos_proveedor = [
            'ver_productos', 'agregar_producto', 
            'editar_producto', 'eliminar_producto'
        ]
        for perm in permisos_proveedor:
            try:
                permission = Permission.objects.get(codename=perm)
                usuario.user_permissions.add(permission)
            except Permission.DoesNotExist:
                continue

    elif nuevo_rol == 'usuario':
        usuario_group, _ = Group.objects.get_or_create(name='Usuarios')
        usuario.groups.add(usuario_group)
        permisos_usuario = ['ver_productos', 'rentar_producto', 'sumar_pumapuntos']
        for perm in permisos_usuario:
            try:
                permission = Permission.objects.get(codename=perm)
                usuario.user_permissions.add(permission)
            except Permission.DoesNotExist:
                continue
        
        # Crear perfil de usuario y asignar pumapuntos si no existe
        usuario_perfil, created = Usuario.objects.get_or_create(user=usuario)
        if created:
            usuario_perfil.pumapuntos = 100
            usuario_perfil.save()
        
        

"""
@login_required
@user_passes_test(is_admin,login_url='iniciar_sesion')
def usuarios_vista(request):
    usuarios = SuperUsuario.objects.all()
    return render(request, 'usuario/ver_usuarios.html', {'usuarios': usuarios})
"""



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

