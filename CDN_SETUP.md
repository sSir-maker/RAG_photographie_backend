# 🌐 Configuration CDN

## 📋 Vue d'ensemble

Un CDN (Content Delivery Network) améliore les performances en servant les assets statiques depuis des serveurs proches des utilisateurs.

## 🚀 Options de CDN

### 1. Cloudflare (Gratuit)

**Avantages** :
- Gratuit pour usage basique
- SSL automatique
- Protection DDoS
- Cache automatique

**Configuration** :
1. Créer un compte sur https://cloudflare.com
2. Ajouter ton domaine
3. Suivre les instructions pour changer les DNS
4. Activer le cache pour les assets statiques

### 2. AWS CloudFront

**Configuration** :
1. Créer un bucket S3 pour les assets
2. Créer une distribution CloudFront
3. Configurer les origines et comportements de cache

### 3. Nginx comme CDN local

Configuration dans `nginx.conf` :

```nginx
# Cache pour les assets statiques
location ~* \.(jpg|jpeg|png|gif|ico|css|js|svg|woff|woff2|ttf|eot)$ {
    root /var/www/rag-photographie-frontend;
    expires 1y;
    add_header Cache-Control "public, immutable";
    add_header Vary "Accept-Encoding";
    
    # Compression
    gzip on;
    gzip_types text/css application/javascript image/svg+xml;
    gzip_vary on;
}
```

## 📁 Structure des Assets

```
frontend_RAG/
├── dist/              # Build de production
│   ├── assets/
│   │   ├── js/        # JavaScript (cache 1 an)
│   │   ├── css/       # CSS (cache 1 an)
│   │   └── images/    # Images (cache 1 an)
│   └── index.html     # HTML (cache court)
```

## 🔧 Configuration Vite pour CDN

Dans `vite.config.ts` :

```typescript
export default defineConfig({
  build: {
    rollupOptions: {
      output: {
        // Hash pour cache busting
        entryFileNames: 'assets/[name]-[hash].js',
        chunkFileNames: 'assets/[name]-[hash].js',
        assetFileNames: 'assets/[name]-[hash].[ext]'
      }
    }
  },
  base: process.env.CDN_URL || '/',  // URL du CDN si disponible
})
```

## 📊 Headers de Cache

### Assets statiques (long terme)
```
Cache-Control: public, max-age=31536000, immutable
```

### HTML (court terme)
```
Cache-Control: public, max-age=3600, must-revalidate
```

### API (pas de cache)
```
Cache-Control: no-cache, no-store, must-revalidate
```

## 🐳 Docker avec CDN

```yaml
version: '3.8'

services:
  nginx-cdn:
    image: nginx:alpine
    ports:
      - "80:80"
    volumes:
      - ./frontend_RAG/dist:/usr/share/nginx/html
      - ./nginx-cdn.conf:/etc/nginx/conf.d/default.conf
```

## ✅ Avantages

- **Performance** : Chargement plus rapide des assets
- **Réduction de bande passante** : Moins de charge sur le serveur
- **Disponibilité** : Assets servis depuis plusieurs emplacements
- **SEO** : Temps de chargement amélioré

## 🔒 Sécurité CDN

- Utiliser HTTPS
- Valider les assets servis
- Configurer CORS correctement
- Utiliser Subresource Integrity (SRI) pour les scripts externes

---

**✅ CDN configuré !**

