import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

# ==========================================================
# SECURITY AND PRODUCTION SETTINGS
# ==========================================================

DEBUG = False  # ✅ Required for production

ALLOWED_HOSTS = ["127.0.0.1", "localhost", "your-production-domain.com"]

# ==========================================================
# APPLICATION DEFINITION
# ==========================================================

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",

    # REST framework & Token auth
    "rest_framework",
    "rest_framework.authtoken",

    # Your apps
    "accounts",
    "posts",
    "notifications",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "social_media_api.urls"

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

WSGI_APPLICATION = "social_media_api.wsgi.application"

# ==========================================================
# DATABASE CONFIGURATION
# ==========================================================
# ✅ Example for production PostgreSQL
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.getenv("DB_NAME", "social_media_db"),
        "USER": os.getenv("DB_USER", "postgres"),
        "
