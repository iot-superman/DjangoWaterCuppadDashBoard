# Render dashboard GitHub push helper.
# ASCII-only text is intentional for Windows PowerShell 5.1 compatibility.

$ErrorActionPreference = "Stop"
$ProjectDirectory = $PSScriptRoot
$RepositoryUrl = "https://github.com/iot-superman/DjangoWaterCuppadDashBoard.git"

Set-Location $ProjectDirectory

if (-not (Get-Command git -ErrorAction SilentlyContinue)) {
    Write-Host "Git was not found." -ForegroundColor Red
    Write-Host "Install Git for Windows: https://git-scm.com/download/win"
    Read-Host "Press Enter to exit"
    exit 1
}

if (-not (Test-Path ".git")) {
    git init
    if ($LASTEXITCODE -ne 0) {
        Read-Host "git init failed. Press Enter to exit"
        exit 1
    }
}

git add .
if ($LASTEXITCODE -ne 0) {
    Read-Host "git add failed. Press Enter to exit"
    exit 1
}

# Run the HEAD probe through cmd.exe so an empty new repository does not
# become a PowerShell NativeCommandError before the first commit exists.
cmd.exe /d /c "git rev-parse --verify HEAD >nul 2>nul"
$HasCommit = ($LASTEXITCODE -eq 0)
$Changes = git status --porcelain

if (-not $HasCommit) {
    git commit -m "Deploy smart water dashboard to Render"
    if ($LASTEXITCODE -ne 0) {
        Write-Host "Commit failed. Configure your Git name and email first:" -ForegroundColor Red
        Write-Host 'git config --global user.name "Your Name"'
        Write-Host 'git config --global user.email "your-email@example.com"'
        Read-Host "Press Enter to exit"
        exit 1
    }
}
elseif ($Changes) {
    git commit -m "Update Render smart water dashboard"
    if ($LASTEXITCODE -ne 0) {
        Read-Host "git commit failed. Press Enter to exit"
        exit 1
    }
}
else {
    Write-Host "No new changes to commit." -ForegroundColor Yellow
}

git branch -M main
if ($LASTEXITCODE -ne 0) {
    Read-Host "git branch failed. Press Enter to exit"
    exit 1
}

git remote get-url origin *> $null
if ($LASTEXITCODE -eq 0) {
    git remote set-url origin $RepositoryUrl
}
else {
    git remote add origin $RepositoryUrl
}

if ($LASTEXITCODE -ne 0) {
    Read-Host "Git remote setup failed. Press Enter to exit"
    exit 1
}

Write-Host "Pushing to GitHub..." -ForegroundColor Cyan
git push -u origin main

if ($LASTEXITCODE -ne 0) {
    Write-Host "Push failed. Do not use --force." -ForegroundColor Red
    Write-Host "Keep the error above and send a screenshot for diagnosis."
    Read-Host "Press Enter to exit"
    exit 1
}

Write-Host "Push completed successfully." -ForegroundColor Green
Write-Host "Check: https://github.com/iot-superman/DjangoWaterCuppadDashBoard"
Read-Host "Press Enter to exit"
