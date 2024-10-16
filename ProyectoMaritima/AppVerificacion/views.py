#DJANGO MTV. Modelo ->Base de datos Template-> consultas que puede hacer el usuario View-> respuesta ante un link

from django.http import HttpResponse
import datetime
from django.shortcuts import render
import requests
from openpyxl import Workbook
import csv
from .funciones import *


# ACA BAN LAS FUNCIONES VISTAS
# COMO ARGUMENTO TIENEN UNA REQUEST Y COMO RESPUESTA UN HTTP RESPONSE POR COMO TRABAJA DJANGO
#UNA URL VA A IR A ESTA VISTA QUE DEVUELVE UN TEXTO ->> IR A URLS.PY

#FUNCION PARA PASAR LA FEXA UNIX A DATETIME
def timestamp_to_date(timestamp):
    timestamp_seconds = timestamp / 1000
    date = datetime.datetime.fromtimestamp(timestamp_seconds)
    return date.strftime('%Y-%m-%d %H:%M:%S')





def fecha_hoy(request, numero=None):
        
        if numero is None:
            numero = 12
    
        # Obtener la fecha actual y la fecha de hace 24 horas
        fecha_fin = datetime.datetime.now()
        fecha_inicio = fecha_fin - datetime.timedelta(hours=numero)

        # Convertir las fechas a formato de cadena para la consulta
        fecha_inicio_str = fecha_inicio.strftime('%Y-%m-%d %H:%M:%S')
        fecha_fin_str = fecha_fin.strftime('%Y-%m-%d %H:%M:%S')

        # Paso 1: Obtener Token
        credential = obtenerCredenciales()

        url_token = "https://gis.prefecturanaval.gob.ar/portal/sharing/rest/generateToken"
        data = {
            "username": credential.username,
            "password": credential.password,
            "client": credential.client,
            "referer": credential.referer,
            "expiration": credential.expiration,
            "f": credential.f
        }
        
        response = requests.post(url_token, data=data)
        token_data = response.json()
        token = token_data["token"]

        # Construir la cláusula WHERE usando las fechas calculadas
        where_clause = f"fecha >= '{fecha_inicio_str}' AND fecha < '{fecha_fin_str}'"

        # Paso 2: Ejecutar Reporte SELECCIONAR LA FECHA
        url_reporte = "https://gis.prefecturanaval.gob.ar/server/rest/services/Hosted/service_5afcf589c1aa464da69eb803356762ff/FeatureServer/0/query"
        params = {
            "token": token,
            "where": where_clause,
            "outFields": "*",
            "f": "json"
        }
        response = requests.get(url_reporte, params=params)
        reporte_data = response.json()
        
        print("API Response:", reporte_data)
        barcos = []
        for reporte in reporte_data['features']:
            
            attributes = reporte['attributes']
            latitud = reporte['geometry'].get('y')
            longitud = reporte['geometry'].get('x')
            direccion_viento = attributes.get('direccion')
            vientobeaufort = attributes.get('vientobeaufort')

            # Solo agregar el barco si todos los valores requeridos no son nulos
            if latitud is not None and longitud is not None and direccion_viento is not None and vientobeaufort is not None:


                barco = {
                    'fecha_reporte': attributes.get('fecha') or 'null',
                    'nombre_buque': attributes.get('nombre') or 'null',
                    'matricula': attributes.get('matricula') or 'null',
                    'imo': attributes.get('imo') or 'null',
                    'latitud': reporte['geometry'].get('y') or 'null',
                    'longitud': reporte['geometry'].get('x') or 'null',
                    'marbeaufort': attributes.get('marbeaufort') or 'null',
                    'vientoKt': beaufort_to_knots(attributes.get('vientobeaufort') or 'null'),
                    'vientobeaufort':attributes.get('vientobeaufort') or 'null',
                    'direccion_viento': attributes.get('direccion') or 'null',
                    'marmedido': attributes.get('marmedido') or 'null',
                    'vientomedido': attributes.get('vientomedido') or 'null',
                    'direccionmedido': attributes.get('direccionmedido') or 'null',
                    'presion': attributes.get('presion') or 'null',
                }
                barcos.append(barco)
 
        # Renderizar la plantilla HTML con los datos
        return render(request, 'AppVerificacion/reporte_barcos.html', {'barcos': barcos})



