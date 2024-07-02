

from django.http.response import HttpResponse
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.contrib import messages
from django.db import transaction


from AppMaritima.funciones import cargarAreasDesdeElXML, cargarPronosticosDesdeElXML, enviarMail

from AppMaritima.form import AvisoForm, BoletinForm,SituacionForm,SituacionFormUpdate,AvisoFormUpdate, HieloForm, HieloFormUpdate


from AppMaritima.models import *
from django.views.generic.edit import FormView

#Para hacer CBV
from django.views.generic import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import  UpdateView, DeleteView


from django.contrib.admin.views.decorators import staff_member_required

from django.contrib.auth.mixins import LoginRequiredMixin

from django.contrib.auth.models import User






#VISTAS genericas

def editor(request):
    
    

    return render(request, 'AppMaritima/editor.html')


def inicio(request):
    
    
    #return HttpResponse("Esto es una prueba del inicio")
    return render(request, 'AppMaritima/inicio.html')


def escaterometro(request):
    
    
    
    return render(request, 'AppMaritima/escaterometro.html')


def bordeDeHielos(request):
    
    
    
    return render(request, 'AppMaritima/borde.html')



#Carga los pronosticos de cada area al ultimo bolerin
def cargarPronosticos(idBoletin):
    
    #Los pronosticos los lee del xml de pimet. 
    #habria que hacer que el xml tenga el nombre segun el día del pronostico
    #y validar que se está cargando el pronostico del día. 
    archivo = "xmlPIMET/prueba.xml"
    
    #Función que genera los textos en ingles para cada area y asigna los pronos al boletín que se creo. 
    #print("QUIERO CARGAR LOS PRONOSTICOS EN EL BOLETIN: ID:" ,idBoletin)
    lista_areas_candidatas_temporal = cargarPronosticosDesdeElXML(archivo, idBoletin)
    
    #Guardo las areas posibles, por si las uso más adelante. No creo que sea objetivo implementarlo o persistirlo
    f = open (f"xmlPIMET/lista_areas_candidatas_temporal.txt",'w')  
    if (lista_areas_candidatas_temporal):  
        f.write("Areas candidatas para temporales: ")
        for a in lista_areas_candidatas_temporal:
            f.write("\n--> " +a.description )
    else:
        f.write("No hay areas candidatas para temporales.")
    f.close()
    


#CBV
##################################################################
##################### CRUD - Boletin #############################
##################################################################
class BoletinList(ListView):
    
    model = Boletin
    paginate_by = 4 #que solo muestre los ultimos 4
    template_name = "AppMaritima/boletin/boletines_list.html"
    
    ordering = ['-id'] #los ordeno por id
    
class BoletinListTodos(ListView):
    
    model = Boletin
    
    template_name = "AppMaritima/boletin/boletines_list.html"
    
    ordering = ['-id'] #los ordeno por id
    
def ultimoBoletin(request):
    
       try: 
        #id del Boletin 
        pk = ((Boletin.objects.all().order_by("-id"))[0]).id
        print("------>, el boletin : ", pk)

        return redirect(f"../boletin/{pk}")  
       except IndexError:
        diccionario = {"error": "No hay elementos para mostrar. Debe hacer el primer boletín."}
        return render(request, 'AppMaritima/inicio.html', diccionario)
             
 
       

    
class BoletinDetalle(DetailView):
    
    model = Boletin
    template_name = "AppMaritima/boletin/boletin_detalle.html"
    
    def get_context_data(self, **kwargs):
        
        #id del Boletin
        pk = int(self.kwargs['pk'])
        print("------>, el boletin : ", pk)
        # Obtengo el contexto
        context = super().get_context_data(**kwargs)
        
        # Envio al contexto, el detalle del boletin los avisos, situaciones y hielos del mismo
        # Ya sean activos o no. Así no se pierden los ceses
        context['avisosDelBoletin'] = Aviso.objects.filter(boletin = pk)
        
        #Los sistemas no me interesan una vez cesados, así que solo muestro el activo
        context['situacionesDelBoletin'] = Situacion.objects.filter(boletin = pk, activo = True)
        
        #Los hielos no me interesan una vez cesados, así que solo muestro el activo
        context['hielosDelBoletin'] = Hielo.objects.filter(boletin = pk, activo = True)
        
 
        return context
    
