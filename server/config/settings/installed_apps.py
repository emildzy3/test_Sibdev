DJANGO_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'rest_framework',

]

THIRD_APPS = [
]

CUSTOM_APPS = [
    'apps.analytics',
]

INSTALLED_APPS = DJANGO_APPS + THIRD_APPS + CUSTOM_APPS
