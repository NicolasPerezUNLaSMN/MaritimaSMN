from django.urls import path
from AppMaritima import views


urlpatterns = [
    
   
    path('cargarAreas', views.cargarAreas), #Ejecutarlo la primera vez para cargas las areas PIMET
    path('cargarPronosticos', views.cargarPronosticos),
    path('escaterometro', views.escaterometro, name="Escaterometro"),
    
    
    #url a Vistas para crud de las tablas
    
    #BOLETIN
    path('boletin/ultimo', views.ultimoBoletin, name='UltimoBoletin'),
    path('', views.BoletinCreacion.as_view(), name='NewBoletin'),
    path('boletin/list', views.BoletinList.as_view(), name='ListBoletin'),
    path('boletin/listTodos', views.BoletinListTodos.as_view(), name='ListBoletinTodos'),
    path('boletin/<pk>', views.BoletinDetalle.as_view(), name='DetailBoletin'),
    path('nuevo', views.BoletinCreacion.as_view(), name='NewBoletin'),
    path('editar/<pk>', views.BoletinUpdate.as_view(), name='EditBoletin'),
    path('borrar/<pk>', views.BoletinDelete.as_view(), name='DeleteBoletin'),
    
    
    #aviso
    path('aviso/list', views.AvisoList.as_view(), name='ListAviso'),
    path('aviso/<pk>', views.AvisoDetalle.as_view(), name='DetailAviso'),
    path('nuevoAviso', views.AvisoCreacion.as_view(), name='NewAviso'),
    path('editarAviso/<pk>', views.AvisoUpdate.as_view(), name='EditAviso'),
    path('cesarAviso/<pk>', views.cesarAviso, name='CesarAviso'),
    path('borrarAviso/<pk>', views.AvisoDelete.as_view(), name='DeleteAviso'),
    
    
    #situación
    path('situacion/list', views.SituacionList.as_view(), name='ListSituacion'),
    path('situacion/<pk>', views.SituacionDetalle.as_view(), name='DetailSituacion'),
    path('nuevoSituacion', views.SituacionCreacion.as_view(), name='NewSituacion'),
    path('editarSituacion/<pk>', views.SituacionUpdate.as_view(), name='EditSituacion'),
    path('borrarSituacion/<pk>', views.SituacionDelete.as_view(), name='DeleteSituacion'),
    path('cesarSituacion/<pk>', views.cesarSituacion, name='CesarSituacion'),
    
    
    #Hielo
    path('hielo/list', views.HieloList.as_view(), name='ListHielo'),
    path('nuevoHielo', views.HieloCreacion.as_view(), name='NewHielo'),
    path('editarHielo/<pk>', views.HieloUpdate.as_view(), name='EditHielo'),
    path('cesarHielo/<pk>', views.cesarHielo, name='CesarHielo'),
    path('borrarHielo/<pk>', views.HieloDelete.as_view(), name='DeleteHielo'),
    
    #Otros url
    path('crearTXT/<pk>', views.crearTXT, name='CrearTXT'),
    path('editor', views.editor, name='Editor'),
    
    
]