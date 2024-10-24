
from django.http.response import HttpResponse
from django.shortcuts import render
from AppMaritima.models import *
from django.db.models import Q


##################################################################
##################### ESCRITURA DE tXT #############################
##################################################################

#Vista que escribe todos los txt y los muestra en un html
def crearTXT(request, pk): 
    
    #Uso get porque es uno solo
    boletin = Boletin.objects.get(id = pk)
    
    avisos =  Aviso.objects.filter(boletin = pk)
  
    situaciones = Situacion.objects.filter(boletin = pk, activo = True,esPresente = True)
        
    hielos = Hielo.objects.filter(boletin = pk, activo = True)
    
    pronosticosOffshore = Pronostico.objects.filter(boletin = pk, tipo = "Offshore - N").order_by("area__orden")
    pronosticosOffshoreS = Pronostico.objects.filter(boletin = pk, tipo = "Offshore - S").order_by("area__orden")
    
    pronosticosMetarea = Pronostico.objects.filter(boletin = pk,tipo = "Metarea VI - N").order_by("area__orden")
    pronosticosMetareaS = Pronostico.objects.filter(boletin = pk,tipo = "Metarea VI - S").order_by("area__orden")

    pronosticosCostas = Pronostico.objects.filter(boletin = pk,tipo = "Costa").order_by("area__orden")
    
    avisosNavtex =  Aviso.objects.filter(boletin = pk, navtex = True)

    situacionesNavtex = Situacion.objects.filter(boletin = pk, activo = True, navtex = True, esPresente = True)
    
    #Envio toda la info
    #nortes
    textoAltamar = crearTXTnaveganteAltamar(boletin,avisos, situaciones,hielos,pronosticosMetarea) #:)
    textoOff = crearTXTnaveganteOffShore(boletin,avisosNavtex , situacionesNavtex,hielos,pronosticosOffshore)#:)

    textoCostas = crearTXTnaveganteCostas(boletin,avisosNavtex , situacionesNavtex,hielos,pronosticosCostas)


    #sures
    textoAltamarS = crearTXTnaveganteAltamarS(boletin,avisos, situaciones,hielos,pronosticosMetareaS)#:)
    textoOffS = crearTXTnaveganteOffShoreS(boletin,avisosNavtex , situacionesNavtex,hielos,pronosticosOffshoreS)#:)


    textoSupremo = crearTXTnaveganteSupremo(boletin,avisos, situaciones,hielos,pronosticosMetarea, pronosticosMetareaS, pronosticosOffshore, pronosticosOffshoreS) #:)


    array_navtex = crearTXTnavtex(boletin,avisosNavtex, situaciones,pronosticosOffshore)
    
    diccionario = {"textoAltamar":textoAltamar, "textoOff":textoOff, "textoAltamarS":textoAltamarS, "textoOffS":textoOffS, "textoCostas":textoCostas, "array_navtex": array_navtex, "textoSupremo":textoSupremo }
    
    return render(request, 'AppMaritima/editor.html', diccionario)


