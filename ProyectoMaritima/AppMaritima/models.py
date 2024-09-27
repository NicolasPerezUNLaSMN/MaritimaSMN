from cgi import print_form
from django.db import models
from django.db.models.fields import BooleanField


# Create your models here.

class Area(models.Model): #son fijas, son las areas pimet
    
    #Mantengo los nombres del xml por comodidad
    idPimet = models.IntegerField()
    latitude = models.CharField(max_length=20)
    longitude = models.CharField(max_length=20)
    description = models.CharField(max_length=80) #castellano
    descriptionIngles= models.CharField(max_length=80,default='INGLES')  #En ingles
    domain = models.CharField(max_length=30)
    
    orden = models.IntegerField(default=999)
    
    def __str__(self):
        return f"IDPIME: {self.idPimet}--- {self.description} ({self.domain} {self.latitude}  {self.longitude})"
    

class Boletin(models.Model):
    
    #fecha exacta de la creación
    emitido = models.DateTimeField(auto_now_add=True)
    modificado = models.DateTimeField(auto_now=True)
    #Fecha del boletin
    valido = models.DateField()  
    hora = models.IntegerField(null=True)
    
    pronosticosGuardados = models.CharField(max_length=60 ,default='0000000')

    pronosticosOlasSHN = models.TextField(default='0000000')
    
    def __str__(self):
        return f"Boletín para -------> {self.valido}:{self.hora}  --> Generado/id: {self.emitido}{self.id}"
    
#Parte II SItuacion 
class Situacion(models.Model):
    
    #Inicia en cero cada año
    numero = models.IntegerField(null=True, blank=True)
    #incrementa en uno cada vez que se actualiza, no cabia el numero
    actualizacion = models.IntegerField(null=True, blank=True)
    
    sistema = models.CharField(max_length=60)
    
    valorInicial = models.IntegerField(null=True, blank=True)

    
    movimiento = models.CharField(max_length=8,null=True, blank=True)
    evolucion = models.CharField(max_length=30,null=True, blank=True)
    
    posicionInicial = models.CharField(max_length=60,null=True, blank=True)
    momentoInicial = models.DateField(null=True, blank=True)
    horaInicial = models.IntegerField(null=True, blank=True)
    
    posicionFinal = models.CharField(max_length=60,null=True, blank=True) 
    momentoFinal = models.DateField(null=True, blank=True)
    horaFinal = models.IntegerField(null=True, blank=True)
    
    navtex = BooleanField(default = False, null=True, blank=True)
    sur60= BooleanField(default = False, null=True, blank=True)

    esPresente = BooleanField(null=True, blank=True)
    
    #Si la situacion está vigente lo mantenemos activo
    activo = models.BooleanField(null=True, blank=True)
    
    #Cada situacion puede estar en varios boletines, y cada boletin tiene muchas situaciones
    boletin = models.ManyToManyField(Boletin)
    
    def __str__(self):
        return self.paraTXTEnIngles()
    
    def paraTXTEnIngles(self): #Texto en ingles que aparece en el boletín
        
        #Solo me interesan los activos, cesados no aparecen en el boletin
        #if ( self.activo):
            
            #mejorar esto, porque en la base de datos en vez de vacio se guarda con -1
            valorInicial = ""
            if ( self.valorInicial != -1):
                valorInicial = self.valorInicial
            

            if ( self.movimiento != "NOT MOV"):
                texto = f"{self.sistema} {valorInicial} MOVING {self.movimiento} {self.evolucion}"
            else:
                texto = f"{self.sistema} {valorInicial}  NOT MOV {self.evolucion}"
            
            
            #Si tiene posición inicial
            if (not self.horaInicial == -1):
                
                texto = texto +f" AT {self.posicionInicial} BY {self.momentoInicial}/{self.horaInicial}"
                
            #Si tiene posición final
            if (not self.horaFinal == -1):
                
                texto = texto +f" EXPECTED {self.posicionFinal} BY {self.momentoFinal}/{self.horaFinal}"
            texto = texto +"\n"
            return texto
        
    def paraTXTEnInglesResumen(self): #Este texto es el que aparece en el aviso de temporal asociado
        
        #Solo me interesan los activos, cesados no aparecen en el boletin
        if ( self.activo):
            
           
            
            texto = f"{self.sistema} "
            
            return texto

    
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
    
    situacion = models.ManyToManyField(Situacion)
    
    provoca = models.CharField(default="PROVOKE", max_length=30)
    
    navtex = BooleanField(default = False, null=True, blank=True)
    sur60= BooleanField(default = False, null=True, blank=True)

    def __str__2(self):
        return f"NUMERO: ---->  {self.numero} TIPO: ---> {self.tipo} ---> DIRECCIÓN ---> {self.direccion}"
    
    def __str__(self):
        return self.paraTXTEnIngles()
    
    
    def paraTXTEnIngles(self):
        

        
        #Hay dos casos, aviso activo y aviso cesado
        
        #traigo la situación, a futuro se podria tener varias, por ahora solo UNA
        listaDeSituacionesAsignadas= []
        contador = 0
        for s in self.situacion.all():
            listaDeSituacionesAsignadas.append(s)
            contador = contador * 1
        
      
    # Verifica si hay situaciones asignadas
    
        if listaDeSituacionesAsignadas:
          texto = f"WARNING {self.numero}: {listaDeSituacionesAsignadas[0].paraTXTEnInglesResumen()} {self.provoca} "
        else:
          texto = f"WARNING {self.numero}: Información no disponible"

        #Si está activo
        if (self.activo):
                
                texto = texto + f"{self.tipo} " + f" FROM {self.direccion} WITH GUST IN"
                
                #En qué areas?
                
                for a in self.area.all():
                    texto = texto + f" {(a.descriptionIngles.upper())}"
                
                
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
    
    
#Lo envia prefectura, solo guardo el texto
class Hielo(models.Model):
    
    creado = models.DateField(auto_now_add=True)
    texto = models.TextField(null=True, blank=True)
    activo = models.BooleanField(null=True, blank=True)
    
    #Planteo un muchos a muchos porque los hielos no siempre llegan a horario, por ahí el mismo hielo pertenece a varios boletines
    boletin = models.ManyToManyField(Boletin)
    
    def __str__(self):
        return f"Ultima modificación: {self.creado}"
    
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
    
    
    
class Credential(models.Model):
    username = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    client = models.CharField(max_length=100)
    referer = models.CharField(max_length=100)
    expiration = models.IntegerField()
    f = models.CharField(max_length=10)

    def __str__(self):
        return self.username