#Necesitas estar logueado para crearlo

class BoletinCreacion(LoginRequiredMixin, FormView):
    login_url = 'Login'
    template_name = "AppMaritima/boletin/boletin_form.html"
    form_class = BoletinForm
    #success_url = reverse_lazy("boletin/ultimo")
    success_url = "boletin/ultimo" 

    def form_valid(self, form):
        try:
            with transaction.atomic():
                boletin = Boletin(valido=form.cleaned_data.get("valido"), hora=int(form.cleaned_data.get("hora")))
                boletin.save()

                listaAvisosActivos = Aviso.objects.filter(activo=True)
                listaSituacionesActivas = Situacion.objects.filter(activo=True)
                hielosActivos = Hielo.objects.filter(activo=True)

                for h in hielosActivos:
                    h.boletin.add(boletin)
                    h.save()

                for aviso in listaAvisosActivos:
                    aviso.boletin.add(boletin)
                    aviso.save()

                for situacion in listaSituacionesActivas:
                    situacion.boletin.add(boletin)
                    situacion.save()

                print("Nuevo Boletin con ID: ", boletin.id)

                cargarPronosticos(boletin.id)

        except Exception as e:
            # Si ocurre una excepción, redirigir a una plantilla de error
            messages.error(self.request, "El archivo XML tiene faltante de información. Por favor vuelva a PIMET, recuerde cargar METAREA-VI, COSTAS y RIO DE LA PLATA.")
            return render(self.request, "AppMaritima/boletin/error_xml.html")

        #return redirect(self.success_url)
        return redirect("boletin/ultimo")   


class BoletinCreacion2(LoginRequiredMixin,FormView):
    
    login_url = 'Login'
   

    
    template_name = "AppMaritima/boletin/boletin_form.html"
    form_class = BoletinForm
    success_url = "boletin/ultimo" 
    
    def form_valid(self, form):
                    
                    
                    boletin = Boletin(valido = form.cleaned_data.get("valido"),hora = int(form.cleaned_data.get("hora")))
                   
                    boletin.save()
                    
                    #Ahora ademas le asigno todos los avisos activos, para que se puedan actualizar o cesar
                    listaAvisosActivos = Aviso.objects.filter(activo = True)
                    
                    #Ahora ademas le asigno todos lassituaciones , para que se puedan actualizar o cesaro borrar
                    listaSituacionesActivas = Situacion.objects.filter(activo = True)
                    
                    hielosActivos = Hielo.objects.filter(activo = True)
                    
                    for h in hielosActivos:
                        h.boletin.add(boletin)
                        h.save()
                        
                        
                    for aviso in listaAvisosActivos:
                        
                        
                        aviso.boletin.add(boletin)
                        aviso.save()
                        
                    for situacion in listaSituacionesActivas:
                        
                        
                        situacion.boletin.add(boletin)
                        situacion.save()
                    
                    print("Nuevo bOletin con ID: ", boletin.id) 
                    cargarPronosticos( boletin.id)   
                   
                    
                    return redirect("boletin/ultimo")    
                
                
    
    
  
class BoletinUpdate(UpdateView):
    
    model = Boletin
    success_url = "../boletin/list"
    template_name = "AppMaritima/boletin/boletin_form_update.html"
    fields = ["valido","hora"]
  

class BoletinDelete(DeleteView):
    
    model = Boletin
    template_name = "AppMaritima/boletin/boletin_confirm_delete.html"
    success_url = "../boletin/list"
    

    
    
#FIN - CRUD - Boletin


