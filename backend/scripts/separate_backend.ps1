# Script PowerShell pour séparer le backend
# Usage: .\scripts\separate_backend.ps1

Write-Host "🔀 Séparation du Backend..." -ForegroundColor Cyan
Write-Host "=" * 60

$backendRepo = Read-Host "URL du nouveau repository backend (ex: https://github.com/sSir-maker/RAG_photographie_backend.git)"

if ([string]::IsNullOrWhiteSpace($backendRepo)) {
    Write-Host "❌ URL du repository requise" -ForegroundColor Red
    exit 1
}

# Vérifier qu'on est dans le bon répertoire
if (-not (Test-Path "app")) {
    Write-Host "❌ Ce script doit être exécuté depuis la racine du projet" -ForegroundColor Red
    exit 1
}

# Créer un dossier temporaire
$tempDir = "..\RAG-Backend-Temp"
if (Test-Path $tempDir) {
    Remove-Item -Recurse -Force $tempDir
}
New-Item -ItemType Directory -Path $tempDir | Out-Null

Write-Host "`n📦 Copie des fichiers backend..." -ForegroundColor Yellow

# Copier les fichiers backend
$backendFiles = @(
    "app",
    "mlops",
    "tests",
    "scripts",
    "data",
    "storage",
    "alembic",
    "docker-compose.yml",
    "docker-compose.prod.yml",
    "docker-compose.monitoring.yml",
    "Dockerfile",
    "requirements.txt",
    "requirements-dev.txt",
    "requirements-test.txt",
    "requirements-optional.txt",
    ".gitignore",
    ".flake8",
    ".pylintrc",
    "pyproject.toml",
    "pytest.ini",
    "alembic.ini",
    "run_api.py",
    "run_example.py",
    "run_tests.py",
    "run_coverage.py",
    "test_installation.py",
    "test_streaming.py",
    "nginx-load-balancer.conf",
    "nginx.conf",
    "Makefile",
    "Makefile.windows"
)

# Copier les fichiers
foreach ($file in $backendFiles) {
    if (Test-Path $file) {
        Copy-Item -Path $file -Destination $tempDir -Recurse -Force
        Write-Host "  ✅ $file" -ForegroundColor Green
    }
}

# Copier les fichiers de documentation backend
$backendDocs = @(
    "README.md",
    "CREATE_ENV.md",
    "AUTH_SETUP.md",
    "DATABASE_SETUP.md",
    "POSTGRESQL_SETUP.md",
    "POSTGRESQL_QUICKSTART.md",
    "SECURITY_*.md",
    "ALERTING_SETUP.md",
    "METRICS_SETUP.md",
    "HEALTH_DASHBOARD_SETUP.md",
    "EXPORT_FEATURES.md",
    "SEARCH_FEATURES.md",
    "SHARING_FEATURES.md",
    "MULTI_LLM_SETUP.md",
    "PHOENIX_SETUP.md",
    "REDIS_SETUP.md",
    "TESTING_GUIDE.md",
    "MLOPS_GUIDE.md",
    "DEPLOYMENT_GUIDE.md",
    "DEPLOYMENT_QUICKSTART.md",
    "QUICK_DEPLOY.md",
    "WINDOWS_SCRIPTS.md"
)

foreach ($doc in $backendDocs) {
    $files = Get-ChildItem -Path . -Filter $doc -ErrorAction SilentlyContinue
    foreach ($file in $files) {
        Copy-Item -Path $file.FullName -Destination $tempDir -Force
        Write-Host "  ✅ $($file.Name)" -ForegroundColor Green
    }
}

# Créer un README backend spécifique
$backendReadme = @"
# 🎯 RAG Photographie - Backend

API FastAPI pour le système RAG de photographie.

## 🚀 Installation

\`\`\`powershell
# Créer l'environnement virtuel
py -3.12 -m venv venv
.\venv\Scripts\Activate.ps1

# Installer les dépendances
pip install -r requirements.txt
\`\`\`

## 📝 Configuration

Voir \`CREATE_ENV.md\` pour configurer le fichier \`.env\`.

## 🏃 Démarrer l'API

\`\`\`powershell
python run_api.py
\`\`\`

Ou avec uvicorn :

\`\`\`powershell
uvicorn app.api:app --host 0.0.0.0 --port 8001 --reload
\`\`\`

## 🐳 Docker

\`\`\`powershell
docker-compose up -d
\`\`\`

## 📚 Documentation

- \`DEPLOYMENT_GUIDE.md\` - Guide de déploiement
- \`AUTH_SETUP.md\` - Configuration authentification
- \`DATABASE_SETUP.md\` - Configuration base de données
- \`TESTING_GUIDE.md\` - Guide des tests

## 🔗 Frontend

Le frontend est dans un repository séparé :
\`https://github.com/sSir-maker/RAG_photographie_frontend\`

---

**Backend RAG Photographie** - API FastAPI avec pipeline MLOps complet
"@

$backendReadme | Out-File -FilePath "$tempDir\README.md" -Encoding UTF8

# Initialiser Git dans le dossier temporaire
Write-Host "`n📦 Initialisation Git..." -ForegroundColor Yellow
Set-Location $tempDir
git init
git add .
git commit -m "Initial commit: Backend RAG Photographie"

# Ajouter le remote
Write-Host "`n🔗 Configuration du remote..." -ForegroundColor Yellow
git remote add origin $backendRepo

Write-Host "`n✅ Backend séparé avec succès !" -ForegroundColor Green
Write-Host "`n📝 Prochaines étapes :" -ForegroundColor Cyan
Write-Host "  1. Vérifier les fichiers dans : $tempDir"
Write-Host "  2. Pousser vers le nouveau repo :"
Write-Host "     cd $tempDir"
Write-Host "     git push -u origin main"

Set-Location ..
