from asyncio.constants import DEBUG_STACK_DEPTH
from asyncio.windows_events import NULL
from winreg import HKEY_PERFORMANCE_DATA
from django.http.response import HttpResponse
from django.shortcuts import redirect, render

from AppMaritima.funciones import leerXML,cargarAreasDesdeElXML

from AppMaritima.form import AvisoForm, BoletinForm


from AppMaritima.models import *
from django.views.generic.edit import FormView

#Para hacer CBV
from django.views.generic import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import  CreateView, UpdateView, DeleteView


# Create your views here.


#VISTAS

def inicio(request):
    
    
    
    return HttpResponse("Iniciandoo...")

#Ejectucarlo solo una vez, y con permisos de admin 
def cargarAreas(request):
    
    cargarAreasDesdeElXML()
    
    return HttpResponse("Areas cargadas")


#CBV

#CRUD - Boletin
class BoletinList(ListView):
    
    model = Boletin
    template_name = "AppMaritima/boletin/boletines_list.html"
    
    
class BoletinDetalle(DetailView):
    
    model = Boletin
    template_name = "AppMaritima/boletin/boletin_detalle.html"
    
    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Add in a QuerySet of all the books
        context['avisos'] = Aviso.objects.filter(activo = True)
        return context
    

class BoletinCreacion(FormView):
    

    
    template_name = "AppMaritima/boletin/boletin_form.html"
    form_class = BoletinForm
    success_url = "boletin/list" 
    
    def form_valid(self, form):
                    
                    
                    boletin = Boletin(valido = form.cleaned_data.get("valido"),hora = int(form.cleaned_data.get("hora")))
                   
                    boletin.save()
                    
                    #Ahora ademas le asigno todos los avisos activos, para que se puedan actualizar o cesar
                    listaAvisosActivos = Aviso.objects.filter(activo = True)
                    
                    for aviso in listaAvisosActivos:
                        
                        
                        aviso.boletin.add(boletin)
                        aviso.save()
                        
                       
                    
                    
                    return redirect("boletin/list")    
                
                
    
    
  
class BoletinUpdate(UpdateView):
    
    model = Boletin
    success_url = "../boletin/list"
    template_name = "AppMaritima/boletin/boletin_form.html"
    fields = ["valido"]
  

class BoletinDelete(DeleteView):
    
    model = Boletin
    template_name = "AppMaritima/boletin/boletin_confirm_delete.html"
    success_url = "../boletin/list"
    

    
    
#FIN - CRUD - Boletin


#CRUD - Aviso
class AvisoList(ListView):
    
    model = Aviso
    template_name = "AppMaritima/aviso/avisos_list.html"
    
    
   
    
    
class AvisoDetalle(DetailView):
    
    model = Aviso
    template_name = "AppMaritima/aviso/aviso_detalle.html"


def ultimoAviso():
    
    ultimo = 0
    avisos = Aviso.objects.all()
    
    for a in avisos:
        
        if a.numero > 0:
            ultimo = a.numero
    
    return ultimo   


def ultimoID():
    
    ultimo = 0
    avisoUltimo = Aviso.objects.all().order_by("id")[0]
    
    
    return avisoUltimo.id

class AvisoCreacion(FormView):
    
                template_name="AppMaritima/aviso/aviso_form.html"
                form_class = AvisoForm
                success_url = "boletin/list" 
                
                
                
                
                def form_valid(self, form):
                    
                    
                    
                    #Si se cargo la hora la paso a entera, sino, -1
                    horaD = -1
                    horaH = -1
                    if form.cleaned_data.get("horaDesde") != ' ':
                        horaD  =int(form.cleaned_data.get("horaDesde"))
               
                        
                    if form.cleaned_data.get("horaHasta") != ' ':
                        
                        horaH  =int(form.cleaned_data.get("horaHasta"))
              
                    
                    aviso = Aviso(numero = ultimoAviso() + 1,
                    actualizacion = 0,
                    tipo = form.cleaned_data.get("tipo"),
                    direccion = form.cleaned_data.get("direccion"),
                    desde = form.cleaned_data.get("desde"),
                    horaDesde = horaD,
                    hasta = form.cleaned_data.get("hasta"),
                    horaHasta = horaH,
                    activo = True)
                    #boletin = Boletin.objects.all().order_by("-id")[0] 
                    
                    aviso.save()
                    
                    lista = form.cleaned_data.get("area")
                    
                    
                    
                    for a in lista:
                        aviso.area.add(a)
                    
                    #Le asigno el ultimo boletin
                    aviso.boletin.add(Boletin.objects.all().order_by("id")[0])
                  
                    aviso.save()
                    
                    return redirect("aviso/list")
                    
                
             
            
          

    
    
    
  
class AvisoUpdate(UpdateView):
    
    model = Aviso
    success_url = "../boletin/list"
    template_name = "AppMaritima/aviso/aviso_form.html"
    fields = ["tipo", "direccion", "desde", "hasta", "boletin","area", "activo"]
  

class AvisoDelete(DeleteView):
    
    model = Aviso
    template_name = "AppMaritima/aviso/aviso_confirm_delete.html"
    success_url = "../aviso/list"
    
    
   
    
#FIN - CRUD - Boletin