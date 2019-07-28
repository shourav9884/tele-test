from tele.settings import *
DEBUG = True

# GDAL_LIBRARY_PATH = '/usr/local/lib/libgdal.so' # for production

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    },
    'btc_db': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'btc_db',
        'USER': 'btc_user',
        'PASSWORD': 'btc_pass',
        'HOST': 'localhost',
        'PORT': '5432',
    },
    'warehouse_db': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'warehouse_db',
        'USER': 'warehouse_user',
        'PASSWORD': 'warehouse_pass',
        'HOST': 'localhost',  # Or an IP Address that your DB is hosted on
        'PORT': '5432',
    },
}

CELERY_BROKER_URL = 'redis://localhost:6379/0'
CELERY_RESULT_BACKEND = 'django-db'
