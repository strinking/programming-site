import os
import sys
from pathlib import Path

import environ
from django.contrib.messages import constants as message_constants

from website.converters import markdownify
from .discord import *  # noqa

env = environ.Env(DEBUG=(bool, False))

DEBUG = env('DEBUG')
BASE_DIR = Path(".").resolve()
PROJECT_DIR = BASE_DIR / "website"
IS_TESTING = ' '.join(sys.argv).endswith(("test", "test --keepdb")) or sys.argv[1] == 'test'


# Application definition

INSTALLED_APPS = [
    "home.apps.HomeConfig",
    "guides.apps.GuidesConfig",
    "oauth.apps.OauthConfig",
    "profiles.apps.ProfilesConfig",
    "stats.apps.StatsConfig",

    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.humanize",
    "django.contrib.sessions",
    "django.contrib.sites",  # required by django-allauth
    "django.contrib.messages",
    "django.contrib.staticfiles",

    "allauth",
    "allauth.account",
    "allauth.socialaccount",
    "guardian",
    "widget_tweaks",
]

AUTHENTICATION_BACKENDS = (
    "django.contrib.auth.backends.ModelBackend",
    "allauth.account.auth_backends.AuthenticationBackend",
    "guardian.backends.ObjectPermissionBackend"
)

SOCIALACCOUNT_EMAIL_VERIFICATION = "none"

LOGIN_REDIRECT_URL = "/"

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "website.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [PROJECT_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ]
        }
    }
]

WSGI_APPLICATION = "website.wsgi.application"

# Database
# https://docs.djangoproject.com/en/2.0/ref/settings/#databases

DATABASES = {
    "default": env.db('SQLITE_URL', default=f'sqlite:///{BASE_DIR / "db.sqlite3"}'),
    "stats": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.environ["PGSQL_DBNAME"]
        if not IS_TESTING
        else os.environ.get("PGSQL_DBNAME"),
        "HOST": os.environ["PGSQL_HOST"]
        if not IS_TESTING
        else os.environ["PGSQL_TEST_HOST"],
        "USER": os.environ["PGSQL_USER"]
        if not IS_TESTING
        else os.environ["PGSQL_TEST_USER"],
        "PASSWORD": os.environ["PGSQL_PASSWORD"]
        if not IS_TESTING
        else os.environ["PGSQL_TEST_PASSWORD"],
        "CONN_MAX_AGE": 60 * 30,
        "TEST": {"NAME": os.getenv("PGSQL_TEST_DBNAME")},
    },
}

if not (IS_TESTING or bool(os.getenv("PGSQL_NO_SSL"))):
    DATABASES["stats"]["OPTIONS"] = {"sslmode": "require"}


# Password validation
# https://docs.djangoproject.com/en/2.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"
    },
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]


LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'console': {
            'level': 'DEBUG' if DEBUG else 'WARNING',
            'class': 'logging.StreamHandler'
        },
        'file': {
            'level': 'WARNING',
            'filters': ['require_debug_false'],
            'class': 'logging.FileHandler',
            'filename': env('LOGGING_FILE', default=str(BASE_DIR / 'info.log'))
        }
    },
    'loggers': {
        'django': {
            'handlers': ['console', 'file'],
            'level': 'DEBUG' if DEBUG else 'WARNING',
            'propagate': True
        }
    }
}


# Internationalization
# https://docs.djangoproject.com/en/2.0/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.0/howto/static-files/

STATIC_URL = "/static/"
STATICFILES_DIRS = [PROJECT_DIR / "static"]
SITE_ID = 1


MARKUP_FIELD_TYPES = [("markdown", markdownify)]


# https://imperavi.com/kube/docs/messages/
MESSAGE_TAGS = {
    message_constants.DEBUG: "",
    message_constants.INFO: "",
    message_constants.SUCCESS: "success",
    message_constants.ERROR: "error",
    message_constants.WARNING: "warning",
}

# TEST_RUNNER = 'website.runners.ManagedModelTestRunner'
DATABASE_ROUTERS = ["website.routers.StatbotRouter"]

ANONYMOUS_USER_NAME = 'Guest'


# When multiple Discord users with the same username sign up,
# Django will mangle the username to something like `person24`.
# Displaying the first name will show the actual username as
# returned by Discord's OAuth endpoint.
def ACCOUNT_USER_DISPLAY(user):
    return user.first_name