#escfitura del boletin  Altamar
def crearTXTnaveganteAltamar(boletin,avisos, situaciones,hielos,pronosticosMetarea):
    
    
    #Encabezado "casi" fijo  #01 en español
    textoEnIngles = f"""FQST02 SABM {boletin.valido} {boletin.hora}00 
1:31:06:01:00 
SECURITE 
WEATHER BULLETIN ON METAREA VI
SMN ARGENTINA, {boletin.valido} AT {boletin.hora}UTC WIND SPEED IN BEAUFORT SCALE WAVES IN METERS
Please be aware wind gust can be a further 40 percent stronger than the averages 
and maximum waves may be up to twice the significant height, sea ice and icebergs issued by SHN
                    
PART 1 GALE WARNING\n"""
    


    # Contar los avisos activos que no son del sur de 60
    no_sur60_count = Aviso.objects.filter(activo=True, sur60=False).count()

  
    
    if (no_sur60_count  != 0):            
        #Escritura de los avisos
        for a in avisos: 
            
            if ( a.activo and not a.sur60):
                #Defino en un metodo del modelo la escritura de txt
                textoEnIngles = textoEnIngles +a.paraTXTEnIngles()
    else:
        textoEnIngles = textoEnIngles +"NO WARNINGS"
        
    #Escritura de las situaciones
    textoEnIngles = textoEnIngles +"\nPART 2 GENERAL SYNOPSIS\n"
    
    
    
    
    #escribo la situación   
    for s in situaciones: 
        
        if (s.activo  and s.esPresente and not s.sur60 ):
            textoEnIngles = textoEnIngles +s.paraTXTEnIngles()


    textoEnIngles = textoEnIngles +"\n"

    #Escribo los hielos, aún es uno solo
    
    for h in hielos:
        
        textoEnIngles = textoEnIngles +h.paraTXTEnIngles()
    textoEnIngles = textoEnIngles +"\n"
    
    
    #Escribo los pronosticos--- OJO en que orden los quieren poner!!!!!!
    textoEnIngles = textoEnIngles +"\nPART 3 FORECAST\n"
    
    #textoEnIngles = textoEnIngles +"COASTAL AREAS:\n"
   
    
    #for p in pronosticosOffshore:
        
    #   textoEnIngles = textoEnIngles +p.paraTXTEnIngles()
        
    textoEnIngles = textoEnIngles +"\nOCEANIC AREAS - NORTH 60S\n"
    for p in pronosticosMetarea:
        
        textoEnIngles = textoEnIngles +p.paraTXTEnIngles()



    #Cierre pedido por comunicaciones
    textoEnIngles = textoEnIngles + "-----------------------------------------------------------------\nNNNN="
    
    #Por si algo quedó mal lo paso todo a mayusculas
    textoEnIngles = textoEnIngles.upper()
    
    #Abro el archivo, escribo y lo cierro... boletin maritimo en ingles -- carpeta archivo
    nombreArchivo = f"{boletin.valido}_{boletin.hora}_nav_ing_n.txt"
    f = open (f"txtGuardados/{nombreArchivo}",'w')
    f.write(textoEnIngles)
    f.close()

    #Abro el archivo, escribo y lo cierro... boletin maritimo en ingles - Carpeta para difusión
    nombreArchivoUltimo = "nav_ing_n.txt"
    f = open (f"txtUltimos/{nombreArchivoUltimo}",'w')
    f.write(textoEnIngles)
    f.close()
    
    return textoEnIngles


#escfitura del boletin  Altamar
def crearTXTnaveganteAltamarS(boletin,avisos, situaciones,hielos,pronosticosMetareaS):
    
    
    #Encabezado "casi" fijo
    textoEnIngles = f"""FQA02 SAWB {boletin.valido} {boletin.hora}00
1:31:06:01:00 
SECURITE 
WEATHER BULLETIN ON METAREA VI
SMN ARGENTINA, {boletin.valido} AT {boletin.hora}UTC WIND SPEED IN BEAUFORT SCALE WAVES IN METERS
Please be aware wind gust can be a further 40 percent stronger than the averages 
and maximum waves may be up to twice the significant height, sea ice and icebergs issued by SHN
                    
PART 1 GALE WARNING\n"""
    
    # Contar los avisos activos que no son del sur de 60
    sur60_count = Aviso.objects.filter(activo=True, sur60=True).count()
    
    if (sur60_count!=0):            
        #Escritura de los avisos
        for a in avisos: 
            
            if( a.sur60 and a.activo):
                #Defino en un metodo del modelo la escritura de txt
                textoEnIngles = textoEnIngles +a.paraTXTEnIngles()
    else:
        textoEnIngles = textoEnIngles +"NO WARNINGS"
        
    #Escritura de las situaciones
    textoEnIngles = textoEnIngles +"\nPART 2 GENERAL SYNOPSIS\n"
    
    
    
    
    #escribo la situación   
    for s in situaciones: 
        
        if (s.esPresente and s.sur60 and s.activo):
            textoEnIngles = textoEnIngles +s.paraTXTEnIngles()


    textoEnIngles = textoEnIngles +"\n"

    #Escribo los hielos, aún es uno solo
    
    for h in hielos:
        
        textoEnIngles = textoEnIngles +h.paraTXTEnIngles()
    textoEnIngles = textoEnIngles +"\n"
    
    
    #Escribo los pronosticos--- OJO en que orden los quieren poner!!!!!!
    textoEnIngles = textoEnIngles +"PART 3 FORECAST\n"
    
    #textoEnIngles = textoEnIngles +"COASTAL AREAS:\n"
   
    
    #for p in pronosticosOffshore:
        
    #   textoEnIngles = textoEnIngles +p.paraTXTEnIngles()
        
    textoEnIngles = textoEnIngles +"\nOCEANIC AREAS - SOUTH 60S\n"

    for p in pronosticosMetareaS:
        
        textoEnIngles = textoEnIngles +p.paraTXTEnIngles()

    #Cierre pedido por comunicaciones
    textoEnIngles = textoEnIngles + "-----------------------------------------------------------------\nNNNN="
    
    #Por si algo quedó mal lo paso todo a mayusculas
    textoEnIngles = textoEnIngles.upper()
    
    #Abro el archivo, escribo y lo cierro... boletin maritimo en ingles -- carpeta archivo
    nombreArchivo = f"{boletin.valido}_{boletin.hora}_nav_ing_s.txt"
    f = open (f"txtGuardados/{nombreArchivo}",'w')
    f.write(textoEnIngles)
    f.close()

    #Abro el archivo, escribo y lo cierro... boletin maritimo en ingles - Carpeta para difusión
    nombreArchivoUltimo = "nav_ing_s.txt"
    f = open (f"txtUltimos/{nombreArchivoUltimo}",'w')
    f.write(textoEnIngles)
    f.close()
    
    return textoEnIngles



