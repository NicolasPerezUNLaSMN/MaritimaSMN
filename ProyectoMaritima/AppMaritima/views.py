
from cgi import print_arguments
from django.http.response import HttpResponse
from django.shortcuts import redirect, render


from AppMaritima.funciones import cargarAreasDesdeElXML, cargarPronosticosDesdeElXML

from AppMaritima.form import AvisoForm, BoletinForm,SituacionForm,AvisoFormUpdate, HieloForm, HieloFormUpdate


from AppMaritima.models import *
from django.views.generic.edit import FormView

#Para hacer CBV
from django.views.generic import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import  CreateView, UpdateView, DeleteView


# Create your views here.


#VISTAS genericas

def editor(request):
    
    

    return render(request, 'AppMaritima/editor.html')


def inicio(request):
    
    
    #return HttpResponse("Esto es una prueba del inicio")
    return render(request, 'AppMaritima/inicio.html')


def escaterometro(request):
    
    
    
    return render(request, 'AppMaritima/escaterometro.html')


#Ejectucarlo solo una vez, y con permisos de admin 
def cargarAreas(request):
    
    cantidadAreas =  Area.objects.all().count()
    print("------->", cantidadAreas)
    
    #Solo permite cargar areas cuando no hay nada en la base de datos
    #Esto lo podemos mejorar, actualizando. 
    if ( cantidadAreas == 0):
        
        archivo = "xmlPIMET/prueba.xml"
        cargarAreasDesdeElXML(archivo)
        return HttpResponse("Areas cargadas")
    
   
    return HttpResponse("No se cargaron las areas, ya estaban en la base")
    
    

#Carga los pronosticos de cada area al ultimo bolerin
def cargarPronosticos(idBoletin):
    
    #Los pronosticos los lee del xml de pimet. 
    #habria que hacer que el xml tenga el nombre segun el día del pronostico
    #y validar que se está cargando el pronostico del día. 
    archivo = "xmlPIMET/prueba.xml"
    
    #Función que genera los textos en ingles para cada area y asigna los pronos al boletín que se creo. 
    print("QUIERO CARGAR LOS PRONOSTICOS EN EL BOLETIN: ID:" ,idBoletin)
    cargarPronosticosDesdeElXML(archivo, idBoletin)
    
    return HttpResponse("Pronosticos cargados")



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
    
        
        #id del Boletin 
        pk = ((Boletin.objects.all().order_by("-id"))[0]).id
        print("------>, el boletin : ", pk)

        return redirect(f"../boletin/{pk}")  
 
       

    
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
    

class BoletinCreacion(FormView):
    

    
    template_name = "AppMaritima/boletin/boletin_form.html"
    form_class = BoletinForm
    success_url = "boletin/list" 
    
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

                    
                    return redirect("boletin/list")    
                
                
    
    
  
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
                    provoca = form.cleaned_data.get("provoca"))
                    #boletin = Boletin.objects.all().order_by("-id")[0] 
                    
                    aviso.save()
                    
                    lista = form.cleaned_data.get("area")
                    
                    situacionQueLogenera = form.cleaned_data.get("situacion")
                    
                    for s in situacionQueLogenera:
                        aviso.situacion.add(s)
                    
                    for a in lista:
                        aviso.area.add(a)
                    
                    #Le asigno el ultimo boletin
                    boletin = (Boletin.objects.all().order_by("-id")[0])
                    aviso.boletin.add(boletin)
                         
                    aviso.save()
                    
                    
                    
                    return redirect(f"boletin/{boletin.id}")
                    
                
class AvisoUpdate(FormView):
    
                template_name="AppMaritima/aviso/aviso_form_update.html"
                form_class = AvisoFormUpdate
                success_url = "boletin/list" 
                
                
                
                
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
                    provoca = form.cleaned_data.get("provoca"))
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
                       activo = True
                        
                        
                    )
                    
                  
                  
                    situacion.save()
                    
                    boletin =  (Boletin.objects.all().order_by("-id"))[0]
                    
                    situacion.boletin.add(boletin)
                    
                    situacion.save()
                    
                    return redirect("situacion/list")
                    
                
             
            
          

    
    
    
  
class SituacionUpdate(UpdateView):
    
    model = Situacion
    success_url = "../situacion/list"
    template_name = "AppMaritima/situacion/situacion_form.html"
    fields = ["sistema", "valorInicial", "movimiento", "evolucion", "posicionInicial","momentoInicial", "horaInicial","posicionFinal","momentoFinal", "horaFinal", "navtex" ]
  

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

##################################################################
##################### ESCRITURA DE tXT #############################
##################################################################
    
def crearTXT(request, pk):
    
    #Uso get porque es uno solo
    boletin = Boletin.objects.get(id = pk)
    
    avisos =  Aviso.objects.filter(boletin = pk)
  
    situaciones = Situacion.objects.filter(boletin = pk, activo = True)
        
    hielos = Hielo.objects.filter(boletin = pk, activo = True)
    
    pronosticosOffshore = Pronostico.objects.filter(boletin = pk, tipo = "Offshore")
    
    pronosticosMetarea = Pronostico.objects.filter(boletin = pk,tipo = "Metarea VI - N")
    
    #Encabezado "casi" fijo
    textoEnIngles = f"""FQST02 SABM {boletin.valido}{boletin.hora}
1:31:06:01:00 
SECURITE 
WEATHER BULLETIN ON METAREA VI
SMN ARGENTINA, {boletin.valido} AT {boletin.hora}UTC WIND SPEED IN BEAUFORT SCALE WAVES IN METERS
Please be aware wind gust can be a further 40 percent stronger than the averages 
and maximum waves may be up to twice the significant height, sea ice and icebergs issued by SHN
                    
PART 1 GALE WARNING\n"""
                    
    #Escritura de los avisos
    for a in avisos: 
        
        #Defino en un metodo del modelo la escritura de txt
        textoEnIngles = textoEnIngles +a.paraTXTEnIngles()
        
    #Escritura de las situaciones
    textoEnIngles = textoEnIngles +"\nPART 2 GENERAL SYNOPSIS\n"
    
    
    #Escribo los hielos, aún es uno solo
    
    for h in hielos:
        
        textoEnIngles = textoEnIngles +h.paraTXTEnIngles()
    textoEnIngles = textoEnIngles +"\n"
    
       
    for s in situaciones: 
        
        textoEnIngles = textoEnIngles +s.paraTXTEnIngles()
    textoEnIngles = textoEnIngles +"\n"
    
    
    #Escribo los pronosticos--- OJO en que orden los quieren poner!!!!!!
    textoEnIngles = textoEnIngles +"\nPART 3 FORECAST\n"
    for p in pronosticosOffshore:
        
        textoEnIngles = textoEnIngles +p.paraTXTEnIngles()
        
    for p in pronosticosMetarea:
        
        textoEnIngles = textoEnIngles +p.paraTXTEnIngles()
    #Cierre pedido por comunicaciones
    textoEnIngles = textoEnIngles + "-----------------------------------------------------------------\nNNNN="
    
    #Por si algo quedó mal lo paso todo a mayusculas
    textoEnIngles = textoEnIngles.upper()
    
    #Abro el archivo, escribo y lo cierro
    nombreArchivo = f"{boletin.valido}_{boletin.hora}.txt"
    f = open (f"txtGuardados/{nombreArchivo}",'w')
    f.write(textoEnIngles)
    f.close()
    
    texto = textoEnIngles
    
    diccionario = {"texto": texto, "nombreArchivo":nombreArchivo}

 
    return render(request, 'AppMaritima/editor.html', diccionario)