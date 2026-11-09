from pathlib import Path
import os
BASE_DIR = Path(__file__).resolve().parent.parent
SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY', 'local-control-work-26-zoo-feedings')
# DEBUG=False позволяет показывать свою страницу 404 без технических сведений.
DEBUG = False
ALLOWED_HOSTS = ['localhost', '127.0.0.1', '[::1]', 'testserver']
INSTALLED_APPS = ['django.contrib.staticfiles', 'homepage.apps.HomepageConfig',
                  'aviaries.apps.AviariesConfig', 'feedings.apps.FeedingsConfig']
MIDDLEWARE = ['django.middleware.security.SecurityMiddleware',
              'django.middleware.common.CommonMiddleware',
              'django.middleware.csrf.CsrfViewMiddleware',
              'django.middleware.clickjacking.XFrameOptionsMiddleware']
ROOT_URLCONF = 'zoo_feedings.urls'
TEMPLATES = [{'BACKEND': 'django.template.backends.django.DjangoTemplates',
              'DIRS': [BASE_DIR / 'templates'], 'APP_DIRS': True,
              'OPTIONS': {'context_processors': ['django.template.context_processors.request']}}]
WSGI_APPLICATION = 'zoo_feedings.wsgi.application'
ASGI_APPLICATION = 'zoo_feedings.asgi.application'
# Django ORM не используется; основной файл открывает только feedings/db.py.
DATABASES = {}
FEEDINGS_DB = BASE_DIR / 'data' / 'feedings.db'
LANGUAGE_CODE = 'ru-ru'
TIME_ZONE = 'Europe/Moscow'
USE_I18N = True
USE_TZ = False
STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'static']
STATIC_ROOT = BASE_DIR / 'static_collected'
