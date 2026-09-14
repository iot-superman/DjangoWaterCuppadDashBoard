#!/usr/bin/env bash
# V4 Render 建置：安裝套件由 Render 負責，此處收集靜態檔並建立／更新資料表。
set -o errexit

# Render 的 Python Build Command 必須先安裝 requirements.txt。
python -m pip install -r requirements.txt
python manage.py collectstatic --no-input
python manage.py migrate
