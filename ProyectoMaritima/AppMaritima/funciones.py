from cgi import print_form
from xml.etree.ElementTree import parse
from django.shortcuts import render
from datetime import datetime

from AppMaritima.models import Pronostico, Boletin, Area

from AppMaritima.clasesLecturaDelXML import *
import random

#Envio de mails
import smtplib, ssl

#Para saber a la hora que se ejecuta el algoritmo
import time

def queHoraEs():
  
  return int(time.strftime('%H', time.localtime()))



#!!!!!Ya no se acepta iniciar sección con smtplib
def enviarMail(enviarA,texto):
    # on rentre les renseignements pris sur le site du fournisseur
    smtp_address = 'smtp.gmail.com'
    smtp_port = 465

    # on rentre les informations sur notre adresse e-mail
    email_address = 'metareavi@gmail.com'
    email_password = 'pronos_smn'

    # on rentre les informations sur le destinataire
    email_receiver = enviarA

    # on crée la connexion
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(smtp_address, smtp_port, context=context) as server:
      # connexion au compte
      server.login(email_address, email_password)
      # envoi du mail
      server.sendmail(email_address, email_receiver, texto)




def definirRoot(nombreArchivo):#en este caso el argumento a recibir debe ser 'prueba.xml'
  
  archivoXML = nombreArchivo

  tree = parse(archivoXML)

  root = tree.getroot() 
  
  return root

def leerXML(nombreArchivo): #en este caso el argumento a recibir debe ser 'prueba.xml'
  
  root = definirRoot(nombreArchivo)
  
  #Inicio los pronosticos para probar
  forecast = Forecast(0,0,0,0,0)
  forecastSur60 = Forecast(0,0,0,0,0)
  forecastOffShore = Forecast(0,0,0,0,0)
  forecastCostas = Forecast(0,0,0,0,0)
  forecastRio = Forecast(0,0,0,0,0)

  for pronostico in root: 
    #Instancia vacia
    #Por ahora no se usaria

    #Accedo a cada Area, elimino la posicion 0 porque es issue y esta vacio
    for area in pronostico:

      ####################CARGA LA HORA Y FECHA DEL PRONOSTICO
      #horrible pero estan muy mal los tag del XML
      if ( area.tag == 'issue'):
        for x in area:
          if (x.tag == 'year'):
            forecast.year = x.text
            forecastOffShore.year = x.text
            forecastCostas.year = x.text
            forecastRio.year = x.text
          if (x.tag == 'month'):
            forecast.month = x.text
            forecastOffShore.month = x.text
            forecastCostas.month = x.text
            forecastRio.month = x.text
          if (x.tag == 'day'):
            forecast.day = x.text
            forecastOffShore.day = x.text
            forecastRio.day = x.text
            forecastCostas.day = x.text
          if (x.tag == 'hour'):
            forecast.hour = x.text
            forecastOffShore.hour = x.text
            forecastCostas.hour = x.text
            forecastRio.hour = x.text
          if (x.tag == 'minute'):
            forecast.minute = x.text
            forecastOffShore.minute = x.text
            forecastRio.minute = x.text
            forecastCostas.minute = x.text




      ###################ESTRUCTURA PRINCIPAL; CARGA AREAS CON PRONOSTICOS######
      if (area.tag == 'area'):
          #instancio un area
          a = AreaXML(area.attrib['id'],area.attrib['latitude'],area.attrib['longitude'],area.attrib['description'], area.attrib['domain'])
        
          print(f"------>TRABAJO CON AREA: {a.description}")

          #Accedo a cada parametro
          for parameter in area: 
            #filtro los tag que no sean utiles
            if (parameter.tag == 'parameter'):
              #instancio el parametro
              p = Parameter(parameter.attrib['id'])

              ###################TIME RANGE#########################
              #accedo a las horas de mi parametro
              for timerange in parameter:
                #instancio el timerange
                t = Timerange(timerange.attrib['h'],timerange.attrib['datetime'])

                ###################VALUE#########################
                #accedo al value de ese horario
                for value in timerange:

                  #instancio al valor
                  v = Value(value.text,value.attrib['unit'])

                  #Agrego el valor a la lista de timerange
                  t.list_values.append(v)
                ###################FIN VALUE#########################


                #agrego el timerange a la lista de parameter
                p.list_timeranges.append(t)

              ###################FIN TIME RANGE#########################
                  
              #agrego el parametro a la lista de area
              a.list_parameters.append(p)
          
          #antes de terminar el area la agrego a la lista de area del pronostico que corresponde
         

          if (a.domain == 'Metarea VI'):
           
            if ( float(a.latitude) <= -60):
              forecastSur60.list_area.append(a)

            if ( float(a.latitude) > -60):
              forecast.list_area.append(a)

          if (a.domain == 'Costas'):

            if (a.description.find('OFFSHORE')!=-1):
              
              forecastOffShore.list_area.append(a)
            else:
                forecastCostas.list_area.append(a)
                
          
          if (a.domain == 'Rio de la Plata'):
            forecastRio.list_area.append(a)
     

     
     
     
        
def transformarOlasA8Cuadrantes(olaD):

  retorno = olaD

  if (olaD == "N" or olaD == "NNE" or olaD == "NNW"):

    retorno = "N"

  if (olaD == "S" or olaD == "SSE" or olaD == "SSW"):

    retorno = "S"


  if (olaD == "W" or olaD == "WNW" or olaD == "WSW"):

    retorno = "W"

  if (olaD == "E" or olaD == "ENE" or olaD == "ESE"):

    retorno = "E"

  return retorno


def agregarONoRafagas(velBeaufort):

  retorno = ""
  if ( int(velBeaufort) >= 4):

    retorno = "WITH GUSTS"

  return retorno


def ktABeaufort(velo):

       
      #Si llega un digito lo paso a float
      if (velo.isdigit()):
        
        velo = float(velo)
        
        if (velo <= 0.1):
          vel = 0
          
      #Si no llega un digito lo pongo en 0    
      else:
        velo = float (0)    
        

      retorno = ""
      
    

      if ( velo >= 0 and velo<= 3):
        retorno = 1
      if ( velo >= 4 and velo<= 6):
        retorno = 2
      if ( velo >= 7 and velo<= 10):
        retorno = 3
      if ( velo >= 11 and velo<= 16):
        retorno = 4
      if ( velo >= 17 and velo<= 21):
        retorno = 5
      if ( velo >= 22 and velo<= 27):
        retorno = 6
      if ( velo >= 28 and velo<= 33):
        retorno = 7
      if ( velo >= 34 and velo<= 40):
        retorno = 8
      if ( velo >= 41 and velo<= 47):
        retorno = 9
      if ( velo >= 48 and velo<= 55):
        retorno = 10
      if ( velo >= 56 and velo<= 63):
        retorno = 11
      if ( velo >= 64):
        retorno = 12

      return str(retorno)
  
  
  
