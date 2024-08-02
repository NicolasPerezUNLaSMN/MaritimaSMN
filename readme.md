# Proyecto Maritima SMN
Aplicativo web desarrollado con Python 3.9 y Django 4.0.4, para la generación automáctica de boletines de navegación maritima en la METAREA VI

<<<<<<< HEAD

# Instalación  (Primer despliegue) 
=======
# Instalación  (Primer despliegue)
>>>>>>> origin/Santi
**Seguir los pasos para desplegar por primera vez el proyecto**

1) Instalar Python3
```
sudo apt install python3.9
```

2) Instalar PostgreSQL (recomendamos que usuario sea "postgres" y contraseña sea "root", o modificar el archivo ProyectoMaritima/settings.py)
```
sudo apt install postgresql 
sudo -u postgres psql
CREATE DATABASE maritima;
ALTER USER postgres WITH PASSWORD 'root';
barra invertida. q
 
```
3) Crear una base de datos con nombre "maritima"

```
create database maritima.
```

4) Clonar el repositorio en la "ruta" deseada
```
git clone https://gitlab.smn.gov.ar/desa-smn/boletin-maritimo.git
```


5) Entrar al directorio del proyecto
```
ruta/ cd ProyectoMaritima
```


6) Instalar requirements.txt
```
pip install -r requirements.txt
```

7) Realizar las migraciones a la base de datos
[!] Todos los comandos que digan python, pueden reemplazarse por python3 en caso que tengan python 2  y 3 instalados.
```
python manage.py makemigrations
python manage.py migrate
```

8) Crear un superusuario
```
ruta/ProyectoMaritima/ 
python manage.py createsuperuser
```


9) Correr el servidor
```
ruta/ProyectoMaritima/ 
python manage.py runserver xx.xx.xxx.xxx:8080

Carga las areas

http://127.0.0.1:8000/AppMaritima/cargarAreas

```
(SERVIDOR ACTUAL SMN 10.10.221.2:8080; sino se pone xx.xx.xxx.xxxx:8000 por defecto se asigna a 127.0.0.1:8000)

1) Comandos git
Añadir repositorio nuevo
```
git remote add origin <url-del-repositorio-remoto>
```
Ver ramas remotas / locales / cambiar de rama
```
git fetch
git branch
git checkout <rama nueva>
```
Pushear al remoto
```
git push -u origin <rama>

```



  #######################################################

  Semillas iniciales -  BD - 

  Iniciar como Super Usuario:

  http://xx.xx.xxx.xxx:8000/AppMaritima/Login

  Levantar las areas de pimet

  http://xx.xx.xxx.xxx:8080/AppMaritima/cargarAreas

  Crear usuarios de pronostico:

  http://xx.xx.xxx.xxx:8080/AppMaritima/cargarUsuarios

  #######################################################

  10-a. Para el home acceder a: 
  http://xx.xx.xxx.xxx:8080/AppMaritima

  10-b. Para panel de administración solo "superusuario":
  http://xx.xx.xxx.xxx:8080/admin


# Update del Software  (Actualización del programa, agregado de mejoras)
**Si no es la primera vez que se ejetuca el programa**
**Luego de cambios en modelo o modificacones, ejecutar las migraciones y runserver**

1) Clonar el repositorio, o pullearlo para tener los ultimos cambios
```
git clone https://gitlab.smn.gov.ar/desa-smn/boletin-maritimo.git
```

2) Realizar los cambios en la base de datos
```
python manage.py makemigrations
python manage.py migrate
```

3) Correr el servidor
```
python manage.py runserver
```



# Sobre la versión actual
** Tareas a realizar **

- [x] Ver detalles en Trello: (https://trello.com/b/D9mFdRxZ/proyectos-cpr-maritima)



Reportar pedidos o mejoras a: [PEDIDOS] (https://forms.gle/NtPh4itKtTzjiWRt6)

Manual usuario y técnico del SW: [MANUALES](https://drive.google.com/drive/folders/1EdElg3e95aywZnOQJLetQNT4LN--bmhZ?usp=sharing)

Crear un README mejor que este: [GitHub Docs](https://docs.github.com/es/get-started/writing-on-github/getting-started-with-writing-and-formatting-on-github/basic-writing-and-formatting-syntax).
