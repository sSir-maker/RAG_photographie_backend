# ⚖️ Configuration du Load Balancing

## 📋 Vue d'ensemble

Le load balancing distribue le trafic entre plusieurs instances de l'API pour améliorer les performances et la disponibilité.

## 🚀 Configuration avec Nginx

### 1. Installation Nginx

**Linux (Ubuntu/Debian)**:
```bash
sudo apt update
sudo apt install nginx
```

**Windows**:
- Télécharger depuis https://nginx.org/en/download.html
- Ou utiliser WSL

### 2. Configuration

1. Copier le fichier de configuration :
```bash
sudo cp nginx-load-balancer.conf /etc/nginx/sites-available/rag-photographie
sudo ln -s /etc/nginx/sites-available/rag-photographie /etc/nginx/sites-enabled/
```

2. Tester la configuration :
```bash
sudo nginx -t
```

3. Redémarrer Nginx :
```bash
sudo systemctl restart nginx
```

### 3. Démarrer plusieurs instances de l'API

```bash
# Terminal 1
uvicorn app.api:app --port 8001 --workers 1

# Terminal 2
uvicorn app.api:app --port 8002 --workers 1

# Terminal 3
uvicorn app.api:app --port 8003 --workers 1
```

Ou avec des variables d'environnement différentes :
```bash
# Instance 1
PORT=8001 python run_api.py

# Instance 2
PORT=8002 python run_api.py

# Instance 3
PORT=8003 python run_api.py
```

## 🔧 Méthodes de Load Balancing

### Round-Robin (par défaut)
Distribution équitable entre toutes les instances.

### Least Connections
```nginx
upstream rag_backend {
    least_conn;
    server localhost:8001;
    server localhost:8002;
    server localhost:8003;
}
```

### IP Hash (Session Sticky)
```nginx
upstream rag_backend {
    ip_hash;
    server localhost:8001;
    server localhost:8002;
    server localhost:8003;
}
```

### Weighted
```nginx
upstream rag_backend {
    server localhost:8001 weight=3;  # 3x plus de trafic
    server localhost:8002 weight=2;  # 2x plus de trafic
    server localhost:8003 weight=1;  # Trafic normal
}
```

## 📊 Monitoring

### Vérifier le statut des instances

```bash
# Health check
curl http://localhost/health

# Vérifier les logs Nginx
sudo tail -f /var/log/nginx/rag-photographie-access.log
```

### Statistiques Nginx (nécessite module status)

```nginx
location /nginx_status {
    stub_status on;
    access_log off;
    allow 127.0.0.1;
    deny all;
}
```

## 🐳 Docker Compose avec Load Balancing

```yaml
version: '3.8'

services:
  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx-load-balancer.conf:/etc/nginx/conf.d/default.conf
    depends_on:
      - api1
      - api2
      - api3

  api1:
    build: .
    environment:
      - PORT=8001
    ports:
      - "8001:8001"

  api2:
    build: .
    environment:
      - PORT=8002
    ports:
      - "8002:8002"

  api3:
    build: .
    environment:
      - PORT=8003
    ports:
      - "8003:8003"
```

## ✅ Avantages

- **Haute disponibilité** : Si une instance tombe, les autres continuent
- **Performance** : Distribution de la charge
- **Scalabilité** : Facile d'ajouter/supprimer des instances
- **Maintenance** : Mise à jour sans interruption (rolling update)

## 🔒 Sécurité

- Utiliser HTTPS en production
- Limiter l'accès aux instances backend
- Configurer un firewall
- Utiliser des health checks

---

**✅ Load balancing configuré !**

