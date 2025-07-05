from django.forms import ModelForm
from .models import NotaDebito, ConceptoDebito, NotaCredito, ConceptoCredito
from django import forms

class NotaDebitoForm(ModelForm):
    class Meta:
        model = NotaDebito
        fields = [
            'factura_afectada',
            'observaciones'
        ]
        widgets = {
            'factura_afectada': forms.Select(),
            'observaciones': forms.Textarea(attrs={'rows': 4}),
        }
        labels = {
            'factura_afectada': 'Factura Asociada',
            'observaciones': 'Observaciones',
        }

class ConceptoDebitoForm(ModelForm):
    class Meta:
        model = ConceptoDebito
        fields = ['descripcion', 'monto']

class NotaCreditoForm(ModelForm):
    class Meta:
        model = NotaCredito
        fields = [
            'factura_afectada',
            'observaciones'
        ]
        widgets = {
            'factura_afectada': forms.Select(),
            'observaciones': forms.Textarea(attrs={'rows': 4}),
        }
        labels = {
            'factura_afectada': 'Factura Asociada',
            'observaciones': 'Observaciones',
        }

class ConceptoCreditoForm(ModelForm):
    class Meta:
        model = ConceptoCredito
        fields = ['descripcion', 'monto']