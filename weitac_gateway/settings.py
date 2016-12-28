
# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os

BASE_DIR = os.path.dirname(os.path.dirname(__file__))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.7/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 't+nh=x##f=ysmg4jjn!6plzi9o=e_qoe#!(l)jfs8(grt3yyje'
# SECRET_KEY = 'q4n*cl8yx_(hg=pk5jk&uuouh6ftfawhhkgz)97h_*buu(+5c-'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = []

# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'rest_framework.authtoken',
    'services',
    'login',
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
ROOT_URLCONF = 'weitac_gateway.urls'

WSGI_APPLICATION = 'weitac_gateway.wsgi.application'

# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases

DATABASES = {
    'default': {
        # 'NAME': os.path.join(BASE_DIR, 'user_data'),
        'NAME': 'user_data',
        'ENGINE': 'django.db.backends.mysql',
        'USER': 'root',
        'PASSWORD': '111111',
        'HOST': 'localhost',
        'PORT': '3306',
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.7/topics/i18n/

# LANGUAGE_CODE = 'en-us'
LANGUAGE_CODE = 'zh-CN'
# TIME_ZONE = 'UTC'
TIME_ZONE = 'Asia/Shanghai'
USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.7/howto/static-files/

STATIC_URL = '/static/'
# template
TEMPLATE_DIRS = (
    os.path.join(BASE_DIR,'templates'),
)
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, "static"),
)
# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.9/howto/static-files/
# SITE_ROOT = os.path.join(os.path.abspath(os.path.dirname(__file__)), '..')
# STATIC_ROOT = os.path.join(SITE_ROOT, 'static')

# STATICFILES_DIRS = (
# ("css", os.path.join(STATIC_ROOT, 'css')),
# ("js", os.path.join(STATIC_ROOT, 'js')),
# ("images", os.path.join(STATIC_ROOT, 'images')),
# ("bower_components", os.path.join(STATIC_ROOT, 'bower_components')),
# # ("templates", os.path.join(STATIC_ROOT, '../login_old/templates')),
# )

SESSION_EXPIRE_AT_BROWSER_CLOSE = True