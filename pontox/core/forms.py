#coding: utf-8
__author__ = 'pedro'
from django import forms
from django.forms import TimeField
from datetime import timedelta
from core.models import Departamento, Regra

class UploadForm(forms.Form):
    arquivo = forms.FileField(
        label='Selecione um arquivo'
    )
    titulo = forms.CharField(max_length=120)

class DepartamentoForm(forms.ModelForm):
    class Meta:
        model = Departamento
        fields = '__all__'

class RegraForm(forms.ModelForm):
    class Meta:
        model = Regra
        fields = ['horario_entrada', 'horario_saida']