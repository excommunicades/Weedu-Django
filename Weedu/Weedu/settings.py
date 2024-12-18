"""
Django settings for Weedu project.

Generated by 'Weedu startproject' using Django 5.1.3.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.1/ref/settings/
"""

from datetime import timedelta
from pathlib import Path
import logging
import os

MIDDLEWARE_LOGGER = logging.getLogger("django.middleware")

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-%wv*(@0*q07dd(7lk68l!s!+(im+fzn4v3!qo08sk2y@=u#y_c'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['localhost', '127.0.0.1', '0.0.0.0']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'rest_framework',
    'rest_framework_simplejwt',
    'rest_framework_swagger',

    'corsheaders',
    'django_redis',
    'drf_yasg',

    'users',
    'api',
    'publish',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    # 'Weedu.middleware.SessionLoggingMiddleware',
]

ROOT_URLCONF = 'Weedu.urls'

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

WSGI_APPLICATION = 'Weedu.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
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

LANGUAGE_CODE = 'en-us' # uk-UK

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/

STATIC_URL = 'static/'

# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

AUTH_USER_MODEL = 'users.Weedu_User'

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

FRONTEND_URL = 'http://localhost:5173'

BACKEND_URL = 'http://localhost:8000'

# CORS SETTINGS

CORS_ALLOW_ALL_ORIGINS = True

CORS_ALLOWED_ORIGINS = [
    'http://localhost:5173',
]

# REST_FRAMEWORK = {
#     'EXCEPTION_HANDLER': 'blog_user.views.custom_exception_handler',

# }

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.SessionAuthentication',  # Сессионная аутентификация
        'rest_framework_simplejwt.authentication.JWTAuthentication',  # Аутентификация через JWT
        'rest_framework.authentication.BasicAuthentication',  # Базовая аутентификация (пара username:password)
    )
}

SESSION_ENGINE = 'django.contrib.sessions.backends.cache'

# SESSION COOKIE SETTINGS

SESSION_CACHE_ALIAS = 'default'

SESSION_COOKIE_NAME = 'sessionid'

SESSION_COOKIE_DOMAIN = 'localhost'

SESSION_COOKIE_SAMESITE = 'None'

SESSION_COOKIE_SECURE = False


SESSION_SAVE_EVERY_REQUEST = True

# CRSF COOKIE SETTINGS

CSRF_COOKIE_SAMESITE = 'None'

CSRF_COOKIE_SECURE = False

CSRF_COOKIE_HTTPONLY = False

CSRF_TRUSTED_ORIGINS = ['http://localhost:5173']

CSRF_COOKIE_DOMAIN = ".localhost"

SESSION_COOKIE_AGE = 3600 * 24 * 14

SESSION_EXPIRE_AT_BROWSER_CLOSE = False

CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': 'redis://127.0.0.1:6379/0',
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
        }
    }
}

SESSION_REDIS = {
    'HOST': '127.0.0.1',
    'PORT': 6379,
    'DB': 0,
    'PASSWORD': None,
    'PREFIX': 'session:',
    'SOCKET_TIMEOUT': 1
}

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'

CORS_ALLOW_CREDENTIALS = True

CSRF_COOKIE_NAME = "csrftoken"  # Убедитесь, что имя cookie соответствует
CSRF_COOKIE_PATH = '/' 
# LOGGING = {
#     'version': 1,
#     'disable_existing_loggers': False,
#     'handlers': {
#         'console': {
#             'level': 'DEBUG',
#             'class': 'logging.StreamHandler',
#         },
#     },
#     'loggers': {
#         'django': {
#             'handlers': ['console'],
#             'level': 'DEBUG',
#             'propagate': True,
#         },
#         'django_redis': {  # Логгирование для django_redis
#             'handlers': ['console'],
#             'level': 'DEBUG',
#             'propagate': True,
#         },
#     },
# }
