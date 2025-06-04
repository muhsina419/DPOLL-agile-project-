from pathlib import Path
import os
import urllib.parse
from dotenv import load_dotenv
from urllib.parse import quote_plus
import urllib.parse


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-k7ksj(mpf6o63d(1qe6&9+by4@i++mq0lm*p#fj9)aqu_+&@=x'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['dpoll-agile-project.onrender.com', 'localhost', '127.0.0.1']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'myprojectdpoll', 
    'rest_framework',
    
  

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

ROOT_URLCONF = 'dpoll.urls'

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
                'myprojectdpoll.context_processors.userprofile',
            ],
        },
    },
]

WSGI_APPLICATION = 'dpoll.wsgi.application'


load_dotenv()  # Load environment variables


# Encode username and password
username = urllib.parse.quote_plus("abhinandana")
password = urllib.parse.quote_plus("Abhi@nandu8589")  # Encodes special characters


DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": "postgres",
        "USER": "postgres",
        "PASSWORD": "abhinandu8589",
        "HOST": "localhost",
        "PORT": "5432",
    }
}

# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/5.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/
BASE_DIR = Path(__file__).resolve().parent.parent
STATIC_URL = '/static/'
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "static"), 
]


# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# dpoll/settings.py

import os

# Add this at the end of the file
STATIC_URL = '/static/'
STATICFILES_DIRS = [os.path.join(BASE_DIR , 'static')]
# settings.py

STATIC_URL = '/static/'

# Add the directory where your static files are located
STATICFILES_DIRS = [
    BASE_DIR / 'static',  # Adjust this path if your static folder is elsewhere
]

STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')  # Static files will be collected here

EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = "smtp.gmail.com"
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = "email"
EMAIL_HOST_PASSWORD = "password"

FRONTEND_URL = "http://127.0.0.1:8000"

MEDIA_URL='/media/'
MEDIA_ROOT=os.path.join(BASE_DIR, 'media')

APPEND_SLASH = True
CSRF_TRUSTED_ORIGINS = ['http://127.0.0.1:8000/api/register/']
