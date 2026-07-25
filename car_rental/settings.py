"""
Django settings for car_rental project.
"""

import os
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# ─── SECURITY ───────────────────────────────────────────────────────────────

# Reads from environment variable in production; falls back to dev key locally
SECRET_KEY = os.environ.get(
    'SECRET_KEY',
    'django-insecure-e7na^1%$@ahctl2gcq8h$1ug2e0#^vu5ehqh*mf4(so!3+(3)1'
)

# DEBUG=False in production (set via env var); True locally
DEBUG = os.environ.get('DEBUG', 'True') == 'True'

# Accept all hosts locally; production Railway URL is added automatically
ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS', '*').split(',')

# CSRF trusted origins for Railway deployment
CSRF_TRUSTED_ORIGINS = [
    origin for origin in
    os.environ.get('CSRF_TRUSTED_ORIGINS', '').split(',')
    if origin
]


# ─── APPLICATIONS ───────────────────────────────────────────────────────────

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',

    # Local apps
    'accounts',
    'cars',
    'bookings',
]

AUTH_USER_MODEL = 'accounts.CustomUser'
LOGIN_URL = 'accounts:login'
LOGIN_REDIRECT_URL = 'home'
LOGOUT_REDIRECT_URL = 'home'


# ─── MIDDLEWARE ──────────────────────────────────────────────────────────────

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    # WhiteNoise: serves static files efficiently in production (right after SecurityMiddleware)
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'car_rental.urls'


# ─── TEMPLATES ───────────────────────────────────────────────────────────────

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'cars.context_processors.categories_processor',
            ],
        },
    },
]

WSGI_APPLICATION = 'car_rental.wsgi.application'


# ─── DATABASE ────────────────────────────────────────────────────────────────

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# ─── PASSWORD VALIDATION ─────────────────────────────────────────────────────

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]


# ─── INTERNATIONALISATION ────────────────────────────────────────────────────

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Asia/Kolkata'
USE_I18N = True
USE_TZ = True


# ─── STATIC & MEDIA FILES ────────────────────────────────────────────────────

STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'static']
STATIC_ROOT = BASE_DIR / 'staticfiles'

# WhiteNoise compressed manifest storage for production
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# ─── MESSAGES ────────────────────────────────────────────────────────────────

MESSAGE_TAGS = {
    10: 'debug',
    20: 'info',
    25: 'success',
    30: 'warning',
    40: 'danger',
}


# ─── EMAIL CONFIGURATION ─────────────────────────────────────────────────────

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER', 'me.dmpatel19@gmail.com')
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD', 'dprrgfhstgwikvvq')
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER
