#!/bin/bash
# Script de déploiement AWS pour le backend

set -e

# Configuration
AWS_REGION=${AWS_REGION:-us-east-1}
AWS_ACCOUNT_ID=$(aws sts get-caller-identity --query Account --output text)
ECR_REPO="rag-photographie-backend"
SERVICE_NAME="rag-photographie-backend"

echo "🚀 Déploiement sur AWS..."
echo "Region: $AWS_REGION"
echo "Account ID: $AWS_ACCOUNT_ID"

# 1. Créer le repository ECR si nécessaire
echo "📦 Création du repository ECR..."
aws ecr describe-repositories --repository-names $ECR_REPO --region $AWS_REGION 2>/dev/null || \
aws ecr create-repository --repository-name $ECR_REPO --region $AWS_REGION

# 2. Se connecter à ECR
echo "🔐 Connexion à ECR..."
aws ecr get-login-password --region $AWS_REGION | docker login --username AWS --password-stdin $AWS_ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com

# 3. Build l'image
echo "🔨 Build de l'image Docker..."
docker build -t $ECR_REPO:latest -f Dockerfile.aws .

# 4. Tag pour ECR
echo "🏷️  Tag de l'image..."
docker tag $ECR_REPO:latest $AWS_ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com/$ECR_REPO:latest

# 5. Push vers ECR
echo "📤 Push vers ECR..."
docker push $AWS_ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com/$ECR_REPO:latest

echo "✅ Image poussée vers ECR: $AWS_ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com/$ECR_REPO:latest"
echo ""
echo "📝 Prochaines étapes:"
echo "1. Créer le service App Runner ou ECS"
echo "2. Configurer les variables d'environnement"
echo "3. Configurer RDS et ElastiCache"
echo ""
echo "Voir AWS_DEPLOY.md pour les instructions complètes"