#escfitura del boletin  OffShore
def crearTXTnaveganteOffShore(boletin,avisos, situaciones,hielos,pronosticosOffshore):
    
    
    #Encabezado "casi" fijo  04 español
    textoEnIngles = f"""FQST05 SABM {boletin.valido} {boletin.hora}00
1:31:06:01:00 
SECURITE 
WEATHER BULLETIN ON METAREA VI
SMN ARGENTINA, {boletin.valido} AT {boletin.hora}UTC WIND SPEED IN BEAUFORT SCALE WAVES IN METERS
Please be aware wind gust can be a further 40 percent stronger than the averages 
and maximum waves may be up to twice the significant height, sea ice and icebergs issued by SHN
                    
PART 1 GALE WARNING\n"""
    
     # Contar los avisos activos que no son del sur de 60
    no_sur60_count = Aviso.objects.filter(activo=True, sur60=False, navtex=True).count()

    if (no_sur60_count !=0):            
        #Escritura de los avisos
        for a in avisos: 
            
            if (a.navtex and a.activo and not a.sur60):
                #Defino en un metodo del modelo la escritura de txt
                textoEnIngles = textoEnIngles +a.paraTXTEnIngles()
    else:
        textoEnIngles = textoEnIngles +"NO WARNINGS"
        
    #Escritura de las situaciones
    textoEnIngles = textoEnIngles +"\nPART 2 GENERAL SYNOPSIS\n"

     #escribo la situación   
    for s in situaciones: 
        
        if (s.esPresente and s.activo and not s.sur60):
            textoEnIngles = textoEnIngles +s.paraTXTEnIngles()


    textoEnIngles = textoEnIngles +"\n"
    
    
    #Escribo los hielos, aún es uno solo
    
    #for h in hielos:
        
        #textoEnIngles = textoEnIngles +h.paraTXTEnIngles()
    #textoEnIngles = textoEnIngles +"\n"
    
       


    textoEnIngles = textoEnIngles +"\n"
    
    
    #Escribo los pronosticos--- OJO en que orden los quieren poner!!!!!!
    textoEnIngles = textoEnIngles +"\nPART 3 FORECAST\n"
    
    textoEnIngles = textoEnIngles +"COASTAL AREAS:\n"
   
    
    for p in pronosticosOffshore:
        
       textoEnIngles = textoEnIngles +p.paraTXTEnIngles()
        
    #textoEnIngles = textoEnIngles +"OCEANIC AREAS:\n"
    #for p in pronosticosMetarea:
        
    #    textoEnIngles = textoEnIngles +p.paraTXTEnIngles()

    #Cierre pedido por comunicaciones
    textoEnIngles = textoEnIngles + "-----------------------------------------------------------------\nNNNN="
    
    #Por si algo quedó mal lo paso todo a mayusculas
    textoEnIngles = textoEnIngles.upper()
    
    #Abro el archivo, escribo y lo cierro... boletin maritimo en ingles -- carpeta archivo
    nombreArchivo = f"{boletin.valido}_{boletin.hora}_nav_off_n_ing.txt"
    f = open (f"txtGuardados/{nombreArchivo}",'w')
    f.write(textoEnIngles)
    f.close()

    #Abro el archivo, escribo y lo cierro... boletin maritimo en ingles - Carpeta para difusión
    nombreArchivoUltimo = "nav_off_n_ing.txt"
    f = open (f"txtUltimos/{nombreArchivoUltimo}",'w')
    f.write(textoEnIngles)
    f.close()
    
    return textoEnIngles

