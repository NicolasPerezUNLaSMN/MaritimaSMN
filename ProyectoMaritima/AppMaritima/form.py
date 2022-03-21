from email.policy import default
from django import forms
import datetime
from AppMaritima.models import *


class BoletinForm(forms.Form):
    
    CHOICESHORAS = (('0','0'),('12','12'),)
    
    valido = forms.DateTimeField(required=False,widget=forms.widgets.DateInput(attrs={'type': 'date'}))
    hora = forms.ChoiceField(label="Hora validez", required=True,widget=forms.Select, choices=CHOICESHORAS)





class AvisoForm(forms.Form):
    
    CHOICESTIPO = (('GALE','TEMPORAL'),
                   ('SEVERE GALE','TEMPORAL FUERTE'),('VIOLENT STORM','TEMPORAL MUY FUERTE'),)
    
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
    
    
    
class SituacionForm(forms.Form):
    
    
      
    CHOICESTIPO = (('HIGH','ANTICICLON'),
                   ('LOW','DEPRESION'),('CFNT','FRENTE FRIO'),('WFNT','FRENTE CALIENTE'),('OCCLUDED','FRENTE OCLUIDO'),('CYCLOGENESIS','CICLOGENESIS'),('STRONG GRADIENT','FUERTE GRADIENTE BARICO'),('RIDGE','EJE DE CUÑA'),('TROUGH','EJE DE VAGUADA'))
    
    CHOICESMOV = (('N','N'),('NE','NE'),
                   ('E','E'),('SE','SE'),('S','S'), ('SW','SW'),('W','W'),('NW','NW'))
   
    CHOICESEVO = (('DPN','DEBILITANDOSE'),('INTSF','INTENSIFICANDOSE'))
   

    CHOICESHORAS = ((' ',' '),('0','0'),
                   ('3','3'),('6','6'),('9','9'), ('12','12'),('15','15'),('18','18'),('21','21'))
   
    
    
    sistema = forms.ChoiceField(required=True, widget=forms.Select, choices=CHOICESTIPO)
    valorInicial = forms.IntegerField(required=False)
  
   
    movimiento  = forms.ChoiceField(label="Movimiento", required=False,widget=forms.Select, choices=CHOICESMOV)
    evolucion  = forms.ChoiceField(label="Evolución", required=False,widget=forms.Select, choices=CHOICESEVO)
    
    posicionInicial= forms.CharField(max_length=60, required=False)
    momentoInicial= forms.DateTimeField(label="Dia inicial",required=False, widget=forms.widgets.DateInput(attrs={'type': 'date'}))
    horaInicial = forms.ChoiceField(label="Hora inicial", required=False,widget=forms.Select, choices=CHOICESHORAS)
    
    posicionFinal = forms.CharField(max_length=60, required=False)
    momentoFinal= forms.DateTimeField(label="Dia final",required=False, widget=forms.widgets.DateInput(attrs={'type': 'date'}))
    horaFinal = forms.ChoiceField(label="Hora final", required=False,widget=forms.Select, choices=CHOICESHORAS)
    
    navtex = forms.BooleanField(required=False)
    
    
    
    