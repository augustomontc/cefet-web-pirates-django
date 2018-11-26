from django.shortcuts import render
from django.views import View
from pirates.models import Tesouro
from django.db.models import F, ExpressionWrapper, DecimalField
from django import forms
from django.http import HttpResponseRedirect
from django.urls.base import reverse

class ListaTesourosView(View):
    def get(self, request):
        tesouros = Tesouro.objects.annotate(
            valor_total=ExpressionWrapper(F('preco')*F('quantidade'),
            output_field=DecimalField(
                max_digits=10,
                decimal_places=2,
                blank=True,
            ))
        ).all()
        
        total_geral = 0
        for tesouro in tesouros:
            total_geral += tesouro.valor_total

        return render(request, 'lista_tesouros.html', {'tesouros': tesouros,'total_geral': total_geral})


class TesouroForm(forms.ModelForm):
    class Meta:
        model = Tesouro
        fields = ['nome', 'quantidade', 'preco', 'img_tesouro']
        labels = {"img_tesouro": "Imagem"}

class SalvarTesouro(View):
    def get(self, request, id=None):
        tesouro_instance = get_object_or_404(Tesouro, id=id) if id != None else None
        return render(request, 'salvar_tesouro.html', {"tesouroForm": TesouroForm(instance=tesouro_instance)})

    def post(self,request, id=None):
        tesouro_instance = get_object_or_404(Tesouro, id=id) if id != None else None
        form = TesouroForm(request.POST, request.FILES, instance=tesouro_instance)
        
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('inicio'))
        
        return render(request, 'salvar_tesouro.html', {'tesouroForm': form})

class RemoverTesouro(View):
     def get(self, request, id):
        Tesouro.objects.get(id=id).delete()
        return HttpResponseRedirect(reverse('inicio'))