from django.urls import path
from .controllers import CrearFacturaController, FacturaCreadaController, FacturaDashboardController, EditarFacturaController, SeleccionarFacturaController, FacturaEditadaController

urlpatterns = [
    path('factura-dashboard/', FacturaDashboardController.as_view(), name='factura-dashboard'),
    path('crear-factura/', CrearFacturaController.as_view(), name='crear-factura'),
    path('factura-creada/<int:factura_id>/', FacturaCreadaController.as_view(), name='factura-creada'),
    path('editar-factura/<int:factura_id>/', EditarFacturaController.as_view(), name='editar-factura'),
    path('editar-facturas/', SeleccionarFacturaController.as_view(), name='seleccionar-factura'),
    path('factura-editada/<int:factura_id>/', FacturaEditadaController.as_view(), name='factura-editada'),
]