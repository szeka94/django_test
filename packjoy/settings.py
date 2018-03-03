"""
Django settings for packjoy project.

Generated by 'django-admin startproject' using Django 1.11.9.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.11/ref/settings/
"""
from oscar.defaults import *
from oscar import get_core_apps
import os
from django.utils.translation import ugettext_lazy as _
 

location = lambda x: os.path.join(os.path.dirname(os.path.realpath(__file__)), x)

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.11/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.environ.get('DEBUG_MODE', False)

ALLOWED_HOSTS = ['www.packjoy.store',
                 'localhost',
                 'api.mailgun.net',
                 'packjoy.store'
                 'www.packjoy.store',]


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.flatpages',
    'django.contrib.sites',
    'widget_tweaks',
] + get_core_apps([
    'packjoy.apps.shipping',
    'packjoy.apps.checkout',
    'packjoy.apps.partner',
    'packjoy.apps.dashboard',
])

SITE_ID = 1

MIDDLEWARE_CLASSES = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'oscar.apps.basket.middleware.BasketMiddleware',
    'django.contrib.flatpages.middleware.FlatpageFallbackMiddleware',
]

ROOT_URLCONF = 'packjoy.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR, 'packjoy/templates'),
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.template.context_processors.i18n',
                'django.contrib.messages.context_processors.messages',

                'oscar.apps.search.context_processors.search_form',
                'oscar.apps.promotions.context_processors.promotions',
                'oscar.apps.checkout.context_processors.checkout',
                'oscar.apps.customer.notifications.context_processors.notifications',
                'oscar.core.context_processors.metadata',
            ],
        },
    },
]

WSGI_APPLICATION = 'packjoy.wsgi.application'

SECURE_SSL_REDIRECT = not os.environ.get('DEBUG_MODE', False)

# Database
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': os.environ.get('DATABASE_NAME'),
        'USER': os.environ.get('DATABASE_USER'),
        'PASSWORD': os.environ.get('DATABASE_PASSWORD'),
        'HOST': os.environ.get('DATABASE_HOST', 'localhost'),
        'PORT': os.environ.get('DATABASE_PORT'),
    }
}


# Password validation
# https://docs.djangoproject.com/en/1.11/ref/settings/#auth-password-validators

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

AUTHENTICATION_BACKENDS = (
    'oscar.apps.customer.auth_backends.EmailBackend',
    'django.contrib.auth.backends.ModelBackend',
)

# Internationalization
# https://docs.djangoproject.com/en/1.11/topics/i18n/

LANGUAGE_CODE = 'en'

TIME_ZONE = 'Europe/Bucharest'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.11/howto/static-files/
STATIC_URL = '/packjoy/static/'

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'packjoy/static'),
]


# OSCAR settings
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'packjoy/media')

HAYSTACK_CONNECTIONS = {
    'default': {
        'ENGINE': 'haystack.backends.simple_backend.SimpleEngine',
    },
}

gettext_noop = lambda s: s

LANGUAGES = (
    ('en', gettext_noop('English')),
    ('ro', gettext_noop('Romanian')),
    ('hu', gettext_noop('Hungarian')),
)

LOCALE_PATHS = (
    os.path.join(BASE_DIR, 'locale'),
)

OSCAR_SHOP_NAME = 'Ejoy'

OSCAR_IMAGE_FOLDER = 'images/products/'

OSCAR_DEFAULT_CURRENCY = 'RON'

OSCAR_ALLOW_ANON_CHECKOUT = False

OSCAR_HIDDEN_FEATURES = ['wishlists']

OSCAR_REQUIRED_ADDRESS_FIELDS = ('first_name', 'last_name', 'line1', 'line4', 'postcode',
                                 'country', 'phone_number', 'state')
OSCAR_FROM_EMAIL = 'ejoyletter@gmail.com'

OSCAR_MISSING_IMAGE_URL = 'image_not_found.png'

OSCAR_GOOGLE_ANALYTICS_ID = 'UA-113484675-1'

OSCAR_MAX_BASKET_QUANTITY_THRESHOLD = 150

OSCAR_DASHBOARD_NAVIGATION += [
    {
        'label': _('Email Marketing'),
        'icon': 'icon-dashboard',
        'url_name': 'dashboard:email:index',
        'access_fn': lambda user, url_name, url_args, url_kwargs: user.is_staff,
    }
]

# 2CHECKOUT settings
CHECKOUT_SUBMIT_URL = os.environ.get('CHECKOUT_SUBMIT_URL')

CHECKOUT_ACCOUNT_NUMBER = os.environ.get('CHECKOUT_ACCOUNT_NUMBER')

CHECKOUT_SECRET_KEY = os.environ.get('CHECKOUT_SECRET_KEY')


EMAIL_BACKEND = 'django_mailgun.MailgunBackend'

MAILGUN_ACCESS_KEY = os.environ.get('MAILGUN_ACCESS_KEY')

MAILGUN_SERVER_NAME = os.environ.get('MAILGUN_SERVER_NAME')

ADMIN_MAIL_ADDRESSES = ['szeka1994@gmail.com', 'ejoy.main@gmail.com'] if DEBUG else ['szeka1994@gmail.com'] 

MINIMUM_ORDER_QUANTITY = 5
