# Proyecto Maritima SMN
Aplicativo web desarrollado con Python 3.9 y Django 4.0.4, para la generación automáctica de boletines de navegación maritima en la METAREA VI


# Instalación y uso (Primer uso)
**Seguir los pasos para desplegar por primera vez el proyecto**

1) Instalar Python3
sudo apt install python3.9

2) Clonar el repositorio en la "ruta" deseada
git clone https://github.com/NicolasPerezUNLaSMN/MaritimaSMN.git


3) Entrar al directorio del proyecto
ruta/ cd ProyectoMaritima


4) Instalar requirements.txt
pip install -r requirements.txt


5) (Opcional) Crear un superusuario
ruta/ProyectoMaritima/ python manage.py createsuperuser


6) Correr el servidor
ruta/ProyectoMaritima/ python manage.py runserver

7-a) Para el home acceder a: 
http://127.0.0.1:8000/AppMaritima

7-b) Para panel de administración superusuario:
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
- [ ] Redefinir algunos redireccionamientos para mejor experiencia con el usuario #75%
- [x] Versión estable para crear boletín en ingles
- [x] Persistencia de todos los datos en tablas 
- [x] Escaterometro y borde de hielos visibles desde la web. 



Crear un README mejor que este: [GitHub Docs](https://docs.github.com/es/get-started/writing-on-github/getting-started-with-writing-and-formatting-on-github/basic-writing-and-formatting-syntax).