##################################################################
##################### CRUD - AVISO   #############################
##################################################################
class AvisoList(ListView):
    
    model = Aviso
    template_name = "AppMaritima/aviso/avisos_list.html"
    
    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Add in a QuerySet of all the books
        context['avisos'] = Aviso.objects.filter(activo = True)
        return context
    
    
   
    
    
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
    
    
    avisoUltimo = Aviso.objects.all().order_by("-id")
    
    
    return avisoUltimo.id

class AvisoCreacion(FormView):
    
                template_name="AppMaritima/aviso/aviso_form.html"
                form_class = AvisoForm
                success_url = "boletin/list" 
                
                def get_context_data(self, **kwargs):
                    # Call the base implementation first to get a context
                    context = super().get_context_data(**kwargs)
                    # Add in a QuerySet of all the books
                    archivo = open("xmlPIMET/lista_areas_candidatas_temporal.txt")
                    texto = archivo.read()
                    archivo.close()
                    
                    context['tooltip'] = texto
                    return context
                
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
                    activo = True,
                    provoca = form.cleaned_data.get("provoca"),
                    navtex = False)
                    #boletin = Boletin.objects.all().order_by("-id")[0] 
                    
                    aviso.save()
                    
                    lista = form.cleaned_data.get("area")
                    
                    situacionQueLogenera = form.cleaned_data.get("situacion")
                    
                    for s in situacionQueLogenera:
                        aviso.situacion.add(s)
                    
                    entraAlNavtex = False
                    
                    for a in lista:
                        #Si las areas afectadas son de la costa, entra al navtex
                        if (a.domain == "Rio de la Plata" or a.domain == "Costas"):
                            entraAlNavtex = True
                        #Siempre agrego las areas, sean o no del navtex
                        aviso.area.add(a)
                        
                    #Si en verdad entraba lo actualizo
                    if(entraAlNavtex):
                        aviso.navtex = entraAlNavtex
                    
                    
                    #Le asigno el ultimo boletin
                    boletin = (Boletin.objects.all().order_by("-id")[0])
                    aviso.boletin.add(boletin)
                         
                    aviso.save()
                    
                    
                    
                    return redirect(f"boletin/{boletin.id}")
                    
                
class AvisoUpdate(FormView):
    
                template_name="AppMaritima/aviso/aviso_form_update.html"
                form_class = AvisoFormUpdate
                success_url = "boletin/list" 
                
                def get_context_data(self, **kwargs):
                    # Call the base implementation first to get a context
                    context = super().get_context_data(**kwargs)
                    # Add in a QuerySet of all the books
                    archivo = open("xmlPIMET/lista_areas_candidatas_temporal.txt")
                    texto = archivo.read()
                    archivo.close()
                    
                    context['tooltip'] = texto
                    return context
                
                
                def form_valid(self, form):
                    
                    #id del aviso a actualizar
                    pk = int(self.kwargs['pk'])
                    
                    avisoViejo =Aviso.objects.get(id=pk)
                   
                    
                    
                    #Si se cargo la hora la paso a entera, sino, -1
                    horaD = -1
                    horaH = -1
                    if form.cleaned_data.get("horaDesde") != ' ':
                        horaD  =int(form.cleaned_data.get("horaDesde"))
               
                        
                    if form.cleaned_data.get("horaHasta") != ' ':
                        
                        horaH  =int(form.cleaned_data.get("horaHasta"))

                  
                    
                    aviso = Aviso(id=ultimoID()+1,numero = avisoViejo.numero,
                    actualizacion =avisoViejo.actualizacion +1,
                    tipo = form.cleaned_data.get("tipo"),
                    direccion = form.cleaned_data.get("direccion"),
                    desde = form.cleaned_data.get("desde"),
                    horaDesde = horaD,
                    hasta = form.cleaned_data.get("hasta"),
                    horaHasta = horaH,
                    activo = True, 
                    provoca = form.cleaned_data.get("provoca"),
                    navtex = False)
                    #boletin = Boletin.objects.all().order_by("-id")[0] 
                    
                    
                    #Guardo la actualización
                    aviso.save()
                    
                    #Pongo inactivo el aviso desactualizado
                    avisoViejo.activo = False
                    avisoViejo.save()
                    
                    lista = form.cleaned_data.get("area")
                    
                    situacionQueLogenera = form.cleaned_data.get("situacion")
                    
                    for s in situacionQueLogenera:
                        aviso.situacion.add(s)
                    
                    
                    for a in lista:
                        aviso.area.add(a)
                        
                        
                    entraAlNavtex = False
                    
                    for a in lista:
                        #Si las areas afectadas son de la costa, entra al navtex
                        if (a.domain == "Rio de la Plata" or a.domain == "Costas"):
                            entraAlNavtex = True
                        #Siempre agrego las areas, sean o no del navtex
                        aviso.area.add(a)
                        
                    #Si en verdad entraba lo actualizo
                    if(entraAlNavtex):
                        aviso.navtex = entraAlNavtex
                    
                    #Le asigno el ultimo boletin
                    aviso.boletin.add(Boletin.objects.all().order_by("-id")[0])
                  
                    #Modifico el boletín con las areas asociadas
                    aviso.save()
                    
                    idBoletin = (Boletin.objects.all().order_by("-id")[0])
                    
                    return redirect(f"../boletin/{idBoletin.id}")       
            
          
