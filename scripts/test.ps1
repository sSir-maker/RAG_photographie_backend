# Script PowerShell pour exécuter les tests
# Usage: .\scripts\test.ps1

Write-Host "🧪 Exécution des tests..." -ForegroundColor Cyan
Write-Host "=" * 60

python -m pytest tests/ -v --cov=app --cov-report=html --cov-report=term-missing

if ($LASTEXITCODE -eq 0) {
    Write-Host "`n✅ Tous les tests sont passés !" -ForegroundColor Green
    Write-Host "📄 Rapport de couverture: htmlcov/index.html" -ForegroundColor Cyan
} else {
    Write-Host "`n❌ Certains tests ont échoué." -ForegroundColor Red
    exit 1
}

