from django.urls import path
from AppMaritima import views


urlpatterns = [
    
    path('', views.inicio),
    path('cargarAreas', views.cargarAreas),
    
    
    #PARA CLASES BASADAS EN VISTAS
    
    #BOLETIN
    path('boletin/list', views.BoletinList.as_view(), name='ListBoletin'),
    path(r'boletin^(?P<pk>\d+)$', views.BoletinDetalle.as_view(), name='DetailBoletin'),
    path(r'^nuevo$', views.BoletinCreacion.as_view(), name='NewBoletin'),
    path(r'^editar/(?P<pk>\d+)$', views.BoletinUpdate.as_view(), name='EditBoletin'),
    path(r'^borrar/(?P<pk>\d+)$', views.BoletinDelete.as_view(), name='DeleteBoletin'),
    
    
    #aviso
    path('aviso/list', views.AvisoList.as_view(), name='ListAviso'),
    path(r'aviso^(?P<pk>\d+)$', views.AvisoDetalle.as_view(), name='DetailAviso'),
    path(r'^nuevoAviso$', views.AvisoCreacion.as_view(), name='NewAviso'),
    path(r'^editarAviso/(?P<pk>\d+)$', views.AvisoUpdate.as_view(), name='EditAviso'),
    path(r'^borrarAviso/(?P<pk>\d+)$', views.AvisoDelete.as_view(), name='DeleteAviso'),
    
    
    
]