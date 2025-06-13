from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.views import View
from ..forms import RegistroUsuarioForm, EditarUsuarioForm

class RegistrarUsuarioController(View):
    plantilla = 'usuarios/registrar_usuario.html'

    def get(self, request):
        form = RegistroUsuarioForm()
        return render(request, self.plantilla, {'form': form})

    def post(self, request):
        form = RegistroUsuarioForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('usuario-creado')
        return render(request, self.plantilla, {'form': form})

class EditarUsuarioController(View):
    plantilla = 'usuarios/editar_usuario.html'

    def get(self, request, user_id):
        usuario = get_object_or_404(User, pk=user_id)
        form = EditarUsuarioForm(instance=usuario)
        return render(request, self.plantilla, {'form': form, 'usuario': usuario})

    def post(self, request, user_id):
        usuario = get_object_or_404(User, pk=user_id)
        form = EditarUsuarioForm(request.POST, instance=usuario)
        if form.is_valid():
            form.save()
            return redirect('usuario-editado')
        return render(request, self.plantilla, {'form': form, 'usuario': usuario})

class UsuariosDashboardController(View):
    plantilla = 'usuarios/usuarios_dashboard.html'
    
    def get(self, request):
        datos = {
            'is_admin': request.user.is_staff or request.user.is_superuser,
            'username': request.user.username,
        }
        return render(request, self.plantilla, datos)

class UsuarioCreadoController(View):
    plantilla = 'usuarios/usuario_creado.html'

    def get(self, request):
        return render(request, self.plantilla)
    
class UsuarioEditadoController(View):
    plantilla = 'usuarios/usuario_editado.html'

    def get(self, request):
        return render(request, self.plantilla)

class SeleccionarUsuarioEditarController(View):
    plantilla = 'usuarios/seleccionar_usuario_editar.html'

    def get(self, request):
        usuarios = User.objects.all()
        return render(request, self.plantilla, {'usuarios': usuarios})