#escfitura del boletin  OffShore - espñaol GQST04 SAWB
def crearTXTnaveganteOffShoreS(boletin,avisos, situaciones,hielos,pronosticosOffshoreS):
    
    
    #Encabezado "casi" fijo
    textoEnIngles = f"""FQAA05 SAWB {boletin.valido} {boletin.hora}00
1:31:06:01:00 
SECURITE 
WEATHER BULLETIN ON METAREA VI
SMN ARGENTINA, {boletin.valido} AT {boletin.hora}UTC WIND SPEED IN BEAUFORT SCALE WAVES IN METERS
Please be aware wind gust can be a further 40 percent stronger than the averages 
and maximum waves may be up to twice the significant height, sea ice and icebergs issued by SHN
                    
PART 1 GALE WARNING\n"""
    
    sur60_count = Aviso.objects.filter(activo=True, sur60=True, navtex=True).count()

    if (sur60_count !=0):            
        #Escritura de los avisos
        for a in avisos: 
            if( a.sur60 and a.navtex and a.activo):
                #Defino en un metodo del modelo la escritura de txt
                textoEnIngles = textoEnIngles +a.paraTXTEnIngles()
    else:
        textoEnIngles = textoEnIngles +"NO WARNINGS"
        
    #Escritura de las situaciones
    textoEnIngles = textoEnIngles +"\nPART 2 GENERAL SYNOPSIS\n"
    
    #escribo la situación   
    for s in situaciones: 
        
        if (s.esPresente and   s.sur60 and s.activo ):
            textoEnIngles = textoEnIngles +s.paraTXTEnIngles()

    #Escribo los hielos, aún es uno solo
    
    #for h in hielos:
        
        #textoEnIngles = textoEnIngles +h.paraTXTEnIngles()
    #textoEnIngles = textoEnIngles +"\n"
    



    textoEnIngles = textoEnIngles +"\n"
    
    
    #Escribo los pronosticos--- OJO en que orden los quieren poner!!!!!!
    textoEnIngles = textoEnIngles +"\nPART 3 FORECAST\n"
    
    textoEnIngles = textoEnIngles +"COASTAL AREAS:\n"
   
    
    for p in pronosticosOffshoreS:
        
       textoEnIngles = textoEnIngles +p.paraTXTEnIngles()
        
    #textoEnIngles = textoEnIngles +"OCEANIC AREAS:\n"
    #for p in pronosticosMetarea:
        
    #    textoEnIngles = textoEnIngles +p.paraTXTEnIngles()

    #Cierre pedido por comunicaciones
    textoEnIngles = textoEnIngles + "-----------------------------------------------------------------\nNNNN="
    
    #Por si algo quedó mal lo paso todo a mayusculas
    textoEnIngles = textoEnIngles.upper()
    
    #Abro el archivo, escribo y lo cierro... boletin maritimo en ingles -- carpeta archivo
    nombreArchivo = f"{boletin.valido}_{boletin.hora}_nav_off_s_ing.txt"
    f = open (f"txtGuardados/{nombreArchivo}",'w')
    f.write(textoEnIngles)
    f.close()

    #Abro el archivo, escribo y lo cierro... boletin maritimo en ingles - Carpeta para difusión
    nombreArchivoUltimo = "nav_off_s_ing.txt"
    f = open (f"txtUltimos/{nombreArchivoUltimo}",'w')
    f.write(textoEnIngles)
    f.close()
    
    return textoEnIngles



def crearTXTnaveganteCostas(boletin,avisos, situaciones,hielos,pronosticosCostas):
    
    
    #Encabezado "casi" fijo
    textoEnIngles = f"""COSTAS {boletin.valido} {boletin.hora}00
TEXTO SIN DEFINIR; NUEVO PRODUCTO, {boletin.valido} AT {boletin.hora}TEXTO SIN DEFINIR\n"""
    
    
    
    textoEnIngles = textoEnIngles +"COASTAL AREAS:\n"
   
    
    for p in pronosticosCostas:
        
       textoEnIngles = textoEnIngles +p.paraTXTEnIngles()
        
    #textoEnIngles = textoEnIngles +"OCEANIC AREAS:\n"
    #for p in pronosticosMetarea:
        
    #    textoEnIngles = textoEnIngles +p.paraTXTEnIngles()

    #Cierre pedido por comunicaciones
    textoEnIngles = textoEnIngles + "-----------------------------------------------------------------\nNNNN="
    
    #Por si algo quedó mal lo paso todo a mayusculas
    textoEnIngles = textoEnIngles.upper()
    
    #Abro el archivo, escribo y lo cierro... boletin maritimo en ingles -- carpeta archivo
    nombreArchivo = f"{boletin.valido}_{boletin.hora}_nav_cos_ing.txt"
    f = open (f"txtGuardados/{nombreArchivo}",'w')
    f.write(textoEnIngles)
    f.close()

    #Abro el archivo, escribo y lo cierro... boletin maritimo en ingles - Carpeta para difusión
    nombreArchivoUltimo = "nav_cos_ing.txt"
    f = open (f"txtUltimos/{nombreArchivoUltimo}",'w')
    f.write(textoEnIngles)
    f.close()
    
    return textoEnIngles







