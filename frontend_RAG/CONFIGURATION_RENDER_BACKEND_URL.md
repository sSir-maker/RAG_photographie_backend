# 🔗 Configuration de l'URL Backend sur Render

## 📋 Résumé rapide

**Question :** Dois-je ajouter le lien du backend au niveau des variables d'environnement sur Render ?

**Réponse :** **OPTIONNEL mais RECOMMANDÉ** ✅

## 🔍 Situation actuelle

### 1. Configuration automatique (Fallback)

Le frontend détecte automatiquement l'URL du backend :

```typescript
// src/config.ts
function detectBackendUrl(): string {
  // 1. Utilise VITE_API_URL si défini
  if (envApiUrl) {
    return envApiUrl;
  }
  
  // 2. Sinon, URL hardcodée en production
  if (isProduction) {
    return 'https://rag-photographie-backend.onrender.com';
  }
  
  // 3. Sinon, localhost en développement
  return 'http://localhost:8001';
}
```

### 2. Fichier render.yaml

Le fichier `render.yaml` définit déjà la variable :

```yaml
envVars:
  - key: VITE_API_URL
    value: https://rag-photographie-backend.onrender.com
```

## ✅ Conclusion

**Le frontend fonctionnera même SANS ajouter la variable manuellement** car :
- Le code a une URL hardcodée en fallback
- Le fichier `render.yaml` la définit déjà (si Render l'utilise)

## 🎯 Mais c'est RECOMMANDÉ de l'ajouter manuellement

### Pourquoi ?

1. **Flexibilité** : Facile de changer l'URL sans modifier le code
2. **Meilleures pratiques** : Configuration centralisée dans Render
3. **Sécurité** : Pas d'URL hardcodée dans le code
4. **Multi-environnements** : Facile de gérer dev/staging/prod

## 📝 Comment l'ajouter sur Render

### Option 1 : Via le Dashboard Render (Recommandé)

1. Va sur https://dashboard.render.com
2. Sélectionne ton service **frontend** (`rag-photographie-frontend`)
3. Clique sur **Environment** dans le menu de gauche
4. Clique sur **Add Environment Variable**
5. Ajoute :
   - **Key** : `VITE_API_URL`
   - **Value** : `https://rag-photographie-backend.onrender.com`
6. Clique sur **Save Changes**
7. Render redéploiera automatiquement

### Option 2 : Via render.yaml (Déjà fait)

Le fichier `render.yaml` à la racine du frontend contient déjà :

```yaml
envVars:
  - key: VITE_API_URL
    value: https://rag-photographie-backend.onrender.com
```

Si Render utilise ce fichier, la variable est automatiquement configurée.

## 🔍 Vérification

### 1. Vérifier dans le code compilé

Une fois déployé, ouvre la console du navigateur (F12) et cherche :

```
🔧 API Configuration: {
  isProduction: true,
  envApiUrl: "https://rag-photographie-backend.onrender.com",
  hostname: "rag-photographie-frontend.onrender.com",
  finalUrl: "https://rag-photographie-backend.onrender.com"
}
```

### 2. Vérifier dans Render

- Va dans le service frontend sur Render
- Clique sur **Environment**
- Vérifie que `VITE_API_URL` est présent avec la bonne valeur

## 🎯 Recommandation finale

**Ajoute la variable `VITE_API_URL` dans Render** même si ce n'est pas strictement nécessaire, car :
- ✅ C'est une meilleure pratique
- ✅ Plus facile à maintenir
- ✅ Plus flexible pour l'avenir

## 📝 Valeur exacte à utiliser

```
VITE_API_URL = https://rag-photographie-backend.onrender.com
```

⚠️ **Important** : Remplace `rag-photographie-backend` par le nom réel de ton service backend sur Render si différent.

