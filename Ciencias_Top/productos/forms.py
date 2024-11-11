from django import forms
from .models import Producto

class ProductoForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = ['nombre', 'descripcion', 'existencia', 'pumapuntos', 'dias_renta', 'imagen']
        labels = {
            'nombre': 'Nombre del producto',
            'descripcion': 'Descripción del producto',
            'existencia': 'Existencia',
            'pumapuntos': 'PumaPuntos requeridos',
            'dias_renta': 'Días de renta',
            'imagen': 'Imagen del producto',
        }
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control'}),
            'existencia': forms.NumberInput(attrs={'class': 'form-control'}),
            'pumapuntos': forms.NumberInput(attrs={'class': 'form-control'}),
            'dias_renta': forms.Select(attrs={'class': 'form-control'}),
        }
        
    def clean_existencia(self):
        existencia = self.cleaned_data['existencia']
        if existencia < 0:
            raise forms.ValidationError('La existencia no puede ser un número negativo.')
        return existencia
    
    def clean_pumapuntos(self):
        pumapuntos = self.cleaned_data['pumapuntos']
        if pumapuntos < 0:
            raise forms.ValidationError('Los PumaPuntos no pueden ser un número negativo.')
        return pumapuntos
    
    def clean_imagen(self):
        imagen = self.cleaned_data.get('imagen')
        if not imagen:
            raise forms.ValidationError("Se requiere una imagen para el producto.")
        return imagen
    
    