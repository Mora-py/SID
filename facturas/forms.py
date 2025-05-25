from django import forms
from .models import Factura

class FacturaForm(forms.ModelForm):
    productos = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 4}),
        help_text="Ingresa los productos en formato JSON. Ejemplo: [{'nombre': 'Producto A', 'cantidad': 2, 'precio_unitario': 10.5}]"
    )

    class Meta:
        model = Factura
        fields = ['lugar_emision', 'fecha_emision', 'nombre_cliente', 'telefono_cliente', 'cedula_cliente', 'productos']
        widgets = {
            'fecha_emision': forms.DateInput(attrs={'type': 'date'}),
        }

    def clean_productos(self):
        import json
        data = self.cleaned_data['productos']
        try:
            productos = json.loads(data.replace("'", '"'))
            if not isinstance(productos, list):
                raise forms.ValidationError("Debes ingresar una lista de productos.")
            for producto in productos:
                if not all(k in producto for k in ('nombre', 'cantidad', 'precio_unitario')):
                    raise forms.ValidationError("Cada producto debe tener 'nombre', 'cantidad' y 'precio_unitario'.")
            return productos
        except Exception:
            raise forms.ValidationError("Formato de productos inválido. Usa una lista de diccionarios.")