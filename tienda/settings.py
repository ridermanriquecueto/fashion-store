import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

# ¡MUY IMPORTANTE! Reemplaza esta clave secreta con una generada aleatoriamente
SECRET_KEY = os.environ.get('SECRET_KEY', 'django-insecure-893(*gc6s#@f88&b36-mm69yna(hz5sk-1g**f5nqj5196g@7p')  # Clave secreta de respaldo (solo para desarrollo)

# DEBUG debe ser False en producción
DEBUG = os.environ.get('DEBUG', 'True') == 'True'  # Convertir a booleano correctamente

ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS', '127.0.0.1,localhost').split(',')  # Convertir en lista

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'productos',  # Asegúrate de que este nombre sea correcto
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',  # Mueve WhiteNoise a la parte superior después de SecurityMiddleware
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'tienda.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            BASE_DIR / 'templates',  # Directorio para plantillas comunes
        ],
        'APP_DIRS': True,  # Busca plantillas en las apps
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

WSGI_APPLICATION = 'tienda.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

LANGUAGE_CODE = 'es-ar'  # Español de Argentina

TIME_ZONE = 'America/Argentina/Buenos_Aires'  # Zona horaria Argentina

USE_I18N = True

USE_TZ = True

# Configuración de archivos estáticos y media
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'  # Directorio para collectstatic (producción)
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
    BASE_DIR / 'productos/static',  # Directorio de desarrollo para archivos estáticos
]

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'  # Directorio para archivos multimedia

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
