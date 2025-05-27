from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.forms import inlineformset_factory
from .forms import NotaDebitoForm, ConceptoDebitoForm, NotaCreditoForm, ConceptoCreditoForm
from .models import NotaDebito, ConceptoDebito, Factura, NotaCredito, ConceptoCredito


# Create your views here.

class NotasDebitoCreditoView(View):
    plantilla = 'notas-dashboard.html'
    
    def get(self, request):
        return render(request, self.plantilla)

class VerNotasDebitoView(View):
    plantilla = 'notas-debito.html'
    
    def get(self, request):
        return render(request, self.plantilla, {
            'notas_debito': NotaDebito.objects.filter(usuario=request.user),
            'usuario': request.user.username,
        })
    
class CrearNotaDebitoView(View):
    plantilla = 'crear-nota-debito.html'

    def get(self, request):
        ConceptoDebitoFormSet = inlineformset_factory(
            NotaDebito, ConceptoDebito, form=ConceptoDebitoForm, extra=1, can_delete=True
        )
        form = NotaDebitoForm()
        # Filtra las facturas por el usuario actual
        form.fields['factura_afectada'].queryset = Factura.objects.filter(usuario=request.user)
        formset = ConceptoDebitoFormSet()
        return render(request, self.plantilla, {
            'form': form,
            'formset': formset,
        })

    def post(self, request):
        ConceptoDebitoFormSet = inlineformset_factory(
            NotaDebito, ConceptoDebito, form=ConceptoDebitoForm, extra=1, can_delete=True
        )
        form = NotaDebitoForm(request.POST)
        
        form.fields['factura_afectada'].queryset = Factura.objects.filter(usuario=request.user)
        formset = ConceptoDebitoFormSet(request.POST)
        if form.is_valid() and formset.is_valid():
            nota = form.save(commit=False)
            nota.usuario = request.user
            nota.subtotal = 0 
            nota.iva = 0
            nota.total = 0
            nota.save()
            conceptos = formset.save(commit=False)
            for concepto in conceptos:
                concepto.nota_debito = nota
                concepto.save()
            # Recalcular totales
            nota.subtotal = nota.calcular_subtotal()
            nota.iva = nota.calcular_iva()
            nota.total = nota.calcular_total()
            nota.save()
            return redirect('nota_debito')  
        return render(request, self.plantilla, {
            'form': form,
            'formset': formset,
        })

class EditarNotaDebitoView(View):
    plantilla = 'editar-nota-debito.html'
    
    def get(self, request, nota_debito_id):
        nota_debito = get_object_or_404(NotaDebito, id=nota_debito_id, usuario=request.user)
        ConceptoDebitoFormSet = inlineformset_factory(
            NotaDebito, ConceptoDebito, form=ConceptoDebitoForm, extra=1, can_delete=True
        )
        form = NotaDebitoForm(instance=nota_debito)
        form.fields['factura_afectada'].queryset = Factura.objects.filter(usuario=request.user)
        formset = ConceptoDebitoFormSet(instance=nota_debito)
        return render(request, self.plantilla, {
            'form': form,
            'formset': formset,
            'nota_debito': nota_debito,
        })
    
    def post(self, request, nota_debito_id):
        nota_debito = get_object_or_404(NotaDebito, id=nota_debito_id, usuario=request.user)
        ConceptoDebitoFormSet = inlineformset_factory(
            NotaDebito, ConceptoDebito, form=ConceptoDebitoForm, extra=1, can_delete=True
        )
        form = NotaDebitoForm(request.POST, instance=nota_debito)
        form.fields['factura_afectada'].queryset = Factura.objects.filter(usuario=request.user)
        formset = ConceptoDebitoFormSet(request.POST, instance=nota_debito)
        if form.is_valid() and formset.is_valid():
            nota = form.save(commit=False)
            nota.usuario = request.user
            nota.save()
            conceptos = formset.save(commit=False)
            for concepto in conceptos:
                concepto.nota_debito = nota
                concepto.save()
            for concepto in formset.deleted_objects:
                concepto.delete()
            # Recalcular totales
            nota.subtotal = nota.calcular_subtotal()
            nota.iva = nota.calcular_iva()
            nota.total = nota.calcular_total()
            nota.save()
            return redirect('nota_debito')
        return render(request, self.plantilla, {
            'form': form,
            'formset': formset,
            'nota_debito': nota_debito,
        })

