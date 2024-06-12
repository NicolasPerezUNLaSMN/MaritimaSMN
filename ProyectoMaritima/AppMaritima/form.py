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

    CHOICESPROVOCA = (('PROVOKES','PROVOCA'),
                        ('WILL PROVOKE','PROVOCARÁ'),)
    
    CHOICESTIPO = (('NEAR GALE FORCE','RAFAGAS DE TEMPORAL (7)'),('GALE FORCE','TEMPORAL (8y9)'),
                   ('STORM FORCE','TEMPORAL FUERTE (10y11)' ),('HURRICANE FORCE','TEMPORAL MUY FUERTE (+11)'),)
    
    CHOICESDIR = (('SECTOR N','SECTOR N'),
                   ('SECTOR S','SECTOR S'),('SECTOR W','SECTOR W'),('SECTOR E','SECTOR E'), ('NW','NW'), ('SW','SO'), ('SE','SE'), ('NE','NE'),('N','N'),('S','S'),('W','W'),('E','E'),)
    

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
    
            CHOICESPROVOCA = (('PROVOKES','PROVOCA'),
                        ('WILL PROVOKE','PROVOCARÁ'),)
    
            CHOICESTIPO = (('NEAR GALE FORCE','RAFAGAS DE TEMPORAL (7)'),('GALE FORCE','TEMPORAL (8y9)'),
                   ('STORM FORCE','TEMPORAL FUERTE (10y11)' ),('HURRICANE FORCE','TEMPORAL MUY FUERTE (+11)'),)
    
            CHOICESDIR = (('SECTOR N','SECTOR N'),
                   ('SECTOR S','SECTOR S'),('SECTOR W','SECTOR W'),('SECTOR E','SECTOR E'), ('NW','NW'), ('SW','SW'), ('SE','SE'), ('NE','NE'),('N','N'),('S','S'),('W','W'),('E','E'),)
    
            

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
    
    CHOICESFUTURO =(('Es presente','Es presente'),("Es a futuro","Es a futuro"))

    CHOICESNAVTEX= (('Incluir','Incluir'),("No incluir","No incluir"))
      
    CHOICESTIPO = (('HIGH PRESSURE','ANTICICLON'),('LOW PRESSURE','DEPRESION'),('SECUNDARY LOW PRESSURE','DEPRESION SECUNDARIA'),('CYCLOGENESIS','CICLOGENESIS'),
                   ('COLD FRONT','FRENTE FRIO'),('STATIONARY FRONT','FRENTE ESTACIONARIO'),('WARM FRONT','FRENTE CALIENTE'),('OCCLUSION','FRENTE OCLUIDO'),
                   ('STRONG GRADIENT','FUERTE GRADIENTE BARICO'),('RIDGE','EJE DE CUÑA'),
                   ('TROUGH','EJE DE VAGUADA'),('FRONTAL WAVE','ONDA FRONTAL'),('STRONG FLOW','FUERTE FLUJO'))
    
    CHOICESMOV = (('NOT MOV', 'SIN MOVIMIENTO'),('N','N'),('NE','NE'),
                   ('E','E'),('SE','SE'),('S','S'), ('SW','SW'),('W','W'),('NW','NW'))
   
    CHOICESEVO = (('WITHOUT CHANGES','SIN CAMBIOS'),('WEAKENING','DEBILITANDOSE'),('INTENSIFYING','INTENSIFICANDOSE'),('IDEEPENING','PROFUNDIZANDOSE'))
   

    CHOICESHORAS = ((' ',' '),('0','0'),
                   ('3','3'),('6','6'),('9','9'), ('12','12'),('15','15'),('18','18'),('21','21'))
   
    
    
    sistema = forms.ChoiceField(label="Sistema",required=True, widget=forms.Select(attrs={"class":"form-control"}), choices=CHOICESTIPO)
    valorInicial = forms.IntegerField(label="Valor",required=False, widget=forms.NumberInput(attrs={"class":"form-control"}))
  
   
    movimiento  = forms.ChoiceField(label="Movimiento", required=False,widget=forms.Select(attrs={"class":"form-control"}), choices=CHOICESMOV)
    evolucion  = forms.ChoiceField(label="Evolución", required=False,widget=forms.Select(attrs={"class":"form-control"}), choices=CHOICESEVO)
    
    posicionInicial= forms.CharField(label="Posición inicial",max_length=60, required=False,widget=forms.TextInput(attrs={"class":"form-control",'placeholder': 'SS-WW,SS-WW,.....,SS-WW'}))
    momentoInicial= forms.DateTimeField(label="Dia inicial",required=False, widget=forms.widgets.DateInput(attrs={'type': 'date',"class":"form-control"}))
    horaInicial = forms.ChoiceField(label="Hora inicial", required=False,widget=forms.Select(attrs={"class":"form-control"}), choices=CHOICESHORAS)
    
    posicionFinal = forms.CharField(label="Posición final",max_length=60, required=False,widget=forms.TextInput(attrs={"class":"form-control",'placeholder': 'SS-WW,SS-WW,......,SS-WW'}))
    momentoFinal= forms.DateTimeField(label="Dia final",required=False, widget=forms.widgets.DateInput(attrs={'type': 'date',"class":"form-control"}))
    horaFinal = forms.ChoiceField(label="Hora final", required=False,widget=forms.Select(attrs={"class":"form-control"}), choices=CHOICESHORAS)
    
    navtex = forms.ChoiceField(label="Incluir en navtex", required=False,widget=forms.Select(attrs={"class":"form-control"}), choices=CHOICESNAVTEX)
    esPresente = forms.ChoiceField(label="¿Es presente?:", required=False,widget=forms.Select(attrs={"class":"form-control"}), choices=CHOICESFUTURO)
    
