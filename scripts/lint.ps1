# Script PowerShell pour linter le code Python
# Usage: .\scripts\lint.ps1

Write-Host "🔍 Vérification du code..." -ForegroundColor Cyan
Write-Host "=" * 60

$errors = @()

# Black check
Write-Host "`n📝 Vérification du formatage (Black)..." -ForegroundColor Yellow
python -m black --check app/ tests/ scripts/ 2>&1 | Out-Null
if ($LASTEXITCODE -ne 0) {
    $errors += "Black"
    Write-Host "❌ Erreurs de formatage détectées" -ForegroundColor Red
    python -m black --check app/ tests/ scripts/
} else {
    Write-Host "✅ Formatage OK" -ForegroundColor Green
}

# isort check
Write-Host "`n📦 Vérification du tri des imports (isort)..." -ForegroundColor Yellow
python -m isort --check-only app/ tests/ scripts/ 2>&1 | Out-Null
if ($LASTEXITCODE -ne 0) {
    $errors += "isort"
    Write-Host "❌ Erreurs de tri des imports détectées" -ForegroundColor Red
    python -m isort --check-only app/ tests/ scripts/
} else {
    Write-Host "✅ Tri des imports OK" -ForegroundColor Green
}

# Flake8
Write-Host "`n🔍 Vérification avec Flake8..." -ForegroundColor Yellow
python -m flake8 app/ tests/ scripts/ 2>&1 | Out-Null
if ($LASTEXITCODE -ne 0) {
    $errors += "Flake8"
    Write-Host "❌ Erreurs Flake8 détectées" -ForegroundColor Red
    python -m flake8 app/ tests/ scripts/
} else {
    Write-Host "✅ Flake8 OK" -ForegroundColor Green
}

# Pylint
Write-Host "`n🔍 Vérification avec Pylint..." -ForegroundColor Yellow
python -m pylint app/ 2>&1 | Out-Null
if ($LASTEXITCODE -ne 0) {
    $errors += "Pylint"
    Write-Host "⚠️ Avertissements Pylint détectés" -ForegroundColor Yellow
    python -m pylint app/
} else {
    Write-Host "✅ Pylint OK" -ForegroundColor Green
}

if ($errors.Count -gt 0) {
    Write-Host "`n❌ Erreurs détectées avec: $($errors -join ', ')" -ForegroundColor Red
    exit 1
} else {
    Write-Host "`n✅ Toutes les vérifications sont passées !" -ForegroundColor Green
    exit 0
}