def  cesarAviso(request,pk):
    
                   
                    
                    avisoViejo =Aviso.objects.get(id=pk)
                   
                    avisoViejo.activo = False
                    #GUardo el aviso cesado
                    avisoViejo.save()
                    
                   
                    
                    
                    return redirect(f"../aviso/list")    
    
    
    
  
class AvisoUpdateGenerico(UpdateView):
    
    model = Aviso
   
    success_url = "../boletin/list"
    template_name = "AppMaritima/aviso/aviso_form_update.html"
    fields = ["tipo", "direccion", "desde", "hasta", "boletin","area"]
  

class AvisoDelete(DeleteView):
    
    model = Aviso
    template_name = "AppMaritima/aviso/aviso_confirm_delete.html"
    success_url = "../aviso/list"
    
    
   
    
#FIN - CRUD - Aviso



##################################################################
##################### CRUD - Situacion ###########################
##################################################################

def ultimoSituacion():
    
    ultimo = 0
    situaciones = Situacion.objects.all()
    
    for a in situaciones:
        
        if a.numero > 0:
            ultimo = a.numero
    
    return ultimo 

def  cesarSituacion(request,pk):
    
                   
                    
                    situacionVieja =Situacion.objects.get(id=pk)
                   
                    situacionVieja.activo = False
                    #GUardo el aviso cesado
                    situacionVieja.save()
                    
            
                    
                    return redirect(f"../situacion/list")  
                
                
class SituacionList(ListView):
    
    model = Situacion
    template_name = "AppMaritima/situacion/situaciones_list.html"
    
    
    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Add in a QuerySet of all the books
        context['situaciones'] = Situacion.objects.filter(activo = True)
        return context
    
    
   
    
    
class SituacionDetalle(DetailView):
    
    model = Situacion
    template_name = "AppMaritima/situacion/situacion_detalle.html"




