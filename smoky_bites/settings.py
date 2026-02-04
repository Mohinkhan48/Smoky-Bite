from pathlib import Path
import os

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.environ.get('SECRET_KEY', 'django-insecure-smokybites-mock-key')

DEBUG = False

ALLOWED_HOSTS = ["*.railway.app"] # Allowed for initial staging, usually restricted to specific domains

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'orders',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'smoky_bites.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'smoky_bites.context_processors.app_context',
            ],
        },
    },
]

WSGI_APPLICATION = 'smoky_bites.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db_v2.sqlite3',
    }
}

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

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'static']
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_STORAGE = 'whitenoise.storage.CompressedStaticFilesStorage'
WHITENOISE_MANIFEST_STRICT = False  # Prevent crash if an asset is missing

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# UPI Configuration
UPI_CONFIG = {
    'ID': 'paytm.s17ewnw@pty',  # Confirmed Merchant UPI ID
    'MERCHANT_NAME': 'SHAUL KHAN',
    'MC': '5812',              # Updated to 5812 (Restaurants/Eating Places)
    'CURRENCY': 'INR',
}

# Hardcoded Admin Credentials
HARDCODED_USERNAME = 'admin'
HARDCODED_PASSWORD = 'password123'  # CHANGE THIS!

AUTHENTICATION_BACKENDS = [
    'orders.backends.HardcodedAuthBackend',
    'django.contrib.auth.backends.ModelBackend', # Keep default for potential other users, or remove if strictly only hardcoded allowed
]
