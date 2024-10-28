from django import forms
from django.contrib.auth.models import Group, Permission
from .models import SuperUsuario 



class UsuarioForm(forms.ModelForm):
    class Meta:
        model = SuperUsuario
        fields = ['numero_cuenta', 'nombre', 'apellido_paterno', 'apellido_materno', 
                 'celular', 'correo', 'carrera', 'rol']

    def clean_correo(self):
        correo = self.cleaned_data.get('correo')
        if not correo.endswith('@unam.mx'):
            raise forms.ValidationError('El correo debe terminar en @unam.mx')
        return correo
    
    def clean_celular(self):
        celular = self.cleaned_data.get('celular')
        if len(celular) != 10 or not celular.isdigit():
            raise forms.ValidationError('El número de celular debe tener exactamente 10 dígitos numéricos.')
        return celular

    def save(self, commit=True):
        usuario = super().save(commit=False)
        # Establecer el username igual al número de cuenta
        usuario.username = usuario.numero_cuenta
        # Generar contraseña aleatoria
        contrasenia = usuario.generar_contraseña()
        usuario.set_password(contrasenia)
        usuario.contrasenia_temp = contrasenia

        if commit:
            usuario.save()

            # Asignar grupo basado en el rol
            if usuario.rol == 'admin':
                admin_group, _ = Group.objects.get_or_create(name='Administradores')
                usuario.groups.clear()
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

            elif usuario.rol == 'proveedor':
                proveedor_group, _ = Group.objects.get_or_create(name='Proveedores')
                usuario.groups.clear()
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

            elif usuario.rol == 'usuario':
                usuario_group, _ = Group.objects.get_or_create(name='Usuarios')
                usuario.groups.clear()
                usuario.groups.add(usuario_group)
                permisos_usuario = ['ver_productos', 'rentar_producto']
                for perm in permisos_usuario:
                    try:
                        permission = Permission.objects.get(codename=perm)
                        usuario.user_permissions.add(permission)
                    except Permission.DoesNotExist:
                        continue
                
                # Asignar puma puntos solo si es un usuario normal
                usuario.pumapuntos = 100

            usuario.save()

        return usuario
    
