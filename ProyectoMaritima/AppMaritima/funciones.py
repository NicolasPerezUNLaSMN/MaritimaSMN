from cgi import print_form
from xml.etree.ElementTree import parse


from AppMaritima.models import Pronostico, Boletin, Area

from AppMaritima.clasesLecturaDelXML import *

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
        
          print(f"TRABAJO CON AREA: {a}")

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
          print(f"--------FIN DEL AREA---> {a}")

          if (a.domain == 'Metarea VI'):
            print(f"--------META---> \n")
            if ( float(a.latitude) <= -60):
              forecastSur60.list_area.append(a)

            if ( float(a.latitude) > -60):
              forecast.list_area.append(a)

          if (a.domain == 'Costas'):

            if (a.description.find('OFFSHORE')!=-1):
              print(f"--------OFF--> \n")
              forecastOffShore.list_area.append(a)
            else:
                forecastCostas.list_area.append(a)
                print(f"--------COSTAS---> \n")
          
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

      vel = 0
      print("VELOOOO", velo , type(velo))
      
      #Si llega un digito lo paso a float
      if (velo.isdigit()):
        
        velo = float(velo)
        
        if (velo <= 0.1):
          vel = 0
      #Si no llega un digito lo pongo en 0    
      else:
        velo = float (0)    
        

      retorno = ""

      if ( vel >= 0 and vel<= 3):
        retorno = 1
      if ( vel >= 4 and vel<= 6):
        retorno = 2
      if ( vel >= 7 and vel<= 10):
        retorno = 3
      if ( vel >= 11 and vel<= 16):
        retorno = 4
      if ( vel >= 17 and vel<= 21):
        retorno = 5
      if ( vel >= 22 and vel<= 27):
        retorno = 6
      if ( vel >= 28 and vel<= 33):
        retorno = 7
      if ( vel >= 34 and vel<= 40):
        retorno = 8
      if ( vel >= 41 and vel<= 47):
        retorno = 9
      if ( vel >= 48 and vel<= 55):
        retorno = 10
      if ( vel >= 56 and vel<= 63):
        retorno = 11
      if ( vel >= 64):
        retorno = 12

      return str(retorno)
  
  
  
def transformarASectores(vientoD):
  retorno = vientoD

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
       
        if (horaActual < 18): #Si se crea el boletin en el turno diurno
          
          for i,horasDelXML in enumerate(elemento.list_timeranges):
            
            if horasDelXML.h == 12:
              
              hora1 = i
              
            if horasDelXML.h == 24:
              
              hora2 = i
              
            if horasDelXML.h == 36:
              
              hora3 = i
        else:  #Si se ejecuta para el turno noche
          
            for i,horasDelXML in enumerate(elemento.list_timeranges):
            
              if horasDelXML.h == 24:
                
                hora1 = i
                
              if horasDelXML.h == 36:
                
                hora2 = i
                
              if horasDelXML.h == 48:
                
                hora3 = i


        return hora1,hora2,hora3 #Retorno las tres horaas que uso para el pronos

def escribirTextoOlas(direccion, altura):


        

        #####Checkear y validar esto entre diuno y nocturno y distintos modelos
        hora1,hora2,hora3 = tomarHorasIndicadasSegunTurno(altura)
        ########


       

        #Value[0] altura en metros
        alturaInicial = altura.list_timeranges[hora1].list_values[0].text
        alturaMedia = altura.list_timeranges[hora2].list_values[0].text
        alturaFinal = altura.list_timeranges[hora3].list_values[0].text
        
        print(f"\nPRUEBA DE HORARIOS DE OLAS: {altura.list_timeranges[hora1]}{altura.list_timeranges[hora2]}{altura.list_timeranges[hora3]}")
        

        #Value[1] direccion en 16 cuadrantes
        dirInicial = transformarOlasA8Cuadrantes(direccion.list_timeranges[hora1].list_values[1].text)
        dirMedia = transformarOlasA8Cuadrantes(direccion.list_timeranges[hora2].list_values[1].text)
        dirFinal = transformarOlasA8Cuadrantes(direccion.list_timeranges[hora3].list_values[1].text)

     
        #Acá se guarda el texto final
        retorno = ""


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

                        retorno = retorno +" TEMPO BACK " +dirMedia +f" {alturaMedia} "



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

                            

                            retorno = retorno + dirInicial  +f" {alturaInicial}/{alturaMedia} "  +f" BACK " + dirFinal +f" {alturaFinal}"


                      #Misma direccion que la ultima pero cambio de velocidad
                      if (dirMedia == dirFinal and not alturaMedia == alturaFinal):

                          

                            retorno = retorno + dirInicial  +f" {alturaInicial}" +f" BACK " + dirFinal +f" {alturaMedia}/{alturaFinal}"  



        retorno = retorno +". "
        

        return retorno 