#escfitura de TODOS los navtex  
def crearTXTnavtex(boletin,avisosNavtex, situaciones,pronosticosOffshore):
    
    array_con_todos_los_textos = []
    
    #solo lo hago para estaciones NAVTEX, si quiro para todas, sacar el IF
    
    for p in pronosticosOffshore:
            
        if(p.area.description in ["DESEMBOCADURA RIO DE LA PLATA","OFFSHORE BAHIA BLANCA","OFFSHORE MAR DEL PLATA","OFFSHORE SAN JORGE","OFFSHORE FIN DEL MUNDO","OFFSHORE PATAGONIA SUR"]) :
        
            #Encabezado "casi" fijo
            textoEnIngles = f"""WWST03 SABM {boletin.valido}{boletin.hora}
WEATHER BULLETIN FOR NAVTEX STATIONS - METAREA 6 -
{boletin.valido}, {boletin.hora}:00UTC
NATIONAL WEATHER SERVICE
SEA ICE AND ICEBERGS ISSUED BY SHN
PRESSURE HPA
BEAUFORT SCALE WINDS.
                            
GALE WARNING\n"""
                            
            if (len(avisosNavtex)!=0):            
                #Escritura de los avisos
                for a in avisosNavtex: 
                    
                    #Defino en un metodo del modelo la escritura de txt
                    textoEnIngles = textoEnIngles +a.paraTXTEnIngles()
            else:
                textoEnIngles = textoEnIngles +"NO WARNINGS"
                
            #Escritura de las situaciones
            textoEnIngles = textoEnIngles +"\nGENERAL SYNOPSIS\n"
        
            
            for s in situaciones: 
                
                textoEnIngles = textoEnIngles +s.paraTXTEnIngles()
            textoEnIngles = textoEnIngles +"\n"
            
            
            #Escribo los pronosticos--- OJO en que orden los quieren poner!!!!!!
            textoEnIngles = textoEnIngles +"FORECAST\n"
            
            textoEnIngles = textoEnIngles +p.paraTXTEnIngles()
            
                
            
            #Cierre pedido por comunicaciones
            textoEnIngles = textoEnIngles + "-----------------------------------------------------------------\nNNNN="
            
            #Por si algo quedó mal lo paso todo a mayusculas
            textoEnIngles = textoEnIngles.upper()
            
            #Abro el archivo, escribo y lo cierro... boletin maritimo en ingles
            nombreArchivo = f"{boletin.valido}_{boletin.hora}_navtex_ing_{p.area.description}.txt"
            f = open (f"txtGuardados/{nombreArchivo}",'w')
            f.write(textoEnIngles)
            f.close()
            
            array_con_todos_los_textos.append(textoEnIngles)
        
    
    return array_con_todos_los_textos

##################################################################
##################### DESCARGA  DE tXT #############################
##################################################################
import pathlib
import mimetypes
import os

def descargar_archivo(request): 
    
    if request.method == "POST":
        
        data = request.POST
        print(f"-----> {data['listatxt']}")
        nombreArchivo = data['listatxt']
        
        BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) 
    
        filename = nombreArchivo #name
    
        filepath = BASE_DIR + '/txtGuardados/' + filename 
    
        path = open(filepath, 'r') 
    
        mime_type, _ = mimetypes.guess_type(filepath)
        
        response = HttpResponse(path, content_type = mime_type)
    
        response['Content-Disposition'] = f"attachment; filename={filename}"
    
        return response
    else:
        
        listaArchivos = []
    
        ejemplo_dir = 'txtGuardados/'
        directorio = pathlib.Path(ejemplo_dir)
    
        for fichero in directorio.iterdir():
        
            listaArchivos.append(fichero.name)

        # Ordenar la lista por orden alfabético
        listaArchivos.sort(reverse=True)
     
        diccionario = {"listaArchivos":listaArchivos} 
        
        return render(request, 'AppMaritima/descarga.html', diccionario)
        
        

          


