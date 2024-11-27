from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from datetime import datetime, timedelta , timezone
from productos.models import Producto
from .models import Renta
from django.conf import settings
from usuarios.models import SuperUsuario
from django.contrib.auth.decorators import user_passes_test

# Verificar permisos
def is_admin(user):
    return user.groups.filter(name='Administradores').exists()

def is_prov(user):
    return user.groups.filter(name='Proveedores').exists()

def is_admin_or_prov(user):
    return is_admin(user) or is_prov(user)

# Vista para la pantalla de rentas
@login_required
def rentar_producto_vista(request):
    query = request.GET.get('q', '')  # Obtener parámetro de búsqueda
    user = request.user

    # Inicializar los productos a un queryset vacío
    productos = Producto.objects.none()

    # Buscar productos que están disponibles para rentar
    if query:
        productos = Producto.objects.filter(
            Q(nombre__icontains=query) | Q(codigo__icontains=query)
        ).exclude(estado='R')  # Excluir productos ya rentados
    else:
        productos = Producto.objects.filter(estado='A')  # Mostrar solo productos disponibles ('A' para disponible)

    context = {
        'productos': productos,
        'query': query,
    }
    return render(request, 'paginas/rentar_producto.html', context)

# Vista para mostrar los detalles del producto y confirmar la renta
@login_required
def renta_producto(request, producto_codigo):
    producto = get_object_or_404(Producto, codigo=producto_codigo)
    user = request.user

    if request.method == 'POST':
        # Verificar el límite de 3 rentas diarias
        hoy = datetime.now().date()
        rentas_hoy = Renta.objects.filter(usuario=user, fecha_renta__date=hoy).count()
        if rentas_hoy >= 3:
            messages.error(request, "Ya has rentado el máximo de productos permitido para hoy.")
            return redirect('inicio')

        # Verificar la disponibilidad del producto
        if producto.existencia <= 0:
            messages.error(request, "El producto no está disponible.")
            return redirect('inicio')

        renta = Renta(usuario=user, producto=producto)
        puede_rentar, mensaje = renta.puede_rentar()
        if puede_rentar:
            fecha_renta = datetime.now()
            fecha_devolucion_estimada = fecha_renta + timedelta(days=producto.dias_renta)

            renta.fecha_renta = fecha_renta
            renta.fecha_devolucion_estimada = fecha_devolucion_estimada
            renta.estado = 'R'
            renta.save()

            # Actualizar el estado del producto y restar la existencia
            producto.existencia -= 1
            producto.save()

            # Actualizar los puntos del usuario
            user.usuario.pumapuntos -= producto.pumapuntos
            user.usuario.pumapuntos += producto.pumapuntos // 2
            user.usuario.save()

            messages.success(request, 'Producto rentado exitosamente.')
            return redirect('ver_perfil')
        else:
            messages.error(request, mensaje)

    context = {
        'producto': producto,
    }
    return render(request, 'paginas/renta_producto.html', context)
@login_required
def lista_rentas(request):
    user = request.user
    rentas = Renta.objects.filter(usuario=user)

    context = {
        'rentas': rentas,
    }
    return render(request, 'paginas/lista_rentas.html', context)

@login_required
@user_passes_test(is_admin)
def devolver_producto(request, renta_id):
    renta = get_object_or_404(Renta, id_renta=renta_id)
    user = request.user

    if request.method == 'POST':
        fecha_devolucion_real = datetime.now(timezone.utc)
        renta.registrar_devolucion(fecha_devolucion_real)

        # Actualizar la existencia del producto
        renta.producto.existencia += 1
        renta.producto.save()

        messages.success(request, 'Producto devuelto exitosamente.')
        return redirect('rentas:lista_rentas')

    context = {
        'renta': renta,
    }
    return render(request, 'paginas/devolver_producto.html', context)

@login_required
def historial_rentas_usuario(request, usuario_id):
    usuario = get_object_or_404(SuperUsuario, numero_cuenta=usuario_id)  # Usa el campo numero_cuenta
    rentas = Renta.objects.filter(usuario=usuario).order_by('-fecha_renta')

    context = {
        'usuario': usuario,
        'rentas': rentas,
    }
    return render(request, 'paginas/historial_rentas_usuario.html', context)