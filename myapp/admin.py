from django.contrib import admin

from .models import DrinkRecord, WaterGoal


@admin.register(DrinkRecord)
class DrinkRecordAdmin(admin.ModelAdmin):
    """V5：PostgreSQL 喝水紀錄 Viewer 的欄位、搜尋及篩選設定。"""

    list_display = (
        "id",
        "recorded_at",
        "amount_ml",
        "source",
        "device_uid",
        "note",
        "created_at",
    )
    list_filter = ("source", "recorded_at")
    search_fields = ("device_uid", "note")
    date_hierarchy = "recorded_at"
    ordering = ("-recorded_at", "-id")
    readonly_fields = ("created_at",)
    list_per_page = 50


@admin.register(WaterGoal)
class WaterGoalAdmin(admin.ModelAdmin):
    """V5：每日目標管理畫面。"""

    list_display = ("id", "daily_goal_ml", "updated_at")
    readonly_fields = ("updated_at",)


# V5：後台登入頁與瀏覽器標題改成專題名稱。
admin.site.site_header = "智慧喝水儀表板管理後台"
admin.site.site_title = "智慧喝水管理"
admin.site.index_title = "PostgreSQL 資料管理"
