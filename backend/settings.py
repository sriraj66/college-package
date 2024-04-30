

from pathlib import Path
import os
from dotenv import  load_dotenv
import yaml
load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent



SECRET_KEY = os.getenv('SECREAT_KEY')

with open("config.yml",'r') as config_file:
    config = yaml.safe_load(config_file)
    config_file.close()

DEBUG = config['debug']

del config

ALLOWED_HOSTS = ['*']



INSTALLED_APPS = [
    # Theme
    'jazzmin',
    # 'adminlte3',
    'import_export',
    
    
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # local apps
    'core',
    'rest_framework',
    'storages',
    'corsheaders',
    'smcg',
    'ATS',
    'CG',
    'CP',
    'utils',
    'authentication',
    'feed360',

]
IMPORT_EXPORT_USE_TRANSACTIONS = True
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'corsheaders.middleware.CorsMiddleware',
]

ROOT_URLCONF = 'backend.urls'

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
            ],
        },
    },
]

WSGI_APPLICATION = 'backend.wsgi.application'

if DEBUG is True:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': os.getenv('DB_NAME'),
            'USER': os.getenv('DB_USER'),
            'PASSWORD': os.getenv('DB_PASS'),
            'HOST': os.getenv('DB_HOST'),
            'PORT': os.getenv("DB_PORT"),
        }
    }



if DEBUG is False:
    AUTH_PASSWORD_VALIDATORS = [
        
        {
            'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
        },
        {
            'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
        },
]
else:
    AUTH_PASSWORD_VALIDATORS = []



LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Asia/Kolkata'

USE_I18N = True

USE_L10N = True

USE_TZ = True


STATIC_URL = '/static/'
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
STATIC_ROOT = os.path.join(BASE_DIR, 'static')

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

CORS_ORIGIN_ALLOW_ALL = True

LOGIN_URL = 'login'
LOGOUT_REDIRECT_URL = 'logout'
LOGIN_REDIRECT_URL = 'index'

AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
AWS_STORAGE_BUCKET_NAME = os.getenv("BUCKET_NAME")
AWS_S3_SIGNATURE_NAME = 's3v4',
AWS_S3_REGION_NAME = 'us-east-2'
AWS_S3_FILE_OVERWRITE = False
AWS_DEFAULT_ACL =  None
AWS_S3_VERITY = True
AWS_QUERYSTRING_AUTH = False
DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
STATICFILES_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'

# Email

# settings.py

# Email Configuration
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_FILE_PATH = BASE_DIR / "sent_emails"
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587  
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'neuraa194@gmail.com'
EMAIL_HOST_PASSWORD = 'idkiarlzzzbvyitq' 


if DEBUG is False:
    SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
    # CSRF_TRUSTED_ORIGINS = os.environ.get("CSRF_TRUSTED_ORIGINS").split(" ")

# template theme

JAZZMIN_SETTINGS = {
    "site_title": "Neuraa Admin",
    "site_header": "Neuraa",
    "site_brand": "Neuraa Admin",
    "welcome_sign": "Welcome to the Neuraa Admin panel",
    "copyright": "Team Neuraa",
    "usermenu_links": [
        {"name":"View App","url":'index'},
        {"name":"Logout","url":'logout_get'},
        
    ],
    "topmenu_links": [

        {"name": "Home",  "url": "admin:index", "permissions": ["auth.view_user"]},

        {"name": "Support", "url": "https://github.com/farridav/django-jazzmin/issues", "new_window": True},

        {"model": "auth.User"},

        {"app": "utils"},
        
    ],
    "icons": {
        "auth": "fas fa-users-cog",
        "auth.user": "fas fa-user",
        "auth.Group": "fas fa-users",
    },
    "show_sidebar": True,
    "use_google_fonts_cdn": True,
    "changeform_format": "horizontal_tabs",
    "changeform_format_overrides": {
                                "auth": "collapsible",
                                "core": "vertical_tabs"
                                },
    "navigation_expanded": True,
    "related_modal_active": False,
    "search_model": ["auth.User",'utils.Students','utils.Staffs'],

}
JAZZMIN_SETTINGS["show_ui_builder"] = True