class SituacionCreacion(FormView):
    
                template_name="AppMaritima/situacion/situacion_form.html"
                form_class = SituacionForm
                success_url = "situacion/list" 
                
               
                
                
                def form_valid(self, form):
                    
                    
                     
                    print(form.cleaned_data)
                    #Si se cargo la hora la paso a entera, sino, NULL
                    valorI = -1
                    horaI = -1
                    horaH = -1
                    
                    
                    
                    if not (form.cleaned_data.get("valorInicial") is None):
                        valorI = int (form.cleaned_data.get("valorInicial"))
                    
                    if form.cleaned_data.get("horaInicial") != ' ':
                        
                        horaI  = int(form.cleaned_data.get("horaInicial"))
                        
                    if form.cleaned_data.get("horaFinal") != ' ':
                        
                        horaH  =int(form.cleaned_data.get("horaFinal"))
                        
                        

                    situacion = Situacion(
                       numero = ultimoSituacion() + 1,
                       actualizacion = 0,
                       sistema =  form.cleaned_data.get("sistema"),
                       valorInicial =  valorI,
                       movimiento =  form.cleaned_data.get("movimiento"),
                       evolucion =  form.cleaned_data.get("evolucion"),
                       posicionInicial =  form.cleaned_data.get("posicionInicial"),
                       momentoInicial =  form.cleaned_data.get("momentoInicial"),
                       horaInicial = horaI,
                       posicionFinal =  form.cleaned_data.get("posicionFinal"),
                       momentoFinal =  form.cleaned_data.get("momentoFinal"),
                       horaFinal =  horaH,
                       navtex =  form.cleaned_data.get("navtex")=="Incluir",
                       esPresente=  form.cleaned_data.get("esPresente")=="Es presente",
                       activo = True
                        
                        
                    )
                    
                  
                  
                    situacion.save()
                    
                    boletin =  (Boletin.objects.all().order_by("-id"))[0]
                    
                    situacion.boletin.add(boletin)
                    
                    situacion.save()
                    
                    return redirect("situacion/list")
                


class SituacionUpdate(FormView):
    
                template_name="AppMaritima/situacion/situacion_form_update.html"
                form_class = SituacionFormUpdate
                success_url = "situacion/list" 
                
               
                
                
                def form_valid(self, form):
                    
                    
                    #id de la situación a actualizar
                    pk = int(self.kwargs['pk'])
                    
                    situacionVieja =Situacion.objects.get(id=pk)
                     
                    print(f"ID DE LA SITUACIÖN QUE VOY A ACTUALIZAR {pk}")
                    print(form.cleaned_data)
                    
                    #Si se cargo la hora la paso a entera, sino, NULL
                    valorI = -1
                    horaI = -1
                    horaH = -1
                    
                    
                    
                    if not (form.cleaned_data.get("valorInicial") is None):
                        valorI = int (form.cleaned_data.get("valorInicial"))
                    
                    if form.cleaned_data.get("horaInicial") != ' ':
                        
                        horaI  = int(form.cleaned_data.get("horaInicial"))
                        
                    if form.cleaned_data.get("horaFinal") != ' ':
                        
                        horaH  =int(form.cleaned_data.get("horaFinal"))
                        
                        

                    situacion = Situacion(
                       numero = situacionVieja.numero,
                       actualizacion =situacionVieja.actualizacion +1,
                       sistema =  form.cleaned_data.get("sistema"),
                       valorInicial =  valorI,
                       movimiento =  form.cleaned_data.get("movimiento"),
                       evolucion =  form.cleaned_data.get("evolucion"),
                       posicionInicial =  form.cleaned_data.get("posicionInicial"),
                       momentoInicial =  form.cleaned_data.get("momentoInicial"),
                       horaInicial = horaI,
                       posicionFinal =  form.cleaned_data.get("posicionFinal"),
                       momentoFinal =  form.cleaned_data.get("momentoFinal"),
                       horaFinal =  horaH,
                       navtex =  form.cleaned_data.get("navtex")=="Incluir",
                       esPresente=  form.cleaned_data.get("esPresente")=="Es presente",
                       activo = True
                        
                        
                    )
                    
                  
                  
                    situacion.save()
                    
                    #Pongo inactivo el aviso desactualizado
                    print(situacionVieja)
                    situacionVieja.activo = False
                    situacionVieja.save()
                    
                    boletin =  (Boletin.objects.all().order_by("-id"))[0]
                    
                    situacion.boletin.add(boletin)
                    
                    situacion.save()
                    
                    return redirect("../situacion/list")
                    
                    
                
             
            
          


