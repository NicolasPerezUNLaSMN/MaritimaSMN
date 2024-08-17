from email.policy import default
from pickle import TRUE
from django import forms
import datetime
from AppMaritima.models import *


class BoletinForm(forms.Form):
    
    CHOICESHORAS = (('0','0'),('12','12'),)
    
    valido = forms.DateTimeField(required=False,widget=forms.widgets.DateInput(attrs={'type': 'date'}))
    hora = forms.ChoiceField(label="Hora validez", required=True,widget=forms.Select, choices=CHOICESHORAS)


    pronosticosOlasSHN = forms.CharField(required=False,widget=forms.Textarea(attrs={"class":"form-control"}))


class GroupedModelMultipleChoiceField(forms.ModelMultipleChoiceField):
    def __init__(self, *args, **kwargs):
        self.group_by_field = kwargs.pop('group_by_field', None)
        super(GroupedModelMultipleChoiceField, self).__init__(*args, **kwargs)
    
    def label_from_instance(self, obj):
        if self.group_by_field:
            return f"{getattr(obj, self.group_by_field)} - {obj.description}"
        return super(GroupedModelMultipleChoiceField, self).label_from_instance(obj)

    def _get_choices(self):
        choices = super(GroupedModelMultipleChoiceField, self)._get_choices()
        if self.group_by_field:
            grouped_choices = {}
            for obj in self.queryset:
                key = getattr(obj, self.group_by_field)
                if key not in grouped_choices:
                    grouped_choices[key] = []
                grouped_choices[key].append((obj.pk, self.label_from_instance(obj)))
            final_choices = []
            for group, items in grouped_choices.items():
                final_choices.append((group, items))
            return final_choices
        return choices

    choices = property(_get_choices, forms.ModelMultipleChoiceField._set_choices)



class AvisoForm(forms.Form):

    CHOICESPROVOCA = (('PROVOKES','PROVOCA'),
                        ('WILL PROVOKE','PROVOCARÁ'),)
    
    CHOICESTIPO = (('NEAR GALE FORCE','RAFAGAS DE TEMPORAL (7)'),('GALE FORCE','TEMPORAL (8y9)'),
                   ('STORM FORCE','TEMPORAL FUERTE (10y11)' ),('HURRICANE FORCE','TEMPORAL MUY FUERTE (+11)'),)
    
    CHOICESDIR = (('SECTOR N','SECTOR N'),
                   ('SECTOR S','SECTOR S'),('SECTOR W','SECTOR W'),('SECTOR E','SECTOR E'), ('NW','NW'), ('SW','SO'), ('SE','SE'), ('NE','NE'),('N','N'),('S','S'),('W','W'),('E','E'),)
    

    CHOICESHORAS = ((' ',' '),('0','0'),
                   ('3','3'),('6','6'),('9','9'), ('12','12'),('15','15'),('18','18'),('21','21'))
   

    CHOICESSUR60= (('Es Sur 60','Es Sur 60'),("No Es Sur 60","No Es Sur 60"))

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
    
    sur60 = forms.ChoiceField(label="Es del boletín al S 60:", required=False,widget=forms.Select(attrs={"class":"form-control"}), choices=CHOICESSUR60)

    #area = forms.ModelMultipleChoiceField(
     #   queryset=Area.objects.filter(latitude__range=[-35, -58]).exclude(description__contains='COSTA' ).exclude(description__contains='GOLFO').exclude(domain__contains='Rio de la Plata' ).exclude(description__contains='DESEMBOCADURA').order_by("-domain", "description"), #Traigo todo menos al sur de 60, y no traigo las costas
     #   widget=forms.CheckboxSelectMultiple
    #)

    area = GroupedModelMultipleChoiceField(
        queryset=Area.objects.exclude(description__icontains="COSTA").exclude(description__contains='GOLFO').order_by('orden'),
        group_by_field='domain',
        widget=forms.CheckboxSelectMultiple,
        required=True
    )
    
    
class AvisoFormUpdate(forms.Form):
            
            CHOICESSUR60= (('Es Sur 60','Es Sur 60'),("No Es Sur 60","No Es Sur 60"))
    
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

            sur60 = forms.ChoiceField(label="Es del boletín al S 60:", required=False,widget=forms.Select(attrs={"class":"form-control"}), choices=CHOICESSUR60)
            
            area = forms.ModelMultipleChoiceField(
                queryset=Area.objects.filter(latitude__range=[-35, -58]).exclude(description__contains='COSTA' ).exclude(description__contains='GOLFO').exclude(domain__contains='Rio de la Plata' ).exclude(description__contains='DESEMBOCADURA').order_by("-domain", "description"), #Traigo todo menos al sur de 60, y no traigo las costas
                widget=forms.CheckboxSelectMultiple
            )
            
            
            
    
    
    
    
class SituacionForm(forms.Form):
    
    CHOICESFUTURO =(('Es presente','Es presente'),("Es a futuro","Es a futuro"))

    CHOICESNAVTEX= (('Incluir','Incluir'),("No incluir","No incluir"))
    CHOICESSUR60= (('Es Sur 60','Es Sur 60'),("No Es Sur 60","No Es Sur 60"))
      
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
    sur60 = forms.ChoiceField(label="Es del boletín al S 60:", required=False,widget=forms.Select(attrs={"class":"form-control"}), choices=CHOICESSUR60)

    esPresente = forms.ChoiceField(label="¿Es presente?:", required=False,widget=forms.Select(attrs={"class":"form-control"}), choices=CHOICESFUTURO)


class SituacionFormUpdate(forms.Form):

    CHOICESFUTURO =(('Es presente','Es presente'),("Es a futuro","Es a futuro"))
    CHOICESSUR60= (('Es Sur 60','Es Sur 60'),("No Es Sur 60","No Es Sur 60"))
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
    sur60 = forms.ChoiceField(label="Es del boletín al S 60:", required=False,widget=forms.Select(attrs={"class":"form-control"}), choices=CHOICESSUR60)

    esPresente = forms.ChoiceField(label="¿Es presente?:", required=False,widget=forms.Select(attrs={"class":"form-control"}), choices=CHOICESFUTURO)

class HieloForm(forms.Form):
    
  
    
    texto = forms.CharField(widget=forms.Textarea(attrs={"class":"form-control"}))
    
    
    
class HieloFormUpdate(forms.Form):
    
            texto = forms.CharField(widget=forms.Textarea(attrs={"class":"form-control"}))
          
            
            
            
            
