
# Proyecto Marítima SMN

Aplicación web desarrollada en Python 3.9 y Django 4.0.4, diseñada para la generación automática de boletines de navegación marítima en la METAREA VI.

## Instalación (Primer despliegue)

Sigue los pasos a continuación para desplegar el proyecto por primera vez.

### 1. Instalar Python 3.9

```bash
sudo apt install python3.9
```

### 2. Instalar PostgreSQL

**Recomendación:** Configurar el usuario como "postgres" y la contraseña como "root". Si decides usar diferentes credenciales, deberás modificarlas en `ProyectoMaritima/settings.py`.

```bash
sudo apt install postgresql 
sudo -u postgres psql
CREATE DATABASE maritima;
ALTER USER postgres WITH PASSWORD 'root';
\q
```

### 3. Crear la base de datos "maritima"

```bash
create database maritima;
```

### 4. Clonar el repositorio en la ruta deseada

```bash
git clone https://gitlab.smn.gov.ar/desa-smn/boletin-maritimo.git
```

### 5. Entrar al directorio del proyecto

```bash
cd ruta/ProyectoMaritima
```

### 6. Instalar las dependencias del proyecto

```bash
pip install -r requirements.txt
```

### 7. Realizar las migraciones de la base de datos

**Nota:** Si tienes tanto Python 2 como Python 3 instalados, reemplaza `python` por `python3` en los comandos.

```bash
python manage.py makemigrations
python manage.py migrate
```

### 8. Crear un superusuario

```bash
python manage.py createsuperuser
```

### 9. Iniciar el servidor

```bash
python manage.py runserver xx.xx.xxx.xxx:8080
```

**Carga las áreas iniciales:**

Visita: [http://127.0.0.1:8000/AppMaritima/cargarAreas](http://127.0.0.1:8000/AppMaritima/cargarAreas)

**Nota:** El servidor actual del SMN se ejecuta en `10.10.221.2:8080`. Si no se especifica, se asigna por defecto a `127.0.0.1:8000`.

### 10. Comandos Git útiles

#### Añadir un nuevo repositorio

```bash
git remote add origin <url-del-repositorio-remoto>
```

#### Ver y cambiar de ramas

```bash
git fetch
git branch
git checkout <rama-nueva>
```

#### Subir cambios al repositorio remoto

```bash
git push -u origin <rama>
```

## Semillas iniciales - Base de datos

### Iniciar sesión como superusuario

Visita: [http://xx.xx.xxx.xxx:8000/AppMaritima/Login](http://xx.xx.xxx.xxx:8000/AppMaritima/Login)

### Levantar las áreas de PIMET

Visita: [http://xx.xx.xxx.xxx:8080/AppMaritima/cargarAreas](http://xx.xx.xxx.xxx:8080/AppMaritima/cargarAreas)

### Crear usuarios de pronóstico

Visita: [http://xx.xx.xxx.xxx:8080/AppMaritima/cargarUsuarios](http://xx.xx.xxx.xxx:8080/AppMaritima/cargarUsuarios)

### Acceso al Home

Visita: [http://xx.xx.xxx.xxx:8080/AppMaritima](http://xx.xx.xxx.xxx:8080/AppMaritima)

### Panel de administración (solo superusuario)

Visita: [http://xx.xx.xxx.xxx:8080/admin](http://xx.xx.xxx.xxx:8080/admin)

## Actualización del Software

**Si ya has desplegado el proyecto previamente, sigue estos pasos para actualizar el programa y aplicar mejoras.**

### 1. Clonar o actualizar el repositorio

```bash
git clone https://gitlab.smn.gov.ar/desa-smn/boletin-maritimo.git
```

### 2. Aplicar migraciones a la base de datos

```bash
python manage.py makemigrations
python manage.py migrate
```

### 3. Iniciar el servidor

```bash
python manage.py runserver
```

## Sobre la versión actual

### Tareas pendientes

- [x] Ver detalles en Trello: [Proyectos CPR Marítima](https://trello.com/b/D9mFdRxZ/proyectos-cpr-maritima)

### Reportes y sugerencias

Envía tus pedidos o mejoras aquí: [PEDIDOS](https://forms.gle/NtPh4itKtTzjiWRt6)

### Manual de usuario y técnico

Consulta los manuales aquí: [MANUALES](https://drive.google.com/drive/folders/1EdElg3e95aywZnOQJLetQNT4LN--bmhZ?usp=sharing)