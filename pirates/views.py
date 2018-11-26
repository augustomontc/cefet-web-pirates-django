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
            total=ExpressionWrapper(F('preco')*F('quantidade'),
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