class SituacionDelete(DeleteView):
    
    model = Situacion
    template_name = "AppMaritima/situacion/situacion_confirm_delete.html"
    success_url = "../situacion/list"
    
    
   
    
#FIN - CRUD - Situacion

##################################################################
##################### CRUD - Hiel o #############################
##################################################################

class HieloList(ListView):
    
    model = Hielo
    template_name = "AppMaritima/hielo/hielos_list.html"
    
    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Add in a QuerySet of all the books
        context['hielos'] = Hielo.objects.filter(activo = True)
        return context
    
    
   
    
    
class HieloDetalle(DetailView):
    
    model = Hielo
    template_name = "AppMaritima/hielo/hielo_detalle.html"


def ultimoHielo():
    
    ultimo = 0
    hielos = Hielo.objects.all()
    
    for a in hielos:
        
        if a.numero > 0:
            ultimo = a.numero
    
    return ultimo   


def ultimoID():
    
    
    hieloUltimo = Hielo.objects.all().order_by("-id")[0]
    
    
    return hieloUltimo.id

class HieloCreacion(FormView):
    
                template_name="AppMaritima/hielo/hielo_form.html"
                form_class = HieloForm
                success_url = "boletin/list" 
                
                
                
                
                def form_valid(self, form):
                    
                    
                
                   
                    
                    hielo = Hielo(
                    texto = form.cleaned_data.get("texto"),
                  
                    activo = True)
                    #boletin = Boletin.objects.all().order_by("-id")[0] 
                    
                    hielo.save()
                    
                    
                    #Le asigno el ultimo boletin
                    hielo.boletin.add(Boletin.objects.all().order_by("-id")[0])
                         
                    hielo.save()
                    
                    idBoletin = (Boletin.objects.all().order_by("-id")[0])
                    
                    return redirect(f"boletin/{idBoletin.id}")
                    
                
class HieloUpdate(FormView):
    
                template_name="AppMaritima/hielo/hielo_form_update.html"
                form_class = HieloFormUpdate
                success_url = "boletin/list" 
                
                
                
                
                def form_valid(self, form):
                    
                    #id del hielo a actualizar
                    pk = int(self.kwargs['pk'])
                    
                    hieloViejo =Hielo.objects.get(id=pk)
                   
                    
                    
                    hielo = Hielo(id=ultimoID()+1,
                    texto = form.cleaned_data.get("texto"),
                    
                    activo = True)
                    #boletin = Boletin.objects.all().order_by("-id")[0] 
                    
                    
                    #Guardo la actualización
                    hielo.save()
                    
                    #Pongo inactivo el hielo desactualizado
                    hieloViejo.activo = False
                    hieloViejo.save()
                    
                    
                    
                    #Le asigno el ultimo boletin
                    hielo.boletin.add(Boletin.objects.all().order_by("-id")[0])
                  
                    #Modifico el boletín con las areas asociadas
                    hielo.save()
                    
                    idBoletin = (Boletin.objects.all().order_by("-id")[0])
                    
                    return redirect(f"../boletin/{idBoletin.id}")       
            
          
def  cesarHielo(request,pk):
    
                   
                    
                    hieloViejo =Hielo.objects.get(id=pk)
                   
                    hieloViejo.activo = False
                    #GUardo el hielo cesado
                    hieloViejo.save()
                    
                   
                    
                    
                    return redirect(f"../hielo/list")    
    
    
    
  
class HieloUpdateGenerico(UpdateView):
    
    model = Hielo
   
    success_url = "../boletin/list"
    template_name = "AppMaritima/hielo/hielo_form_update.html"
    fields = ["texto"]
  

class HieloDelete(DeleteView):
    
    model = Hielo
    template_name = "AppMaritima/hielo/hielo_confirm_delete.html"
    success_url = "../hielo/list"
    

#FIN - CRUD - Hielo


