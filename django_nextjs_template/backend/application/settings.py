import os
import sys

import django_stubs_ext
import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration
from application.settings_helper import config_get, config_get_str
from typing import Any
from copy import deepcopy

django_stubs_ext.monkeypatch()

SOURCE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROJECT_DIR = os.path.dirname(SOURCE_DIR)

SECRET_KEY = config_get_str('DJANGO_SECRET_KEY')

DOMAIN = config_get_str('PROJECT_DOMAIN')
PROJECT_NAME = config_get_str('PROJECT_NAME')
PROJECT_VERSION = config_get_str('PROJECT_VERSION', '0')

CSRF_COOKIE_HTTPONLY = False
CSRF_TRUSTED_ORIGINS = [f'https://{DOMAIN}', ]

SESSION_ENGINE = "django.contrib.sessions.backends.signed_cookies"

DEBUG = bool(config_get('DJANGO_DEBUG', default=False))

ALLOWED_HOSTS: list[str] = [
    f'{PROJECT_NAME}-django',
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

AUTHENTICATION_BACKENDS = ( # type: ignore Allow redefinition in project settings
    'application.backends.AsyncModelBackend',
)

TEMPLATES: list[dict[str, Any]] = [
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


DATABASES: dict[str, Any] = {
    "default": {
        "NAME": config_get_str('DATABASE_NAME'),
        "USER": config_get_str('DATABASE_USER'),
        "HOST": config_get_str('DATABASE_HOST'),
        "PORT": config_get_str('DATABASE_PORT', default='5432'),
        "PASSWORD": config_get_str('DATABASE_PASSWORD'),
        "ENGINE": "django.db.backends.postgresql",
        "OPTIONS": db_options
    }
}

S3_ACCESS_KEY_ID = config_get("S3_ACCESS_KEY_ID")
S3_SECRET_KEY = config_get("S3_SECRET_KEY")
S3_ENDPOINT = config_get("S3_ENDPOINT_URL", default=f'http://{PROJECT_NAME}-minio:9000')
S3_MEDIA_DOMAIN = config_get("S3_MEDIA_DOMAIN", default=f'media.{DOMAIN}')
S3_STATIC_DOMAIN = config_get("S3_STATIC_DOMAIN", default=f'static.{DOMAIN}')
S3_SIGNATURE_VERSION = config_get("S3_SIGNATURE_VERSION", default='v4')
S3_ACL = config_get("S3_ACL", default='private')
S3_MEDIA_BUCKET = config_get("S3_MEDIA_BUCKET", default=f'{PROJECT_NAME}-media')
S3_STATIC_BUCKET = config_get("S3_STATIC_BUCKET", default=f'{PROJECT_NAME}-static')

STATIC_URL = '/static/' if DEBUG else f'https://{S3_STATIC_DOMAIN}/{S3_STATIC_BUCKET}/'

MEDIA_S3_STORAGE: dict[str, Any] = {
    "BACKEND": "storages.backends.s3.S3Storage",
    "OPTIONS": {
        'bucket_name': S3_MEDIA_BUCKET,
        'endpoint_url': S3_ENDPOINT,
        'access_key': S3_ACCESS_KEY_ID,
        'secret_key': S3_SECRET_KEY,
        'default_acl': S3_ACL,
        'location': S3_MEDIA_BUCKET if DEBUG else '',
        'signature_version': S3_SIGNATURE_VERSION,
        'file_overwrite': True,
        'querystring_auth': S3_ACL == 'private',
        'querystring_expire': 60 * 2,  # Links valid for two minutes
        'custom_domain': S3_MEDIA_DOMAIN,
    },
}

STATIC_S3_STORAGE: dict[str, Any] = deepcopy(MEDIA_S3_STORAGE)
STATIC_S3_STORAGE['OPTIONS']['default_acl'] = 'public-read'
STATIC_S3_STORAGE['OPTIONS']['querystring_auth'] = False
STATIC_S3_STORAGE['OPTIONS']['custom_domain'] = S3_STATIC_DOMAIN
STATIC_S3_STORAGE['OPTIONS']['bucket_name'] = S3_STATIC_BUCKET

LOCAL_STATIC_STORAGE: dict[str, Any] = { "BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage" }

STORAGES: dict[str, Any] = {
    "default": MEDIA_S3_STORAGE,
    "staticfiles": LOCAL_STATIC_STORAGE if DEBUG else STATIC_S3_STORAGE
}

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

LOGIN_REDIRECT_URL = '/'

LANGUAGE_CODE = 'ru-ru'

TIME_ZONE = 'Europe/Moscow'

USE_I18N = True

USE_L10N = True

USE_TZ = True

SENTRY_DSN = config_get('SENTRY_DSN', default=None)
if SENTRY_DSN is not None:
    sentry_sdk.init(
        dsn=str(config_get('SENTRY_DSN', default=None)),
        integrations=[DjangoIntegration()],
        send_default_pii=True,
        release=PROJECT_VERSION
    )

from application.project_settings import *  # type: ignore used to customize templated settings

SESSION_COOKIE_SECURE = not DEBUG

