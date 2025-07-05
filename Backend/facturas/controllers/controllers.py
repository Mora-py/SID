from django.shortcuts import render, redirect, get_object_or_404
from .forms import FacturaForm, ProductoFacturaFormSet, FacturaEditarForm
from ..models.models import Factura
from django.views import View

class CrearFacturaController(View):
    plantilla_crear_factura = "crear_factura.html"

    def get(self, request):
        factura_form = FacturaForm(initial={'usuario': request.user})
        formset = ProductoFacturaFormSet()
        return render(request, self.plantilla_crear_factura, {
            'factura_form': factura_form,
            'formset': formset,
        })

    def post(self, request):
        factura_form = FacturaForm(request.POST)
        formset = ProductoFacturaFormSet(request.POST)
        if factura_form.is_valid() and formset.is_valid():
            factura = factura_form.save(commit=False)
            factura.usuario = request.user
            factura.save()
            # Aqqui está el cambio importante: pasa la instancia de factura al formset
            formset.instance = factura
            formset.save()
            # Calcula y guarda los totales después de guardar los productos
            factura.calcular_totales()
            factura.save(update_fields=['subtotal', 'iva', 'total'])
            return redirect('factura-creada', factura_id=factura.id)
        return render(request, self.plantilla_crear_factura, {
            'factura_form': factura_form,
            'formset': formset,
        })

class FacturaCreadaController(View):
    plantilla_factura_creada = "factura_creada.html"

    def get(self, request, factura_id):
        factura = get_object_or_404(Factura, id=factura_id)
        productos = factura.productos.all()
        return render(request, self.plantilla_factura_creada, {
            'factura': factura,
            'productos': productos,
        })

class FacturaDashboardController(View):
    plantilla_factura_dashboard = "factura_dashboard.html"

    def get(self, request):
        facturas = Factura.objects.filter(usuario=request.user)
        return render(request, self.plantilla_factura_dashboard, {'facturas': facturas})
    
class EditarFacturaController(View):
    plantilla_editar_factura = "editar_factura.html"

    def get(self, request, factura_id):
        factura = get_object_or_404(Factura, id=factura_id, usuario=request.user)
        form = FacturaEditarForm(instance=factura)
        return render(request, self.plantilla_editar_factura, {'form': form, 'factura': factura})

    def post(self, request, factura_id):
        factura = get_object_or_404(Factura, id=factura_id, usuario=request.user)
        form = FacturaEditarForm(request.POST, instance=factura)
        if form.is_valid():
            form.save()
            return redirect('factura-editada', factura_id=factura.id)
        return render(request, self.plantilla_editar_factura, {'form': form, 'factura': factura})
    
class SeleccionarFacturaController(View):
    plantilla_seleccionar_factura = "seleccionar_factura_para_editar.html"

    def get(self, request):
        facturas = Factura.objects.filter(usuario=request.user)
        return render(request, self.plantilla_seleccionar_factura, {'facturas': facturas})
    
class FacturaEditadaController(View):
    plantilla = 'facturas_editada.html'

    def get(self, request):
        return render(request, self.plantilla)