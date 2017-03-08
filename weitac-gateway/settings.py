# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
import djcelery
from datetime import timedelta

BASE_DIR = os.path.dirname(os.path.dirname(__file__))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.7/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 't+nh=x##f=ysmg4jjn!6plzi9o=e_qoe#!(l)jfs8(grt3yyje'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

# ALLOWED_HOSTS = ['0.0.0.0','localhost']

# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'djcelery',
    # 'rest_framework.authtoken',
    'services',
    'login',
    'jobs',
    'configurations'
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    # 'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)
# 'django.middleware.csrf.CsrfViewMiddleware',
ROOT_URLCONF = 'weitac-gateway.urls'

WSGI_APPLICATION = 'weitac-gateway.wsgi.application'

# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases

DATABASES = {
    'default': {
        # 'NAME': os.path.join(BASE_DIR, 'user_data'),
        'NAME': 'weitac_gateway',
        'ENGINE': 'django.db.backends.mysql',
        'USER': 'root',
        'PASSWORD': '111111',
        # 'HOST': '10.6.168.161',
        'HOST': 'localhost',
        'PORT': '3306',
    }
}
# DATABASES = {'default': {
#     'ENGINE': os.getenv('') or 'django.db.backends.sqlite3',
#     'NAME': os.getenv('DB_NAME') or 'tmp.db',
#     'USER': os.getenv('DB_USER') or '',
#     'PASSWORD': os.getenv('DB_PASSWORD') or '',
#     'HOST': os.getenv('DB_HOST') or '',
#     'PORT': os.getenv('DB_PORT') or '',
# }}
# Internationalization
# https://docs.djangoproject.com/en/1.7/topics/i18n/

# LANGUAGE_CODE = 'en-us'
LANGUAGE_CODE = 'zh-CN'
# TIME_ZONE = 'UTC'
TIME_ZONE = 'Asia/Shanghai'
USE_I18N = True

USE_L10N = True

USE_TZ = True

# PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
# STATIC_ROOT = os.path.join(PROJECT_ROOT, 'weitac-gateway')
STATIC_URL = '/static/'
# template
TEMPLATE_DIRS = (
    os.path.join(BASE_DIR, 'templates'),
)
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, "static"),
)
# Static files (

SESSION_EXPIRE_AT_BROWSER_CLOSE = True

LOG_PATH = '/var/log/weitac-gateway/'

LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'standard': {
            'format': '%(asctime)s [%(levelname)s][%(threadName)s]' +
                      '[%(name)s:%(lineno)d] %(message)s'}
    },
    'handlers': {
        'debug': {
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': LOG_PATH + 'debug.log',
            'maxBytes': 1024 * 1024 * 5,
            'backupCount': 5,
            'formatter': 'standard',
        },
        'info': {
            'level': 'INFO',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': LOG_PATH + 'info.log',
            'maxBytes': 1024 * 1024 * 5,
            'backupCount': 5,
            'formatter': 'standard',
        },
        'error': {
            'level': 'ERROR',
            'class': 'logging.handlers.RotatingFileHandler',
            # 'filename': LOG_PATH + '.error.log',
            'filename': LOG_PATH + 'error.log',
            'maxBytes': 1024 * 1024 * 5,
            'backupCount': 5,
            'formatter': 'standard',
        },
        'console': {
            'level': 'ERROR',
            'class': 'logging.StreamHandler',
            'formatter': 'standard'
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console', 'debug', 'info', 'error'],
            'level': 'INFO',
            'propagate': False
        },
        'django.request': {
            'handlers': ['console', 'debug', 'info', 'error'],
            'level': 'INFO',
            'propagate': False,
        },
        '': {
            'handlers': ['console', 'debug', 'info', 'error'],
            'level': 'DEBUG',
            'propagate': False
        },
    }
}

# config of djcelery
djcelery.setup_loader()
BROKER_URL = 'amqp://guest:guest@localhost:5672//'
# CELERY_RESULT_BACKEND = 'amqp://guest:guest@localhost:5672//'
# CELERY_RESULT_BACKEND = "database"
CELERY_RESULT_BACKEND='djcelery.backends.database:DatabaseBackend'

# CELERY_RESULT_DBURI = "mysql+mysqlconnector://root:111111@localhost:3306/weitac_gateway"
# CELERY_RESULT_DBURI = "db+mysql://root:111111@localhost:3306/weitac_gateway"
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TIMEZONE = TIME_ZONE
CELERY_ENABLE_UTC = True
# CELERY_ALWAYS_EAGER = True
CELERY_IMPORTS = ("jobs.tasks", "jobs.views")
CELERYBEAT_SCHEDULER = 'djcelery.schedulers.DatabaseScheduler'
# CELERYBEAT_SCHEDULER = 'djcelery.schedulers.DatabaseScheduler'
# CELERYBEAT_SCHEDULE = {
#     'add-every-30-seconds': {
#         'task': 'tasks.add',
#         'schedule': timedelta(seconds=1),
#         'args': (16, 16)
#     },
# }


