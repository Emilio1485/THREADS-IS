from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.db.models import Q, Count ,F
from datetime import datetime, timedelta, timezone
from django.http import JsonResponse
from productos.models import Producto
from .models import Renta
from django.conf import settings
from usuarios.models import SuperUsuario, Usuario
import calendar

# Lista de nombres de meses en español
MESES_EN_ESPANOL = [
    "enero", "febrero", "marzo", "abril", "mayo", "junio",
    "julio", "agosto", "septiembre", "octubre", "noviembre", "diciembre"
]

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
            messages.error(request, "Has alcanzado el límite de 3 rentas diarias.")
          

        # Verificar la disponibilidad del producto
        if producto.existencia <= 0:
            messages.error(request, "El producto no está disponible.")
            

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
@user_passes_test(is_admin)
def historial_rentas_usuario(request, usuario_id):
    usuario = get_object_or_404(SuperUsuario, numero_cuenta=usuario_id)  # Usa el campo numero_cuenta
    rentas = Renta.objects.filter(usuario=usuario).order_by('-fecha_renta')

    context = {
        'usuario': usuario,
        'rentas': rentas,
    }
    return render(request, 'paginas/historial_rentas_usuario.html', context)

@login_required
def lista_productos(request):
    productos = Producto.objects.all()
    return render(request, 'paginas/lista_productos.html', {'productos': productos})

from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.db.models import Count, F
from datetime import datetime, timedelta
from usuarios.models import SuperUsuario
from productos.models import Producto
from rentas.models import Renta


@login_required
@user_passes_test(lambda u: u.groups.filter(name='Administradores').exists())
def ver_reportes(request):
    # Cantidad de personas por carrera que tienen una cuenta activa en el sistema
    personas_por_carrera = SuperUsuario.objects.filter(is_active=True).values('carrera').annotate(total=Count('carrera'))

    # Los 5 productos más rentados del mes
    now = datetime.now()
    inicio_mes = now.replace(day=1)
    nombre_mes = MESES_EN_ESPANOL[now.month - 1]  # Nombre del mes en español
    productos_mas_rentados = Producto.objects.filter(rentas__fecha_renta__gte=inicio_mes).annotate(total=Count('rentas')).order_by('-total')[:5]

    # Cantidad de cuentas inactivas
    cuentas_inactivas = SuperUsuario.objects.filter(is_active=False).count()

    # Los productos que requieren menor cantidad de puma puntos para ser canjeados
    productos_menor_puma_puntos = Producto.objects.order_by('pumapuntos')[:5]

    # Los 10 usuarios que más veces han devuelto un producto rentado tarde
    usuarios_mas_tardes = SuperUsuario.objects.annotate(total_tardes=Count('rentas__fecha_devolucion')).filter(rentas__fecha_devolucion__gt=F('rentas__fecha_devolucion_estimada')).order_by('-total_tardes')[:10]

    # Los 5 usuarios con mayor cantidad de productos rentados en la semana
    inicio_semana = now - timedelta(days=now.weekday())
    usuarios_mas_rentas_semana = SuperUsuario.objects.filter(rentas__fecha_renta__gte=inicio_semana).annotate(total=Count('rentas')).order_by('-total')[:5]

    context = {
        'personas_por_carrera': personas_por_carrera,
        'productos_mas_rentados': productos_mas_rentados,
        'cuentas_inactivas': cuentas_inactivas,
        'productos_menor_puma_puntos': productos_menor_puma_puntos,
        'usuarios_mas_tardes': usuarios_mas_tardes,
        'usuarios_mas_rentas_semana': usuarios_mas_rentas_semana,
        'nombre_mes': nombre_mes,
    }
    return render(request, 'paginas/ver_reportes.html', context)