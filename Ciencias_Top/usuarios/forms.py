from django import forms
from django.contrib.auth.models import Group
from .models import SuperUsuario 



class UsuarioForm(forms.ModelForm):
    class Meta:
        model = SuperUsuario
        fields = ['numero_cuenta','nombre', 'apellido_paterno', 'apellido_materno', 
                  'celular', 'correo', 'carrera', 'rol']

    def clean_correo(self):
        correo = self.cleaned_data.get('correo')
        if not correo.endswith('@unam.mx'):
            raise forms.ValidationError('El correo debe terminar en @unam.mx')
        return correo
    
    def clean_celular(self):
        """
        Valida que el número de celular tenga exactamente 10 dígitos.
        """
        celular = self.cleaned_data.get('celular')
        if len(celular) != 10 or not celular.isdigit():
            raise forms.ValidationError('El número de celular debe tener exactamente 10 dígitos numéricos.')
        return celular

    def save(self, commit=True):
        usuario = super().save(commit=False)
        # Generar contraseña aleatoria
        contrasenia = usuario.generar_contraseña()
        usuario.set_password(contrasenia)  # Establecer la contraseña generada
        
        # Asignar grupo basado en el rol
        if usuario.rol == 'admin':
            admin_group, _ = Group.objects.get_or_create(name='Administradores')
            admin_group.user_set.add(usuario)  # Agregar el usuario al grupo
            
        elif usuario.rol == 'proveedor':
            proveedor_group, _ = Group.objects.get_or_create(name='Proveedores')
            proveedor_group.user_set.add(usuario)  # Agregar el usuario al grupo
            
        elif usuario.rol == 'usuario':
            usuario_group, _ = Group.objects.get_or_create(name='Usuarios')
            usuario_group.user_set.add(usuario)  # Agregar el usuario al grupo
        
        # Asignar puma puntos solo si es un usuario normal
        if usuario.rol == 'usuario':
            usuario.pumapuntos = 100  # Asignar los puma puntos iniciales
        
        if commit:
            usuario.save()  # Guardar el usuario
        return usuario  # Devuelve el usuario guardado
    
