# Script PowerShell pour séparer le frontend
# Usage: .\scripts\separate_frontend.ps1

Write-Host "🔀 Séparation du Frontend..." -ForegroundColor Cyan
Write-Host "=" * 60

$frontendRepo = Read-Host "URL du nouveau repository frontend (ex: https://github.com/sSir-maker/RAG_photographie_frontend.git)"

if ([string]::IsNullOrWhiteSpace($frontendRepo)) {
    Write-Host "❌ URL du repository requise" -ForegroundColor Red
    exit 1
}

# Vérifier qu'on est dans le bon répertoire
if (-not (Test-Path "frontend_RAG")) {
    Write-Host "❌ Ce script doit être exécuté depuis la racine du projet" -ForegroundColor Red
    exit 1
}

# Créer un dossier temporaire
$tempDir = "..\RAG-Frontend-Temp"
if (Test-Path $tempDir) {
    Remove-Item -Recurse -Force $tempDir
}
New-Item -ItemType Directory -Path $tempDir | Out-Null

Write-Host "`n📦 Copie des fichiers frontend..." -ForegroundColor Yellow

# Copier tout le dossier frontend_RAG
Copy-Item -Path "frontend_RAG\*" -Destination $tempDir -Recurse -Force
Write-Host "  ✅ frontend_RAG copié" -ForegroundColor Green

# Créer un .gitignore pour le frontend
$frontendGitignore = @"
# Dependencies
node_modules/
.pnp
.pnp.js

# Testing
coverage/

# Production
dist/
build/

# Misc
.DS_Store
.env.local
.env.development.local
.env.test.local
.env.production.local

npm-debug.log*
yarn-debug.log*
yarn-error.log*

# IDE
.vscode/
.idea/
*.swp
*.swo

# Vite
.vite/
"@

$frontendGitignore | Out-File -FilePath "$tempDir\.gitignore" -Encoding UTF8

# Créer un README frontend spécifique
$frontendReadme = @"
# 🎨 RAG Photographie - Frontend

Interface React/Vite pour le système RAG de photographie.

## 🚀 Installation

\`\`\`powershell
# Installer les dépendances
npm install
\`\`\`

## ⚙️ Configuration

Créer un fichier \`.env.local\` :

\`\`\`env
VITE_API_URL=http://localhost:8001
\`\`\`

## 🏃 Démarrer le serveur de développement

\`\`\`powershell
npm run dev
\`\`\`

L'application sera accessible sur \`http://localhost:3000\`

## 🏗️ Build pour production

\`\`\`powershell
npm run build
\`\`\`

## 🐳 Docker

\`\`\`powershell
docker build -t rag-frontend .
docker run -p 80:80 rag-frontend
\`\`\`

## 📚 Documentation

- \`README.md\` - Documentation complète
- \`README_API.md\` - Documentation de l'API

## 🔗 Backend

Le backend est dans un repository séparé :
\`https://github.com/sSir-maker/RAG_photographie_backend\`

---

**Frontend RAG Photographie** - Interface React moderne avec Tailwind CSS
"@

$frontendReadme | Out-File -FilePath "$tempDir\README.md" -Encoding UTF8

# Initialiser Git dans le dossier temporaire
Write-Host "`n📦 Initialisation Git..." -ForegroundColor Yellow
Set-Location $tempDir
git init
git add .
git commit -m "Initial commit: Frontend RAG Photographie"

# Ajouter le remote
Write-Host "`n🔗 Configuration du remote..." -ForegroundColor Yellow
git remote add origin $frontendRepo

Write-Host "`n✅ Frontend séparé avec succès !" -ForegroundColor Green
Write-Host "`n📝 Prochaines étapes :" -ForegroundColor Cyan
Write-Host "  1. Vérifier les fichiers dans : $tempDir"
Write-Host "  2. Pousser vers le nouveau repo :"
Write-Host "     cd $tempDir"
Write-Host "     git push -u origin main"

Set-Location ..
