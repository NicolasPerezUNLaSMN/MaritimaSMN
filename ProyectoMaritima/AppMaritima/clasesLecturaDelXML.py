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
