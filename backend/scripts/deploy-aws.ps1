# Script PowerShell de déploiement AWS pour le backend

$ErrorActionPreference = "Stop"

# Configuration
$AWS_REGION = if ($env:AWS_REGION) { $env:AWS_REGION } else { "us-east-1" }
$AWS_ACCOUNT_ID = (aws sts get-caller-identity --query Account --output text)
$ECR_REPO = "rag-photographie-backend"

Write-Host "🚀 Déploiement sur AWS..." -ForegroundColor Cyan
Write-Host "Region: $AWS_REGION"
Write-Host "Account ID: $AWS_ACCOUNT_ID"

# 1. Créer le repository ECR si nécessaire
Write-Host "`n📦 Création du repository ECR..." -ForegroundColor Yellow
$repoExists = aws ecr describe-repositories --repository-names $ECR_REPO --region $AWS_REGION 2>$null
if (-not $repoExists) {
    aws ecr create-repository --repository-name $ECR_REPO --region $AWS_REGION
    Write-Host "✅ Repository ECR créé" -ForegroundColor Green
} else {
    Write-Host "✅ Repository ECR existe déjà" -ForegroundColor Green
}

# 2. Se connecter à ECR
Write-Host "`n🔐 Connexion à ECR..." -ForegroundColor Yellow
$loginCmd = aws ecr get-login-password --region $AWS_REGION | docker login --username AWS --password-stdin "$AWS_ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com"
if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Erreur lors de la connexion à ECR" -ForegroundColor Red
    exit 1
}
Write-Host "✅ Connecté à ECR" -ForegroundColor Green

# 3. Build l'image
Write-Host "`n🔨 Build de l'image Docker..." -ForegroundColor Yellow
docker build -t $ECR_REPO`:latest -f Dockerfile.aws .
if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Erreur lors du build" -ForegroundColor Red
    exit 1
}
Write-Host "✅ Image buildée" -ForegroundColor Green

# 4. Tag pour ECR
Write-Host "`n🏷️  Tag de l'image..." -ForegroundColor Yellow
docker tag "$ECR_REPO`:latest" "$AWS_ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com/$ECR_REPO`:latest"

# 5. Push vers ECR
Write-Host "`n📤 Push vers ECR..." -ForegroundColor Yellow
docker push "$AWS_ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com/$ECR_REPO`:latest"
if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Erreur lors du push" -ForegroundColor Red
    exit 1
}

Write-Host "`n✅ Image poussée vers ECR: $AWS_ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com/$ECR_REPO`:latest" -ForegroundColor Green
Write-Host "`n📝 Prochaines étapes:" -ForegroundColor Cyan
Write-Host "1. Créer le service App Runner ou ECS" -ForegroundColor White
Write-Host "2. Configurer les variables d'environnement" -ForegroundColor White
Write-Host "3. Configurer RDS et ElastiCache" -ForegroundColor White
Write-Host "`nVoir AWS_DEPLOY.md pour les instructions complètes" -ForegroundColor Gray

