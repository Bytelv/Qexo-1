from pathlib import Path
import os
import json
import random
import hexoweb.exceptions as exceptions
import logging

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

LOGIN_REDIRECT_URL = "home"  # Route defined in home/urls.py
LOGOUT_REDIRECT_URL = "home"  # Route defined in home/urls.py

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-mrf1flh+i8*!ao73h6)ne#%gowhtype!ld#+(j^r*!^11al2vz'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

try:
    import configs  # 本地部署

    ALLOWED_HOSTS = configs.DOMAINS
except:
    logging.info("获取本地配置文件失败, 使用环境变量获取配置")  # Serverless部署
    ALLOWED_HOSTS = json.loads(os.environ.get("DOMAINS", False)) if os.environ.get("DOMAINS", False) else ["*"]

# Application definition

INSTALLED_APPS = [
    # 'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    # 'django.contrib.staticfiles',
    'hexoweb.apps.ConsoleConfig',
    'corsheaders',
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

CORS_ORIGIN_ALLOW_ALL = True
CORS_ALLOW_CREDENTIALS = True

ROOT_URLCONF = 'core.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates']
        ,
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

WSGI_APPLICATION = 'core.wsgi.application'

# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

try:
    import configs

    print("获取本地配置文件成功, 使用本地数据库配置")
    DATABASES = configs.DATABASES
except:
    if os.environ.get("MONGODB_HOST"):  # 使用MONGODB
        print("使用环境变量中的MongoDB数据库")
        for env in ["MONGODB_HOST", "MONGODB_PORT", "MONGODB_USER", "MONGODB_PASS", "MONGODB_DB"]:
            if env not in os.environ:
                raise exceptions.InitError(f"\"{env}\"环境变量未设置")
        DATABASES = {
            'default': {
                'ENGINE': 'djongo',
                'ENFORCE_SCHEMA': False,
                'LOGGING': {
                    'version': 1,
                },
                'NAME': 'django',
                'CLIENT': {
                    'host': os.environ["MONGODB_HOST"],
                    'port': int(os.environ["MONGODB_PORT"]),
                    'username': os.environ["MONGODB_USER"],
                    'password': os.environ["MONGODB_PASS"],
                    'authSource': os.environ["MONGODB_DB"],
                    'authMechanism': 'SCRAM-SHA-1'
                }
            }
        }
    elif os.environ.get("PG_HOST"):  # 使用 PostgreSQL
        print("使用环境变量中的PostgreSQL数据库")
        for env in ["PG_HOST", "PG_PORT", "PG_USER", "PG_PASS", "PG_DB"]:
            if env not in os.environ:
                raise exceptions.InitError(f"\"{env}\"环境变量未设置")
        DATABASES = {
            'default': {
                'ENGINE': 'django.db.backends.postgresql',
                'NAME': os.environ["PG_DB"],
                'USER': os.environ["PG_USER"],
                'PASSWORD': os.environ["PG_PASS"],
                'HOST': os.environ["PG_HOST"],
                'PORT': os.environ["PG_PORT"],
            }
        }
    else:  # 使用MYSQL
        print("使用环境变量中的MySQL数据库")
        for env in ["MYSQL_NAME", "MYSQL_HOST", "MYSQL_PORT", "MYSQL_USER", "MYSQL_PASSWORD"]:
            if env not in os.environ:
                raise exceptions.InitError(f"\"{env}\"环境变量未设置")
        import pymysql

        pymysql.install_as_MySQLdb()
        DATABASES = {
            'default': {
                'ENGINE': 'django.db.backends.mysql',
                'NAME': os.environ.get('MYSQL_NAME'),
                'HOST': os.environ.get('MYSQL_HOST'),
                'PORT': os.environ.get('MYSQL_PORT'),
                'USER': os.environ.get('MYSQL_USER'),
                'PASSWORD': os.environ.get('MYSQL_PASSWORD'),
                'OPTIONS': {'ssl': {'ca': False}}
            }
        }
        if os.environ.get("PLANETSCALE"):
            DATABASES["default"]["ENGINE"] = "hexoweb.libs.django_psdb_engine"

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

# Internationalization
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = 'zh-Hans'

TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

# STATIC_URL = '/static/'
# STATICFILES_DIRS = [
#     os.path.join(BASE_DIR, "static"),
# ]
# STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles_build', 'static')

# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

SESSION_COOKIE_AGE = 86400