def selector_fechas(request):


    if request.method == 'POST':
        # Obtener las fechas del formulario
        fecha_inicio = request.POST.get('fecha_inicio')
        fecha_fin = request.POST.get('fecha_fin')

        print(f"ME LLEGO: {fecha_inicio} ---------- {fecha_fin}")
        try:
            datetime.datetime.strptime(fecha_inicio, '%Y-%m-%d').date()
            datetime.datetime.strptime(fecha_fin, '%Y-%m-%d').date()
        except ValueError:
            return HttpResponse("Formato de fecha incorrecto", status=400)
        # Paso 1: Obtener Token

        credential = obtenerCredenciales()

        url_token = "https://gis.prefecturanaval.gob.ar/portal/sharing/rest/generateToken"
        data = {
            "username": credential.username,
        "password": credential.password,
        "client": credential.client,
        "referer": credential.referer,
        "expiration": credential.expiration,
        "f": credential.f
        }
        
        response = requests.post(url_token, data=data)
        token_data = response.json()
        token = token_data["token"]

        where_clause = f"fecha >= '{fecha_inicio} 00:00:00' AND fecha < '{(datetime.datetime.strptime(fecha_inicio, '%Y-%m-%d') + datetime.timedelta(days=1)).strftime('%Y-%m-%d')} 00:00:00'"
        #where_clause = f'1=1'
        # Paso 2: Ejecutar Reporte SELECCIONAR LA FECHA

        url_reporte = "https://gis.prefecturanaval.gob.ar/server/rest/services/Hosted/service_5afcf589c1aa464da69eb803356762ff/FeatureServer/0/query"
        params = {
            "token": token,
        "where": where_clause,
            "outFields": "*",
            "f": "json"
        }
        response = requests.get(url_reporte, params=params)
        reporte_data = response.json()
        
        print("API Response:", reporte_data)
        #print("AAAAAAAAAAAAAAAAAAAA Clause:", where_clause)
        barcos = []
        for reporte in reporte_data['features']:
            attributes = reporte['attributes']
            barco = {
                'fecha_reporte': attributes.get('fecha') or 'null',
                'nombre_buque': attributes.get('nombre') or 'null',
                'matricula': attributes.get('matricula') or 'null',
                'imo': attributes.get('imo') or 'null',
                'latitud': reporte['geometry'].get('y') or 'null',
                'longitud': reporte['geometry'].get('x') or 'null',
                'marbeaufort': attributes.get('marbeaufort') or 'null',
                'vientoKt': beaufort_to_knots(attributes.get('vientobeaufort') or 'null'),
                'vientobeaufort':attributes.get('vientobeaufort') or 'null',
                'direccion_viento': attributes.get('direccion') or 'null',
                'marmedido': attributes.get('marmedido') or 'null',
                'vientomedido': attributes.get('vientomedido') or 'null',
                'direccionmedido': attributes.get('direccionmedido') or 'null',
                'presion': attributes.get('presion') or 'null',
            }
            barcos.append(barco)
 
        # Renderizar la plantilla HTML con los datos
        return render(request, 'AppVerificacion/reporte_barcos.html', {'barcos': barcos})

    # Si es un GET o no se ha enviado el formulario, renderizar el formulario vacío
    return render(request, 'AppVerificacion/seleccion_fechas.html')


def reporte_barcos(request):
    # Lógica para obtener los datos del reporte
    context = {
        'titulo_reporte': 'Reporte de Barcos',
        # Otros datos que quieras pasar al template
    }
    return render(request, 'AppVerificacion/reporte_barcos.html', context)

