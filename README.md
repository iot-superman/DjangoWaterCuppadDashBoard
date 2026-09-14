# 智慧喝水儀表板 V4（Render 自動部署版）

GitHub 目標：<https://github.com/iot-superman/DjangoWaterCuppadDashBoard.git>

這一版在 Render 只啟動 Django 智慧喝水儀表板，不會在 Render 啟動
`mqtt_subscriber`。Render 會建立以下兩個資源：

1. Free Web Service：顯示智慧喝水儀表板。
2. Free PostgreSQL：儲存喝水紀錄。

> 重要：Render 免費 PostgreSQL 建立後 30 天到期；免費 Web Service 的本機檔案
> 會在重新部署、重新啟動或休眠後消失，因此正式資料不能使用 Render 上的 SQLite。

## 系統架構

```text
瀏覽器
   │ HTTPS
   ▼
Render Django Web Service ──────► Render PostgreSQL
   ▲
   │ POST /api/drinks/mqtt/
   │ Header: X-API-Key
Raspberry Pi（未來可選）
   ▲
   │ MQTT
MQTT Broker／智慧水杯墊
```

## 主要檔案

```text
water_dashboard_render_v4/
├── manage.py
├── requirements.txt
├── build.sh                         Render 建置指令
├── render.yaml                      一鍵建立 Web＋PostgreSQL
├── PUSH_TO_GITHUB.ps1               Windows 推送 GitHub 輔助程式
├── water_dashboard_sqlite/          Django Project
├── myapp/                           Django App
│   ├── models.py                    PostgreSQL 資料表結構
│   ├── views.py
│   ├── urls.py
│   └── migrations/
└── templates/myapp/dashboard.html   Bootstrap＋Chart.js 儀表板
```

## 第一步：解壓縮

建議解壓縮成：

```text
C:\dvds\water_dashboard_render_v4
```

確認該資料夾打開後，可以直接看到 `manage.py`、`render.yaml` 和
`requirements.txt`，不可再多包一層資料夾。

## 第二步：推送到 GitHub

### 方法 A：PowerShell 一鍵推送

在資料夾空白處按住 Shift，再按滑鼠右鍵，選擇「在這裡開啟 PowerShell
視窗」，執行：

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\PUSH_TO_GITHUB.ps1
```

第一次使用 GitHub 會要求登入瀏覽器或 Git Credential Manager。登入自己的
`iot-superman` 帳號後完成授權。腳本不會儲存 GitHub 密碼。

### 方法 B：自己逐行輸入

```powershell
cd C:\dvds\water_dashboard_render_v4
git init
git add .
git commit -m "Deploy smart water dashboard to Render"
git branch -M main
git remote add origin https://github.com/iot-superman/DjangoWaterCuppadDashBoard.git
git push -u origin main
```

如果顯示 `remote origin already exists`，改執行：

```powershell
git remote set-url origin https://github.com/iot-superman/DjangoWaterCuppadDashBoard.git
git push -u origin main
```

如果 GitHub Repository 原本不是空的，而且出現 `non-fast-forward`，先不要使用
`--force`，避免覆蓋舊程式。先在 GitHub 下載或備份原有內容，再決定合併方式。

## 第三步：Render 連接 GitHub

1. 開啟 <https://dashboard.render.com/> 並登入。
2. 第一次使用時，選擇連接 GitHub，授權 Render 讀取 Repository。
3. Render 左上角選擇 **New +**。
4. 選擇 **Blueprint**。
5. 找到 `iot-superman/DjangoWaterCuppadDashBoard`，按 **Connect**。
6. Blueprint Path 保持 `render.yaml`。
7. Blueprint 名稱可填 `django-water-cuppad-dashboard`。
8. 檢查畫面會建立一個 Web Service 及一個 PostgreSQL。
9. 按 **Deploy Blueprint** 或 **Apply**。
10. 等待 Web Service 顯示 **Live**。

不必進入 Render Shell，也不必在 Render 手動輸入 `migrate`；`build.sh` 每次部署
會自動執行 `collectstatic` 與 `migrate`。

## 第四步：開啟智慧喝水儀表板

進入 Render 的 `django-water-cuppad-dashboard` Web Service，按上方網址，例如：

```text
https://django-water-cuppad-dashboard.onrender.com/
```

實際網址若因名稱重複被 Render 加上亂數，請以 Render 顯示的網址為準。

免費 Web Service 如果 15 分鐘沒有流量會休眠；下一次開啟可能需要約一分鐘喚醒。

## 第五步：測試新增紀錄

在儀表板的手動新增區輸入喝水量、喝水時間與備註，按新增。重新整理後仍能看到
紀錄，代表 Django 已連到 PostgreSQL。

## GitHub 更新後自動部署

日後修改程式後執行：

```powershell
cd C:\dvds\water_dashboard_render_v4
git add .
git commit -m "Update water dashboard"
git push
```

`render.yaml` 已設定 `autoDeployTrigger: commit`。GitHub 的 `main` 分支收到新的
Commit 後，Render 會重新建置並自動部署，不需要 CMD 或 Render Shell。

## Raspberry Pi 未來傳送喝水紀錄

Render 會產生 `MQTT_API_KEY`。到 Web Service 的 **Environment** 頁面查看或重新
設定一個自己知道的值。Raspberry Pi 呼叫方式：

```powershell
$headers = @{ "X-API-Key" = "請換成Render的MQTT_API_KEY" }
$body = @{
    uid = "311"
    amount_ml = 250
    timestamp = "2026-09-14T10:30:00+08:00"
} | ConvertTo-Json

Invoke-RestMethod `
    -Uri "https://你的服務名稱.onrender.com/api/drinks/mqtt/" `
    -Method Post `
    -Headers $headers `
    -ContentType "application/json" `
    -Body $body
```

成功回應範例：

```json
{
  "ok": true,
  "id": 1,
  "amount_ml": 250
}
```

## 官方參考資料

- Render 部署 Django：<https://render.com/docs/deploy-django>
- Render Blueprint：<https://render.com/docs/infrastructure-as-code>
- Render Blueprint YAML：<https://render.com/docs/blueprint-spec>
- Render 免費方案限制：<https://render.com/docs/free>
- Render 自動部署：<https://render.com/docs/deploys>
- Django 部署檢查表：<https://docs.djangoproject.com/en/6.0/howto/deployment/checklist/>
