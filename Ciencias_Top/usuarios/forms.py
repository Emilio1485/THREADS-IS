from django import forms
from .models import Usuario

"""
class UsuarioForm(forms.ModelForm):
    class Meta:
        modelo = Usuario
        campos = ['nombre', 'apellido_paterno', 'apellido_materno', 'numero_cuenta', 'celular',
                  'correo', 'carrera', 'rol']

    def verificar_correo(self):
        correo = self.cleaned_data['correo']
        if not correo.endswith('@unam.mx'):
            raise forms.ValidationError('El correo debe terminar en @unam.mx')
        return correo
    
    def save(self, commit = True):
        usuario = super().save(commit = False)
        # Generar contraseña aleatoria
        contrasenia =  usuario.generar_contraseña()
        usuario.set_password(contrasenia)
        if commit:
            usuario.save()
        return Usuario # devuelve usuario guardado

"""