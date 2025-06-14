from datetime import timedelta
import os
from pathlib import Path
import config.db as db

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv(
    "SECRET_KEY", "django-insecure-#a4$*hi^a5ml$v1vs7pv=l&o&=93@ozg&4k3fv&i_(im##%o(e"
)
# si no hay ninguna variable se considera como TRUE
DEBUG = os.getenv("DEBUG", "True") == "True"
ALLOWED_HOSTS = os.getenv("ALLOWED_HOSTS", "").split(",")

# Application definition
BASE_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
]

THIRD_APPS = [
    "rest_framework",
    "rest_framework.authtoken",
    "rest_framework_simplejwt.token_blacklist",
    "drf_spectacular",
    "corsheaders",
    "django_filters",
]

OWN_APPS = [
    "api",
    "api.personal",
    "api.user",
    "api.poi",
    "api.dvi",
    "api.ipress",
    "api.informatica",
    "api.patrimonio",
]

INSTALLED_APPS = BASE_APPS + THIRD_APPS + OWN_APPS

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

# agregando q dominios locales para consumir la API
CORS_ALLOWED_ORIGINS = [
    "http://localhost:8000",  
    "http://localhost:80",  
    "http://localhost:81",  
    "http://localhost:8080", 
    "http://localhost:9090", 
    "http://localhost:8081", 
    "http://localhost", 
    "http://127.0.0.1:8080",
    "http://127.0.0.1:8081",
    "http://192.168.18.23:8080",
    "http://192.168.18.23:80",
    "http://192.168.18.23",
    "http://172.27.0.222:81",
    "http://172.27.1.117:80",
    "http://172.27.1.117",
    #"http://192.168.18.23",
    "http://172.27.0.222:81",
    "http://172.27.0.222:80",
    "http://172.27.0.222",
]

CORS_ALLOW_METHODS = (
    "DELETE",
    "GET",
    "OPTIONS",
    "PATCH",
    "POST",
    "PUT",
)

CORS_ALLOW_HEADERS = [
    "content-type",
    "authorization",
    "x-requested-with",
    "accept",
]

REST_FRAMEWORK = {
    "DEFAULT_FILTER_BACKENDS": ["django_filters.rest_framework.DjangoFilterBackend"],
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework_simplejwt.authentication.JWTAuthentication",
        "rest_framework.authentication.SessionAuthentication",
    ),
    "DEFAULT_PERMISSION_CLASSES": ("rest_framework.permissions.IsAuthenticated",),
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
}

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(hours=8),  # Tiempo de vida del token de acceso
    "REFRESH_TOKEN_LIFETIME": timedelta(days=7),  # Tiempo de vida del token de refresco
    "ROTATE_REFRESH_TOKENS": True,  # Rotar los tokens de refresco
    "BLACKLIST_AFTER_ROTATION": True,  # Añadir tokens de refresco a la lista negra después de rotación
    "UPDATE_LAST_LOGIN": True,  # Actualizar la última fecha de inicio de sesión del usuario
}

# django-spectacular
SPECTACULAR_SETTINGS = {
    "TITLE": "API",
    "DESCRIPTION": "Description API",
    "VERSION": "1.0.0",
    "CONTACT": {
        "name ": "AxiosCore",
        "email": "Angel@master.com",
        "url": "https://devcod.org",
    },
    "SWAGGER_UI_SETTINGS": {
        "persistAuthorization": True,
    },
}

ROOT_URLCONF = "config.urls"
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "config.wsgi.application"
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

DATABASES = db.DATABASES


# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]
# Establece el tiempo de inactividad (en segundos) después del cual la sesión debe expirar
SESSION_COOKIE_AGE = 12 * 60 * 60  # 12 horas
# SESSION_COOKIE_AGE = 43200  # 12 horas

# Configura la expiración de la sesión
SESSION_EXPIRE_AT_BROWSER_CLOSE = True

# Internationalization
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = "es-pe"
TIME_ZONE = "America/Lima"
USE_I18N = True
USE_L10N = True
USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

STATIC_URL = "static/"
STATICFILES_DIRS = [os.path.join(BASE_DIR, "static")]
STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")
#
MEDIA_URL = "/media/"
MEDIA_ROOT = os.path.join(BASE_DIR, "media")
# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

AUTH_USER_MODEL = "user.User"  # Ajusta 'user.User' según el nombre de tu app y modelo

# settings.py (Django ejemplo)
DATA_UPLOAD_MAX_MEMORY_SIZE = 250 * 1024 * 1024  # 250MB
FILE_UPLOAD_MAX_MEMORY_SIZE = 250 * 1024 * 1024  # 250MB
MAX_UPLOAD_SIZE = 250 * 1024 * 1024  # 250MB