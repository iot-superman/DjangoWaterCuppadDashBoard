from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    # V3：所有喝水功能集中在老師熟悉的 myapp。
    path("", include("myapp.urls")),
]