def transformarASectores(vientoD):
  retorno = vientoD

  ###!!!!!!!!!!!!!En 8 Cuadrantes!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

  if ( vientoD == "N" or vientoD == "NNE" or vientoD == "NNW"):
    retorno = "SECTOR N"

  if ( vientoD == "S" or vientoD == "SSE" or vientoD == "SSW"):
    retorno = "SECTOR S"

  if ( vientoD == "W" or vientoD == "WSW" or vientoD == "WNW"):
    retorno = "SECTOR W"

  if ( vientoD == "E" or vientoD == "ESE" or vientoD == "ENE"):
    retorno = "SECTOR E"

  return retorno


def tomarHorasIndicadasSegunTurno(elemento):
        horaActual = queHoraEs()

        hora1 = 0
        hora2 = 0
        hora3 = 0

        print(f"HORA QUE TOMA: {horaActual}")
       
        #Hora actual en hora local :) 
        if (horaActual < 18): #Si se crea el boletin en el turno diurno
          
          for i,horasDelXML in enumerate(elemento.list_timeranges):
            #OJO SON STRING NO INT
            #print(f"Horas de los pronos: {horasDelXML.h } -- INDICE: {i}")
            if horasDelXML.h == "12":
              
              hora1 = i
              
            if horasDelXML.h == "24":
              
              hora2 = i
              
            if horasDelXML.h == "36":
              
              hora3 = i
        else:  #Si se ejecuta para el turno noche
          
            for i,horasDelXML in enumerate(elemento.list_timeranges):

              #print(f"Horas de los pronos: {horasDelXML.h } -- INDICE: {i}")
            
              if horasDelXML.h == "24":
                
                hora1 = i
                
              if horasDelXML.h == "36":
                
                hora2 = i
                
              if horasDelXML.h == "48":
                
                hora3 = i

      
        return hora1,hora2,hora3 #Retorno las tres horaas que uso para el pronos

def escribirTextoOlas(direccion, altura):


        

        #####Checkear y validar esto entre diuno y nocturno y distintos modelos
        hora1,hora2,hora3 = tomarHorasIndicadasSegunTurno(altura)
        ########


        print(f"HORAS OLAS: {hora1} {hora2} {hora3}")

        print(f"{altura.list_timeranges[hora1]}")
        print(f"{altura.list_timeranges[hora2]}")
        print(f"{altura.list_timeranges[hora3]}")

        #Value[0] altura en metros
        alturaInicial = altura.list_timeranges[hora1].list_values[0].text
        alturaMedia = altura.list_timeranges[hora2].list_values[0].text
        alturaFinal = altura.list_timeranges[hora3].list_values[0].text

        hora1d,hora2d,hora3d = tomarHorasIndicadasSegunTurno(direccion)
        
        print(f"{direccion.list_timeranges[hora1d]}")
        print(f"{direccion.list_timeranges[hora2d]}")
        print(f"{direccion.list_timeranges[hora3d]}")
        
        print(f"\nPRUEBA DE HORARIOS DE OLAS: {altura.list_timeranges[hora1]}//{altura.list_timeranges[hora2]}//{altura.list_timeranges[hora3]}")
        

        #Value[1] direccion en 16 cuadrantes
        dirInicial = transformarOlasA8Cuadrantes(direccion.list_timeranges[hora1d].list_values[1].text)
        print(f" {direccion.list_timeranges[hora1d].list_values[1].text}  ")
        dirMedia = transformarOlasA8Cuadrantes(direccion.list_timeranges[hora2d].list_values[1].text)
        print(f"  {direccion.list_timeranges[hora2d].list_values[1].text }   ")
        dirFinal = transformarOlasA8Cuadrantes(direccion.list_timeranges[hora3d].list_values[1].text)
        print(f"   {direccion.list_timeranges[hora3d].list_values[1].text}")


        print(f" {dirInicial} {dirMedia }    {dirFinal}")

        #Acá se guarda el texto final
        retorno = "\nWAVES: "


        #Si la inicial es igual a la final
        if ( dirInicial == dirFinal):

                #Aumento o disminuyo?
                cambio = "SIN CAMBIO"
             

                #Si cambio la velocidad
                if (not( cambio == "SIN CAMBIO")):
                  retorno = retorno + dirInicial +"/"  +f" {alturaFinal}"

                else: #No cambio la velocidad
                  retorno = retorno + dirInicial +f" {alturaInicial} "


                #Si la intermedia es distinta, le hago un cambio temporario
                if (not  dirInicial == dirMedia):

                        retorno = retorno +" TEMPORARY CHANGE " +dirMedia +f" {alturaMedia} "



        else:  #distintas direcciones iniciales y finales

                #Si la del medio no es igual a ninguna de las dos, hago el cambio
                if (not (dirMedia == dirInicial) and not (dirMedia == dirFinal) ):

                      retorno = retorno + dirInicial +f" {alturaInicial} " +f" LATER " + dirMedia +f" {alturaMedia} "+f" AND LATER " + dirFinal +f" {alturaFinal}"


                else:  #Si la dirección del medio es igual a alguna de las dos

                      #Igual a la primera  o a la ultima, ignoro ese cambio
                      if ((dirMedia == dirInicial and alturaMedia == alturaInicial) or (dirMedia == dirFinal and alturaMedia == alturaFinal)):

                            retorno = retorno + dirInicial +f" {alturaInicial} " +f" LATER " + dirFinal +f" {alturaFinal}"

                      #Misma direccion que la primera pero cambio de velocidad
                      if (dirMedia == dirInicial and not alturaMedia == alturaInicial):

                            

                            retorno = retorno + dirInicial  +f" {alturaInicial}/{alturaMedia} "  +f" BACKING " + dirFinal +f" {alturaFinal}"


                      #Misma direccion que la ultima pero cambio de velocidad
                      if (dirMedia == dirFinal and not alturaMedia == alturaFinal):

                          

                            retorno = retorno + dirInicial  +f" {alturaInicial}" +f" BACKING " + dirFinal +f" {alturaMedia}/{alturaFinal}"  



        retorno = retorno +". "
        
        print(f"\n\nPRUEBA OLAS: {retorno}")

        return retorno 

