# Script PowerShell pour nettoyer les fichiers temporaires
# Usage: .\scripts\clean.ps1

Write-Host "🧹 Nettoyage des fichiers temporaires..." -ForegroundColor Cyan
Write-Host "=" * 60

# Supprimer __pycache__
Write-Host "`nSuppression des __pycache__..." -ForegroundColor Yellow
Get-ChildItem -Path . -Include __pycache__ -Recurse -Force | Remove-Item -Recurse -Force -ErrorAction SilentlyContinue

# Supprimer .pyc
Write-Host "Suppression des .pyc..." -ForegroundColor Yellow
Get-ChildItem -Path . -Include *.pyc -Recurse -Force | Remove-Item -Force -ErrorAction SilentlyContinue

# Supprimer .pyo
Write-Host "Suppression des .pyo..." -ForegroundColor Yellow
Get-ChildItem -Path . -Include *.pyo -Recurse -Force | Remove-Item -Force -ErrorAction SilentlyContinue

# Supprimer .egg-info
Write-Host "Suppression des .egg-info..." -ForegroundColor Yellow
Get-ChildItem -Path . -Include *.egg-info -Recurse -Force | Remove-Item -Recurse -Force -ErrorAction SilentlyContinue

# Supprimer .pytest_cache
Write-Host "Suppression des .pytest_cache..." -ForegroundColor Yellow
Get-ChildItem -Path . -Include .pytest_cache -Recurse -Force | Remove-Item -Recurse -Force -ErrorAction SilentlyContinue

# Supprimer htmlcov
if (Test-Path "htmlcov") {
    Write-Host "Suppression de htmlcov..." -ForegroundColor Yellow
    Remove-Item -Path "htmlcov" -Recurse -Force -ErrorAction SilentlyContinue
}

# Supprimer .coverage
if (Test-Path ".coverage") {
    Write-Host "Suppression de .coverage..." -ForegroundColor Yellow
    Remove-Item -Path ".coverage" -Force -ErrorAction SilentlyContinue
}

# Supprimer coverage.xml
if (Test-Path "coverage.xml") {
    Write-Host "Suppression de coverage.xml..." -ForegroundColor Yellow
    Remove-Item -Path "coverage.xml" -Force -ErrorAction SilentlyContinue
}

Write-Host "`n✅ Nettoyage terminé !" -ForegroundColor Green

