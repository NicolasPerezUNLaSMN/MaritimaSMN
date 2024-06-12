from email.policy import default
from pickle import TRUE
from django import forms
import datetime
from AppMaritima.models import *


class BoletinForm(forms.Form):
    
    CHOICESHORAS = (('0','0'),('12','12'),)
    
    valido = forms.DateTimeField(required=False,widget=forms.widgets.DateInput(attrs={'type': 'date'}))
    hora = forms.ChoiceField(label="Hora validez", required=True,widget=forms.Select, choices=CHOICESHORAS)





class AvisoForm(forms.Form):

    CHOICESPROVOCA = (('PROVOKE','PROVOCA'),
                        ('PROVOKES','PROVOCARÁ'),)
    
    CHOICESTIPO = (('GALE','TEMPORAL'),
                   ('SEVERE GALE','TEMPORAL FUERTE'),('VIOLENT STORM','TEMPORAL MUY FUERTE'),)
    
    CHOICESDIR = (('SECTOR N','SECTOR N'),
                   ('SECTOR S','SECTOR S'),('SECTOR W','SECTOR W'),('SECTOR E','SECTOR E'),)
    

    CHOICESHORAS = ((' ',' '),('0','0'),
                   ('3','3'),('6','6'),('9','9'), ('12','12'),('15','15'),('18','18'),('21','21'))
   
    situacion = forms.ModelMultipleChoiceField(
        queryset=Situacion.objects.filter(activo=True), #solo situaciones activas
        widget=forms.CheckboxSelectMultiple
    )
    
    provoca = forms.ChoiceField(widget=forms.Select(attrs={"class":"form-control"}), choices=CHOICESPROVOCA)
    
    tipo = forms.ChoiceField(widget=forms.Select(attrs={"class":"form-control"}), choices=CHOICESTIPO)
    direccion = forms.ChoiceField(widget=forms.Select(attrs={"class":"form-control"}), choices=CHOICESDIR)
    
    desde = forms.DateTimeField(required=False,widget=forms.widgets.DateInput(attrs={'type': 'date',"class":"form-control"}))
    horaDesde = forms.ChoiceField(label="Hora (desde)", required=False,widget=forms.Select(attrs={"class":"form-control"}), choices=CHOICESHORAS)
    hasta = forms.DateTimeField(required=False, widget=forms.widgets.DateInput(attrs={'type': 'date',"class":"form-control"}))
    
    
    
    horaHasta = forms.ChoiceField(label="Hora (hasta)", required=False,widget=forms.Select(attrs={"class":"form-control"}), choices=CHOICESHORAS)
    
    
    
    area = forms.ModelMultipleChoiceField(
        queryset=Area.objects.filter(latitude__range=[-35, -58]).exclude(description__contains='COSTA' ).exclude(description__contains='GOLFO').exclude(domain__contains='Rio de la Plata' ).exclude(description__contains='DESEMBOCADURA').order_by("-domain", "description"), #Traigo todo menos al sur de 60, y no traigo las costas
        widget=forms.CheckboxSelectMultiple
    )
    
    
class AvisoFormUpdate(forms.Form):
    
            CHOICESPROVOCA = (('PROVOKE','PROVOCA'),
                        ('PROVOKES','PROVOCARÁ'),)
    
            CHOICESTIPO = (('GALE','TEMPORAL'),
                        ('SEVERE GALE','TEMPORAL FUERTE'),('VIOLENT STORM','TEMPORAL MUY FUERTE'),)
            
            CHOICESDIR = (('SECTOR N','SECTOR N'),
                        ('SECTOR S','SECTOR S'),('SECTOR W','SECTOR W'),('SECTOR E','SECTOR E'),)
            

            CHOICESHORAS = ((' ',' '),('0','0'),
                        ('3','3'),('6','6'),('9','9'), ('12','12'),('15','15'),('18','18'),('21','21'))

            #CHOICESACTIVO= (('Activo','Activo'),("Cesar","Cesar"))
            situacion = forms.ModelMultipleChoiceField(
                queryset=Situacion.objects.filter(activo=True), #solo situaciones activas
                widget=forms.CheckboxSelectMultiple
                 )
            
            provoca = forms.ChoiceField(widget=forms.Select(attrs={"class":"form-control"}), choices=CHOICESPROVOCA)
            
            
            tipo = forms.ChoiceField(widget=forms.Select(attrs={"class":"form-control"}), choices=CHOICESTIPO)
            direccion = forms.ChoiceField(widget=forms.Select(attrs={"class":"form-control"}), choices=CHOICESDIR)
            
            
            
            
            desde = forms.DateTimeField(required=False,widget=forms.widgets.DateInput(attrs={'type': 'date',"class":"form-control"}))
            horaDesde = forms.ChoiceField(label="Hora (desde)", required=False,widget=forms.Select(attrs={"class":"form-control"}), choices=CHOICESHORAS)
            hasta = forms.DateTimeField(required=False, widget=forms.widgets.DateInput(attrs={'type': 'date',"class":"form-control"}))
            
            
            
            horaHasta = forms.ChoiceField(label="Hora (hasta)", required=False,widget=forms.Select(attrs={"class":"form-control"}), choices=CHOICESHORAS)
            
            #activo = forms.ChoiceField(label="¿Está activo?",widget=forms.Select(attrs={"class":"form-control"}), choices=CHOICESACTIVO)
            
            area = forms.ModelMultipleChoiceField(
                queryset=Area.objects.filter(latitude__range=[-35, -58]).exclude(description__contains='COSTA' ).exclude(description__contains='GOLFO').exclude(domain__contains='Rio de la Plata' ).exclude(description__contains='DESEMBOCADURA').order_by("-domain", "description"), #Traigo todo menos al sur de 60, y no traigo las costas
                widget=forms.CheckboxSelectMultiple
            )
            
            
            
    
    
    
    
