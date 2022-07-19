# Proyecto Maritima SMN
Aplicativo web desarrollado con Python 3.9 y Django 4.0.4, para la generación automáctica de boletines de navegación maritima en la METAREA VI


# Instalación y uso (Primer uso)
**Seguir los pasos para desplegar por primera vez el proyecto**

1) Instalar Python3
sudo apt install python3.9

2) Instalar PostgreSQL
sudo apt install postgresql

3) Crear una base de datos con nombre maritima
create database maritima

4) Clonar el repositorio en la "ruta" deseada
git clone https://github.com/NicolasPerezUNLaSMN/MaritimaSMN.git


5) Entrar al directorio del proyecto
ruta/ cd ProyectoMaritima


6) Instalar requirements.txt
pip install -r requirements.txt

7) Realizar las migraciones a la base de datos
python manage.py makemigrations
python manage.py migrate

8) Crear un superusuario
ruta/ProyectoMaritima/ 
python manage.py createsuperuser


9) Correr el servidor
ruta/ProyectoMaritima/ 
python manage.py runserver

10-a) Para el home acceder a: 
http://127.0.0.1:8000/AppMaritima

10-b) Para panel de administración superusuario:
http://127.0.0.1:8000/admin


# Uso (Luego de tener todo instalado)
**Si no es la primera vez que se ejetuca el programa**
Repetir los pasos 6 y 7.


# Sobre la versión actual
** Tareas a realizar **

- [ ] Verificar generación de pronosticos nocturnos (00UTC)
- [ ] Definir nombre del archivo PIMET generado diariamente y leer ese archivo, no leer el archivo de prueba.
- [ ] Crear TXT para NAVTEX
- [ ] Crear informes en español #0%
- [ ] Mejorar formato de horas y días, a definir #0%
- [ ] Definir en qué orden deben aparecer las areas, mantener o no? #0%
- [ ] Definir módulo de estadisticas
- [x] Documentar DER
- [x] Documentar DC
- [x] Documentar flujo de trabajo
- [ ] Redefinir algunos redireccionamientos para mejor experiencia con el usuario #75%
- [x] Versión estable para crear boletín en ingles
- [x] Persistencia de todos los datos en tablas 
- [x] Escaterometro y borde de hielos visibles desde la web. 
- [ ] Definir qué hacer con las divisiones Rio De la Plata.
- [!] Documentar los manuales de usuario y de desarrollo.
- [!] Cada ciclo terminado, con todos los txt guadados ocuparia 11/12Kb en el servidor. 


Manual usuario y técnico del SW: [MANUALES](https://drive.google.com/drive/folders/1EdElg3e95aywZnOQJLetQNT4LN--bmhZ?usp=sharing)

Crear un README mejor que este: [GitHub Docs](https://docs.github.com/es/get-started/writing-on-github/getting-started-with-writing-and-formatting-on-github/basic-writing-and-formatting-syntax).