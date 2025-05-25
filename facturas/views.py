from django.shortcuts import render, redirect, get_object_or_404
from .forms import FacturaForm
from .models import Factura
from django.views import View

class CrearFacturaView(View):
    plantila_factura = "facturas/factura_form.html"

    def get(self, request):
        form = FacturaForm()
        return render(request, self.plantila_factura, {'form': form})

    def post(self, request):
        form = FacturaForm(request.POST)
        if form.is_valid():
            factura = form.save(commit=False)
            factura.usuario = request.user 
            factura.save()
            return redirect('factura_creada', factura_id=factura.id)
        return render(request, self.plantilla_factura, {'form': form})

class FacturaCreadaView(View):
    plantilla_factura_creada = "facturas/factura_creada.html"

    def get(self, request, factura_id):
        factura = get_object_or_404(Factura, id=factura_id)
        return render(request, self.plantilla_factura_creada, {'factura': factura})
    
class FacturaDashboardView(View):
    plantilla_factura_dashboard = "facturas/factura_dashboard.html"

    def get(self, request):
        facturas = Factura.objects.filter(usuario=request.user)
        return render(request, self.plantilla_factura_dashboard, {'facturas': facturas})