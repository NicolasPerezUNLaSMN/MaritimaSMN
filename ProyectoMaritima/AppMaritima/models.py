from cgi import print_form
from django.db import models
from django.db.models.fields import BooleanField


# Create your models here.

class Area(models.Model): #son fijas, son las areas pimet
    
    #Mantengo los nombres del xml por comodidad
    idPimet = models.IntegerField()
    latitude = models.CharField(max_length=10)
    longitude = models.CharField(max_length=10)
    description = models.CharField(max_length=30)
    domain = models.CharField(max_length=30)
    
    def __str__(self):
        return f"{self.description} ({self.domain})"
    

class Boletin(models.Model):
    
    #fecha exacta de la creación
    emitido = models.DateTimeField(auto_now_add=True)
    modificado = models.DateTimeField(auto_now=True)
    #Fecha del boletin
    valido = models.DateField()
    
    hora = models.IntegerField(null=True)
    
    def __str__(self):
        return f"ID: {self.id} ------- {self.valido}"
    
    
#Parte I Avisos
class Aviso(models.Model):
    
    #Inicia en cero cada año
    numero = models.IntegerField(null=True, blank=True)
    #incrementa en uno cada vez que se actualiza, no cabia el numero
    actualizacion = models.IntegerField(null=True, blank=True)
    
    
    
    tipo = models.CharField(max_length=30)
    direccion = models.CharField(max_length=10,null=True, blank=True)
    
    desde = models.DateField(null=True, blank=True)
    horaDesde = models.IntegerField(null=True, blank=True)
    hasta = models.DateField(null=True, blank=True)
    horaHasta = models.IntegerField(null=True, blank=True)
    activo = models.BooleanField(null=True, blank=True)
    
    #Cada aviso puede estar en varios boletines, y cada boletin tiene muchos avisos
    boletin = models.ManyToManyField(Boletin)
    
    area = models.ManyToManyField(Area)
    
    def __str__(self):
        return f"ID: {self.id} ----  {self.numero} --- {self.tipo} --- {self.direccion}"
    
    
    def paraTXTEnIngles(self):
        
        #Hay dos casos, aviso activo y aviso cesado
        texto = f"WARNING {self.numero}: "
        
        #Si está activo
        if (self.activo):
            
            texto = texto + f"{self.tipo} " + f" FROM {self.direccion} WITH GUST IN"
            
            #En qué areas?
            
            for a in self.area.all():
                texto = texto + f" {(a.description.upper())}"
            
            
            #si tiene hora de inicio
            if (not self.horaDesde == -1):
                
                texto = texto + f" FROM {self.desde} / {self.horaDesde}"
                
            #si tiene hora de fin
            if (not self.horaHasta == -1):
                
                texto = texto + f" UNTIL {self.hasta} / {self.horaHasta}"
            
        #Si fue cesado   
        else:
            texto = texto + "CEASED"  
        
        texto = texto +"\n"
        
        return texto
    
   
#Parte II SItuacion 
class Situacion(models.Model):
    
    sistema = models.CharField(max_length=60)
    
    valorInicial = models.IntegerField(null=True, blank=True)

    
    movimiento = models.CharField(max_length=4,null=True, blank=True)
    evolucion = models.CharField(max_length=30,null=True, blank=True)
    
    posicionInicial = models.CharField(max_length=60,null=True, blank=True)
    momentoInicial = models.DateField(null=True, blank=True)
    horaInicial = models.IntegerField(null=True, blank=True)
    
    posicionFinal = models.CharField(max_length=60,null=True, blank=True) 
    momentoFinal = models.DateField(null=True, blank=True)
    horaFinal = models.IntegerField(null=True, blank=True)
    
    navtex = BooleanField(null=True, blank=True)
    
    #Si la situacion está vigente lo mantenemos activo
    activo = models.BooleanField(null=True, blank=True)
    
    #Cada situacion puede estar en varios boletines, y cada boletin tiene muchas situaciones
    boletin = models.ManyToManyField(Boletin)
    
    def __str__(self):
        return f"ID: {self.id} ----  SISTEMA:  {self.sistema} --- "
    
    def paraTXTEnIngles(self):
        
        #Solo me interesan los activos, cesados no aparecen en el boletin
        if ( self.activo):
            
            #mejorar esto, porque en la base de datos en vez de vacio se guarda con -1
            valorInicial = ""
            if ( self.valorInicial != -1):
                valorInicial = self.valorInicial
            
            texto = f"{self.sistema} {valorInicial} MOV {self.movimiento} {self.evolucion}"
            
            
            #Si tiene posición inicial
            if (not self.horaInicial == -1):
                
                texto = texto +f"AT {self.posicionInicial} BY {self.momentoInicial}/{self.horaInicial}"
                
            #Si tiene posición final
            if (not self.horaFinal == -1):
                
                texto = texto +f" EXP {self.posicionFinal} BY {self.momentoFinal}/{self.horaFinal}"
            texto = texto +"\n"
            return texto

#Lo envia prefectura, solo guardo el texto
class Hielo(models.Model):
    
    creado = models.DateField(auto_now_add=True)
    texto = models.TextField(null=True, blank=True)
    activo = models.BooleanField(null=True, blank=True)
    
    #Planteo un muchos a muchos porque los hielos no siempre llegan a horario, por ahí el mismo hielo pertenece a varios boletines
    boletin = models.ManyToManyField(Boletin)
    
    
    def paraTXTEnIngles(self):
        
        if ( self.activo):
            
            return self.texto
    
#Parte III - Pronostico
#Esto esta persistido en el xml,no se si tiene sentido guardarlo en la bd, por eso
#solo guardo el texto. 

class Pronostico (models.Model):
    
    
    tipo = models.TextField(null=True, blank=True)
    
    texto = models.TextField(null=True, blank=True)
    
    #Cada pronostico es de un area pimet - y cada area tiene muchos 
    # #pronsoticos, según boletin 
    area = models.ForeignKey(Area,on_delete=models.CASCADE, null=True)
    
    #boletin = models.ForeignKey(Boletin,on_delete=models.CASCADE, null=True)
    boletin = models.ManyToManyField(Boletin)
    
    
    def __str__(self):
        return f"ID: {self.id} ------ > ({self.tipo}) "

    def paraTXTEnIngles(self):
        
        return self.texto.upper() +"\n"
    
    
    