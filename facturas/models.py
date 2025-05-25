from django.db import models
from django.utils import timezone
from django.conf import settings
import re
from django.core.exceptions import ValidationError


# Create your models here.

def validar_cedula_rif(valor):
    patron = r'^(J-\d{9}|V-\d{8}|E-\d{8}|P-\d{9}|G-\d{9})$'
    if not re.match(patron, valor):
        raise ValidationError(
            'El RIF/Cédula debe tener el formato J-XXXXXXXXX, V-XXXXXXXX, E-XXXXXXXX, P-XXXXXXXXX o G-XXXXXXXXX.'
        )


class Factura(models.Model):
    lugar_emision = models.CharField(max_length=100)
    fecha_emision = models.DateField(default=timezone.now)
    nombre_cliente = models.CharField(max_length=100)
    telefono_cliente = models.CharField(max_length=11)
    cedula_cliente = models.CharField(
        max_length=11,
        validators=[validar_cedula_rif]
    )
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='facturas')
    numero_factura = models.PositiveIntegerField()
    productos = models.JSONField(
        help_text="Lista de productos con cantidad, nombre y precio_unitario. Ejemplo: [{'nombre': 'Producto A', 'cantidad': 2, 'precio_unitario': 10.5}]"
    )
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)
    iva = models.DecimalField(max_digits=10, decimal_places=2)
    total = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        unique_together = ('usuario', 'numero_factura')

    def asignar_numero_factura(self):
        ultima = Factura.objects.filter(usuario=self.usuario).order_by('-numero_factura').first()
        if ultima:
            return ultima.numero_factura + 1
        return 1

    def calcular_subtotal(self):
        total = 0
        for producto in self.productos:
            cantidad = producto.get('cantidad', 0)
            precio_unitario = producto.get('precio_unitario', 0)
            total += cantidad * precio_unitario
        return total
    
    def calcular_iva(self):
        return self.subtotal * 0.16
    
    def calcular_total(self):
        return self.subtotal + self.iva
    
    def save(self, *args, **kwargs):
        self.numero_factura = self.asignar_numero_factura()
        self.subtotal = self.calcular_subtotal()
        self.iva = self.calcular_iva()
        self.total = self.calcular_total()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Factura {self.id} - {self.nombre_cliente}"





