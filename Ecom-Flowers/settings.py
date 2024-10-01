import os
from dotenv import load_dotenv
import django_heroku
import dj_database_url
import warnings


ENVIRONMENT = os.getenv('ENVIRONMENT', 'development')

DEBUG = True
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SECRET_KEY = os.getenv('SECRET_KEY')
ALLOWED_HOSTS = [
    'flower-ecom-web-6bf01dafa3e0.herokuapp.com',
    'www.flower-ecom-web-6bf01dafa3e0.herokuapp.com',  # Add www version if needed
    '.herokuapp.com',
]

SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')


# CSRF Trusted Origins
CSRF_TRUSTED_ORIGINS = [
    'https://flower-ecom-web-6bf01dafa3e0.herokuapp.com',  # HTTPS version
    'http://flower-ecom-web-6bf01dafa3e0.herokuapp.com',   # HTTP version (if necessary)
]


INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'crispy_forms',
    'crispy_bootstrap4',    
    'django.contrib.sites', 
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'core',
    'django_daraja', 
     
]

# Load environment variables from .env file
load_dotenv()
MPESA_ENVIRONMENT = os.getenv('MPESA_ENVIRONMENT')
MPESA_CONSUMER_KEY = os.getenv('MPESA_CONSUMER_KEY')
MPESA_CONSUMER_SECRET = os.getenv('MPESA_CONSUMER_SECRET')
MPESA_EXPRESS_SHORTCODE = os.getenv('MPESA_EXPRESS_SHORTCODE')
MPESA_PASSKEY = os.getenv('MPESA_PASSKEY')
CALLBACK_URL = os.getenv('CALLBACK_URL')

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    "allauth.account.middleware.AccountMiddleware",
    'whitenoise.middleware.WhiteNoiseMiddleware',
]

ROOT_URLCONF = 'Ecom-Flowers.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
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

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True

STATIC_URL = '/static/'
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static_files')]
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'etbjgpv1z5h1jh22',
        'USER': 'hk56gmnnvjz9cw9y',
        'PASSWORD': 'j6jji880x4ul3ayj',
        'HOST': 'l3855uft9zao23e2.cbetxkdyhwsb.us-east-1.rds.amazonaws.com',
        'PORT': '3306',
        'OPTIONS': {
            'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
            'ssl': {
                'ca': '/static_files/ssl/global-bundle.pem',  # Path to your CA certificate
                'cert': '/static_files/ssl/global-bundle.pem',  # Path to your client certificate
                'key': '/static_files/ssl/global-bundle.pem',  # Path to your client key
            },
        },
        'CONN_MAX_AGE': 600,  # Persistent connections
    }
}
DATABASES['default'].update(dj_database_url.config(conn_max_age=600, ssl_require=True))
SECURE_REFERRER_POLICY = 'no-referrer'


if ENVIRONMENT == 'production':
    DEBUG = True
    SECRET_KEY = os.getenv('SECRET_KEY')
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SECURE_BROWSER_XSS_FILTER = True
    SECURE_CONTENT_TYPE_NOSNIFF = True
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_SECONDS = 31536000
    SECURE_REDIRECT_EXEMPT = []
    SECURE_SSL_REDIRECT = True
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

#authentication
AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
]
SITE_ID =1
#autofield
DEFAULT_AUTO_FIELD = 'django.db.models.AutoField'

#CRISPY-FORMS
CRISPY_TEMPLATE_PACK = 'bootstrap4'



django_heroku.settings(locals())
del DATABASES['default']['OPTIONS']['sslmode']

# Silence specific warnings
warnings.filterwarnings("ignore", category=UserWarning, module="allauth")

#load error
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': 'DEBUG',
        },
    },
}
