from django.urls import path
from AppMaritima import views


urlpatterns = [
    
    path('inicio', views.inicio, name="Inicio"),
    path('cargarAreas', views.cargarAreas), #Ejecutarlo la primera vez para cargas las areas PIMET
    path('cargarPronosticos', views.cargarPronosticos),
    path('escaterometro', views.escaterometro, name="Escaterometro"),
    
    
    #PARA CLASES BASADAS EN VISTAS
    
    #BOLETIN
    path('boletin/list', views.BoletinList.as_view(), name='ListBoletin'),
    path('boletin/listTodos', views.BoletinListTodos.as_view(), name='ListBoletinTodos'),
    path('boletin/<pk>', views.BoletinDetalle.as_view(), name='DetailBoletin'),
    path(r'^nuevo$', views.BoletinCreacion.as_view(), name='NewBoletin'),
    path(r'^editar/(?P<pk>\d+)$', views.BoletinUpdate.as_view(), name='EditBoletin'),
    path(r'^borrar/(?P<pk>\d+)$', views.BoletinDelete.as_view(), name='DeleteBoletin'),
    
    
    #aviso
    path('aviso/list', views.AvisoList.as_view(), name='ListAviso'),
    path(r'aviso^(?P<pk>\d+)$', views.AvisoDetalle.as_view(), name='DetailAviso'),
    path(r'^nuevoAviso$', views.AvisoCreacion.as_view(), name='NewAviso'),
    path('editarAviso/<pk>', views.AvisoUpdate.as_view(), name='EditAviso'),
    path('cesarAviso/<pk>', views.cesarAviso, name='CesarAviso'),
    path(r'^borrarAviso/(?P<pk>\d+)$', views.AvisoDelete.as_view(), name='DeleteAviso'),
    
    
    #situación
    path('situacion/list', views.SituacionList.as_view(), name='ListSituacion'),
    path(r'situacion^(?P<pk>\d+)$', views.SituacionDetalle.as_view(), name='DetailSituacion'),
    path(r'^nuevoSituacion$', views.SituacionCreacion.as_view(), name='NewSituacion'),
    path(r'^editarSituacion/(?P<pk>\d+)$', views.SituacionUpdate.as_view(), name='EditSituacion'),
    path(r'^borrarSituacion/(?P<pk>\d+)$', views.SituacionDelete.as_view(), name='DeleteSituacion'),
    
    
    
]