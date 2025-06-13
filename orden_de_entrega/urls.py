from django.urls import path
from .controllers.controllers import VerOrdenesEntregaController, CrearOrdenDeEntregaController, EditarOrdenDeEntregaController

urlpatterns = [
    path('ordenes/', VerOrdenesEntregaController.as_view(), name='orden_entrega'),
    path('ordenes/crear/', CrearOrdenDeEntregaController.as_view(), name='crear_orden_entrega'),
    path('ordenes/<int:orden_id>/', EditarOrdenDeEntregaController.as_view(), name='editar_orden_entrega'),
]