#Direccion y velocidad tienen una lista de horas y en cada hora esta el valor
def escribirTextoViento(direccion, velocidad):
        


        #Transformo direcciones a sectores 

        for t in direccion.list_timeranges:

          t.list_values[1].text = transformarASectores(t.list_values[1].text)

          print(f"VIENTO EN DIRECCIONES: {t.list_values[1].text}" )

        #"""OBS: list_ parametros : #1-WD viento direccion  6- WS vel viento
        #        list_timeranges:   #0 - 6z  #1- 12Z    2-18  3-24/00   4-30/06   5-36/12
        #        list_values: 1 para la direccion así transforma grados en puntos cardinales list_values[1]
        #        list_values: 0 para velocidad así lo da en kT list_values[0]"""

        #####Checkear y validar esto entre diuno y nocturno y distintos modelos
        hora1,hora2,hora3 = tomarHorasIndicadasSegunTurno(velocidad)
        ########

        print(f"HORAS SEGUN TURNO: {hora1} {hora2} {hora3}")
         
        #print(f"\nPRUEBA DE HORARIOS DE VEINTO: {velocidad.list_timeranges[hora1]}{velocidad.list_timeranges[hora2]}{velocidad.list_timeranges[hora3]}")
        

        #print(f"HORAS DEL PRONOS 2022: {hora1} {hora2} {hora3}")

        #GRAN CAMBIO 2023, compara con las siguientes horas
        #Supongo que me quedo con las horas dadas
        hora1Maxima = hora1
        hora2Maxima = hora2
        hora3Maxima = hora3

       

        #Si la hora siguiente es mayor, me quedo con la siguiente

        if((int(ktABeaufort(velocidad.list_timeranges[hora1].list_values[0].text) )) < int(ktABeaufort(velocidad.list_timeranges[hora1+1].list_values[0].text) )):
          hora1Maxima = hora1 +1

        if((int(ktABeaufort(velocidad.list_timeranges[hora2].list_values[0].text) )) < int(ktABeaufort(velocidad.list_timeranges[hora2+1].list_values[0].text) )):
          hora2Maxima = hora2 +1

        print("---------------------------")

        if((int(ktABeaufort(velocidad.list_timeranges[hora3].list_values[0].text) )) < int(ktABeaufort(velocidad.list_timeranges[hora3+1].list_values[0].text) )):
          hora3Maxima = hora3 +1

        print("xxxxxxxxxxxxxxxxxxx")

        print(f"HORAS DEL PRONOS 2023: {hora1Maxima} {hora2Maxima} {hora3Maxima}")

        #Ahora ya se cual es mi dato más importante, uso ese

        velInicial = int(ktABeaufort(velocidad.list_timeranges[hora1Maxima ].list_values[0].text) )
      
        velMedia = int(ktABeaufort(velocidad.list_timeranges[hora2Maxima ].list_values[0].text))
        
        velFinal = int(ktABeaufort(velocidad.list_timeranges[hora3Maxima ].list_values[0].text) )
        

        velInicialConRafagas = ktABeaufort(velocidad.list_timeranges[hora1Maxima ].list_values[0].text) +" " +agregarONoRafagas(ktABeaufort(velocidad.list_timeranges[hora1Maxima ].list_values[0].text))
        velMediaConRafagas = ktABeaufort(velocidad.list_timeranges[hora2Maxima ].list_values[0].text) +" " +agregarONoRafagas(ktABeaufort(velocidad.list_timeranges[hora2Maxima ].list_values[0].text))
        velFinalConRafagas = ktABeaufort(velocidad.list_timeranges[hora3Maxima ].list_values[0].text)+" "  +agregarONoRafagas(ktABeaufort(velocidad.list_timeranges[hora3Maxima ].list_values[0].text))


        dirInicial = direccion.list_timeranges[hora1Maxima ].list_values[1].text
        dirMedia = direccion.list_timeranges[hora2Maxima ].list_values[1].text
        dirFinal = direccion.list_timeranges[hora3Maxima ].list_values[1].text

       
     
        #Acá se guarda el texto final
        retorno = "\nWINDS: "


        #Si la inicial es igual a la final
        if ( dirInicial == dirFinal):

                #Aumento o disminuyo?
                cambio = "SIN CAMBIO"
                if (velInicial < velFinal):
                  cambio = "INCREASING"

                if (velInicial > velFinal):
                  cambio = "DECREASING"

                #Si cambio la velocidad
                if (not( cambio == "SIN CAMBIO")):
                  retorno = retorno + dirInicial +f" {velInicialConRafagas} " +f" {cambio} "  +f" {velFinalConRafagas}"

                else: #No cambio la velocidad
                  retorno = retorno + dirInicial +f" {velInicialConRafagas} "


                #Si la intermedia es distinta, le hago un cambio temporario
                if (not  dirInicial == dirMedia):

                        retorno = retorno +" TEMPORARY CHANGE " +dirMedia +f" {velMediaConRafagas} "



        else:  #distintas direcciones iniciales y finales

                #Si la del medio no es igual a ninguna de las dos, hago el cambio
                if (not (dirMedia == dirInicial) and not (dirMedia == dirFinal) ):

                      retorno = retorno + dirInicial +f" {velInicialConRafagas} " +f" BACKING  " + dirMedia +f" {velMediaConRafagas} "+f" AND BACKING " + dirFinal +f" {velFinalConRafagas}"


                else:  #Si la dirección del medio es igual a alguna de las dos

                      #Igual a la primera  o a la ultima, ignoro ese cambio
                      if ((dirMedia == dirInicial and velMedia == velInicial) or (dirMedia == dirFinal and velMedia == velFinal)):

                            retorno = retorno + dirInicial +f" {velInicialConRafagas} " +f" BACKING  " + dirFinal +f" {velFinalConRafagas}"

                      #Misma direccion que la primera pero cambio de velocidad
                      if (dirMedia == dirInicial and not velMedia == velInicial):

                            maximo = max([velInicial, velMedia])

                            retorno = retorno + dirInicial  +f" {velInicial}/{velMedia} " +agregarONoRafagas(maximo) +f" BACKING  " + dirFinal +f" {velFinalConRafagas}"


                      #Misma direccion que la ultima pero cambio de velocidad
                      if (dirMedia == dirFinal and not velMedia == velFinal):

                            maximo = max([velFinal, velMedia])

                            retorno = retorno + dirInicial  +f" {velInicialConRafagas}" +f" BACKING  " + dirFinal +f" {velMedia}/{velFinal}" +agregarONoRafagas(maximo) 



        retorno = retorno + ". "
        
        print(f"\n\nPRUEBA VIENTOS: {retorno}")
        return retorno 



