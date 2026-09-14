"""依 Render 環境變數建立或更新 Django 管理員。"""

import os

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Create or update the Django admin account from environment variables."

    def handle(self, *args, **options):
        username = os.environ.get("DJANGO_SUPERUSER_USERNAME", "").strip()
        email = os.environ.get("DJANGO_SUPERUSER_EMAIL", "").strip()
        password = os.environ.get("DJANGO_SUPERUSER_PASSWORD", "")

        # 未設定密碼時略過，讓服務仍可正常啟動，且不使用任何預設密碼。
        if not username or not email or not password:
            self.stdout.write(
                self.style.WARNING(
                    "Admin account skipped: set DJANGO_SUPERUSER_USERNAME, "
                    "DJANGO_SUPERUSER_EMAIL and DJANGO_SUPERUSER_PASSWORD."
                )
            )
            return

        user_model = get_user_model()
        user, created = user_model.objects.get_or_create(
            username=username,
            defaults={"email": email},
        )

        # 每次部署都同步權限與密碼；修改 Render 密碼後重新部署即可生效。
        user.email = email
        user.is_staff = True
        user.is_superuser = True
        user.is_active = True
        user.set_password(password)
        user.save()

        action = "created" if created else "updated"
        self.stdout.write(self.style.SUCCESS(f"Admin account {action}: {username}"))