#Direccion y velocidad tienen una lista de horas y en cada hora esta el valor
def escribirTextoViento(direccion, velocidad):

        #Transformo direcciones a sectores 

        for t in direccion.list_timeranges:

          t.list_values[1].text = transformarASectores(t.list_values[1].text)

        #"""OBS: list_ parametros : #1-WD viento direccion  6- WS vel viento
        #        list_timeranges:   #0 - 6z  #1- 12Z    2-18  3-24/00   4-30/06   5-36/12
        #        list_values: 1 para la direccion así transforma grados en puntos cardinales list_values[1]
        #        list_values: 0 para velocidad así lo da en kT list_values[0]"""

        #####Checkear y validar esto entre diuno y nocturno y distintos modelos
        hora1,hora2,hora3 = tomarHorasIndicadasSegunTurno(velocidad)
        ########
         
        print(f"\nPRUEBA DE HORARIOS DE VEINTO: {velocidad.list_timeranges[hora1]}{velocidad.list_timeranges[hora2]}{velocidad.list_timeranges[hora3]}")
        

        velInicial = int(ktABeaufort(velocidad.list_timeranges[hora1].list_values[0].text) )
      
        velMedia = int(ktABeaufort(velocidad.list_timeranges[hora2].list_values[0].text))
        
        velFinal = int(ktABeaufort(velocidad.list_timeranges[hora3].list_values[0].text) )
        

        velInicialConRafagas = ktABeaufort(velocidad.list_timeranges[hora1].list_values[0].text) +" " +agregarONoRafagas(ktABeaufort(velocidad.list_timeranges[hora1].list_values[0].text))
        velMediaConRafagas = ktABeaufort(velocidad.list_timeranges[hora2].list_values[0].text) +" " +agregarONoRafagas(ktABeaufort(velocidad.list_timeranges[hora2].list_values[0].text))
        velFinalConRafagas = ktABeaufort(velocidad.list_timeranges[hora3].list_values[0].text)+" "  +agregarONoRafagas(ktABeaufort(velocidad.list_timeranges[hora3].list_values[0].text))


        dirInicial = direccion.list_timeranges[hora1].list_values[1].text
        dirMedia = direccion.list_timeranges[hora2].list_values[1].text
        dirFinal = direccion.list_timeranges[hora3].list_values[1].text

     
        #Acá se guarda el texto final
        retorno = ""


        #Si la inicial es igual a la final
        if ( dirInicial == dirFinal):

                #Aumento o disminuyo?
                cambio = "SIN CAMBIO"
                if (velInicial < velFinal):
                  cambio = "INCR"

                if (velInicial > velFinal):
                  cambio = "DISM"

                #Si cambio la velocidad
                if (not( cambio == "SIN CAMBIO")):
                  retorno = retorno + dirInicial +f" {velInicialConRafagas} " +f" {cambio} "  +f" {velFinalConRafagas}"

                else: #No cambio la velocidad
                  retorno = retorno + dirInicial +f" {velInicialConRafagas} "


                #Si la intermedia es distinta, le hago un cambio temporario
                if (not  dirInicial == dirMedia):

                        retorno = retorno +" TEMPO BACK " +dirMedia +f" {velMediaConRafagas} "



        else:  #distintas direcciones iniciales y finales

                #Si la del medio no es igual a ninguna de las dos, hago el cambio
                if (not (dirMedia == dirInicial) and not (dirMedia == dirFinal) ):

                      retorno = retorno + dirInicial +f" {velInicialConRafagas} " +f" BACK " + dirMedia +f" {velMediaConRafagas} "+f" AND BACK " + dirFinal +f" {velFinalConRafagas}"


                else:  #Si la dirección del medio es igual a alguna de las dos

                      #Igual a la primera  o a la ultima, ignoro ese cambio
                      if ((dirMedia == dirInicial and velMedia == velInicial) or (dirMedia == dirFinal and velMedia == velFinal)):

                            retorno = retorno + dirInicial +f" {velInicialConRafagas} " +f" BACK " + dirFinal +f" {velFinalConRafagas}"

                      #Misma direccion que la primera pero cambio de velocidad
                      if (dirMedia == dirInicial and not velMedia == velInicial):

                            maximo = max([velInicial, velMedia])

                            retorno = retorno + dirInicial  +f" {velInicial}/{velMedia} " +agregarONoRafagas(maximo) +f" BACK " + dirFinal +f" {velFinalConRafagas}"


                      #Misma direccion que la ultima pero cambio de velocidad
                      if (dirMedia == dirFinal and not velMedia == velFinal):

                            maximo = max([velFinal, velMedia])

                            retorno = retorno + dirInicial  +f" {velInicialConRafagas}" +f" BACK " + dirFinal +f" {velMedia}/{velFinal}" +agregarONoRafagas(maximo) 



        retorno = retorno + ". "
        

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

        retorno = " "

        #Si 1 y 5 son distintas agrego el TO
 
        hora1,hora2,hora3 = tomarHorasIndicadasSegunTurno(visibilidad)
 
        print(f"\nPRUEBA DE HORARIOS DE VEINTO: {visibilidad.list_timeranges[hora1]}{visibilidad.list_timeranges[hora2]}{visibilidad.list_timeranges[hora3]}")
        

        
        
        if (visibilidad.list_timeranges[hora1].list_values[0].text != visibilidad.list_timeranges[hora3].list_values[0].text ):

          retorno = f"VIS {transformarNumeroAVisibilidad(visibilidad.list_timeranges[hora1].list_values[0].text)} TO  {transformarNumeroAVisibilidad(visibilidad.list_timeranges[hora3].list_values[0].text)}"
        
        else: 

          retorno = f"VIS {transformarNumeroAVisibilidad(visibilidad.list_timeranges[hora1].list_values[0].text)}"


        if (visibilidad.list_timeranges[hora1].list_values[0].text != visibilidad.list_timeranges[hora2].list_values[0].text ):
          
          if (visibilidad.list_timeranges[hora3].list_values[0].text != visibilidad.list_timeranges[hora2].list_values[0].text ):

            retorno = retorno + f", OCNL {transformarNumeroAVisibilidad(visibilidad.list_timeranges[hora2].list_values[0].text)}"

        retorno = retorno +". "
        
        return retorno
      
    