def transformarNumeroAVisibilidad (visi):
  
  retorno = "CODIGOMALO"
    
  if ( visi == "500"):
      retorno = "VERY POOR"

  if ( visi == "2000"):
      retorno = "POOR"
      
  if ( visi == "5000"):
      retorno = "REGULAR"


  if ( visi == "10000"):
      retorno = "GOOD"
      
  return retorno

#Visibilidad tienen una lista de horas y en cada hora esta el valor
def escribirVisibilidad(visibilidad):

        #list_timeranges[5].list_values[0].text)  #parametro 7 es visibilidad... 10000 B, 5000 Re... 2000 Mala... 500 MM

        #tengo que pararme en 12z, 00z y 12z+1 ... eso son las posiciones 1 - 3 - 5

        retorno = ""

        #Si 1 y 5 son distintas agrego el TO
 
        hora1,hora2,hora3 = tomarHorasIndicadasSegunTurno(visibilidad)
 
       # print(f"\nPRUEBA DE HORARIOS DE VEINTO: {visibilidad.list_timeranges[hora1]}{visibilidad.list_timeranges[hora2]}{visibilidad.list_timeranges[hora3]}")
        
      
        
        
        
        if (visibilidad.list_timeranges[hora1].list_values[0].text != visibilidad.list_timeranges[hora3].list_values[0].text ):

          retorno = f"\nVISIBILITY:  {transformarNumeroAVisibilidad(visibilidad.list_timeranges[hora1].list_values[0].text)} TO  {transformarNumeroAVisibilidad(visibilidad.list_timeranges[hora3].list_values[0].text)}"
        
        else: 

          retorno = f"\nVISIBILITY: {transformarNumeroAVisibilidad(visibilidad.list_timeranges[hora1].list_values[0].text)}"


        if (visibilidad.list_timeranges[hora1].list_values[0].text != visibilidad.list_timeranges[hora2].list_values[0].text ):
          
          if (visibilidad.list_timeranges[hora3].list_values[0].text != visibilidad.list_timeranges[hora2].list_values[0].text ):

            retorno = retorno + f", OCCASIONALLY {transformarNumeroAVisibilidad(visibilidad.list_timeranges[hora2].list_values[0].text)}"

        retorno = retorno +". "
        
        print(f"\n\nPRUEBA VISI: {retorno}")
        return retorno
      
    
def codigoAFenomeno(codigo):

  

  retorno = "WORSENING"  #Inicialmente desmejorando, para que simplifique el algoritmo

  
 

  if codigo == "74":
    retorno = "SHOWERS"

  if codigo == "73":
    retorno = "RAIN"

  if codigo == "83":
    retorno = "HEAVY RAIN"

  if codigo == "85":
    retorno = "HEAVY SNOW"

  if codigo == "71":
    retorno = "DRIZZLE"

  

  if codigo == "77":
    retorno = "RAIN AND SNOW"

  if codigo == "79":
    retorno = "OCCASIONALLY SNOW"

  if codigo == "81":
    retorno = "RAIN AND THUNDERSTORM"

  if codigo == "84":
    retorno = "HEAVY THUNDERSTORM"

  if codigo == "72":
    retorno = "ISOLATED RAIN"

  if codigo == "76":
    retorno = "ISOLATED STORM"

  #if codigo == "51":
    #retorno = "SPRAY"

  if codigo == "69":
    retorno = "FREEZING FOG"

  if codigo == "67":
    retorno = "FOG"

  if codigo == "61":
    retorno = "MIST"

  if codigo == "94":
    retorno = "BLIZZARD"

  if codigo == "96":
    retorno = "DRIFTING SNOW"

  if codigo == "92":
    retorno = "BLOWING SNOW"

  #NUEVAS AL 2023
  if codigo == "78":
    retorno = "FREEZING RAIN"

  if codigo == "80":
    retorno = "ISOLATED SNOWFALL"

  if codigo == "86":
    retorno = "STORM WITH SNOWFALL"

  if codigo == "87":
    retorno = "HEAVY RAIN AND HEAVY SNOW"

  if codigo == "75":
    retorno = "LIGTH SNOW"

  return retorno


