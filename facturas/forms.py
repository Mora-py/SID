from django import forms
from django.forms import inlineformset_factory
from .models import Factura, ProductoFactura

class FacturaForm(forms.ModelForm):
    class Meta:
        model = Factura
        fields = [
            'nombre_cliente',
            'lugar_emision',
            'fecha_emision',
            'telefono_cliente',
            'cedula_cliente',
            'numero_factura',
        ]
        widgets = {
            'fecha_emision': forms.DateInput(attrs={'type': 'date'}),
        }

class ProductoFacturaForm(forms.ModelForm):
    class Meta:
        model = ProductoFactura
        fields = ['nombre', 'cantidad', 'precio_unitario']

# Formset para productos asociados a una factura
ProductoFacturaFormSet = inlineformset_factory(
    Factura,
    ProductoFactura,
    form=ProductoFacturaForm,
    extra=1,
    can_delete=True
)

class FacturaEditarForm(forms.ModelForm):
    class Meta:
        model = Factura
        fields = [
            'nombre_cliente',
            'cedula_cliente',
            'telefono_cliente',
            'lugar_emision',
            'fecha_emision'
            
        ]
        widgets = {
            'fecha_emision': forms.DateInput(attrs={'type': 'date'}),
        }
