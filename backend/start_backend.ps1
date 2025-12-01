# Script pour démarrer le backend avec logs visibles
Write-Host "🚀 Démarrage du backend RAG Photographie..." -ForegroundColor Cyan
Write-Host ""

# Activer l'environnement virtuel
Write-Host "Activation de l'environnement virtuel..." -ForegroundColor Yellow
& "..\venv\Scripts\Activate.ps1"

# Vérifier que l'environnement est activé
if ($env:VIRTUAL_ENV) {
    Write-Host "✅ Environnement virtuel activé: $env:VIRTUAL_ENV" -ForegroundColor Green
} else {
    Write-Host "❌ Erreur: Environnement virtuel non activé" -ForegroundColor Red
    exit 1
}

# Vérifier le fichier .env
if (-not (Test-Path ".env")) {
    Write-Host "⚠️  Fichier .env non trouvé, création depuis ENV_TEMPLATE.txt..." -ForegroundColor Yellow
    Copy-Item "ENV_TEMPLATE.txt" ".env"
    Write-Host "✅ Fichier .env créé" -ForegroundColor Green
}

# Démarrer le serveur
Write-Host ""
Write-Host "Démarrage du serveur sur http://localhost:8001..." -ForegroundColor Cyan
Write-Host ""
Write-Host "Appuyez sur Ctrl+C pour arrêter le serveur" -ForegroundColor Yellow
Write-Host ""

python run_api.py

