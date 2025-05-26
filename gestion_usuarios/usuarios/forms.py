from django import forms
from .models import Usuario

class UsuarioForm(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = ['primer_nombre', 'segundo_nombre', 'primer_apellido', 'segundo_apellido', 'documento_identidad', 'numero_identidad', 'correo_electronico', 'contrasena_inicial', 'rol']