class VerNotasCreditoView(View):
    plantilla = 'notas-credito.html'
    def get(self, request):
        return render(request, self.plantilla, {
            'notas_credito': NotaCredito.objects.filter(usuario=request.user),
            'usuario': request.user.username,
        })

class CrearNotaCreditoView(View):
    plantilla = 'crear-nota-credito.html'
    def get(self, request):
        ConceptoCreditoFormSet = inlineformset_factory(
            NotaCredito, ConceptoCredito, form=ConceptoCreditoForm, extra=1, can_delete=True
        )
        form = NotaCreditoForm()
        form.fields['factura_afectada'].queryset = Factura.objects.filter(usuario=request.user)
        formset = ConceptoCreditoFormSet()
        return render(request, self.plantilla, {
            'form': form,
            'formset': formset,
        })

    def post(self, request):
        ConceptoCreditoFormSet = inlineformset_factory(
            NotaCredito, ConceptoCredito, form=ConceptoCreditoForm, extra=1, can_delete=True
        )
        form = NotaCreditoForm(request.POST)
        form.fields['factura_afectada'].queryset = Factura.objects.filter(usuario=request.user)
        formset = ConceptoCreditoFormSet(request.POST)
        if form.is_valid() and formset.is_valid():
            nota = form.save(commit=False)
            nota.usuario = request.user
            nota.subtotal = 0
            nota.iva = 0
            nota.total = 0
            nota.save()
            conceptos = formset.save(commit=False)
            for concepto in conceptos:
                concepto.nota_credito = nota
                concepto.save()
            nota.subtotal = nota.calcular_subtotal()
            nota.iva = nota.calcular_iva()
            nota.total = nota.calcular_total()
            nota.save()
            return redirect('nota_credito')
        return render(request, self.plantilla, {
            'form': form,
            'formset': formset,
        })

class EditarNotaCreditoView(View):
    plantilla = 'editar-nota-credito.html'
    
    def get(self, request, nota_credito_id):
        nota_credito = get_object_or_404(NotaCredito, id=nota_credito_id, usuario=request.user)
        ConceptoCreditoFormSet = inlineformset_factory(
            NotaCredito, ConceptoCredito, form=ConceptoCreditoForm, extra=1, can_delete=True
        )
        form = NotaCreditoForm(instance=nota_credito)
        form.fields['factura_afectada'].queryset = Factura.objects.filter(usuario=request.user)
        formset = ConceptoCreditoFormSet(instance=nota_credito)
        return render(request, self.plantilla, {
            'form': form,
            'formset': formset,
            'nota_credito': nota_credito,
        })
    
    def post(self, request, nota_credito_id):
        nota_credito = get_object_or_404(NotaCredito, id=nota_credito_id, usuario=request.user)
        ConceptoCreditoFormSet = inlineformset_factory(
            NotaCredito, ConceptoCredito, form=ConceptoCreditoForm, extra=1, can_delete=True
        )
        form = NotaCreditoForm(request.POST, instance=nota_credito)
        form.fields['factura_afectada'].queryset = Factura.objects.filter(usuario=request.user)
        formset = ConceptoCreditoFormSet(request.POST, instance=nota_credito)
        if form.is_valid() and formset.is_valid():
            nota = form.save(commit=False)
            nota.usuario = request.user
            nota.save()
            conceptos = formset.save(commit=False)
            for concepto in conceptos:
                concepto.nota_credito = nota
                concepto.save()
            for concepto in formset.deleted_objects:
                concepto.delete()
            # Recalcular totales
            nota.subtotal = nota.calcular_subtotal()
            nota.iva = nota.calcular_iva()
            nota.total = nota.calcular_total()
            nota.save()
            return redirect('nota_credito')
        return render(request, self.plantilla, {
            'form': form,
            'formset': formset,
            'nota_credito': nota_credito,
        })


