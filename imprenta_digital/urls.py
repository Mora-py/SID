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
from core.controllers.controllers import LoginController, DashboardController, LogoutController
from facturas.controllers.controllers import CrearFacturaController, FacturaCreadaController, FacturaDashboardController, EditarFacturaController, SeleccionarFacturaController, FacturaEditadaController
from usuarios.controllers.controllers import RegistrarUsuarioController, EditarUsuarioController, UsuariosDashboardController, UsuarioCreadoController, SeleccionarUsuarioEditarController, UsuarioEditadoController

urlpatterns = [
    #paths de la aplicacion core
    path('admin/', admin.site.urls),
    path('login/', LoginController.as_view(), name='login'),
    path('dashboard/', DashboardController.as_view(), name='dashboard'),
    path('logout/', LogoutController.as_view(), name='logout'),
    path('', LoginController.as_view(), name='root'),

    #paths de facturas
    path('factura-dashboard/', FacturaDashboardController.as_view(), name='factura-dashboard'),
    path('crear-factura/', CrearFacturaController.as_view(), name='crear-factura'),
    path('factura-creada/<int:factura_id>/', FacturaCreadaController.as_view(), name='factura-creada'),
    path('editar-factura/<int:factura_id>/', EditarFacturaController.as_view(), name='editar-factura'),
    path('editar-facturas/', SeleccionarFacturaController.as_view(), name='seleccionar-factura'),
    path('factura-editada/<int:factura_id>/', FacturaEditadaController.as_view(), name='factura-editada'),
    

    #paths de usuarios
    path('usuario-dashboard/', UsuariosDashboardController.as_view(), name='usuario-dashboard'),
    path('crear-usuario/', RegistrarUsuarioController.as_view(), name='crear-usuario'),
    path('usuario-creado/', UsuarioCreadoController.as_view(), name='usuario-creado'),
    path('usuario-editado/', UsuarioEditadoController.as_view(), name='usuario-editado'),
    path('editar-usuario/<int:user_id>/', EditarUsuarioController.as_view(), name='editar-usuario'),
    path('editar-usuario/', SeleccionarUsuarioEditarController.as_view(), name='seleccionar-usuario'),
    
    # paths de las notas
    path('', include('notas_de_debito_credito.urls')), 
    
    # paths de las ordenes de entrega
    path('', include('orden_de_entrega.urls')), 
]