def codigoAFenomeno(codigo):

  

  retorno = "WORSENING"   #Inicialmente desmejorando, para que simplifique el algoritmo


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

  if codigo == "74":
    retorno = "SHOWERS"

  if codigo == "77":
    retorno = "RAIN AND SNOW"

  if codigo == "79":
    retorno = "OCNL SNOW"

  if codigo == "81":
    retorno = "RAIN AND THUNDERSTORM"

  if codigo == "84":
    retorno = "HEAVY THUNDERSTORM"

  if codigo == "72":
    retorno = "OCNL RAIN"

  if codigo == "76":
    retorno = "OCNL STORM"

  if codigo == "51":
    retorno = "SPRAY"

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

  return retorno


#Pronsotico tienen una lista de horas y en cada hora esta el valor, solo el valor 0 interesa
def escribirPronostico(pronostico):

        #list_timeranges[5].list_values[0].text)  #
        
        #5 ---pronostico del tiempo.... 0,2,4 son las 12, 00 y 12(+1)

        retorno = ". "
        
        hora1,hora2,hora3 = tomarHorasIndicadasSegunTurno(pronostico)

        #escribo los tres fenomenos que usaremos
        fenomeno1 = codigoAFenomeno(pronostico.list_timeranges[hora1].list_values[0].text)
        fenomeno2 = codigoAFenomeno(pronostico.list_timeranges[hora2].list_values[0].text)
        fenomeno3 = codigoAFenomeno(pronostico.list_timeranges[hora2].list_values[0].text)



        print(f"\nPRUEBA DE HORARIOS DE FENOMENO: {pronostico.list_timeranges[hora1]}{pronostico.list_timeranges[hora2]}{pronostico.list_timeranges[hora3]}")
        



        #Si hay algun fenomeno significativo
        if (not(fenomeno1 == "WORSENING" and fenomeno2 == "WORSENING" and fenomeno3 == "WORSENING") ):

          
          #12 = 00   pero distinto de 12+1
          if (fenomeno1 == fenomeno2 and not fenomeno2 == fenomeno3):

            if (fenomeno3 == "WORSENING"):

              fenomeno3 = "IMPR"

            retorno = retorno + fenomeno1  + " LATER " +fenomeno3 +"."


          #Los tres dintintos
          if ( not (fenomeno1 == fenomeno2)  and  not (fenomeno2 == fenomeno3) and  not (fenomeno1 == fenomeno3)):

            if (fenomeno3 == "WORSENING"):

              fenomeno3 = "IMPR"

              retorno =retorno + fenomeno1  + " LATER " +fenomeno2 +" AND LATER " +fenomeno3 +"."



            if (fenomeno2 == "WORSENING"):

              fenomeno2 = "IMPR"

              retorno =retorno + fenomeno1  + " LATER " +fenomeno3 +", OCNL  " +fenomeno2 +"."


            if (fenomeno1 == "WORSENING"):
            
              retorno =retorno + fenomeno1 +", " +fenomeno2 +" LATER " +fenomeno3 +"."


          #12 = 12+1 pero distintos a 00
          if ( fenomeno1 == fenomeno3 and not (fenomeno2 == fenomeno3)):


             if (fenomeno2 == "WORSENING"):

              fenomeno2 = "IMPR"

              retorno =retorno + fenomeno1  + " AND OCNL " +fenomeno2 +"."


             if (fenomeno1 == "WORSENING"):

              fenomeno2 = "IMPR"

              retorno =retorno +  " OCNL " +fenomeno2 +"."

          

          #12 != 00 pero == igual a 12+1
          if ( not (fenomeno1 == fenomeno2) and fenomeno2 == fenomeno3):

            if (fenomeno2 == "WORSENING"):
              fenomeno2 = "IMPR"

            retorno =retorno + fenomeno1 + " LATER " +fenomeno2 +"."

        retorno = retorno +". "

        return retorno
    
