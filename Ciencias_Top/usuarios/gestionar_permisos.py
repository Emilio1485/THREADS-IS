from django.contrib.auth.models import Group, Permission

# Crear grupos y asignar permisos
def crear_grupos_y_permisos():
    # Crear el grupo de Administradores
    admin_group, _ = Group.objects.get_or_create(name='Administradores')
    permisos_admin = [
        'ver_productos', 
        'agregar_producto', 
        'editar_producto', 
        'eliminar_producto',
        'agregar_usuario', 
        'editar_usuario', 
        'eliminar_usuario', 
        'ver_usuarios',
        'sumar_pumapuntos', 
    ]
    for perm in permisos_admin:
        permission = Permission.objects.get(codename=perm)
        admin_group.permissions.add(permission)
    
    # Crear el grupo de Proveedores
    proveedor_group, _ = Group.objects.get_or_create(name='Proveedores')
    permisos_proveedor = [
        'ver_productos', 
        'agregar_producto', 
        'editar_producto', 
        'eliminar_producto'
    ]
    for perm in permisos_proveedor:
        permission = Permission.objects.get(codename=perm)
        proveedor_group.permissions.add(permission)

    # Crear el grupo de Usuarios
    usuario_group, _ = Group.objects.get_or_create(name='Usuarios')
    permisos_usuario = ['ver_productos', 'sumar_pumapuntos', 'rentar_producto']
    for perm in permisos_usuario:
        permission = Permission.objects.get(codename=perm)
        usuario_group.permissions.add(permission)
