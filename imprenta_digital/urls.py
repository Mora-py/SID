"""
URL configuration for imprenta_digital project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from core.views import LoginView, DashboardView, LogoutView
from facturas.views import CrearFacturaView, FacturaCreadaView, FacturaDashboardView, EditarFacturaView, SeleccionarFacturaView, FacturaEditadaView
from usuarios.views import RegistrarUsuarioView, EditarUsuarioView, UsuariosDashboardView, UsuarioCreadoView, SeleccionarUsuarioEditarView, UsuarioEditadoView

urlpatterns = [
    #paths de la aplicacion core
    path('admin/', admin.site.urls),
    path('login/', LoginView.as_view(), name='login'),
    path('dashboard/', DashboardView.as_view(), name='dashboard'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('', LoginView.as_view(), name='root'),

    #paths de facturas
    path('factura-dashboard/', FacturaDashboardView.as_view(), name='factura-dashboard'),
    path('crear-factura/', CrearFacturaView.as_view(), name='crear-factura'),
    path('factura-creada/<int:factura_id>/', FacturaCreadaView.as_view(), name='factura-creada'),
    path('editar-factura/<int:factura_id>/', EditarFacturaView.as_view(), name='editar-factura'),
    path('editar-facturas/', SeleccionarFacturaView.as_view(), name='seleccionar-factura'),
    path('factura-editada/<int:factura_id>/', FacturaEditadaView.as_view(), name='factura-editada'),
    

    #paths de usuarios
    path('usuario-dashboard/', UsuariosDashboardView.as_view(), name='usuario-dashboard'),
    path('crear-usuario/', RegistrarUsuarioView.as_view(), name='crear-usuario'),
    path('usuario-creado/', UsuarioCreadoView.as_view(), name='usuario-creado'),
    path('usuario-editado/', UsuarioEditadoView.as_view(), name='usuario-editado'),
    path('editar-usuario/<int:user_id>/', EditarUsuarioView.as_view(), name='editar-usuario'),
    path('editar-usuario/', SeleccionarUsuarioEditarView.as_view(), name='seleccionar-usuario'),
    
    # paths de las notas
    path('', include('notas_de_debito_credito.urls')), 
    
    # paths de las ordenes de entrega
    path('', include('orden_de_entrega.urls')), 
]
