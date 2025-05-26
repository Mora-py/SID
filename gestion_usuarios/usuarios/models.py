from django.core.validators import RegexValidator
from django.core.validators import MinLengthValidator
from django.db import models

solo_letras = RegexValidator(
    regex=r'^[a-zA-ZáéíóúÁÉÍÓÚñÑ\s]+$',
    message='Este campo solo puede contener letras y espacios.'
)

solo_numeros = RegexValidator(
    regex=r'^\d+$',
    message='Este campo solo puede contener números.'
)

class Usuario(models.Model):
    DOCUMENTO_IDENTIDAD_CHOICES = [
        ('V', 'Venezolano'),
        ('E', 'Extranjero'),
        ('J', 'Jurídico'),
        ('G', 'Gubernamental'),
        ('P', 'Pasaporte'),
    ]
    ROL_CHOICES = [
        ('A', 'Administrador'),
        ('U', 'Usuario'),
    ]

    primer_nombre = models.CharField(max_length=30, validators=[solo_letras])
    segundo_nombre = models.CharField(max_length=30, blank=True, validators=[solo_letras])
    primer_apellido = models.CharField(max_length=30, validators=[solo_letras])
    segundo_apellido = models.CharField(max_length=30, blank=True, validators=[solo_letras])
    documento_identidad = models.CharField(max_length=1, choices=DOCUMENTO_IDENTIDAD_CHOICES)
    numero_identidad = models.CharField(max_length=20, unique=True, validators=[MinLengthValidator(6),solo_numeros])
    correo_electronico = models.EmailField(unique=True)
    contrasena_inicial = models.CharField(max_length=100)
    rol = models.CharField(max_length=20, choices=[('Administrador', 'Administrador'), ('Usuario', 'Usuario')])

    def __str__(self):
        return f"{self.primer_nombre} {self.primer_apellido}"
