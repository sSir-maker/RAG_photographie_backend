# Script PowerShell pour séparer le projet en deux repositories
# Backend et Frontend

Write-Host "🔀 Séparation du projet en Backend et Frontend..." -ForegroundColor Cyan
Write-Host "=" * 60

$projectRoot = Get-Location
$backendDir = Join-Path $projectRoot ".." "RAG-Photographie-Backend"
$frontendDir = Join-Path $projectRoot ".." "RAG-Photographie-Frontend"

# Créer les dossiers
Write-Host "`n📁 Création des dossiers..." -ForegroundColor Yellow
New-Item -ItemType Directory -Force -Path $backendDir | Out-Null
New-Item -ItemType Directory -Force -Path $frontendDir | Out-Null

# ========== BACKEND ==========
Write-Host "`n🔧 Copie des fichiers Backend..." -ForegroundColor Yellow

# Fichiers backend
$backendFiles = @(
    "app",
    "mlops",
    "tests",
    "alembic",
    "alembic.ini",
    "requirements.txt",
    "requirements-dev.txt",
    "requirements-test.txt",
    "requirements-optional.txt",
    "Dockerfile",
    "docker-compose.yml",
    "docker-compose.prod.yml",
    "docker-compose.monitoring.yml",
    "run_api.py",
    "run_example.py",
    "run_tests.py",
    "run_coverage.py",
    "test_installation.py",
    "test_streaming.py",
    "pytest.ini",
    "pyproject.toml",
    ".flake8",
    ".pylintrc",
    ".gitignore",
    "scripts",
    "data",
    "storage",
    "nginx.conf",
    "nginx-load-balancer.conf"
)

# Documentation backend
$backendDocs = @(
    "README.md",
    "PROJECT_STATUS.md",
    "CREATE_ENV.md",
    "AUTH_SETUP.md",
    "DATABASE_SETUP.md",
    "POSTGRESQL_SETUP.md",
    "POSTGRESQL_QUICKSTART.md",
    "SETUP_PYTHON.md",
    "SETUP_OLLAMA.md",
    "START_API.md",
    "TESTING_GUIDE.md",
    "TESTS_SUMMARY.md",
    "ALERTING_SETUP.md",
    "METRICS_SETUP.md",
    "HEALTH_DASHBOARD_SETUP.md",
    "MONITORING_COMPLETE.md",
    "PHOENIX_SETUP.md",
    "PHOENIX_FIXED.md",
    "PHOENIX_INSTALL_FIX.md",
    "START_PHOENIX.md",
    "EXPORT_FEATURES.md",
    "SEARCH_FEATURES.md",
    "SHARING_FEATURES.md",
    "MULTI_LLM_SETUP.md",
    "SECURITY_IMPLEMENTATION.md",
    "SECURITY_CHECKLIST.md",
    "SECURITY_COMPLETE.md",
    "SECURITY_SUMMARY.md",
    "REDIS_SETUP.md",
    "PERFORMANCE_SETUP.md",
    "PERFORMANCE_COMPLETE.md",
    "LOAD_BALANCING_SETUP.md",
    "CDN_SETUP.md",
    "CI_CD_SETUP.md",
    "CI_CD_COMPLETE.md",
    "QUICK_START_CI_CD.md",
    "LINTING_SETUP.md",
    "COVERAGE_IMPROVEMENT.md",
    "DEPLOYMENT_GUIDE.md",
    "DEPLOYMENT_CHECKLIST.md",
    "DEPLOYMENT_QUICKSTART.md",
    "DEPLOYMENT_AUTOMATION.md",
    "QUICK_DEPLOY.md",
    "SSL_SETUP.md",
    "MLOPS_GUIDE.md",
    "STACK_OVERVIEW.md",
    "WINDOWS_SCRIPTS.md",
    "Makefile",
    "Makefile.windows"
)

foreach ($file in $backendFiles) {
    $source = Join-Path $projectRoot $file
    $dest = Join-Path $backendDir $file
    if (Test-Path $source) {
        Copy-Item -Path $source -Destination $dest -Recurse -Force
        Write-Host "  ✅ $file" -ForegroundColor Green
    }
}

foreach ($file in $backendDocs) {
    $source = Join-Path $projectRoot $file
    $dest = Join-Path $backendDir $file
    if (Test-Path $source) {
        Copy-Item -Path $source -Destination $dest -Force
        Write-Host "  ✅ $file" -ForegroundColor Green
    }
}

# ========== FRONTEND ==========
Write-Host "`n🎨 Copie des fichiers Frontend..." -ForegroundColor Yellow

# Copier le dossier frontend_RAG
$frontendSource = Join-Path $projectRoot "frontend_RAG"
$frontendDest = $frontendDir
if (Test-Path $frontendSource) {
    Copy-Item -Path $frontendSource -Destination $frontendDest -Recurse -Force
    Write-Host "  ✅ frontend_RAG/" -ForegroundColor Green
}

# Documentation frontend
$frontendDocs = @(
    "README_FRONTEND.md"
)

foreach ($file in $frontendDocs) {
    $source = Join-Path $projectRoot $file
    $dest = Join-Path $frontendDir $file
    if (Test-Path $source) {
        Copy-Item -Path $source -Destination $dest -Force
        Write-Host "  ✅ $file" -ForegroundColor Green
    }
}

# Créer .gitignore pour frontend
$frontendGitignore = @"
# Dependencies
node_modules/
.pnp
.pnp.js

# Testing
coverage/

# Production
build/
dist/
out/

# Misc
.DS_Store
*.pem

# Debug
npm-debug.log*
yarn-debug.log*
yarn-error.log*

# Local env files
.env.local
.env.development.local
.env.test.local
.env.production.local

# Vercel
.vercel

# Typescript
*.tsbuildinfo
next-env.d.ts

# IDE
.vscode/
.idea/
*.swp
*.swo
*~
"@

Set-Content -Path (Join-Path $frontendDir ".gitignore") -Value $frontendGitignore
Write-Host "  ✅ .gitignore (frontend)" -ForegroundColor Green

# ========== INITIALISER LES REPOS GIT ==========
Write-Host "`n🔧 Initialisation des repositories Git..." -ForegroundColor Yellow

# Backend
Set-Location $backendDir
git init
git add .
git commit -m "Initial commit: RAG Photographie Backend"
Write-Host "  ✅ Repository Backend initialisé" -ForegroundColor Green

# Frontend
Set-Location $frontendDir
git init
git add .
git commit -m "Initial commit: RAG Photographie Frontend"
Write-Host "  ✅ Repository Frontend initialisé" -ForegroundColor Green

Set-Location $projectRoot

Write-Host "`n✅ Séparation terminée !" -ForegroundColor Green
Write-Host "`n📁 Backend: $backendDir" -ForegroundColor Cyan
Write-Host "📁 Frontend: $frontendDir" -ForegroundColor Cyan
Write-Host "`n💡 Prochaines étapes:" -ForegroundColor Yellow
Write-Host "  1. Créer les repositories sur GitHub"
Write-Host "  2. Ajouter les remotes:"
Write-Host "     cd $backendDir"
Write-Host "     git remote add origin https://github.com/sSir-maker/RAG-Photographie-Backend.git"
Write-Host "     git push -u origin main"
Write-Host "`n     cd $frontendDir"
Write-Host "     git remote add origin https://github.com/sSir-maker/RAG-Photographie-Frontend.git"
Write-Host "     git push -u origin main"

