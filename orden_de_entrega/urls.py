from django.urls import path
from .views import VerOrdenesEntregaView, CrearOrdenDeEntregaView, EditarOrdenDeEntregaView

urlpatterns = [
    path('ordenes/', VerOrdenesEntregaView.as_view(), name='orden_entrega'),
    path('ordenes/crear/', CrearOrdenDeEntregaView.as_view(), name='crear_orden_entrega'),
    path('ordenes/<int:orden_id>/', EditarOrdenDeEntregaView.as_view(), name='editar_orden_entrega'),
]