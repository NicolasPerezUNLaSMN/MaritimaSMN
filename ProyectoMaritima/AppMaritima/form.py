from django import forms
import datetime
from AppMaritima.models import *


class BoletinForm(forms.Form):
    
    CHOICESHORAS = (('0','0'),('12','12'),)
    
    valido = forms.DateTimeField(required=False,widget=forms.widgets.DateInput(attrs={'type': 'date'}))
    hora = forms.ChoiceField(label="Hora validez", required=True,widget=forms.Select, choices=CHOICESHORAS)





class AvisoForm(forms.Form):
    
    CHOICESTIPO = (('TEMPORAL','GALE'),
                   ('TEMPORAL FUERTE','SEVERE GALE'),('TEMPORAL MUY FUERTE','VIOLENT STORM'),)
    
    CHOICESDIR = (('SECTOR N','SECTOR N'),
                   ('SECTOR S','SECTOR S'),('SECTOR W','SECTOR W'),('SECTOR E','SECTOR E'),)
    

    CHOICESHORAS = ((' ',' '),('0','0'),
                   ('3','3'),('6','6'),('9','9'), ('12','12'),('15','15'),('18','18'),('21','21'))
   
    
    
    tipo = forms.ChoiceField(widget=forms.Select, choices=CHOICESTIPO)
    direccion = forms.ChoiceField(widget=forms.Select, choices=CHOICESDIR)
    
    desde = forms.DateTimeField(required=False,widget=forms.widgets.DateInput(attrs={'type': 'date'}))
    horaDesde = forms.ChoiceField(label="Hora (desde)", required=False,widget=forms.Select, choices=CHOICESHORAS)
    hasta = forms.DateTimeField(required=False, widget=forms.widgets.DateInput(attrs={'type': 'date'}))
    
    
    
    horaHasta = forms.ChoiceField(label="Hora (hasta)", required=False,widget=forms.Select, choices=CHOICESHORAS)
    
    
    
    area = forms.ModelMultipleChoiceField(
        queryset=Area.objects.all(),
        widget=forms.CheckboxSelectMultiple
    )