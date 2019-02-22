import os
import dj_database_url
from prettyconf import Configuration
from django.utils.translation import ugettext_lazy as _
from django.contrib import messages

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

config = Configuration(starting_path=BASE_DIR)


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = config('DEBUG', cast=config.boolean, default=False)

ALLOWED_HOSTS = config('ALLOWED_HOSTS', cast=config.list, default='localhost')


# Application definition

INSTALLED_APPS = [
    # Admin
    'admin_interface',
    'colorfield',

    # Default
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Third-party apps
    'model_utils',
    'cities_light',
    'anymail',

    # Local apps
    'apps.core',
    'apps.site',
    'apps.dashboard',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'expertise.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
        ],
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

WSGI_APPLICATION = 'expertise.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.1/ref/settings/#databases

DATABASES = {
    'default': dj_database_url.config(default=config('DATABASE_URL'))
}
DATABASES['default']['ENGINE'] = 'django.contrib.gis.db.backends.postgis'


# Password validation
# https://docs.djangoproject.com/en/2.1/ref/settings/#auth-password-validators

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

AUTH_USER_MODEL = 'core.User'

# Internationalization
# https://docs.djangoproject.com/en/2.1/topics/i18n/

LANGUAGE_CODE = 'pt-BR'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

LANGUAGES = [
    ('en-US', _('English')),
    ('pt-BR', _('Brazilian Portuguese')),
]

LOCALE_PATHS = [
    os.path.join(BASE_DIR, 'locale')
]


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.1/howto/static-files/

STATIC_URL = '/static/'

STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# Cities Light

CITIES_LIGHT_INCLUDE_COUNTRIES = ['BR']

# S3 Storage

AWS_REGION = config('BUCKETEER_AWS_REGION')
AWS_ACCESS_KEY_ID = config('BUCKETEER_AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = config('BUCKETEER_AWS_SECRET_ACCESS_KEY')
AWS_S3_BUCKET_NAME = config('BUCKETEER_BUCKET_NAME')

# GDAL library config

GDAL_LIBRARY_PATH = config('GDAL_LIBRARY_PATH', default=None)
GEOS_LIBRARY_PATH = config('GEOS_LIBRARY_PATH', default=None)

# Login

LOGIN_URL = '/dashboard/login'
LOGIN_REDIRECT_URL = '/dashboard'
SECURE_SSL_REDIRECT = config('SECURE_SSL_REDIRECT', default=False, cast=config.boolean)


# Messages

MESSAGE_TAGS = {
    messages.ERROR: 'danger'
}

# E-mail
ANYMAIL = {
    "MAILGUN_API_KEY": config('MAILGUN_API_KEY'),
    "MAILGUN_SENDER_DOMAIN": config('MAILGUN_SENDER_DOMAIN'),
}
EMAIL_BACKEND = "anymail.backends.mailgun.EmailBackend"
DEFAULT_FROM_EMAIL = config('DEFAULT_FROM_EMAIL')
TEMPLATED_EMAIL_EMAIL_MESSAGE_CLASS='anymail.message.AnymailMessage'
TEMPLATED_EMAIL_EMAIL_MULTIALTERNATIVES_CLASS='anymail.message.AnymailMessage'
TEMPLATED_EMAIL_FILE_EXTENSION = 'email.html'