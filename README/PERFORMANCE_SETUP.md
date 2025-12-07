# ⚡ Guide de Configuration Performance

## 📋 Vue d'ensemble

Ce guide explique comment configurer toutes les optimisations de performance :
- Cache Redis
- Load Balancing
- CDN
- Database Connection Pooling

## 🚀 Installation Rapide

### 1. Redis (Cache)

```bash
# Linux
sudo apt install redis-server
sudo systemctl start redis-server

# Docker
docker run -d -p 6379:6379 --name redis redis:alpine

# Python
pip install redis
```

### 2. Nginx (Load Balancing)

```bash
# Linux
sudo apt install nginx

# Configuration
sudo cp nginx-load-balancer.conf /etc/nginx/sites-available/rag-photographie
sudo ln -s /etc/nginx/sites-available/rag-photographie /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

### 3. Configuration .env

```env
# Redis
REDIS_URL=redis://localhost:6379/0
CACHE_TTL=3600

# Database Pooling
DB_POOL_SIZE=20
DB_MAX_OVERFLOW=40
DB_POOL_TIMEOUT=30
DB_POOL_RECYCLE=3600
```

## 📊 Architecture Recommandée

```
                    ┌─────────────┐
                    │   Nginx     │
                    │ (Load Bal.) │
                    └──────┬──────┘
                           │
        ┌──────────────────┼──────────────────┐
        │                  │                  │
   ┌────▼────┐       ┌─────▼─────┐      ┌─────▼─────┐
   │ API 1   │       │  API 2    │      │  API 3   │
   │ :8001   │       │  :8002    │      │  :8003   │
   └────┬────┘       └─────┬─────┘      └─────┬─────┘
        │                  │                  │
        └──────────────────┼──────────────────┘
                           │
                    ┌──────▼──────┐
                    │  PostgreSQL │
                    │   + Redis   │
                    └─────────────┘
```

## 🔧 Optimisations

### Cache Redis

- **RAG responses** : Cache 1h
- **User data** : Cache 30min
- **Vector store metadata** : Cache 24h

### Database Pooling

- **Pool size** : 20 connexions
- **Max overflow** : 40 connexions
- **Recycle** : 1h (évite les timeouts)

### Load Balancing

- **Method** : Round-robin (ou least_conn)
- **Health checks** : Toutes les 10s
- **Failover** : Automatique

### CDN

- **Assets statiques** : Cache 1 an
- **HTML** : Cache 1h
- **API** : Pas de cache

## 📈 Monitoring

### Redis

```bash
redis-cli INFO stats
redis-cli MONITOR
```

### Nginx

```bash
sudo tail -f /var/log/nginx/rag-photographie-access.log
```

### Database

```sql
-- Voir les connexions actives
SELECT count(*) FROM pg_stat_activity;

-- Voir les connexions par base
SELECT datname, count(*) FROM pg_stat_activity GROUP BY datname;
```

## ✅ Checklist

- [ ] Redis installé et démarré
- [ ] Nginx configuré
- [ ] Variables d'environnement configurées
- [ ] Plusieurs instances API démarrées
- [ ] Health checks fonctionnels
- [ ] Cache testé
- [ ] Load balancing testé
- [ ] CDN configuré (optionnel)

## 🐳 Docker Compose Complet

Voir `docker-compose.yml` pour une configuration complète avec tous les services.

---

**✅ Performance optimisée !**

