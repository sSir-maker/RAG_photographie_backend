# 🔒 Configuration HTTPS/SSL

## Option 1 : Let's Encrypt (Gratuit - Recommandé)

### Installation Certbot

```bash
# Ubuntu/Debian
sudo apt update
sudo apt install certbot python3-certbot-nginx

# CentOS/RHEL
sudo yum install certbot python3-certbot-nginx
```

### Génération du certificat

```bash
# Automatique avec Nginx
sudo certbot --nginx -d ton-domaine.com -d www.ton-domaine.com

# Manuel (si tu veux plus de contrôle)
sudo certbot certonly --standalone -d ton-domaine.com -d www.ton-domaine.com
```

### Renouvellement automatique

Certbot configure automatiquement le renouvellement. Vérifier :

```bash
# Tester le renouvellement
sudo certbot renew --dry-run

# Vérifier le cron job
sudo systemctl status certbot.timer
```

## Option 2 : Reverse Proxy avec Traefik

### docker-compose.yml avec Traefik

```yaml
version: '3.8'

services:
  traefik:
    image: traefik:v2.10
    container_name: traefik
    command:
      - "--api.insecure=true"
      - "--providers.docker=true"
      - "--providers.docker.exposedbydefault=false"
      - "--entrypoints.web.address=:80"
      - "--entrypoints.websecure.address=:443"
      - "--certificatesresolvers.letsencrypt.acme.tlschallenge=true"
      - "--certificatesresolvers.letsencrypt.acme.email=ton-email@example.com"
      - "--certificatesresolvers.letsencrypt.acme.storage=/letsencrypt/acme.json"
    ports:
      - "80:80"
      - "443:443"
      - "8080:8080"  # Dashboard Traefik
    volumes:
      - /var/run/docker.sock:/var/run/docker.sock:ro
      - ./letsencrypt:/letsencrypt
    networks:
      - rag-network

  backend:
    # ... configuration existante ...
    labels:
      - "traefik.enable=true"
      - "traefik.http.routers.backend.rule=Host(`api.ton-domaine.com`)"
      - "traefik.http.routers.backend.entrypoints=websecure"
      - "traefik.http.routers.backend.tls.certresolver=letsencrypt"
      - "traefik.http.services.backend.loadbalancer.server.port=8001"

networks:
  rag-network:
    driver: bridge
```

## Option 3 : Cloudflare (Gratuit)

1. Créer un compte Cloudflare
2. Ajouter ton domaine
3. Changer les nameservers
4. Activer SSL/TLS en mode "Full" ou "Full (strict)"
5. Cloudflare gère automatiquement HTTPS

## Vérification

```bash
# Vérifier le certificat
openssl s_client -connect ton-domaine.com:443 -servername ton-domaine.com

# Tester avec curl
curl -I https://ton-domaine.com

# Tester avec SSL Labs
# https://www.ssllabs.com/ssltest/analyze.html?d=ton-domaine.com
```

## Configuration Nginx

Voir `nginx.conf` pour la configuration complète.

## Headers de sécurité

Les headers suivants sont configurés dans nginx.conf :
- `Strict-Transport-Security` : Force HTTPS
- `X-Frame-Options` : Protection contre clickjacking
- `X-Content-Type-Options` : Protection MIME sniffing
- `X-XSS-Protection` : Protection XSS

