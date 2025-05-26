from django.contrib import admin
from django.urls import path
from usuarios import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.lista_usuarios, name='home'),  # Root URL shows the list of users
    path('crear_usuario/', views.crear_usuario, name='crear_usuario'),
    path('lista_usuarios/', views.lista_usuarios, name='lista_usuarios'),
    path('modificar_usuario/<int:id>/', views.modificar_usuario, name='modificar_usuario'),
    path('eliminar_usuario/<int:id>/', views.eliminar_usuario, name='eliminar_usuario'),
]
