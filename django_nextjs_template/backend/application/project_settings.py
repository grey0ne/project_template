PROJECT_APPS = [
    'users',
]

INSTALLED_APPS = [
    'application.admin.ProjectAdminConfig',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.staticfiles',
    'django.contrib.messages',
] + PROJECT_APPS

AUTH_USER_MODEL = 'users.User'