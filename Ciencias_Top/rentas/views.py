from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from productos.models import Producto
from .models import Renta
from django.utils import timezone


def rentar_producto(request, producto_id):
    if request.method == "POST":
        producto = get_object_or_404(Producto, id=producto_id)
        usuario = request.user  # Asumiendo que el usuario está autenticado

        # Verifica si el usuario tiene suficientes Puma Puntos
        if usuario.pumapuntos >= producto.pumapuntos and producto.existencia > 0:
            # Resta los puntos y guarda la renta
            usuario.pumapuntos -= producto.pumapuntos
            usuario.save()

            renta = Renta(
                usuario=usuario,
                producto=producto,
                fecha_renta=timezone.now(),
                estado="Rentado",
                pumapuntos_obtenidos=producto.pumapuntos,
            )
            renta.save()

            # Actualiza la disponibilidad del producto
            producto.existencia -= 1
            producto.save()

            # Mensaje de éxito
            messages.success(request, f'Has rentado "{producto.nombre}" con éxito.')
        else:
            messages.error(request, "No tienes suficientes Puma Puntos o el producto no está disponible.")

        return redirect('nombre_de_la_vista_de_productos')  # Redirige a la lista de productos o a otra página
