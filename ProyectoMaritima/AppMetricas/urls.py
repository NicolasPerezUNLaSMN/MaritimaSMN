from django.urls import path
from . import views

urlpatterns = [
    path('', views.verificacion, name='AppMetricas'),
]
