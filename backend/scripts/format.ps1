# Script PowerShell pour formater le code Python
# Usage: .\scripts\format.ps1

Write-Host "🎨 Formatage du code..." -ForegroundColor Cyan
Write-Host "=" * 60

# Black
Write-Host "`n📝 Formatage avec Black..." -ForegroundColor Yellow
python -m black app/ tests/ scripts/

if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Erreur lors du formatage avec Black" -ForegroundColor Red
    exit 1
}

# isort
Write-Host "`n📦 Tri des imports avec isort..." -ForegroundColor Yellow
python -m isort app/ tests/ scripts/

if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Erreur lors du tri des imports" -ForegroundColor Red
    exit 1
}

Write-Host "`n✅ Formatage terminé avec succès !" -ForegroundColor Green

