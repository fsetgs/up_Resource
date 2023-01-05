"""
Django settings for Resource project.

Generated by 'django-admin startproject' using Django 3.2.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.2/ref/settings/
"""

import os
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-91_4o+al1k8txad4%a-q5!=a#!ns9nk2%swqqn05(@dv^o7w$('

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ["*"]

# 配置session的存在时间
SESSION_COOKIE_AGE=60*60*24*7*2

SESSION_SAVE_EVERY_REQUEST = True

# 配置Session是否生效
SESSION_EXPIRE_AT_BROWSER_CLOSE = True

#设置是否启用frame或iframe
X_FRAME_OPTIONS = 'SAMEORIGIN'


# Broker配置，使用Redis作为消息中间件
BROKER_URL = 'redis://127.0.0.1:6379/0' 
 
# BACKEND配置，这里使用redis
CELERY_RESULT_BACKEND = 'redis://127.0.0.1:6379/0' 
 
# 结果序列化方案
CELERY_RESULT_SERIALIZER = 'json' 
 
# 任务结果过期时间，秒
CELERY_TASK_RESULT_EXPIRES = 60 * 60 * 24 
 
# 时区配置
CELERY_TIMEZONE='Asia/Shanghai'   
 
# 指定导入的任务模块，可以指定多个
#CELERY_IMPORTS = (     
#    'other_dir.tasks',
#)

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'userControl',
    'mainControl',
    'dataControl',
    'checkControl',
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

ROOT_URLCONF = 'Resource.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR,'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        'builtins':['django.templatetags.static'],
        'libraries':{
            'my_filter':'dataControl.templatetags.my_filter',
        }
        },
    },
]

WSGI_APPLICATION = 'Resource.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'resource',
        'USER': 'root',
        'PASSWORD': '123456',
        'HOST': '172.18.161.83',
        'PORT': '3307',
    }
}


# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

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

# 数据缓存模块
CACHES = {
    'default':{
        'BACKEND':'django.core.cache.backends.locmem.LocMemCache',# 本地内存的缓存
        'LOCATION':'unique-snowflake',
    }
}

# Internationalization
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = 'zh-Hans'

TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_L10N = True

USE_TZ = False

APPKEY = "dingex3ufgx6u2hmv0k7"
APPSECRET = "hOkKqbMcVOApokfNZw7ER6Mb9lt5nIxSRU26TwjAp-msOzcu9u_Id-sVC7XHe32P"

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR,'static_all')
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "static"),  # 实际名，即实际文件夹的名字
]

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR,'media')

# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
