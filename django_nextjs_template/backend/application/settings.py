import os
import sys

import django_stubs_ext
import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration
from application.settings_helper import config_get

django_stubs_ext.monkeypatch()

SOURCE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROJECT_DIR = os.path.dirname(SOURCE_DIR)

SECRET_KEY = config_get('DJANGO_SECRET_KEY')

DOMAIN = config_get('PROJECT_DOMAIN')
PROJECT_NAME = config_get('PROJECT_NAME')

CSRF_COOKIE_HTTPONLY = False
CSRF_TRUSTED_ORIGINS = [f'https://{DOMAIN}', 'http://{DOMAIN}']

SESSION_ENGINE = "django.contrib.sessions.backends.signed_cookies"

DEBUG = False # type: ignore

ALLOWED_HOSTS = [
    'django',
    DOMAIN,
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

ROOT_URLCONF = 'application.urls'

AUTHENTICATION_BACKENDS = (
    'social_core.backends.steam.SteamOpenId',
    'social_core.backends.github.GithubOAuth2',
    'social_core.backends.strava.StravaOAuth',
    'application.backends.AsyncModelBackend',
)

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            'templates',
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'social_django.context_processors.backends',
                'social_django.context_processors.login_redirect',
            ],
        },
    },
]

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

WSGI_APPLICATION = 'application.wsgi.application'

if 'migrate' in sys.argv:
    db_options = {}
else:
    db_options = {"options": "-c statement_timeout=500"} 


DATABASES = {
    "default": {
        "NAME": config_get('DATABASE_NAME'),
        "USER": config_get('DATABASE_USER'),
        "HOST": config_get('DATABASE_HOST'),
        "PORT": config_get('DATABASE_PORT', default='5432'),
        "PASSWORD": config_get('DATABASE_PASSWORD'),
        "ENGINE": "django.db.backends.postgresql",
        "OPTIONS": db_options
    }
}

S3_ACCESS_KEY_ID = config_get("S3_ACCESS_KEY_ID")
S3_SECRET_KEY = config_get("S3_SECRET_KEY")
S3_ENDPOINT = config_get("S3_ENDPOINT_URL", default='http://minio:9000')
S3_DOMAIN = config_get("S3_DOMAIN", default=DOMAIN)
S3_SIGNATURE_VERSION = config_get("S3_SIGNATURE_VERSION", default='s3')

MEDIA_S3_STORAGE = {
    "BACKEND": "application.storages.CustomS3Storage",
    "OPTIONS": {
        'bucket_name': config_get(
            "S3_BUCKET_NAME", default=f'{PROJECT_NAME}-media'
        ),
        'endpoint_url': S3_ENDPOINT,
        'access_key': S3_ACCESS_KEY_ID,
        'secret_key': S3_SECRET_KEY,
        'default_acl': 'private',
        'signature_version': S3_SIGNATURE_VERSION,
        'file_overwrite': False,
        'querystring_auth': True,
        'querystring_expire': 60 * 2,  # Links valid for two minutes
        'domain': S3_DOMAIN,
    },
}

# This is used during build phase to collect static files to nginx image
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(SOURCE_DIR, 'static')

STORAGES = {
    "default": MEDIA_S3_STORAGE,
    "staticfiles": {
        "BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage",
    }
}


AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'
    },
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]


LANGUAGE_CODE = 'ru-ru'

TIME_ZONE = 'Europe/Moscow'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# EMAIL SETTINGS #

EMAIL_HOST = config_get('EMAIL_HOST', default=None)
EMAIL_HOST_PASSWORD = config_get('EMAIL_PASSWORD', default=None)
EMAIL_HOST_USER = config_get('EMAIL_USER', default=None)
SERVER_EMAIL = config_get('EMAIL_USER', default=None)
EMAIL_PORT = config_get('EMAIL_PORT', default=None)
EMAIL_USE_SSL = True
EMAIL_SUBJECT_PREFIX = '[METAGAME] '

# END EMAIL SETTINGS #


LOGGING = {
    'version': 1,
    'filters': {
        'require_debug_true': {
            '()': 'django.utils.log.RequireDebugTrue',
        }
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'filters': ['require_debug_true'],
            'class': 'logging.StreamHandler',
        }
    },
    'loggers': {
        'django.db.backends': {
            'level': 'DEBUG',
            'handlers': ['console'],
        }
    }
}

SENTRY_DSN = config_get('SENTRY_DSN', default=None)
if SENTRY_DSN is not None:
    sentry_sdk.init(
        dsn=config_get('SENTRY_DSN', default=None),
        integrations=[DjangoIntegration()],
        send_default_pii=True,
    )

from application.project_settings import *  # noqa used to customize templated settings

try:
    from local_settings import *  # noqa
except ImportError:
    pass

SESSION_COOKIE_SECURE = not DEBUG