def areaAtexto(area):

  texto = f"{area.description}: ".upper()

  #genero el viento del area, solo con los parametros 1 y 6
  viento = escribirTextoViento(area.list_parameters[1], area.list_parameters[6])

  #genero el pronostico, solo con el parametro ww
  fenomeno = escribirPronostico(area.list_parameters[5])

  #genero la visibilidad
  visibilidad = escribirVisibilidad(area.list_parameters[7])

  ola = escribirTextoOlas(area.list_parameters[2],area.list_parameters[0])

  texto = texto + viento  +fenomeno  +visibilidad  +ola+"."

  #Limpiar errores tippicos, luego hacerlo mejor, prioridad baja


  texto = texto.replace(" . . ", ".")
  texto = texto.replace(". .", ".")
  texto = texto.replace("..", ".")
  texto = texto.replace("   ", " ")
  texto = texto.replace(" .", ".")
  texto = texto.replace(". ", ".")
  
  

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
                            domain= area.attrib['domain'], orden=ordenNav)
          
          areaModels.save()
          
          
          
def cargarPronosticosDesdeElXML(nombreArchivo, idBoletin):
  
    root = definirRoot(nombreArchivo)
    
    for pronostico in root: 
    #Instancia vacia
    #Por ahora no se usaria

    #Accedo a cada Area, elimino la posicion 0 porque es issue y esta vacio
      for area in pronostico:

      
      
          ###################ESTRUCTURA PRINCIPAL; CARGA AREAS CON PRONOSTICOS######
          if (area.tag == 'area'):
              #instancio un area
              a = AreaXML(area.attrib['id'],area.attrib['latitude'],area.attrib['longitude'],area.attrib['description'], area.attrib['domain'])
            
              print(f"TRABAJO CON AREA: {a}")

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
             
              queAreaEs = Area.objects.get(description__contains = a.description)
              
              #SEGUN QUE AREA ES DEBO DEFINIR EL TIPO- METAREA VI - OFF SHORE - COSTA
              tipo = definirTipoDePronostico(queAreaEs)
              

              pronos = Pronostico(texto = areaAtexto(a), area =  queAreaEs, tipo = tipo)
              
              #Guardo el pronostico pero aun no le asigne el boletín
              pronos.save()
              
              #Ahora le asigno el boletín y vuelvo a guardarlo para que se genere el vinculo, en un solo paso no se puede hacer porque
              #es una relación muchos a muchos. 
              b = Boletin.objects.get(id = idBoletin)
              
              pronos.boletin.add(b)
              
              pronos.save()
              
              

#Esto es para no estar consultando el area ya que las divisiones de PIMET no se adaptan al boletin en cuanto 
#al subdomino.... Importante separar Norte y sur de 60 para no agregar areas antartida          
def definirTipoDePronostico(area):
  
  tipo = "Costa"
              
  if ("OFFSHORE" in area.description):
                tipo = "Offshore"
                
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
                  
                if ("ZonaMalvinas" in area.description):
                  tipo= "Offshore" #Ojo en realidaden pimet es Metarea
                  
          
                #Esto es domain Costas, pero de esa forma no aparece en navegante. lo dejamos en offshore
                if ("RIO DE LA PLATA INTERIOR" in area.description):
                  tipo= "Offshore" #Ojo en realidaden pimet es Metarea
                  
                if ("RIO DE LA PLATA INTERMEDIO" in area.description):
                  tipo= "Offshore" #Ojo en realidaden pimet es Metarea
                  
                if ("RIO DE LA PLATA EXTERIOR" in area.description):
                  tipo= "Offshore" #Ojo en realidaden pimet es Metarea
                  
                if ("DESEMBOCADURA RIO DE LA PLATA" in area.description):
                  tipo= "Offshore" #Ojo en realidaden pimet es Metarea
                  
              
                  
  return tipo