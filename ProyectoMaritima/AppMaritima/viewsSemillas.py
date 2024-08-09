


from django.http.response import HttpResponse

from AppMaritima.funciones import cargarAreasDesdeElXML


from AppMaritima.models import *


from django.contrib.admin.views.decorators import staff_member_required

from django.contrib.auth.models import User

#-----------------------------------------------------------------------------------
#Ejectucarlo solo una vez, y con permisos de admin 
@staff_member_required
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



@staff_member_required
def cargarCredencialesIniciales(request):

    credential = Credential(
        username="smn_user",
        password="Dico1234!",
        client="referer",
        referer="https://gis.prefecturanaval.gob.ar/portal/",
        expiration=60,
        f="json"
    )
    credential.save()

    return HttpResponse("Credenciales cargadas")


#Ejectucarlo solo una vez, y con permisos de admin 
@staff_member_required
def cargarUsuarios(request):
    

       lista_usuarios = ["gtechoueyres",
                        "dcabral",
                        "cvillegas",
                        "nperez",
                        "mpirotte",
                        "vlopez",
                        "mmedone",
                        "flopretto",
                        "nbisero",
                        "apalavecino",
                        "nreinoso",
                        "emartire",
                        "skseminski",
                        "smayer",
                        "jtrupiano",
                        "agcejas",
                        "msaucedo",
                        "agargiulo",
                        "ccastro",
                        "cgaravaglia",
                        "gramirez",
                        "amontero",
                        "mcorvalan",
                        "sgalgano",
                        "rvidal",
                        "ngiletto"
                        ]
        
       for n in lista_usuarios:
 
            user = User.objects.create_user(n, n+'@smn.gob.ar', n+'@smn.gob.ar')
            user.is_staff=True
            user.save()

        
        
    
   
       return HttpResponse("Usuarios cargados")
#-----------------------------------------------------------------------------------  