#Pronsotico tienen una lista de horas y en cada hora esta el valor, solo el valor 0 interesa
def escribirPronostico(pronostico):

        #list_timeranges[5].list_values[0].text)  #
        
        #5 ---pronostico del tiempo.... 0,2,4 son las 12, 00 y 12(+1)

        retorno = "\nFORECAST: "
        
        hora1,hora2,hora3 = tomarHorasIndicadasSegunTurno(pronostico)

        #escribo los tres fenomenos que usaremos
        fenomeno1 = codigoAFenomeno(pronostico.list_timeranges[hora1].list_values[0].text)
        fenomeno11 = codigoAFenomeno(pronostico.list_timeranges[hora1+1].list_values[0].text)

        fenomeno2 = codigoAFenomeno(pronostico.list_timeranges[hora2].list_values[0].text)
        fenomeno22 = codigoAFenomeno(pronostico.list_timeranges[hora2+1].list_values[0].text)

        fenomeno3 = codigoAFenomeno(pronostico.list_timeranges[hora3].list_values[0].text)
        fenomeno33 = codigoAFenomeno(pronostico.list_timeranges[hora3+1].list_values[0].text)

    
        
        # Definir los fenómenos
        fenomenos = [(fenomeno1, fenomeno11), (fenomeno2, fenomeno22), (fenomeno3, fenomeno33)]

        # Inicializar el retorno
        retorno = "\nFORECAST: "

        # Función para combinar fenómenos
        def combinar_fenomenos(fen1, fen2):
            if fen1 == fen2 or fen1 in fen2 or fen2 in fen1:
                return fen1
            else:
                return fen1 + "/" + fen2

        # Lista para almacenar los fenómenos combinados que no son redundantes
        fenomenos_combinados = []

        # Iterar sobre los pares de fenómenos
        for fen1, fen2 in fenomenos:
            fenomeno_final = combinar_fenomenos(fen1, fen2)
            # Añadir solo si no está contenido en el último fenómeno significativo añadido
            if not fenomenos_combinados or fenomeno_final not in fenomenos_combinados[-1] :
                fenomenos_combinados.append(fenomeno_final)

        # Construir la cadena final
        if fenomenos_combinados:
            retorno += " LATER ".join(fenomenos_combinados)
        else:
            retorno += "NO SIGNIFICANT WEATHER EVENTS."

        retorno += "."

        # Reemplazar barras por "then" o "followed by" aleatoriamente
        def reemplazar_barras(string):
            opciones = [", then", ", followed by"]
            partes = string.split("/")
            resultado = partes[0]

            for parte in partes[1:]:
                resultado += random.choice(opciones) + " " + parte

            return resultado
        
         # Reemplazar "LATER" por un sinónimo aleatoriamente sin repeticiones consecutivas
        def reemplazar_later(string):
            sinonimos = ["afterwards", "subsequently", "later"]
            partes = string.split(" LATER ")
            resultado = partes[0]
            ultimo_usado = None

            for parte in partes[1:]:
                opciones = [sinonimo for sinonimo in sinonimos if sinonimo != ultimo_usado]
                sinonimo_elegido = random.choice(opciones)
                resultado += " " + sinonimo_elegido + " " + parte
                ultimo_usado = sinonimo_elegido

            return resultado
        
        retorno = reemplazar_barras(retorno)
        retorno = reemplazar_later(retorno)

        #Si los fenomenos y  su consecutivo son distintos los uno. Sino dejo el de la hora clave. 
        """
        if fenomeno1 != fenomeno11:
           fenomeno1 = fenomeno1 +"/" +fenomeno11

        if fenomeno2 != fenomeno22:
           fenomeno2 = fenomeno2 +"/" +fenomeno22

        if fenomeno3 != fenomeno33:
           fenomeno3 = fenomeno3 +"/" +fenomeno33



        #print(f"\nPRUEBA DE HORARIOS DE FENOMENO: {pronostico.list_timeranges[hora1]}{pronostico.list_timeranges[hora2]}{pronostico.list_timeranges[hora3]}")
      


        #Si hay algun fenomeno significativo
       
        if (not(fenomeno1 == "WORSENING" and fenomeno2 == "WORSENING" and fenomeno3 == "WORSENING") ):

          
          #12 = 00   pero distinto de 12+1
          if (fenomeno1 == fenomeno2 and not fenomeno2 == fenomeno3):

            if (fenomeno3 == "WORSENING"):

              fenomeno3 = "IMPROVING"

            retorno = retorno + fenomeno1  + " LATER " +fenomeno3 +"."


          #Los tres dintintos
          if ( not (fenomeno1 == fenomeno2 or )  and  not (fenomeno2 == fenomeno3) and  not (fenomeno1 == fenomeno3)):

            if (fenomeno3 == "WORSENING"): #el tres es solo nube

              fenomeno3 = "IMPROVING"

              retorno =retorno + fenomeno1  + " LATER " +fenomeno2 +" AND LATER " +fenomeno3 +"."



            if (fenomeno2 == "WORSENING"):

              fenomeno2 = "IMPROVING"

              retorno =retorno + fenomeno1  + " LATER " +fenomeno3 +", OCCASIONALLY " +fenomeno2 +"."


            if (fenomeno1 == "WORSENING"):
            
              retorno =retorno + fenomeno1 +", " +fenomeno2 +" LATER " +fenomeno3 +"."


          #12 = 12+1 pero distintos a 00
          if ( fenomeno1 == fenomeno3 and not (fenomeno2 == fenomeno3)):


             if (fenomeno2 == "WORSENING"):

              fenomeno2 = "IMPROVING"

              retorno =retorno + fenomeno1  + " AND OCCASIONALLY " +fenomeno2 +"."


             if (fenomeno1 == "WORSENING"):

              fenomeno2 = "IMPROVING"

              retorno =retorno +  " OCCASIONALLY " +fenomeno2 +"."

          

          #12 != 00 pero == igual a 12+1
          if ( not (fenomeno1 == fenomeno2) and fenomeno2 == fenomeno3):

            if (fenomeno2 == "WORSENING"):
              fenomeno2 = "IMPROVING"

            retorno =retorno + fenomeno1 + " LATER " +fenomeno2 +"."

        #En caso que no hay fenomenos importantes
        #else:
           #retorno = retorno +"WITHOUT PRECIPITATION"

        if (retorno == "\nFORECAST: "):
           retorno = retorno +"NO SIGNIFICANT WEATHER EVENTS."
           
        retorno = retorno +". "
        """


        print(f"\n\nPRUEBA FENO: {retorno}")
        return retorno
   
#Esta funcion retorna el area de pronostico recibida solo si tiene pronostico de temporal
def areaParaTemporal(area): #Retorna el area solo si tiene pronostico de temporal
        #Agarro el parametro velocidad del area pronosticada

        velocidad = next((p for p in area.list_parameters if p.id == "ws"), None)
        #velocidad = area.list_parameters[6]
        
        print(velocidad)
        
        #####Checkear y validar esto entre diuno y nocturno y distintos modelos
        hora1,hora2,hora3 = tomarHorasIndicadasSegunTurno(velocidad)
        ########
  
       
        velInicial = int(ktABeaufort(velocidad.list_timeranges[hora1].list_values[0].text) )
      
        velMedia = int(ktABeaufort(velocidad.list_timeranges[hora2].list_values[0].text))
        
        velFinal = int(ktABeaufort(velocidad.list_timeranges[hora3].list_values[0].text) )

        #Si antes hubo temporal tambien-- cambiio 2023
        velInicialPrevias = int(ktABeaufort(velocidad.list_timeranges[hora1-1].list_values[0].text) )
      
        velMediaPrevias = int(ktABeaufort(velocidad.list_timeranges[hora2-1].list_values[0].text))
        
        velFinalPrevias = int(ktABeaufort(velocidad.list_timeranges[hora3-1].list_values[0].text) )

     
        
        if velInicial > 7 or velMedia >7 or velFinal > 7 or velInicialPrevias > 7 or velMediaPrevias>7 or velFinalPrevias > 7:
          
            return area
     
    
