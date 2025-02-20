from pathlib import Path
import os
from datetime import timedelta
from dotenv import load_dotenv
import dotenv

# Load environment variables from the 'env.dev' file
BASE_DIR = Path(__file__).resolve().parent.parent

dotenv_file = BASE_DIR / '.env.dev'

if os.path.isfile(dotenv_file):
    dotenv.load_dotenv(dotenv_file)


# SECURITY WARNING: keep the secret key used in production secret!
# SECRET_KEY = os.environ.get("SECRET_KEY")

SECRET_KEY ='your_secret_key_any_can_do'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = bool(os.environ.get("DEBUG", default=0))

SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

ALLOWED_HOSTS = ['198.211.99.20', 'localhost', '127.0.0.1', "*"]

AUTH_USER_MODEL = 'accounts.User'
# Application definition

SITE_ID = 1
WEBSITE_URL = 'http://localhost:8000'
CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels.layers.InMemoryChannelLayer'
    }
}

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',


    'rest_framework',
    'rest_framework_simplejwt.token_blacklist',
    'corsheaders',
    'django_extensions',
    'anymail',


    'drf_yasg',

    'accounts',
    'oauth',
    'course',
    'forum',
    'blog',
    'askhive',
    'jobs',
]

SWAGGER_SETTINGS = {
    'SECURITY_DEFINITIONS': {
        'Bearer': {
            'type': 'apiKey',
            'name': 'Authorization',
            'in': 'header'
        }
    }
}

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',

    "corsheaders.middleware.CorsMiddleware",

    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'api.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

# EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
# EMAIL_HOST = 'smtp.gmail.com'
# EMAIL_PORT = 587
# EMAIL_USE_TLS = True
# EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER', default="")
# EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD', default="")


EMAIL_BACKEND = 'django_ses.SESBackend'
DEFAULT_FROM_EMAIL =os.environ.get('AWS_SES_FROM_EMAIL')

AWS_SES_ACCESS_KEY_ID = os.environ.get('AWS_SES_ACCESS_KEY_ID')
AWS_SES_SECRET_ACCESS_KEY = os.environ.get('AWS_SES_SECRET_ACCESS_KEY')
AWS_SES_REGION_NAME = os.environ.get('AWS_SES_REGION_NAME')
AWS_SES_REGION_ENDPOINT = f'email.{AWS_SES_REGION_NAME}.amazonaws.com'
AWS_SES_FROM_EMAIL = os.environ.get('AWS_SES_FROM_EMAIL')
USE_SES_V2 = True


DOMAIN = os.environ.get('DOMAIN')
SITE_NAME = os.environ.get('SITE_NAME')
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# # Configure email backend to use Anymail with Mailjet
# EMAIL_BACKEND = "anymail.backends.mailjet.EmailBackend"

# # Set the Mailjet API Key and Secret from environment variables
# ANYMAIL = {
#     'MAILJET_API_KEY': "356d950591852c84f04646d2245dfec2",
#     'MAILJET_API_SECRET': "8220546a7b3a65c7711126af7afa9955" ,
# }

# # Set the default "from" email address
# DEFAULT_FROM_EMAIL = 'codeweavers.org@gmail.com'


WSGI_APPLICATION = 'api.wsgi.application'

# CORS WHITELIST
# CORS_ORIGIN_WHITELIST = [
#     "http://localhost:3000",
#     "http://127.0.0.1:8080"
# ]


CORS_ALLOW_ALL_ORIGINS = True
#CORS_ORIGIN_REGEX_WHITELIST = [
 #   r"^https://\w+\.netlify\.app$",
#]


# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases

# DATABASES = {
#     'default': {
#         'ENGINE': os.environ.get("SQL_ENGINE"),
#         'NAME': os.environ.get("SQL_DATABASE"),
#         'USER': os.environ.get("SQL_USER"),
#         'PASSWORD': os.environ.get("SQL_PASSWORD"),
#         'HOST': os.environ.get("SQL_HOST"),
#         'PORT': os.environ.get("SQL_PORT"),
#     }
# }

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    )
}


SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=5),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=90),
    'ROTATE_REFRESH_TOKENS': True,
    'BLACKLIST_AFTER_ROTATION': True,
    'UPDATE_LAST_LOGIN': False,

    'ALGORITHM': 'HS256',
    'VERIFYING_KEY': None,
    'AUDIENCE': None,
    'ISSUER': None,
    'JWK_URL': None,
    'LEEWAY': 0,

    'AUTH_HEADER_TYPES': ('Bearer',),
    'AUTH_HEADER_NAME': 'HTTP_AUTHORIZATION',
    'USER_ID_FIELD': 'id',
    'USER_ID_CLAIM': 'user_id',
    'USER_AUTHENTICATION_RULE': 'rest_framework_simplejwt.authentication.default_user_authentication_rule',

    'AUTH_TOKEN_CLASSES': ('rest_framework_simplejwt.tokens.AccessToken',),
    'TOKEN_TYPE_CLAIM': 'token_type',

    'JTI_CLAIM': 'jti',

    'SLIDING_TOKEN_REFRESH_EXP_CLAIM': 'refresh_exp',
    'SLIDING_TOKEN_LIFETIME': timedelta(minutes=5),
    'SLIDING_TOKEN_REFRESH_LIFETIME': timedelta(days=1),
}

# Password validation
# https://docs.djangoproject.com/en/2.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/2.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.2/howto/static-files/

STATIC_URL = '/static/'

