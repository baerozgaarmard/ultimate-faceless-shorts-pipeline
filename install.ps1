# Ultimate Faceless Shorts Pipeline - One-Liner Installer for Windows PowerShell
$ErrorActionPreference = "Stop"

$RepoUrl = "https://github.com/baerozgaarmard/ultimate-faceless-shorts-pipeline.git"
$CloneDir = Join-Path $HOME ".faceless-shorts-pipeline"

Write-Host "========================================================================" -ForegroundColor Cyan
Write-Host "    ULTIMATE FACELESS SHORTS PIPELINE — ONE-LINER INSTALLER" -ForegroundColor Cyan
Write-Host "========================================================================" -ForegroundColor Cyan

$PythonCmd = (Get-Command python.exe -ErrorAction SilentlyContinue).Source
if (-not $PythonCmd) {
    $PythonCmd = (Get-Command py.exe -ErrorAction SilentlyContinue).Source
}
if (-not $PythonCmd) {
    Write-Error "Python 3 is required. Please install Python 3.10+ from python.org or via 'winget install Python.Python.3.11'."
    exit 1
}

# If running inside the repo already
if ((Test-Path "install.py") -and (Test-Path "faceless-shorts")) {
    & $PythonCmd install.py $args
    exit 0
}

# Clone or pull latest
if (Test-Path "$CloneDir\.git") {
    Write-Host "Updating repository in $CloneDir..." -ForegroundColor Yellow
    git -C "$CloneDir" pull --quiet origin main
} else {
    Write-Host "Cloning repository to $CloneDir..." -ForegroundColor Yellow
    git clone --depth 1 $RepoUrl $CloneDir
}

Set-Location $CloneDir
& $PythonCmd install.py $args
