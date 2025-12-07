# Script de déploiement pour production
# Usage: .\deploy.ps1

Write-Host "🚀 Déploiement en production..." -ForegroundColor Cyan
Write-Host "=" * 60

# Vérifier que Docker est disponible
if (-not (Get-Command docker -ErrorAction SilentlyContinue)) {
    Write-Host "❌ Docker n'est pas installé ou n'est pas dans le PATH" -ForegroundColor Red
    exit 1
}

# Vérifier que docker-compose est disponible
if (-not (Get-Command docker-compose -ErrorAction SilentlyContinue)) {
    Write-Host "❌ docker-compose n'est pas installé" -ForegroundColor Red
    exit 1
}

# Vérifier que .env existe
if (-not (Test-Path .env)) {
    Write-Host "❌ Le fichier .env n'existe pas" -ForegroundColor Red
    Write-Host "💡 Crée le fichier .env avec les variables nécessaires" -ForegroundColor Yellow
    exit 1
}

Write-Host "`n📦 Étape 1: Build des images Docker..." -ForegroundColor Yellow

# Build backend
Write-Host "  Building backend..." -ForegroundColor White
docker build -t rag-photographie/rag-photographie-backend:latest -f Dockerfile .

if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Erreur lors du build du backend" -ForegroundColor Red
    exit 1
}

# Build frontend
Write-Host "  Building frontend..." -ForegroundColor White
Set-Location ../frontend_RAG
docker build -t rag-photographie/rag-photographie-frontend:latest -f Dockerfile .
Set-Location ../backend

if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Erreur lors du build du frontend" -ForegroundColor Red
    exit 1
}

Write-Host "`n🗄️ Étape 2: Vérification des variables d'environnement..." -ForegroundColor Yellow

# Vérifier les variables critiques
$envContent = Get-Content .env -Raw
$requiredVars = @("SECRET_KEY", "POSTGRES_PASSWORD", "DATABASE_URL", "OLLAMA_BASE_URL")

foreach ($var in $requiredVars) {
    if ($envContent -notmatch "$var=") {
        Write-Host "  ⚠️  $var n'est pas défini dans .env" -ForegroundColor Yellow
    } else {
        Write-Host "  ✅ $var est défini" -ForegroundColor Green
    }
}

Write-Host "`n🚀 Étape 3: Démarrage des services..." -ForegroundColor Yellow

# Démarrer avec docker-compose.prod.yml
docker-compose -f docker-compose.prod.yml up -d

if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Erreur lors du démarrage des services" -ForegroundColor Red
    exit 1
}

Write-Host "`n⏳ Attente du démarrage des services..." -ForegroundColor Yellow
Start-Sleep -Seconds 10

Write-Host "`n📊 Étape 4: Vérification de l'état des services..." -ForegroundColor Yellow
docker-compose -f docker-compose.prod.yml ps

Write-Host "`n✅ Déploiement terminé !" -ForegroundColor Green
Write-Host "`n🌐 Services disponibles :" -ForegroundColor Cyan
Write-Host "  - Frontend: http://localhost" -ForegroundColor White
Write-Host "  - Backend API: http://localhost:8001" -ForegroundColor White
Write-Host "  - Phoenix Monitoring: http://localhost:6006" -ForegroundColor White
Write-Host "  - PostgreSQL: localhost:5432" -ForegroundColor White

Write-Host "`n📝 Commandes utiles :" -ForegroundColor Yellow
Write-Host "  - Voir les logs: docker-compose -f docker-compose.prod.yml logs -f" -ForegroundColor White
Write-Host "  - Arrêter: docker-compose -f docker-compose.prod.yml down" -ForegroundColor White
Write-Host "  - Redémarrer: docker-compose -f docker-compose.prod.yml restart" -ForegroundColor White

