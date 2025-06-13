from django.db import models
from django.utils import timezone
import re
from django.core.exceptions import ValidationError
from django.conf import settings
from facturas.models.models import Factura
from decimal import Decimal

def validar_cedula_rif(valor):
    patron = r'^(J-\d{9}|V-\d{8}|E-\d{8}|P-\d{9}|G-\d{9})$'
    if not re.match(patron, valor):
        raise ValidationError(
            'El RIF/Cédula debe tener el formato J-XXXXXXXXX, V-XXXXXXXX, E-XXXXXXXX, P-XXXXXXXXX o G-XXXXXXXXX.'
        )

# Create your models here.
class NotaDebito(models.Model):
    factura_afectada = models.ForeignKey(Factura, on_delete=models.CASCADE)
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    numero_nota_debito = models.CharField(max_length=20, unique=True)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)
    iva = models.DecimalField(max_digits=10, decimal_places=2)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    observaciones = models.TextField(blank=True, null=True)

    # Campos copiados de la factura
    lugar_emision = models.CharField(max_length=100, editable=False)
    fecha_emision = models.DateField(editable=False)
    nombre_cliente = models.CharField(max_length=100, editable=False)
    telefono_cliente = models.CharField(max_length=11, editable=False)
    cedula_cliente = models.CharField(max_length=11, editable=False)

    def save(self, *args, **kwargs):
        # Copia los datos de la factura asociada
        if self.factura_afectada:
            self.lugar_emision = self.factura_afectada.lugar_emision
            self.fecha_emision = self.factura_afectada.fecha_emision
            self.nombre_cliente = self.factura_afectada.nombre_cliente
            self.telefono_cliente = self.factura_afectada.telefono_cliente
            self.cedula_cliente = self.factura_afectada.cedula_cliente

        # Generar número de nota de débito si no existe
        if not self.numero_nota_debito:
            count = NotaDebito.objects.filter(usuario=self.usuario).count() + 1
            while True:
                numero = f"ND-{count:05d}"
                if not NotaDebito.objects.filter(numero_nota_debito=numero).exists():
                    self.numero_nota_debito = numero
                    break
                count += 1

        super().save(*args, **kwargs)
    
    def calcular_subtotal(self):
        return sum(concepto.monto for concepto in self.conceptos.all())
    
    def calcular_iva(self):
        return self.subtotal * Decimal('0.16')
    
    def calcular_total(self):
        return self.subtotal + self.iva
    
    def __str__(self):
        return f"Nota de Débito {self.numero_nota_debito} - {self.nombre_cliente} - {self.fecha_emision}"

class ConceptoDebito(models.Model):
    nota_debito = models.ForeignKey('NotaDebito', related_name='conceptos', on_delete=models.CASCADE)
    descripcion = models.CharField(max_length=255)
    monto = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.descripcion}: {self.monto}"

class NotaCredito(models.Model):
    factura_afectada = models.ForeignKey(Factura, on_delete=models.CASCADE)
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    numero_nota_credito = models.CharField(max_length=20, unique=True)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)
    iva = models.DecimalField(max_digits=10, decimal_places=2)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    observaciones = models.TextField(blank=True, null=True)

    # Campos copiados de la factura
    lugar_emision = models.CharField(max_length=100, editable=False)
    fecha_emision = models.DateField(editable=False)
    nombre_cliente = models.CharField(max_length=100, editable=False)
    telefono_cliente = models.CharField(max_length=11, editable=False)
    cedula_cliente = models.CharField(max_length=11, editable=False)

    def save(self, *args, **kwargs):
        if self.factura_afectada:
            self.lugar_emision = self.factura_afectada.lugar_emision
            self.fecha_emision = self.factura_afectada.fecha_emision
            self.nombre_cliente = self.factura_afectada.nombre_cliente
            self.telefono_cliente = self.factura_afectada.telefono_cliente
            self.cedula_cliente = self.factura_afectada.cedula_cliente

        if not self.numero_nota_credito:
            count = NotaCredito.objects.filter(usuario=self.usuario).count() + 1
            while True:
                numero = f"NC-{count:05d}"
                if not NotaCredito.objects.filter(numero_nota_credito=numero).exists():
                    self.numero_nota_credito = numero
                    break
                count += 1

        super().save(*args, **kwargs)

    def calcular_subtotal(self):
        return sum(concepto.monto for concepto in self.conceptos.all())

    def calcular_iva(self):
        return self.subtotal * Decimal('0.16')

    def calcular_total(self):
        return self.subtotal + self.iva

    def __str__(self):
        return f"Nota de Crédito {self.numero_nota_credito} - {self.nombre_cliente} - {self.fecha_emision}"

class ConceptoCredito(models.Model):
    nota_credito = models.ForeignKey('NotaCredito', related_name='conceptos', on_delete=models.CASCADE)
    descripcion = models.CharField(max_length=255)
    monto = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.descripcion}: {self.monto}"



