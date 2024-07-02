
from django.http.response import HttpResponse
from django.shortcuts import render
from AppMaritima.models import *


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
    
    pronosticosOffshore = Pronostico.objects.filter(boletin = pk, tipo = "Offshore").order_by("area__orden")
    
    pronosticosMetarea = Pronostico.objects.filter(boletin = pk,tipo = "Metarea VI - N").order_by("area__orden")
    
    avisosNavtex =  Aviso.objects.filter(boletin = pk, navtex = True)

    situacionesNavtex = Situacion.objects.filter(boletin = pk, activo = True, navtex = True, esPresente = True)
    
    #Envio toda la info
    textoAltamar = crearTXTnaveganteAltamar(boletin,avisos, situaciones,hielos,pronosticosMetarea)
    textoOff = crearTXTnaveganteOffShore(boletin,avisosNavtex , situacionesNavtex,hielos,pronosticosOffshore)



    array_navtex = crearTXTnavtex(boletin,avisosNavtex, situaciones,pronosticosOffshore)
    
    diccionario = {"textoAltamar":textoAltamar, "textoOff":textoOff, "array_navtex": array_navtex}
    
    return render(request, 'AppMaritima/editor.html', diccionario)


#escfitura del boletin  Altamar
def crearTXTnaveganteAltamar(boletin,avisos, situaciones,hielos,pronosticosMetarea):
    
    
    #Encabezado "casi" fijo
    textoEnIngles = f"""FQST02 SABM {boletin.valido} {boletin.hora}00
1:31:06:01:00 
SECURITE 
WEATHER BULLETIN ON METAREA VI
SMN ARGENTINA, {boletin.valido} AT {boletin.hora}UTC WIND SPEED IN BEAUFORT SCALE WAVES IN METERS
Please be aware wind gust can be a further 40 percent stronger than the averages 
and maximum waves may be up to twice the significant height, sea ice and icebergs issued by SHN
                    
PART 1 GALE WARNING\n"""
    
    if (len(avisos)!=0):            
        #Escritura de los avisos
        for a in avisos: 
            
            #Defino en un metodo del modelo la escritura de txt
            textoEnIngles = textoEnIngles +a.paraTXTEnIngles()
    else:
        textoEnIngles = textoEnIngles +"NO WARNINGS"
        
    #Escritura de las situaciones
    textoEnIngles = textoEnIngles +"\nPART 2 GENERAL SYNOPSIS\n"
    
    
    
    
    #escribo la situación   
    for s in situaciones: 
        
        if (s.esPresente):
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
        
    textoEnIngles = textoEnIngles +"\nCEANIC AREAS\n"
    for p in pronosticosMetarea:
        
        textoEnIngles = textoEnIngles +p.paraTXTEnIngles()
    #Cierre pedido por comunicaciones
    textoEnIngles = textoEnIngles + "-----------------------------------------------------------------\nNNNN="
    
    #Por si algo quedó mal lo paso todo a mayusculas
    textoEnIngles = textoEnIngles.upper()
    
    #Abro el archivo, escribo y lo cierro... boletin maritimo en ingles -- carpeta archivo
    nombreArchivo = f"{boletin.valido}_{boletin.hora}_nav_ing.txt"
    f = open (f"txtGuardados/{nombreArchivo}",'w')
    f.write(textoEnIngles)
    f.close()

    #Abro el archivo, escribo y lo cierro... boletin maritimo en ingles - Carpeta para difusión
    nombreArchivoUltimo = "nav_ing.txt"
    f = open (f"txtUltimos/{nombreArchivoUltimo}",'w')
    f.write(textoEnIngles)
    f.close()
    
    return textoEnIngles



#escfitura del boletin  OffShore
def crearTXTnaveganteOffShore(boletin,avisos, situaciones,hielos,pronosticosOffshore):
    
    
    #Encabezado "casi" fijo
    textoEnIngles = f"""FQST04 SABM {boletin.valido} {boletin.hora}00
1:31:06:01:00 
SECURITE 
WEATHER BULLETIN ON METAREA VI
SMN ARGENTINA, {boletin.valido} AT {boletin.hora}UTC WIND SPEED IN BEAUFORT SCALE WAVES IN METERS
Please be aware wind gust can be a further 40 percent stronger than the averages 
and maximum waves may be up to twice the significant height, sea ice and icebergs issued by SHN
                    
PART 1 GALE WARNING\n"""
    
    if (len(avisos)!=0):            
        #Escritura de los avisos
        for a in avisos: 
            
            #Defino en un metodo del modelo la escritura de txt
            textoEnIngles = textoEnIngles +a.paraTXTEnIngles()
    else:
        textoEnIngles = textoEnIngles +"NO WARNINGS"
        
    #Escritura de las situaciones
    textoEnIngles = textoEnIngles +"\nPART 2 GENERAL SYNOPSIS\n"
    
    
    #Escribo los hielos, aún es uno solo
    
    for h in hielos:
        
        textoEnIngles = textoEnIngles +h.paraTXTEnIngles()
    textoEnIngles = textoEnIngles +"\n"
    
       
    for s in situaciones: 
        
        if (s.esPresente):
            textoEnIngles = textoEnIngles +s.paraTXTEnIngles()


    textoEnIngles = textoEnIngles +"\n"
    
    
    #Escribo los pronosticos--- OJO en que orden los quieren poner!!!!!!
    textoEnIngles = textoEnIngles +"PART 3 FORECAST\n"
    
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
    nombreArchivo = f"{boletin.valido}_{boletin.hora}_nav_off_ing.txt"
    f = open (f"txtGuardados/{nombreArchivo}",'w')
    f.write(textoEnIngles)
    f.close()

    #Abro el archivo, escribo y lo cierro... boletin maritimo en ingles - Carpeta para difusión
    nombreArchivoUltimo = "nav_off_ing.txt"
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
        
        

          
