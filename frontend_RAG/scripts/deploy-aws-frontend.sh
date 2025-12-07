#!/bin/bash
# Script de déploiement AWS pour le frontend (S3 + CloudFront)

set -e

# Configuration
AWS_REGION=${AWS_REGION:-us-east-1}
S3_BUCKET=${S3_BUCKET:-rag-photographie-frontend}
CLOUDFRONT_DIST_ID=${CLOUDFRONT_DIST_ID:-}

echo "🚀 Déploiement du frontend sur AWS..."

# 1. Build le frontend
echo "🔨 Build du frontend..."
npm run build

# 2. Créer le bucket S3 si nécessaire
echo "📦 Création du bucket S3..."
aws s3 mb s3://$S3_BUCKET --region $AWS_REGION 2>/dev/null || echo "Bucket existe déjà"

# 3. Upload vers S3
echo "📤 Upload vers S3..."
aws s3 sync dist/ s3://$S3_BUCKET --delete --region $AWS_REGION

# 4. Activer le hosting statique
echo "🌐 Configuration du hosting statique..."
aws s3 website s3://$S3_BUCKET \
  --index-document index.html \
  --error-document index.html \
  --region $AWS_REGION

# 5. Invalider CloudFront si distribution existe
if [ ! -z "$CLOUDFRONT_DIST_ID" ]; then
  echo "🔄 Invalidation CloudFront..."
  aws cloudfront create-invalidation \
    --distribution-id $CLOUDFRONT_DIST_ID \
    --paths "/*"
fi

echo "✅ Frontend déployé sur S3: s3://$S3_BUCKET"
echo ""
echo "📝 Prochaines étapes:"
echo "1. Créer une distribution CloudFront"
echo "2. Configurer le domaine personnalisé (optionnel)"
echo "3. Mettre à jour VITE_API_URL avec l'URL du backend"

