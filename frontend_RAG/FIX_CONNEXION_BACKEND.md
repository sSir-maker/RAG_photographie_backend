# 🔧 Fix Problème de Connexion Backend

## 🐛 Problème Identifié

Le frontend ne peut pas se connecter au backend en production, affichant l'erreur :
> "Erreur de connexion. Vérifiez votre connexion internet et réessayez."

## ✅ Solutions Appliquées

### 1. Détection Automatique de l'URL Backend

Le frontend détecte maintenant automatiquement l'URL du backend selon l'environnement :

- **Production (Render)** : `https://rag-photographie-backend.onrender.com`
- **Développement** : `http://localhost:8001`
- **Variable d'environnement** : Priorité à `VITE_API_URL` si définie

### 2. Health Check Automatique

Un système de vérification de santé du backend a été ajouté :

- **Au chargement** : Test automatique de la connexion
- **Message informatif** : Affiche l'état de la connexion
- **Messages d'erreur détaillés** : Avec suggestions de résolution

### 3. Messages d'Erreur Améliorés

Les messages d'erreur sont maintenant plus informatifs :

- **Affiche l'URL du backend** utilisée
- **Suggestions de résolution** selon le type d'erreur
- **Messages clairs** pour l'utilisateur

## 🔍 Diagnostic

### Vérifier la Configuration

1. **Ouvrir la console du navigateur** (F12)
2. **Vérifier les logs** :
   - `🔧 API Configuration:` - Affiche l'URL du backend détectée
   - `🔍 Vérification de la connexion au backend...` - Indique le test en cours
   - `📊 Résultat du health check:` - Affiche le résultat

### Vérifier le Backend

1. **Tester l'endpoint health** :
   ```
   https://rag-photographie-backend.onrender.com/health
   ```
   
2. **Si le backend ne répond pas** :
   - Vérifier que le backend est déployé sur Render
   - Vérifier que le backend est démarré (peut prendre 30-60 secondes)
   - Vérifier les logs du backend sur Render

### Vérifier les Variables d'Environnement

1. **Sur Render Dashboard** :
   - Aller dans le service frontend
   - Vérifier les **Environment Variables**
   - Vérifier que `VITE_API_URL` est défini (optionnel maintenant)

2. **URL du backend attendue** :
   ```
   https://rag-photographie-backend.onrender.com
   ```

## 📝 Configuration Render

Le fichier `render.yaml` contient la configuration :

```yaml
envVars:
  - key: VITE_API_URL
    value: https://rag-photographie-backend.onrender.com
```

**Note** : Même sans cette variable, le frontend détecte maintenant automatiquement l'URL du backend.

## 🔄 Redéploiement

Après ces modifications, il faut redéployer le frontend :

1. **Commiter et pousser les changements**
2. **Render redéploiera automatiquement**
3. **Tester la connexion** une fois redéployé

## 💡 Améliorations Futures

- [ ] Ajouter un bouton de réessai automatique
- [ ] Mettre en cache le résultat du health check
- [ ] Ajouter un mode offline avec message informatif
- [ ] Afficher un indicateur de statut du backend en temps réel

## 🆘 En Cas de Problème Persistant

1. **Vérifier les logs du backend** sur Render
2. **Vérifier les logs du frontend** dans la console (F12)
3. **Tester l'URL du backend** directement dans le navigateur
4. **Vérifier la configuration CORS** du backend

