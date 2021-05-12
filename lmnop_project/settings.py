"""
Django settings for lmnop_project project.

Generated by 'django-admin startproject' using Django 2.2.5.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.2/ref/settings/
"""

import os


# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.2/howto/deployment/checklist/


# To enable random creation of SECRET_KEY
"""
Script From:
https://gist.github.com/ndarville/3452907
Two things are wrong with Django's default `SECRET_KEY` system:
1. It is not random but pseudo-random
2. It saves and displays the SECRET_KEY in `settings.py`
This snippet
1. uses `SystemRandom()` instead to generate a random key
2. saves a local `secret.txt`
The result is a random and safely hidden `SECRET_KEY`.
"""
# try:
#     SECRET_KEY
# except NameError:
#     SECRET_FILE = os.path.join(PROJECT_PATH, 'secret.txt')
#     try:
#         SECRET_KEY = open(SECRET_FILE).read().strip()
#     except IOError:
#         try:
#             import random
#             SECRET_KEY = ''.join([random.SystemRandom().choice('abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)') for i in range(50)])
#             secret = file(SECRET_FILE, 'w')
#             secret.write(SECRET_KEY)
#             secret.close()
#         except IOError:
#             Exception('Please create a %s file with random characters \
#             to generate your secret key!' % SECRET_FILE)

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ['Secret_Key']
# SECURITY WARNING: don't run with debug turned on in production!

# Enable this once branch is tested with photo upload.
if os.getenv('GAE_INSTANCE'):
    DEBUG = False
else:
    DEBUG = True

# Disable this once branch is tested with photo upload
# DEBUG = True

ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_social_share',
    'lmn',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'lmnop_project.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.request',
            ],
        },
    },
]

WSGI_APPLICATION = 'lmnop_project.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases

DATABASES = {

    # Uncomment this when you are ready to use Postgres.

    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'lmnop-postgres',
        'USER' : 'livemusicafficiendo',
        'PASSWORD' : os.environ['LMNOP_PW'],
        'HOST' : '/cloudsql/clear-booking-309320:us-central1:lmnop-db',
        'PORT' : '5432'
    }
}

if not os.getenv('GAE_INSTANCE'): 
    # DATABASES['default']['HOST'] = '127.0.0.1'
    DATABASES = {
    # And when you use Postgres, comment out or remove this DB config. 
    # Using environment variables to detect where this app is running, and automatically use 
    # an appropriate DB configuration, is a good idea.

    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
    }



# Password validation
# https://docs.djangoproject.com/en/2.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/2.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.2/howto/static-files/
STATIC_ROOT = os.path.join(BASE_DIR, 'www', 'static')

MEDIA_ROOT = os.path.join(BASE_DIR, 'www', 'media')

if os.getenv('GAE_INSTANCE'):
    # For Google Cloud App Engine
    GS_STATIC_FILE_BUCKET = 'clear-booking-309320.appspot.com'
    
    STATIC_URL = f'https://storage.cloud.google.com/{GS_STATIC_FILE_BUCKET}/static/'

    DEFAULT_FILE_STORAGE = 'storages.backends.gcloud.GoogleCloudStorage'
    GS_BUCKET_NAME = 'images-user-upload'
    MEDIA_URL = f'https://storage.cloud.google.com/{GS_BUCKET_NAME}/media'

    from google.oauth2 import service_account
    GS_CREDENTIALS = service_account.Credentials.from_service_account_file('image-upload-credentials.json')

else:
    # For Local Development
    STATIC_URL = '/static/'
    MEDIA_URL = '/media/'
    MEDIA_URL = os.path.join(BASE_DIR, MEDIA_URL)


# Where to send user after successful login, and logout, if no other page is provided.
LOGIN_REDIRECT_URL = 'my_user_profile'
LOGOUT_REDIRECT_URL = 'goodbye'
