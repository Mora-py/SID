from django.urls import path
from .controllers import (
    CrearNotaDebitoController, VerNotasDebitoController, EditarNotaDebitoController,
    CrearNotaCreditoController, VerNotasCreditoController, EditarNotaCreditoController,
    NotasDebitoCreditoController
)

urlpatterns = [
    path('notas/', NotasDebitoCreditoController.as_view(), name='notas-dashboard'),
    path('notas/debito/', VerNotasDebitoController.as_view(), name='nota_debito'),
    path('notas/debito/crear/', CrearNotaDebitoController.as_view(), name='crear_nota_debito'),
    path('notas/debito/<int:nota_debito_id>/', EditarNotaDebitoController.as_view(), name='editar_nota_debito'),
    path('notas/credito/', VerNotasCreditoController.as_view(), name='nota_credito'),
    path('notas/credito/crear/', CrearNotaCreditoController.as_view(), name='crear_nota_credito'),
    path('notas/credito/<int:nota_credito_id>/', EditarNotaCreditoController.as_view(), name='editar_nota_credito'),
]