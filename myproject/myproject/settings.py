import os
from pathlib import Path
from .info import *  # Asegúrate de que info.py contiene valores válidos
from .secure import DATABASES
from .secure import COOKIE_SECRET
from corsheaders.defaults import default_headers

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Email settings
EMAIL_USE_TLS = EMAIL_USE_TLS
EMAIL_HOST = EMAIL_HOST
EMAIL_HOST_USER = EMAIL_HOST_USER
EMAIL_HOST_PASSWORD = EMAIL_HOST_PASSWORD
EMAIL_PORT = EMAIL_PORT

# Quick-start development settings - unsuitable for production
SECRET_KEY = 'django-insecure-8)2i&@1dbyn3)@!s5p-#oc^*ix&@ee4j(px-8b8xb7bg^$!yxw'

DEBUG = True

ALLOWED_HOSTS = [
    'localhost',
    '127.0.0.1',
    'acc2-186-77-207-181.ngrok-free.app',  # Dominio de ngrok
    'www.stregasoft.com',
]

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'webapp',
    'django.contrib.sites',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.microsoft',
    'django_extensions',
    'sslserver',
    'corsheaders',
]




MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'corsheaders.middleware.CorsMiddleware',  # Middleware para manejo de CORS
    'social_django.middleware.SocialAuthExceptionMiddleware',  # Middleware para manejo de excepciones de autenticación
    'allauth.account.middleware.AccountMiddleware',  # Middleware necesario para allauth
    'django.contrib.sites.middleware.CurrentSiteMiddleware',  # Middleware para manejo del sitio actual
]

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                # other context processors
                'django.template.context_processors.request',
                'social_django.context_processors.backends',
                'social_django.context_processors.login_redirect',
            ],
        },
    },
]

ROOT_URLCONF = 'myproject.urls'



MEDIA_URL = '/media/'
WSGI_APPLICATION = 'myproject.wsgi.application'

# Database
DATABASES = DATABASES

# Password validation
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

# Internationalization
LANGUAGE_CODE = 'es'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

LANGUAGES = [
    ('es', 'Spanish'),
    ('en', 'English'),
]

LOCALE_PATHS = [
    BASE_DIR / 'locale',
]

# Static files (CSS, JavaScript, Images)
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'

# Media files
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Recaptcha settings
RECAPTCHA_SITE_KEY = '6LcDqR0qAAAAAGSKjUdW86ReLCmI0zs3P_Hn6phC'
RECAPTCHA_SECRET_KEY = '6LcDqR0qAAAAAG-_GbPkXGz9ruh5AZyN6NtAxBW9'

handler404 = 'webapp.views.error_404_view'
handler500 = 'webapp.views.error_500_view'

SITE_ID = 5

DEFAULT_FROM_EMAIL = EMAIL_HOST_USER
CONTACT_EMAIL = 'admin@stregasoft.com'

AUTHENTICATION_BACKENDS = (
    'social_core.backends.microsoft.MicrosoftOAuth2',
    'django.contrib.auth.backends.ModelBackend',
    'social_core.backends.facebook.FacebookOAuth2',
)

SOCIALACCOUNT_PROVIDERS = {
    'microsoft': {
        'APP': {
            'client_id': '181cfc29-d421-4aad-aced-46ddeb4c323f',
            'secret': '40fdd5b1-2a3d-46b9-a954-9d33c7d42bf9',
        },
        'AUTH_PARAMS': {
            'response_type': 'code',
            'redirect_uri': 'http://localhost:8080/'  # Esta debe coincidir con la de Azure
        },
        'OAUTH2_STATIC_NAME': 'microsoft',
        'SCOPE': ['User.Read'],
    }
}
SOCIALACCOUNT_AUTO_LOGIN = True
ACCOUNT_ADAPTER = 'webapp.adapters.MyAccountAdapter'
SOCIALACCOUNT_ADAPTER = 'webapp.adapters.MySocialAccountAdapter'
ACCOUNT_LOGIN_ON_PROVIDER_LOGIN = True
SOCIALACCOUNT_AUTO_SIGNUP = True


TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],  # Asegúrate de que la ruta sea correcta
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',  # Necesario para el admin
                'django.contrib.messages.context_processors.messages',  # Necesario para el admin
            ],
        },
    },
]

# Configuración de OAuth de Facebook
SOCIAL_AUTH_FACEBOOK_KEY = '1024773669312901'
SOCIAL_AUTH_FACEBOOK_SECRET = '5c9f5a3f5f434d8ae9c38d84bcc26490'
SOCIAL_AUTH_FACEBOOK_SCOPE = ['email']
SOCIAL_AUTH_FACEBOOK_REDIRECT_URI = 'https://127.0.0.1:8080/complete/facebook/' #cambiar redireccion a produccion   https://stregasoft.com/complete/facebook/
