from xml.etree.ElementTree import parse

from AppMaritima.models import Area

archivoXML = 'prueba.xml'

tree = parse(archivoXML)

root = tree.getroot()

class Value:

  def __init__(self,  text, unit):
    self.text = text
    self.unit = unit

  def __str__(self):
    return f"Valor:  {self.text} {self.unit}"


class Timerange:

  


  def __init__(self, h, datetime):
    self.h = h
    self.datetime = datetime   
    self.list_values = []


  def __str__(self):
    return f"De la hora: {self.h}, completa: {self.datetime}"


class Parameter:

  


  def __init__(self, id):
    self.id = id
    self.list_timeranges = []
  

  def __str__(self):
    return f"El parametro es: {self.id}" 


class AreaXML:

  
  def __init__(self, id, latitude, longitude, description, domain):
    self.id = id
    self.latitude = latitude
    self.longitude = longitude
    self.description = description
    self.domain = domain
    self.list_parameters  = []
   


  def __str__(self):
    return f"Esta es el area: {self.description} del dominio: {self.domain}" 


class Forecast:

  

  

  def __init__(self, year, month, day, hour, minute ):

    self.year = year
    self.month = month
    self.day = day
    self.hour = hour
    self.minute = minute
    self.list_area = []


  def __str__(self):
    return f"Pronostico del {self.year}/{self.month}/{self.day}   {self.hour}:{self.minute}"


forecast = Forecast(0,0,0,0,0)
forecastSur60 = Forecast(0,0,0,0,0)
forecastOffShore = Forecast(0,0,0,0,0)
forecastCostas = Forecast(0,0,0,0,0)
forecastRio = Forecast(0,0,0,0,0)

def leerXML():

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

      if (velo != '0.1'):
        vel = int (velo)
      else:
        vel = 0

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

def escribirTextoOlas(direccion, altura):


        
       


        #####Checkear y validar esto entre diuno y nocturno y distintos modelos
        hora1 = 1
        hora2 = 3
        hora3 = 5
        ########


       

        #Value[0] altura en metros
        alturaInicial = altura.list_timeranges[hora1].list_values[0].text
        alturaMedia = altura.list_timeranges[hora2].list_values[0].text
        alturaFinal = altura.list_timeranges[hora3].list_values[0].text
        

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

        """OBS: list_ parametros : #1-WD viento direccion  6- WS vel viento
                list_timeranges:   #0 - 6z  #1- 12Z    2-18  3-24/00   4-30/06   5-36/12
                list_values: 1 para la direccion así transforma grados en puntos cardinales list_values[1]
                list_values: 0 para velocidad así lo da en kT list_values[0]"""

        #####Checkear y validar esto entre diuno y nocturno y distintos modelos
        hora1 = 1
        hora2 = 3
        hora3 = 5
        ########


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

        if (visibilidad.list_timeranges[1].list_values[0].text != visibilidad.list_timeranges[5].list_values[0].text ):

          retorno = f"VIS {transformarNumeroAVisibilidad(visibilidad.list_timeranges[1].list_values[0].text)} TO  {transformarNumeroAVisibilidad(visibilidad.list_timeranges[5].list_values[0].text)}"
        
        else: 

          retorno = f"VIS {transformarNumeroAVisibilidad(visibilidad.list_timeranges[1].list_values[0].text)}"


        if (visibilidad.list_timeranges[1].list_values[0].text != visibilidad.list_timeranges[3].list_values[0].text ):
          
          if (visibilidad.list_timeranges[5].list_values[0].text != visibilidad.list_timeranges[3].list_values[0].text ):

            retorno = retorno + f", OCNL {transformarNumeroAVisibilidad(visibilidad.list_timeranges[3].list_values[0].text)}"

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

        #escribo los tres fenomenos que usaremos
        fenomeno1 = codigoAFenomeno(pronostico.list_timeranges[0].list_values[0].text)
        fenomeno2 = codigoAFenomeno(pronostico.list_timeranges[2].list_values[0].text)
        fenomeno3 = codigoAFenomeno(pronostico.list_timeranges[4].list_values[0].text)

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
  
  texto = texto +"\n\r"

  return texto








def cargarAreasDesdeElXML():

  for pronostico in root: 
    #Instancia vacia
    #Por ahora no se usaria

    #Accedo a cada Area, elimino la posicion 0 porque es issue y esta vacio
    for area in pronostico:

      
      ###################ESTRUCTURA PRINCIPAL; CARGA AREAS CON PRONOSTICOS######
      if (area.tag == 'area'):
          #instancio un area
          a = Area(area.attrib['id'],area.attrib['latitude'],area.attrib['longitude'],area.attrib['description'], area.attrib['domain'])
        
          areaModels = Area(idPimet=float(area.attrib['id']), latitude=area.attrib['latitude'],
                            longitude=area.attrib['longitude'], description=area.attrib['description'],
                            domain= area.attrib['domain'])
          
          areaModels.save()
          
          
         