def areaAtexto(area,bole):

  #print(f"BOLETIN: {bole.pronosticosOlasSHN}")
  #print(f"Texto a area: {area}")
  texto = f"\n{traducirAreas(area.description)}: ".upper()


 
  parametroWd = next((p for p in area.list_parameters if p.id == "wd"), None)
  parametroWs = next((p for p in area.list_parameters if p.id == "ws"), None)

  parametroWw = next((p for p in area.list_parameters if p.id == "ww"), None)

  parametroVi = next((p for p in area.list_parameters if p.id == "visibility"), None)

  parametroWad = next((p for p in area.list_parameters if p.id == "waved"), None)
  parametroWah = next((p for p in area.list_parameters if p.id == "waveh"), None)

  

  print(f"--- Parametros viento: {parametroWd} - {parametroWs}")
  print(f"--- Parametros fenomeno: {parametroWw}")
  print(f"--- Parametros visibility: {parametroVi}")
  print(f"--- Parametros olas: {parametroWad} - {parametroWah}")

  #if all(param is not None for param in [parametroWd, parametroWs, parametroWw, parametroVi]):
    #genero el viento del area, solo con los parametros 1 y 6
  viento = escribirTextoViento(parametroWd, parametroWs)

    #genero el pronostico, solo con el parametro ww
  fenomeno = escribirPronostico(parametroWw)

    #genero la visibilidad
  visibilidad = escribirVisibilidad(parametroVi)
  #else:
  #print(f"Faltan datos meteorologicos en: {area}")



  #Si el pronostico de SHN no está, uso PIMET
  if(bole.pronosticosOlasSHN == ""):

    if all(param is not None for param in [parametroWad, parametroWah]):

      ola = escribirTextoOlas(parametroWad,parametroWah)
      #ola = "OLAS SHN"

    else:
      print(f"Faltan datos de olas  o esta congelado en: {area}")
      ola = "\nWAVES: FROZEN SEA."

  #SI hay pronostico de olas... uso SHN
  else:
    ola = escribirTextoOlasSHN(area, bole)

  texto = texto + viento  +fenomeno  +visibilidad  +ola+"."

  #Limpiar errores tippicos, luego hacerlo mejor, prioridad baja


  texto = texto.replace(" . . ", ".")
  texto = texto.replace(". .", ".")
  texto = texto.replace("..", ".")
  texto = texto.replace("   ", " ")
  texto = texto.replace(" .", ".")
  texto = texto.replace(". ", ".")
  
  #print(texto)

  return texto



def calcularOrdenAreas(idPimet):
  
    listaOrden = [284,283,285,3546,739,751,752,753,754,756,757,758,730,729,728,720,721,722,723,724,725,726,727,731,732,733,734,735,736,737,738,755]

    
    try:
      return  listaOrden.index(idPimet)
    except:
      return 999
    


#Para cargar la base de datos con las areas, no ejecutar más de una vez
def cargarAreasDesdeElXML(nombreArchivo):
  
  root = definirRoot(nombreArchivo)

  for pronostico in root: 
    #Instancia vacia
    #Por ahora no se usaria

    #Accedo a cada Area, elimino la posicion 0 porque es issue y esta vacio
    for area in pronostico:

      
      ###################ESTRUCTURA PRINCIPAL; CARGA AREAS CON PRONOSTICOS######
      if (area.tag == 'area'):
          #instancio un area
          a = Area(area.attrib['id'],area.attrib['latitude'],area.attrib['longitude'],area.attrib['description'], area.attrib['domain'])

          idPimet=float(area.attrib['id'])
          ordenNav = calcularOrdenAreas(idPimet)
          
          areaModels = Area(idPimet=idPimet, latitude=area.attrib['latitude'],
                            longitude=area.attrib['longitude'], description=area.attrib['description'],
                            descriptionIngles=traducirAreas(area.attrib['description']),
                            domain= area.attrib['domain'], orden=ordenNav)
          
          areaModels.save()
          
          
          
def cargarPronosticosDesdeElXML(nombreArchivo, idBoletin):
  
    lista_areas_para_temporales = []
  
    root = definirRoot(nombreArchivo)
    pronosticosGuardados = "" #Variable para identificar cuándo se guardaron los
    #pronosticos en PIMET

    b = Boletin.objects.get(id = idBoletin) #Boletin donde guardaré la info
    
    for pronostico in root: 
    #Instancia vacia
    #Por ahora no se usaria

    #Accedo a cada Area, elimino la posicion 0 porque es issue y esta vacio
      for area in pronostico:

          if (area.tag == "issue"):
            for x in area:
              if(x.tag == "timestamp"):
                pronosticosGuardados =x.text 
      
          ###################ESTRUCTURA PRINCIPAL; CARGA AREAS CON PRONOSTICOS######
          if (area.tag == 'area'):
              
              print(f"INTENTANDO HACER EL PRONOS DE: {area.attrib['description']}")

              #instancio un area
              a = AreaXML(area.attrib['id'],area.attrib['latitude'],area.attrib['longitude'],area.attrib['description'], area.attrib['domain'])
            
              

              #Accedo a cada parametro
              for parameter in area: 
                #filtro los tag que no sean utiles
                if (parameter.tag == 'parameter'):
                  #instancio el parametro
                  p = Parameter(parameter.attrib['id'])

                  print(f"ESTOY EN PARAMETER: {p}")

                  ###################TIME RANGE#########################
                  #accedo a las horas de mi parametro
                  for timerange in parameter:
                    #instancio el timerange
                    t = Timerange(timerange.attrib['h'],timerange.attrib['datetime'])

                    print(f"ESTOY EN HORA: {t}")

                    ###################VALUE#########################
                    #accedo al value de ese horario
                    for value in timerange:

                      #instancio al valor
                      v = Value(value.text,value.attrib['unit'])

                      print(f"ESTOY EN VALOR: {v}")

                      #Agrego el valor a la lista de timerange
                      t.list_values.append(v)
                    ###################FIN VALUE#########################


                    #agrego el timerange a la lista de parameter
                    p.list_timeranges.append(t)

                  ###################FIN TIME RANGE#########################
                      
                  #agrego el parametro a la lista de area
                  a.list_parameters.append(p)
              
              #antes de terminar el area la agrego a la lista de area del pronostico que corresponde
             
              queAreaEs = Area.objects.get(description__contains = a.description)
              
              #SEGUN QUE AREA ES DEBO DEFINIR EL TIPO- METAREA VI - OFF SHORE - COSTA
              tipo = definirTipoDePronostico(queAreaEs)
              

              pronos = Pronostico(texto = areaAtexto(a,b), area =  queAreaEs, tipo = tipo)

              print(f"-----> estoy por guardar el pronos de: {queAreaEs}")
              print(f"{pronos}")
              
              #LISTA DE AREAS DE POSIBLE TEMPORAL !!!¡¡????? PENSAR
              
            
              if (areaParaTemporal(a)!=None):
              
                lista_areas_para_temporales.append(queAreaEs)
              
              
              #Guardo el pronostico pero aun no le asigne el boletín
              pronos.save()

              #print(f"-----> GUARDE el pronos de: {queAreaEs}")
              
              #Ahora le asigno el boletín y vuelvo a guardarlo para que se genere el vinculo, en un solo paso no se puede hacer porque
              #es una relación muchos a muchos. 
              
              
              pronos.boletin.add(b)
              
              pronos.save()

              print(f"-----> EDITE y GUARDE el pronos de: {queAreaEs}")
              
    #Una vez que guarde todos los pronos en el boletín seteo 
    #Y guardo el horario del xml para saber cuando se actualizo pimet
    b = Boletin.objects.get(id = idBoletin)
    b.pronosticosGuardados = pronosticosGuardados
    b.save()    
    
    return lista_areas_para_temporales #retorno las areas candidatas a temporales        