class SituacionForm(forms.Form):
    
    CHOICESNAVTEX= (('Incluir','Incluir'),("No incluir","No incluir"))
      
    CHOICESTIPO = (('HIGH','ANTICICLON'),
                   ('LOW','DEPRESION'),('CFNT','FRENTE FRIO'),('WFNT','FRENTE CALIENTE'),('OCCLUDED','FRENTE OCLUIDO'),('CYCLOGENESIS','CICLOGENESIS'),('STRONG GRADIENT','FUERTE GRADIENTE BARICO'),('RIDGE','EJE DE CUÑA'),('TROUGH','EJE DE VAGUADA'))
    
    CHOICESMOV = (('N','N'),('NE','NE'),
                   ('E','E'),('SE','SE'),('S','S'), ('SW','SW'),('W','W'),('NW','NW'))
   
    CHOICESEVO = (('DPN','DEBILITANDOSE'),('INTSF','INTENSIFICANDOSE'))
   

    CHOICESHORAS = ((' ',' '),('0','0'),
                   ('3','3'),('6','6'),('9','9'), ('12','12'),('15','15'),('18','18'),('21','21'))
   
    
    
    sistema = forms.ChoiceField(label="Sistema",required=True, widget=forms.Select(attrs={"class":"form-control"}), choices=CHOICESTIPO)
    valorInicial = forms.IntegerField(label="Valor",required=False, widget=forms.NumberInput(attrs={"class":"form-control"}))
  
   
    movimiento  = forms.ChoiceField(label="Movimiento", required=False,widget=forms.Select(attrs={"class":"form-control"}), choices=CHOICESMOV)
    evolucion  = forms.ChoiceField(label="Evolución", required=False,widget=forms.Select(attrs={"class":"form-control"}), choices=CHOICESEVO)
    
    posicionInicial= forms.CharField(label="Posición inicial",max_length=60, required=False,widget=forms.TextInput(attrs={"class":"form-control",'placeholder': 'SS-WW,SS-WW,.....,SS-WW'}))
    momentoInicial= forms.DateTimeField(label="Dia inicial",required=False, widget=forms.widgets.DateInput(attrs={'type': 'date',"class":"form-control"}))
    horaInicial = forms.ChoiceField(label="Hora inicial", required=False,widget=forms.Select(attrs={"class":"form-control"}), choices=CHOICESHORAS)
    
    posicionFinal = forms.CharField(label="Posición inicial",max_length=60, required=False,widget=forms.TextInput(attrs={"class":"form-control",'placeholder': 'SS-WW,SS-WW,......,SS-WW'}))
    momentoFinal= forms.DateTimeField(label="Dia final",required=False, widget=forms.widgets.DateInput(attrs={'type': 'date',"class":"form-control"}))
    horaFinal = forms.ChoiceField(label="Hora final", required=False,widget=forms.Select(attrs={"class":"form-control"}), choices=CHOICESHORAS)
    
    navtex = forms.ChoiceField(label="Incluir en navtex", required=False,widget=forms.Select(attrs={"class":"form-control"}), choices=CHOICESNAVTEX)
    
    
    

class HieloForm(forms.Form):
    
  
    
    texto = forms.CharField(widget=forms.Textarea(attrs={"class":"form-control"}))
    
    
    
class HieloFormUpdate(forms.Form):
    
            texto = forms.CharField(widget=forms.Textarea(attrs={"class":"form-control"}))
          
            
            
            
            
            