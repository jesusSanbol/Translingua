from django import forms
from traductor.models import ArchivoSTR

class ArchivoSTRForm(forms.ModelForm):
    class Meta:
        model = ArchivoSTR
        fields = ['nombre', 'archivo', 'idioma_destino']
