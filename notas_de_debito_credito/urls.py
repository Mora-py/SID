from django.urls import path
from .views import (
    CrearNotaDebitoView, VerNotasDebitoView, EditarNotaDebitoView,
    CrearNotaCreditoView, VerNotasCreditoView, EditarNotaCreditoView,
    NotasDebitoCreditoView
)

urlpatterns = [
    path('notas/', NotasDebitoCreditoView.as_view(), name='notas-dashboard'),
    path('notas/debito/', VerNotasDebitoView.as_view(), name='nota_debito'),
    path('notas/debito/crear/', CrearNotaDebitoView.as_view(), name='crear_nota_debito'),
    path('notas/debito/<int:nota_debito_id>/', EditarNotaDebitoView.as_view(), name='editar_nota_debito'),
    path('notas/credito/', VerNotasCreditoView.as_view(), name='nota_credito'),
    path('notas/credito/crear/', CrearNotaCreditoView.as_view(), name='crear_nota_credito'),
    path('notas/credito/<int:nota_credito_id>/', EditarNotaCreditoView.as_view(), name='editar_nota_credito'),
]