#Esto es para no estar consultando el area ya que las divisiones de PIMET no se adaptan al boletin en cuanto 
#al subdomino.... Importante separar Norte y sur de 60 para no agregar areas antartida          
def definirTipoDePronostico(area):
  
  tipo = "Costa"
              
  if ("OFFSHORE" in area.description):
                tipo = "Offshore - N"
                
  else:
                if (area.domain == "Metarea VI"):
                  tipo= "Metarea VI - N"
                  
                if ("Weddell" in area.description):
                  tipo= "Metarea VI - S"
                if ("MarDeLaFlota" in area.description):
                  tipo= "Metarea VI - S"
                if ("Drake South" in area.description):
                  tipo= "Metarea VI - S"
                if ("Erebus" in area.description):
                  tipo= "Metarea VI - S"
                if ("Gerlache" in area.description):
                  tipo= "Metarea VI - S"
                  
                if ("Zona Malvinas" in area.description):
                  tipo= "Offshore - N" #Ojo en realidaden pimet es Metarea

                if ("Zona Larsen" in area.description):
                  tipo= "Offshore - S" 

                if ("Mar de la Flota Oeste" in area.description):
                  tipo= "Offshore - S" 

                if ("Mar de la Flota Este" in area.description):
                  tipo= "Offshore - S" 

                if ("Drake Sur (W58W)" in area.description):
                  tipo= "Offshore - S" 

                if ("Bahia Margarita" in area.description):
                  tipo= "Offshore - S" 

                if ("Drake Sur (E58W)" in area.description):
                  tipo= "Offshore - S" 
                  
          
                #Esto es domain Costas, pero de esa forma no aparece en navegante. lo dejamos en offshore
                if ("RIO DE LA PLATA INTERIOR" in area.description):
                  tipo= "Offshore - N" #Ojo en realidaden pimet es Metarea
                  
                if ("RIO DE LA PLATA INTERMEDIO" in area.description):
                  tipo= "Offshore - N" #Ojo en realidaden pimet es Metarea
                  
                if ("RIO DE LA PLATA EXTERIOR" in area.description):
                  tipo= "Offshore - N" #Ojo en realidaden pimet es Metarea
                  
                if ("DESEMBOCADURA RIO DE LA PLATA" in area.description):
                  tipo= "Offshore - N" #Ojo en realidaden pimet es Metarea
                  
              
                  
  return tipo



def verificar(request):
  
    nombreArchivo = "xmlPIMET/prueba.xml"
  
    root = definirRoot(nombreArchivo)
    pronosticosGuardados = "" #Variable para identificar cuándo se guardaron los
    #pronosticos en PIMET
    
    for pronostico in root: 
    #Instancia vacia
    #Por ahora no se usaria

    #Accedo a cada Area, elimino la posicion 0 porque es issue y esta vacio
      for area in pronostico:

          if (area.tag == "issue"):
            for x in area:
              if(x.tag == "timestamp"):
                pronosticosGuardados =x.text 

    fecha_objeto = datetime.strptime(pronosticosGuardados, "%Y%m%d%H%M%S")

#   Crear el diccionario
    diccionario = {
      "pronosticosGuardados":pronosticosGuardados,
      "año": fecha_objeto.year,
      "mes": fecha_objeto.month,
      "día": fecha_objeto.day,
      "hora": fecha_objeto.hour,
      "minuto": fecha_objeto.minute,
      "segundo": fecha_objeto.second
  }       

    # Obtener la fecha actual
    fecha_actual = datetime.now()     

    # Comprobar si la fecha del diccionario es igual a la fecha actual
    if (diccionario["año"] == fecha_actual.year and
      diccionario["mes"] == fecha_actual.month and
      diccionario["día"] == fecha_actual.day):
      resultado = "El día es correcto"
    else:
      resultado = "No es el día de hoy"
    
    
    diccionario["texto"] = resultado
    
    return render(request, 'AppMaritima/verificar.html', diccionario)


def verificarConRetorno(request):
  
    nombreArchivo = "xmlPIMET/prueba.xml"
  
    root = definirRoot(nombreArchivo)
    pronosticosGuardados = "" #Variable para identificar cuándo se guardaron los
    #pronosticos en PIMET
    
    for pronostico in root: 
    #Instancia vacia
    #Por ahora no se usaria

    #Accedo a cada Area, elimino la posicion 0 porque es issue y esta vacio
      for area in pronostico:

          if (area.tag == "issue"):
            for x in area:
              if(x.tag == "timestamp"):
                pronosticosGuardados =x.text 

    fecha_objeto = datetime.strptime(pronosticosGuardados, "%Y%m%d%H%M%S")

