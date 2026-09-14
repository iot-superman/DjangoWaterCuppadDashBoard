import os
from pathlib import Path

import dj_database_url

BASE_DIR = Path(__file__).resolve().parent.parent

# V4：Render 會自動產生 SECRET_KEY；本機未設定時才使用測試值。
SECRET_KEY = os.environ.get("SECRET_KEY", "local-demo-only-change-before-production")
DEBUG = os.environ.get("DEBUG", "False" if os.environ.get("RENDER") else "True").lower() == "true"

# Render 會自動提供 RENDER_EXTERNAL_HOSTNAME，例如 xxx.onrender.com。
ALLOWED_HOSTS = ["127.0.0.1", "localhost", "0.0.0.0"]
render_hostname = os.environ.get("RENDER_EXTERNAL_HOSTNAME")
if render_hostname:
    ALLOWED_HOSTS.append(render_hostname)
    CSRF_TRUSTED_ORIGINS = [f"https://{render_hostname}"]

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "myapp",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    # V4：讓 Gunicorn 可直接提供 collectstatic 後的靜態檔案。
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "water_dashboard_sqlite.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    }
]

WSGI_APPLICATION = "water_dashboard_sqlite.wsgi.application"

# V4：Render 有 DATABASE_URL 時使用 PostgreSQL；本機仍可使用 SQLite。
database_url = os.environ.get("DATABASE_URL")
if database_url:
    DATABASES = {
        "default": dj_database_url.config(
            default=database_url,
            conn_max_age=600,
            conn_health_checks=True,
            ssl_require=True,
        )
    }
else:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": BASE_DIR / "db.sqlite3",
        }
    }

AUTH_PASSWORD_VALIDATORS = []
LANGUAGE_CODE = "zh-hant"
TIME_ZONE = "Asia/Taipei"
USE_I18N = True
USE_TZ = True
STATIC_URL = "static/"
STATIC_ROOT = BASE_DIR / "staticfiles"
STORAGES = {
    "default": {"BACKEND": "django.core.files.storage.FileSystemStorage"},
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage"
    },
}
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# Raspberry Pi 呼叫公網 API 時要帶 X-API-Key；Render 會自動產生此值。
MQTT_API_KEY = os.environ.get("MQTT_API_KEY", "")

# Render 的 Proxy 已終止 HTTPS，告訴 Django 原始連線是 HTTPS。
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
SESSION_COOKIE_SECURE = bool(os.environ.get("RENDER"))
CSRF_COOKIE_SECURE = bool(os.environ.get("RENDER"))
SECURE_SSL_REDIRECT = bool(os.environ.get("RENDER"))
SECURE_HSTS_SECONDS = 31536000 if os.environ.get("RENDER") else 0
SECURE_HSTS_INCLUDE_SUBDOMAINS = bool(os.environ.get("RENDER"))
SECURE_HSTS_PRELOAD = bool(os.environ.get("RENDER"))
