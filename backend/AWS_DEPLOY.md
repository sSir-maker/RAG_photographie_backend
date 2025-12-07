# 🚀 Déploiement sur AWS

## 📋 Options de déploiement AWS

### Option 1 : AWS App Runner (Recommandé - Simple comme Railway)
- ✅ Gestion automatique
- ✅ Scaling automatique
- ✅ HTTPS inclus
- ✅ Déploiement depuis GitHub

### Option 2 : AWS ECS Fargate (Recommandé pour production)
- ✅ Conteneurs serverless
- ✅ Scaling automatique
- ✅ Haute disponibilité

### Option 3 : AWS Elastic Beanstalk (Simple)
- ✅ Gestion simplifiée
- ✅ Auto-scaling
- ✅ Load balancing

### Option 4 : EC2 (Contrôle total)
- ✅ Contrôle complet
- ⚠️ Gestion manuelle

## 🚀 Option 1 : AWS App Runner (Recommandé)

### Prérequis
1. Compte AWS
2. AWS CLI installé et configuré
3. Docker installé

### Étapes

#### 1. Créer un ECR (Elastic Container Registry)

```bash
# Créer le repository ECR
aws ecr create-repository --repository-name rag-photographie-backend --region us-east-1

# Se connecter à ECR
aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin <AWS_ACCOUNT_ID>.dkr.ecr.us-east-1.amazonaws.com
```

#### 2. Build et push l'image Docker

```bash
cd backend

# Build l'image
docker build -t rag-photographie-backend .

# Tag pour ECR
docker tag rag-photographie-backend:latest <AWS_ACCOUNT_ID>.dkr.ecr.us-east-1.amazonaws.com/rag-photographie-backend:latest

# Push vers ECR
docker push <AWS_ACCOUNT_ID>.dkr.ecr.us-east-1.amazonaws.com/rag-photographie-backend:latest
```

#### 3. Créer le service App Runner

```bash
# Créer le fichier apprunner.yaml
cat > apprunner.yaml << EOF
version: 1.0
runtime: docker
build:
  commands:
    build:
      - echo "Build completed"
run:
  runtime-version: latest
  command: python run_api.py
  network:
    port: 8001
    env: PORT
  env:
    - name: DATABASE_URL
      value: "postgresql://..."
    - name: SECRET_KEY
      value: "ton-secret-key"
EOF

# Créer le service via AWS Console ou CLI
aws apprunner create-service \
  --service-name rag-photographie-backend \
  --source-configuration '{
    "ImageRepository": {
      "ImageIdentifier": "<AWS_ACCOUNT_ID>.dkr.ecr.us-east-1.amazonaws.com/rag-photographie-backend:latest",
      "ImageRepositoryType": "ECR"
    }
  }' \
  --instance-configuration '{
    "Cpu": "1 vCPU",
    "Memory": "2 GB"
  }'
```

## 🚀 Option 2 : AWS ECS Fargate

### 1. Créer le cluster ECS

```bash
aws ecs create-cluster --cluster-name rag-photographie-cluster
```

### 2. Créer la task definition

```json
{
  "family": "rag-photographie-backend",
  "networkMode": "awsvpc",
  "requiresCompatibilities": ["FARGATE"],
  "cpu": "1024",
  "memory": "2048",
  "containerDefinitions": [
    {
      "name": "backend",
      "image": "<AWS_ACCOUNT_ID>.dkr.ecr.us-east-1.amazonaws.com/rag-photographie-backend:latest",
      "portMappings": [
        {
          "containerPort": 8001,
          "protocol": "tcp"
        }
      ],
      "environment": [
        {"name": "DATABASE_URL", "value": "postgresql://..."},
        {"name": "SECRET_KEY", "value": "ton-secret-key"}
      ],
      "logConfiguration": {
        "logDriver": "awslogs",
        "options": {
          "awslogs-group": "/ecs/rag-photographie-backend",
          "awslogs-region": "us-east-1",
          "awslogs-stream-prefix": "ecs"
        }
      }
    }
  ]
}
```

### 3. Créer le service ECS

```bash
aws ecs create-service \
  --cluster rag-photographie-cluster \
  --service-name rag-backend-service \
  --task-definition rag-photographie-backend \
  --desired-count 1 \
  --launch-type FARGATE \
  --network-configuration "awsvpcConfiguration={subnets=[subnet-xxx],securityGroups=[sg-xxx],assignPublicIp=ENABLED}"
```

## 🗄️ Base de données : AWS RDS PostgreSQL

```bash
# Créer une instance RDS PostgreSQL
aws rds create-db-instance \
  --db-instance-identifier rag-photographie-db \
  --db-instance-class db.t3.micro \
  --engine postgres \
  --master-username admin \
  --master-user-password ton-mot-de-passe \
  --allocated-storage 20 \
  --vpc-security-group-ids sg-xxx
```

## 💾 Cache : AWS ElastiCache Redis

```bash
# Créer un cluster Redis
aws elasticache create-cache-cluster \
  --cache-cluster-id rag-redis \
  --cache-node-type cache.t3.micro \
  --engine redis \
  --num-cache-nodes 1
```

## 🌐 Frontend : S3 + CloudFront

### 1. Build le frontend

```bash
cd frontend_RAG
npm run build
```

### 2. Upload vers S3

```bash
# Créer le bucket S3
aws s3 mb s3://rag-photographie-frontend

# Upload les fichiers
aws s3 sync dist/ s3://rag-photographie-frontend --delete

# Activer le hosting statique
aws s3 website s3://rag-photographie-frontend \
  --index-document index.html \
  --error-document index.html
```

### 3. Créer CloudFront distribution

```bash
aws cloudfront create-distribution \
  --origin-domain-name rag-photographie-frontend.s3.amazonaws.com
```

## 🔐 Variables d'environnement AWS

### Backend (ECS/App Runner)
- `DATABASE_URL` : URL RDS PostgreSQL
- `REDIS_URL` : URL ElastiCache Redis
- `SECRET_KEY` : Clé secrète
- `FRONTEND_URL` : URL CloudFront du frontend
- `OLLAMA_BASE_URL` : URL Ollama (ou utilise AWS Bedrock)

## 📝 Scripts de déploiement

Voir `scripts/deploy-aws.sh` pour les scripts automatisés.

## 💰 Coûts estimés (par mois)

- **App Runner** : ~$25-50
- **ECS Fargate** : ~$30-60
- **RDS PostgreSQL** : ~$15-30
- **ElastiCache Redis** : ~$15-30
- **S3 + CloudFront** : ~$5-10
- **Total** : ~$70-180/mois

## ✅ Avantages AWS

- ✅ Scalabilité élevée
- ✅ Haute disponibilité
- ✅ Services managés
- ✅ Intégration avec autres services AWS
- ✅ Monitoring avec CloudWatch