#   Crear el diccionario
    diccionario = {
      "pronosticosGuardados":pronosticosGuardados,
      "año": fecha_objeto.year,
      "mes": fecha_objeto.month,
      "día": fecha_objeto.day,
      "hora": fecha_objeto.hour,
      "minuto": fecha_objeto.minute,
      "segundo": fecha_objeto.second
  }       

    # Obtener la fecha actual
    fecha_actual = datetime.now()     

    # Comprobar si la fecha del diccionario es igual a la fecha actual
    if (diccionario["año"] == fecha_actual.year and
      diccionario["mes"] == fecha_actual.month and
      diccionario["día"] == fecha_actual.day):
      resultado = "El día es correcto"
    else:
      resultado = "No es el día de hoy"
    
    
    diccionario["texto"] = resultado
    
    return diccionario


def traducirAreas(areaCastellano):
  areaCastellano = areaCastellano.upper()
  areaIngles = areaCastellano

  #Oceanicas
  if("AREA SUDOESTE" in areaCastellano):
     areaIngles = areaCastellano.replace("AREA SUDOESTE" ,"SOUTH WEST AREA")

  if("AREA SUDESTE" in areaCastellano):
     areaIngles = areaCastellano.replace("AREA SUDESTE","SOUTH EAST AREA")

  if("AREA CENTRO OESTE" in areaCastellano):
     areaIngles = areaCastellano.replace("AREA CENTRO OESTE","CENTRAL WEST AREA")

  if("AREA CENTRO ESTE" in areaCastellano):
     areaIngles = areaCastellano.replace("AREA CENTRO ESTE","CENTRAL EAST AREA")

  if("AREA NORTE" in areaCastellano):
     areaIngles = areaCastellano.replace("AREA NORTE","NORTH AREA")

  if("DRAKE AREA" in areaCastellano):
     areaIngles = areaCastellano.replace("DRAKE AREA" ,"DRAKE AREA")

  #OFF SHORE
  if("ZONAMALVINAS" in areaCastellano):
     areaIngles = areaCastellano.replace("ZONAMALVINAS","ISLAS MALVINAS COASTS")

  if("FIN DEL MUNDO" in areaCastellano):
     areaIngles = areaCastellano.replace("FIN DEL MUNDO","FIN DEL MUNDO COASTS (54ºS - 55ºS)")

  if("PATAGONIA SUR" in areaCastellano):
     areaIngles = areaCastellano.replace("PATAGONIA SUR","SOUTH PATAGONIA COASTS (48ºS - 54ºS)")

  if("OFFSHORE SAN JORGE" in areaCastellano):
     areaIngles = areaCastellano.replace("OFFSHORE SAN JORGE" ,"GOLFO DE SAN JORGE  COASTS (45ºS - 48ºS)")

  #if("SAN JORGE SUR" in areaCastellano):
     #areaIngles = areaCastellano.replace("SAN JORGE SUR" ,"GOLFO DE SAN JORGE SUR COASTS (47ºS - 48ºS)")

  #if("SAN JORGE NORTE" in areaCastellano):
     #areaIngles = areaCastellano.replace("SAN JORGE NORTE" ,"GOLFO DE SAN JORGE NORTE COASTS (45ºS - 47ºS)")

  if("SAN JORGE" in areaCastellano):
     areaIngles = areaCastellano.replace("SAN JORGE" ,"GOLFO DE SAN JORGE COASTS (45ºS - 48ºS)")

  if("VALDES" in areaCastellano):
     areaIngles = areaCastellano.replace("VALDES" ,"PENINSULA DE VALDES COASTS (41ºS - 45ºS)")

  if("BAHIA BLANCA" in areaCastellano):
     areaIngles = areaCastellano.replace("BAHIA BLANCA" ,"RINCON BAHIA BLANCA COASTS (38º30S - 41ºS)")

  if("MAR DEL PLATA" in areaCastellano):
     areaIngles = areaCastellano.replace("MAR DEL PLATA" ,"MAR DEL PLATA COASTS (36º17S - 38º30S)")

  if("DESEMBOCADURA RIO DE LA PLATA" in areaCastellano):
     areaIngles = areaCastellano.replace("DESEMBOCADURA RIO DE LA PLATA","RIO DE LA PLATA MOUTH")

  if("RIO DE LA PLATA EXTERIOR" in areaCastellano):
     areaIngles = areaCastellano.replace("RIO DE LA PLATA EXTERIOR" ,"OUTER RIO DE LA PLATA")

  if("RIO DE LA PLATA INTERIOR" in areaCastellano):
     areaIngles = areaCastellano.replace("RIO DE LA PLATA INTERIOR" ,"INNER RIO DE LA PLATA")

  if("RIO DE LA PLATA INTERMEDIO" in areaCastellano):
     areaIngles = areaCastellano.replace("RIO DE LA PLATA INTERMEDIO" ,"INTERMEDIATE RIO DE LA PLATA")

  if("OFFSHORE RIO DE LA PLATA" in areaCastellano):
     areaIngles = areaCastellano.replace("OFFSHORE RIO DE LA PLATA" ,"URUGUAY SOUTH EAST COASTS")


  # Remover el subString "OFFSHORE"
  areaIngles = areaIngles.replace("OFFSHORE ", "")

  return areaIngles


def escribirTextoOlasSHN(area, bole):

  #print(f"Voy a hacer el pronostico de olas de {area.description}")
  #print(f"El id de boletín en cuestion es: {bole.id}")

  #Uso get porque es uno solo
  boletin = Boletin.objects.get(id = bole.id)

  print(f"--------> BOLETIN: {boletin.pronosticosOlasSHN}")

  texto = get_second_attribute(boletin.pronosticosOlasSHN, area.description)
  print(f"--------> TEXTO: {texto}")
  return f"\nWAVES: {texto}"


def get_second_attribute(datos, first_attribute):
        print(f"BUSCO en la linea: {first_attribute}")
        lines = datos.split('\n')
        for line in lines:
            if ';' in line:
                attrs = line.split(';')
                if attrs[0].strip().upper() in first_attribute.upper():
                    return attrs[1].strip()
        return "Waves Forecast not found"