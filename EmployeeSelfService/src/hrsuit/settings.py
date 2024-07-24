import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'This Is Secret'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

# Email Settings
EMAIL_HOST = 'harivalar00@gmail.com'
EMAIL_HOST_USER = 'valarhari00@gmail.com' #test
EMAIL_HOST_PASSWORD = 'Harivalar@123' #test
EMAIL_PORT = 587
EMAIL_USE_TLS = True

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',

    # INSTALLED APPS
    'crispy_forms',
    'crispy_bootstrap5',
    'phonenumber_field',
    'widget_tweaks',

    # PROJECT APPS
    'dashboard',
    'accounts',
    'employee',
    'leave',
    'attendance',
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

ROOT_URLCONF = 'hrsuit.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates'),],
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

WSGI_APPLICATION = 'hrsuit.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'djongo',
        'NAME': 'employemanagement',
        'ENFORCE_SCHEMA': False,
        'CLIENT': {
            'host': 'localhost',
            'port': 27017,  # Default MongoDB port
            # Uncomment and set these fields if authentication is required
            # 'username': 'your_mongodb_username',
            # 'password': 'your_mongodb_password',
            # 'authSource': 'your_auth_source',
            # 'authMechanism': 'SCRAM-SHA-1',
        },
    }
}



# Password validation
# https://docs.djangoproject.com/en/2.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/2.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

CRISPY_TEMPLATE_PACK = 'bootstrap5'

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.1/howto/static-files/

STATIC_URL = '/static/'

# STATIC FILES WILL BE SERVED FROM STATIC_CDN WHEN WE ARE LIVE - OUTSIDE OF PROJECT
STATIC_ROOT = os.path.join(os.path.dirname(BASE_DIR), 'static_cdn', 'static_root')

# THIS KEEPS THE PROJECT FILES - CSS/JS/IMAGES/FONTS
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static_in_proj', 'our_static'),
]

# MEDIA - UPLOADED FILES/IMAGES
MEDIA_URL = '/media/'

# MEDIA FILES WILL BE SERVED FROM STATIC_CDN WHEN WE ARE LIVE
MEDIA_ROOT = os.path.join(os.path.dirname(BASE_DIR), 'static_cdn', 'media_root')

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
