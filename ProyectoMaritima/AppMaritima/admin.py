from django.contrib import admin
from .models import *

# Register your models here.


class AreaAdmin(admin.ModelAdmin):
    list_display = ('id','idPimet', 'latitude', 'longitude','description','descriptionIngles','domain')

class AvisoAdmin(admin.ModelAdmin):
    list_display = ('id','numero', 'actualizacion', 'tipo','direccion','activo','desde','hasta')

class BoletinAdmin(admin.ModelAdmin):
    list_display = ('id','emitido', 'modificado', 'pronosticosGuardados', 'valido','hora')

class PronosticoAdmin(admin.ModelAdmin):
    list_display = ('id','tipo','texto','area')


admin.site.register(Area,AreaAdmin)
admin.site.register(Boletin, BoletinAdmin)
admin.site.register(Aviso, AvisoAdmin)
admin.site.register(Hielo)
admin.site.register(Situacion)
admin.site.register(Pronostico,PronosticoAdmin)