# ---- supremo
#escfitura del boletin  Altamar

def crearTXTnaveganteSupremo(boletin,avisos, situaciones,hielos,pronosticosMetarea,pronosticosMetareaS, pronosticoOffShore, pronosticoOffShoreS):
    
    
    #Encabezado "casi" fijo  #01 en español
    textoEnIngles = f"""FQST02 SABM {boletin.valido} {boletin.hora}00 
1:31:06:01:00 
SECURITE 
WEATHER BULLETIN ON METAREA VI
SMN ARGENTINA, {boletin.valido} AT {boletin.hora}UTC WIND SPEED IN BEAUFORT SCALE WAVES IN METERS
Please be aware wind gust can be a further 40 percent stronger than the averages 
and maximum waves may be up to twice the significant height, sea ice and icebergs issued by SHN
                    
PART 1 GALE WARNING\n"""
    


    # Contar los avisos activos que no son del sur de 60
    count = Aviso.objects.filter(activo=True).count()

  
    
    if (count != 0):            
        #Escritura de los avisos
        for a in avisos: 
            
            if ( a.activo ):
                #Defino en un metodo del modelo la escritura de txt
                textoEnIngles = textoEnIngles +a.paraTXTEnIngles()
    else:
        textoEnIngles = textoEnIngles +"NO WARNINGS"
        
    #Escritura de las situaciones
    textoEnIngles = textoEnIngles +"\nPART 2 GENERAL SYNOPSIS\n"
    
    
    
    
    #escribo la situación   
    for s in situaciones: 
        
        if (s.activo  ):
            textoEnIngles = textoEnIngles +s.paraTXTEnIngles()


    textoEnIngles = textoEnIngles +"\n"

    #Escribo los hielos, aún es uno solo
    
    for h in hielos:
        
        textoEnIngles = textoEnIngles +h.paraTXTEnIngles()
    textoEnIngles = textoEnIngles +"\n"
    
    
    #Escribo los pronosticos--- OJO en que orden los quieren poner!!!!!!
    textoEnIngles = textoEnIngles +"\nPART 3 FORECAST\n"
    
    #textoEnIngles = textoEnIngles +"COASTAL AREAS:\n"
   
    
    #for p in pronosticosOffshore:
        
    #   textoEnIngles = textoEnIngles +p.paraTXTEnIngles()
    textoEnIngles = textoEnIngles +"\nCOASTS - NORTH 60S\n"

    for p in pronosticoOffShore:
        
        textoEnIngles = textoEnIngles +p.paraTXTEnIngles()

        
    textoEnIngles = textoEnIngles +"\nOCEANIC AREAS - NORTH 60S\n"
    for p in pronosticosMetarea:
        
        textoEnIngles = textoEnIngles +p.paraTXTEnIngles()



    textoEnIngles = textoEnIngles +"\nCOASTS - SOUTH 60S\n"

    for p in pronosticoOffShoreS:
        
        textoEnIngles = textoEnIngles +p.paraTXTEnIngles()

    textoEnIngles = textoEnIngles +"\nOCEANIC AREAS - SOUTH 60S\n"

    for p in pronosticosMetareaS:
        
        textoEnIngles = textoEnIngles +p.paraTXTEnIngles()



    #Cierre pedido por comunicaciones
    textoEnIngles = textoEnIngles + "-----------------------------------------------------------------\nNNNN="
    
    #Por si algo quedó mal lo paso todo a mayusculas
    textoEnIngles = textoEnIngles.upper()
    
    #Abro el archivo, escribo y lo cierro... boletin maritimo en ingles -- carpeta archivo
    nombreArchivo = f"{boletin.valido}_{boletin.hora}_nav_ing_sup.txt"
    f = open (f"txtGuardados/{nombreArchivo}",'w')
    f.write(textoEnIngles)
    f.close()

    #Abro el archivo, escribo y lo cierro... boletin maritimo en ingles - Carpeta para difusión
    nombreArchivoUltimo = "nav_ing_sup.txt"
    f = open (f"txtUltimos/{nombreArchivoUltimo}",'w')
    f.write(textoEnIngles)
    f.close()
    
    return textoEnIngles