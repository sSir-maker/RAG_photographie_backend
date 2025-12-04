FROM node:18-alpine AS builder

WORKDIR /app

# Copier les fichiers de dépendances
COPY package*.json ./
RUN npm ci --legacy-peer-deps || npm ci

# Copier le code source
COPY . .

# Afficher les informations de build
RUN echo "🔍 Informations du build:" && \
    echo "Node version: $(node --version)" && \
    echo "NPM version: $(npm --version)" && \
    echo "📁 Contenu avant build:" && \
    ls -la /app

# Build l'application avec gestion d'erreur améliorée
RUN echo "🔨 Démarrage du build..." && \
    npm run build && \
    echo "✅ Build terminé"

# Vérifier que dist existe après le build et créer un répertoire vide si nécessaire
RUN echo "🔍 Vérification du répertoire de build..." && \
    ls -la /app && \
    if [ -d "dist" ]; then \
        echo "✅ dist trouvé - Contenu:" && \
        ls -la dist/ && \
        echo "✅ Nombre de fichiers: $(find dist -type f | wc -l)" && \
        echo "✅ Build réussi !"; \
    elif [ -d "build" ]; then \
        echo "✅ build trouvé (renommage en dist)" && \
        mv build dist && \
        ls -la dist/; \
    else \
        echo "❌ ERREUR: ni dist ni build trouvé après build" && \
        echo "📁 Contenu complet de /app:" && \
        find /app -type f -o -type d | head -20 && \
        echo "📦 Configuration vite:" && \
        cat vite.config.ts 2>/dev/null || echo "vite.config.ts non trouvé" && \
        exit 1; \
    fi && \
    # S'assurer que dist existe et n'est pas vide
    if [ ! -d "dist" ] || [ -z "$(ls -A dist)" ]; then \
        echo "❌ ERREUR: dist est vide ou n'existe pas" && \
        exit 1; \
    fi

# Stage de production
FROM nginx:alpine

# Copier les fichiers buildés (vérifier que dist existe)
COPY --from=builder /app/dist /usr/share/nginx/html

# Copier la configuration nginx
COPY nginx.conf /etc/nginx/conf.d/default.conf

# Vérifier que les fichiers sont bien copiés
RUN ls -la /usr/share/nginx/html || (echo "ERREUR: fichiers non copiés" && exit 1)

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]