class SituacionFormUpdate(forms.Form):
    
    CHOICESNAVTEX= (('Incluir','Incluir'),("No incluir","No incluir"))

    CHOICESFUTURO =(('Es presente','Es presente'),("Es a futuro","Es a futuro"))
      
    CHOICESTIPO = (('HIGH PRESSURE','ANTICICLON'),('LOW PRESSURE','DEPRESION'),('SECUNDARY LOW PRESSURE','DEPRESION SECUNDARIA'),('CYCLOGENESIS','CICLOGENESIS'),
                   ('COLD FRONT','FRENTE FRIO'),('STATIONARY FRONT','FRENTE ESTACIONARIO'),('WARM FRONT','FRENTE CALIENTE'),('OCCLUSION','FRENTE OCLUIDO'),
                   ('STRONG GRADIENT','FUERTE GRADIENTE BARICO'),('RIDGE','EJE DE CUÑA'),
                   ('TROUGH','EJE DE VAGUADA'),('FRONTAL WAVE','ONDA FRONTAL'),('STRONG FLOW','FUERTE FLUJO'))
    
    CHOICESMOV = (('NOT MOV', 'SIN MOVIMIENTO'),('N','N'),('NE','NE'),
                   ('E','E'),('SE','SE'),('S','S'), ('SW','SW'),('W','W'),('NW','NW'))
   
    CHOICESEVO = (('WITHOUT CHANGES','SIN CAMBIOS'),('WEAKENING','DEBILITANDOSE'),('INTENSIFYING','INTENSIFICANDOSE'),('IDEEPENING','PROFUNDIZANDOSE'))
   

    CHOICESHORAS = ((' ',' '),('0','0'),
                   ('3','3'),('6','6'),('9','9'), ('12','12'),('15','15'),('18','18'),('21','21'))
   
    
    
    sistema = forms.ChoiceField(label="Sistema",required=True, widget=forms.Select(attrs={"class":"form-control"}), choices=CHOICESTIPO)
    valorInicial = forms.IntegerField(label="Valor",required=False, widget=forms.NumberInput(attrs={"class":"form-control"}))
  
   
    movimiento  = forms.ChoiceField(label="Movimiento", required=False,widget=forms.Select(attrs={"class":"form-control"}), choices=CHOICESMOV)
    evolucion  = forms.ChoiceField(label="Evolución", required=False,widget=forms.Select(attrs={"class":"form-control"}), choices=CHOICESEVO)
    
    posicionInicial= forms.CharField(label="Posición inicial",max_length=60, required=False,widget=forms.TextInput(attrs={"class":"form-control",'placeholder': 'SS-WW,SS-WW,.....,SS-WW'}))
    momentoInicial= forms.DateTimeField(label="Dia inicial",required=False, widget=forms.widgets.DateInput(attrs={'type': 'date',"class":"form-control"}))
    horaInicial = forms.ChoiceField(label="Hora inicial", required=False,widget=forms.Select(attrs={"class":"form-control"}), choices=CHOICESHORAS)
    
    posicionFinal = forms.CharField(label="Posición final",max_length=60, required=False,widget=forms.TextInput(attrs={"class":"form-control",'placeholder': 'SS-WW,SS-WW,......,SS-WW'}))
    momentoFinal= forms.DateTimeField(label="Dia final",required=False, widget=forms.widgets.DateInput(attrs={'type': 'date',"class":"form-control"}))
    horaFinal = forms.ChoiceField(label="Hora final", required=False,widget=forms.Select(attrs={"class":"form-control"}), choices=CHOICESHORAS)
    
    navtex = forms.ChoiceField(label="Incluir en navtex", required=False,widget=forms.Select(attrs={"class":"form-control"}), choices=CHOICESNAVTEX)


    esPresente = forms.ChoiceField(label="¿Es presente?:", required=False,widget=forms.Select(attrs={"class":"form-control"}), choices=CHOICESFUTURO)
    
    
    

class HieloForm(forms.Form):
    
  
    
    texto = forms.CharField(widget=forms.Textarea(attrs={"class":"form-control"}))
    
    
    
class HieloFormUpdate(forms.Form):
    
            texto = forms.CharField(widget=forms.Textarea(attrs={"class":"form-control"}))
          
            
            
            
            
            