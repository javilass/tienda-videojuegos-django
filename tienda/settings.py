"""
Configuración del proyecto "tienda".

Lo más importante está en DATABASES (conexión a MySQL/MariaDB de XAMPP)
e INSTALLED_APPS (donde se registra nuestra app "videojuegos").
"""
import os
from pathlib import Path

# Carpeta raíz del proyecto (donde está manage.py)
BASE_DIR = Path(__file__).resolve().parent.parent

# Clave usada por Django para firmar datos (cookies, token CSRF). En un proyecto real va oculta.
SECRET_KEY = 'django-insecure-tienda-videojuegos-evaluacion-backend'

# DEBUG=True muestra errores detallados. Solo para desarrollo.
DEBUG = True

ALLOWED_HOSTS = []


# Aplicaciones instaladas: las de Django + la nuestra
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',      # mensajes "Videojuego creado", etc.
    'django.contrib.staticfiles',
    'videojuegos',                  # <-- NUESTRA APP
]

MIDDLEWARE = [ #es una lista de middlewares que se ejecutan en cada request
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',   # protege los formularios POST
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'tienda.urls' #es el archivo que contiene las urls principales del proyecto, en este caso es tienda/urls.py

TEMPLATES = [ #es la configuración de los templates, que son los archivos HTML que se renderizan en el navegador
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,   # busca templates dentro de cada app (videojuegos/templates/)
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'tienda.wsgi.application' #es el archivo que contiene la configuración de WSGI, que es el protocolo que usa Django para comunicarse con el servidor web


# ==========================================================
# BASE DE DATOS: MySQL / MariaDB de XAMPP
# ==========================================================
# Antes de migrar, crea la base "tienda_videojuegos" en phpMyAdmin.
# XAMPP trae por defecto el usuario "root" SIN contraseña.
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'tienda_videojuegos',
        'USER': 'root',
        'PASSWORD': '',
        'HOST': '127.0.0.1',
        'PORT': '3306',
        'OPTIONS': {
            'charset': 'utf8mb4',
            'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
        },
    }
}

# (Solo para pruebas sin XAMPP: ejecutar con la variable USAR_SQLITE=1)
if os.environ.get('USAR_SQLITE') == '1':
    DATABASES = {'default': {'ENGINE': 'django.db.backends.sqlite3', 'NAME': BASE_DIR / 'prueba.sqlite3'}}


AUTH_PASSWORD_VALIDATORS = []

# Idioma y zona horaria de Chile
LANGUAGE_CODE = 'es-cl'
TIME_ZONE = 'America/Santiago'
USE_I18N = True
USE_TZ = True

# Archivos estáticos (CSS, JS). Django los busca en videojuegos/static/
STATIC_URL = 'static/'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
