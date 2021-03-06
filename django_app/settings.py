"""
Django settings for sichuan_yd_children project.

Generated by 'django-admin startproject' using Django 2.0.4.

For more information on this file, see
https://docs.djangoproject.com/en/2.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.0/ref/settings/
"""

import os
import configparser
from common.iniphaser import IniPhaser

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
WORK_PATH = os.path.abspath(os.path.dirname(__file__))  # 跟settings.py同层路径  sichuan_dx_game/sichuan_dx_game/
PRODUCT_KEY = "pinche"  # 配置不同的项目日志等使用参考

config_file_path = os.path.join(WORK_PATH, "settings.ini")  # todo
cf = IniPhaser()
cf.read(config_file_path, encoding='utf8')
cf_dict = cf.as_dict()


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '=2*_(zch=n6*uka*zg*r&9dn99@n8s$v=!)gju_f!7)82@guz1'

# SECURITY WARNING: don't run with debug turned on in production!
if cf.get('OPTIONS', 'DEBUG') == "True":
    DEBUG = True
else:
    DEBUG = False

ALLOWED_HOSTS = ["*"]


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    # 'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

]

ROOT_URLCONF = 'django_app.urls'


WSGI_APPLICATION = 'django_app.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.0/ref/settings/#databases

DATABASES = {
     'default': cf_dict['DATABASE'],
    # 'activity':cf_dict["DATABASE_ACTIVITY"],
}



# Password validation
# https://docs.djangoproject.com/en/2.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/2.0/topics/i18n/
LANGUAGE_CODE = 'zh-hans'
TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_L10N = False

USE_TZ = False

# 日期格式设置
DATE_FORMAT = 'Y-m-d'
DATETIME_FORMAT = 'Y-m-d H:i:s'


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.0/howto/static-files/

STATIC_URL = '/static/'
if os.name != "posix":
    STATICFILES_DIRS = [
        os.path.join(BASE_DIR, "static"),
    ]
else:
    STATIC_ROOT = os.path.join(BASE_DIR, "static")

TEMPLATE_DIRS = (os.path.join(BASE_DIR, 'templates'),)
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': ["templates"],
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

# 设置log
LOG_DIR = cf.get('OPTIONS', 'LOG_DIR')  #
# if os.name != "posix":
#     LOG_DIR = WORK_PATH
if not os.path.exists(LOG_DIR):
    os.makedirs(LOG_DIR)
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s %(funcName)s %(lineno)d %(message)s'
        },
        'simple': {
            'format': '%(levelname)s %(message)s'
        },
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler'
        },
        'file': {
            'level': 'DEBUG',
            # 'class': 'logging.FileHandler',
            'class': 'logging.handlers.RotatingFileHandler',
            'formatter': 'verbose',
            'maxBytes': 1024 * 1024 * 100,  # 文件大小 5*1024*1024 bytes (5MB)
            'backupCount': 1,
            'filename': os.path.join(LOG_DIR, "%s.log"%PRODUCT_KEY),
        },
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins', 'file'],
            'level': 'ERROR',
            'propagate': True,
        },
        'default': {
            'handlers': ['file'],
            'level': 'DEBUG',
            'propagate': True,
        },

    }
}

# 设置admin上传配置
MEDIA_URL = "/media/"
MEDIA_ROOT = os.path.join(BASE_DIR, "media")
FILE_UPLOAD_PERMISSIONS = 0o644    # 增加media上传权限的问题

# 设置session
# 配置session,如果用root需要先本地运行一下，然后将session权限设置开，这样才可以用
SESSION_ENGINE = 'django.contrib.sessions.backends.file'
SESSION_DIR = cf.get('OPTIONS', 'SESSION_DIR')
if not os.path.exists(SESSION_DIR):
    os.makedirs(SESSION_DIR)

SESSION_FILE_PATH = SESSION_DIR
SESSION_COOKIE_NAME = "session_%s" % PRODUCT_KEY

# Whether to expire the session when the user closes his or her browser.
SESSION_EXPIRE_AT_BROWSER_CLOSE = True

CACHE_DIR = cf.get('OPTIONS', 'CACHE_DIR')  #
if not os.path.exists(CACHE_DIR):
    os.makedirs(CACHE_DIR)
# 设置缓存
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.filebased.FileBasedCache',
        'LOCATION': CACHE_DIR,
    }
}


# 不用验证信息的url
SERVICE_FILTER_URLS = [
    (r'^/admin/*'),
    (r'^/xadmin/*'),
    (r'%s*' % STATIC_URL),
    (r'%s*' % MEDIA_URL),
    (r'/favicon.ico'),
]




# Celery settings
CELERY_BROKER_URL = 'amqp://guest:guest@localhost//'
#: Only add pickle to this list if your broker is secured
#: from unwanted access (see userguide/security.html)
# 不需要开启数据回调数据库，否则压力很大，如果实在不行，都可以再换个新的sqlite
# CELERY_ACCEPT_CONTENT = ['json']
# CELERY_RESULT_BACKEND = 'db+sqlite:///results.sqlite'
# CELERY_TASK_SERIALIZER = 'json'


