import os

from django.core.asgi import get_asgi_application


# V3 補齊 Django startproject 的標準 ASGI 入口。
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "water_dashboard_sqlite.settings")

application = get_asgi_application()

