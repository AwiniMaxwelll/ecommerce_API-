
import os
from pathlib import Path
from datetime import timedelta

import environ
import dj_database_url  

# Build paths
BASE_DIR = Path(__file__).resolve().parent.parent

# Initialize environment variables
env = environ.Env()
# environ.Env.read_env(env_file=str(BASE_DIR / ".env"))  # Safe even if .env missing
environ.Env.read_env(os.path.join(os.path.dirname(__file__), '..', '.env'))


# SECURITY & CORE SETTINGS

SECRET_KEY = env("SECRET_KEY")

DEBUG = env.bool('DEBUG', default=True) 

# ALLOWED_HOSTS = env.list("ALLOWED_HOSTS", default=["localhost", "127.0.0.1"])
# if not DEBUG:
#     ALLOWED_HOSTS += ["*"]  
# CSRF_TRUSTED_ORIGINS = env.list(
#     "CSRF_TRUSTED_ORIGINS",
#     default=["http://localhost:3000", "http://127.0.0.1:3000"],
# )
ALLOWED_HOSTS = env.list("ALLOWED_HOSTS", default=["localhost", "127.0.0.1"])
if DEBUG:
    ALLOWED_HOSTS = ["*"]  # local development
else:
    ALLOWED_HOSTS += ["*.railway.app", ".up.railway.app"]

# For CSRF with frontend on port 3000 (React, etc.)
CSRF_TRUSTED_ORIGINS = env.list(
    "CSRF_TRUSTED_ORIGINS",
    default=["http://localhost:3000", "http://127.0.0.1:3000"],
)

# APPLICATION DEFINITION

INSTALLED_APPS = [
    # Django core
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",

    # Third-party
    "rest_framework",
    "rest_framework_simplejwt",
    "drf_yasg",           # Swagger
    "django_filters",
    "corsheaders",
    "whitenoise.runserver_nostatic",  # For development static serving

    # Local apps
    "apps.users",
    "apps.products",
    "apps.orders",
]

MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",  
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "urls"
WSGI_APPLICATION = "wsgi.application"


# TEMPLATES

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]


# DATABASE – AUTO-DETECT RAILWAY POSTGRES OR MYSQL


DATABASE_URL = env("MYSQL_URL", default=None)

# if DATABASE_URL:
#     DATABASES = {
#         "default": dj_database_url.parse(
#             DATABASE_URL,
#             conn_max_age=600,
#             conn_health_checks=True,
#         )
#     }
# else:
   
DATABASES = {
            "default": {
                "ENGINE": "django.db.backends.mysql",
                "NAME": env("DB_NAME", default="railway"),
                "USER": env("DB_USER", default="root"),
                "PASSWORD": env("DB_PASSWORD", default="UxhYTMwimWUFYCCqTtIAEJQPLLrirKGK"),
                "HOST": env("DB_HOST", default="mysql.railway.internal"),
                "PORT": env("DB_PORT", default="3306"),
                "OPTIONS": {
                    "init_command": "SET sql_mode='STRICT_TRANS_TABLES'",
                    "charset": "utf8mb4",
                },
            }
    }


# AUTH & JWT
AUTH_USER_MODEL = "users.User"

REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework_simplejwt.authentication.JWTAuthentication",
        "rest_framework.authentication.SessionAuthentication",
    ),
    "DEFAULT_PERMISSION_CLASSES": (
        "rest_framework.permissions.IsAuthenticatedOrReadOnly",
    ),
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.PageNumberPagination",
    "PAGE_SIZE": 20,
    "DEFAULT_RENDERER_CLASSES": (
        "rest_framework.renderers.JSONRenderer",
        
        *(
            ("rest_framework.renderers.BrowsableAPIRenderer",)
            if DEBUG
            else ()
        ),
    ),
}

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=60),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=7),
    "ROTATE_REFRESH_TOKENS": True,
}

# CORS
CORS_ALLOWED_ORIGINS = env.list(
    "CORS_ALLOWED_ORIGINS",
    default=["http://localhost:3000", "https://ecommerceapi-production-9f80.up.railway.app"]
)
CORS_ALLOW_CREDENTIALS = True

# STATIC & MEDIA FILES
STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

# EMAIL (optional – keep for future)

EMAIL_BACKEND = env("EMAIL_BACKEND", default="django.core.mail.backends.console.EmailBackend")
EMAIL_HOST = env("EMAIL_HOST", default="")
EMAIL_PORT = env.int("EMAIL_PORT", default=587)
EMAIL_USE_TLS = env.bool("EMAIL_USE_TLS", default=True)
EMAIL_HOST_USER = env("EMAIL_HOST_USER", default="")
EMAIL_HOST_PASSWORD = env("EMAIL_HOST_PASSWORD", default="")
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER

# INTERNATIONALIZATION
LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
