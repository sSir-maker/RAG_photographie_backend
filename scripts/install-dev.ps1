# Script PowerShell pour installer les outils de développement
# Usage: .\scripts\install-dev.ps1

Write-Host "📦 Installation des outils de développement..." -ForegroundColor Cyan
Write-Host "=" * 60

Write-Host "`nInstalling requirements-dev.txt..." -ForegroundColor Yellow
pip install -r requirements-dev.txt

if ($LASTEXITCODE -eq 0) {
    Write-Host "`n✅ Outils de développement installés avec succès !" -ForegroundColor Green
    Write-Host "`nOutils disponibles:" -ForegroundColor Cyan
    Write-Host "  - black (formatage)"
    Write-Host "  - isort (tri imports)"
    Write-Host "  - flake8 (linting)"
    Write-Host "  - pylint (analyse)"
    Write-Host "  - mypy (types)"
    Write-Host "  - pytest (tests)"
} else {
    Write-Host "`n❌ Erreur lors de l'installation" -ForegroundColor Red
    exit 1
}

