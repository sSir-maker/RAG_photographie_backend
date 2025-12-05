# 🔧 Fix Docker BrokenPipeError

## ⚠️ Problème

Erreur lors du build Docker :
```
BrokenPipeError: [Errno 32] Broken pipe
pip._vendor.urllib3.exceptions.ProtocolError: ("Connection broken: BrokenPipeError(32, 'Broken pipe')", BrokenPipeError(32, 'Broken pipe'))
```

Cette erreur survient lors de l'installation des dépendances Python avec pip dans Docker. C'est généralement dû à :
- **Problème de connexion réseau temporaire** lors du téléchargement
- **Timeout** lors du téléchargement de gros packages
- **Connexion instable** vers PyPI

## ✅ Solution Implémentée

J'ai amélioré le Dockerfile pour rendre l'installation plus robuste :

### 1. Timeout Augmenté
- Timeout de **300 secondes** (5 minutes) au lieu du défaut
- Permet de télécharger même les gros packages lentement

### 2. Retries Automatiques
- **5 tentatives** par défaut pour chaque package
- Gère automatiquement les problèmes réseau temporaires

### 3. Nouvelle Tentative Automatique
- Si l'installation échoue, **nouvelle tentative automatique après 10 secondes**
- Double protection contre les problèmes réseau

### 4. Gestion d'Erreurs Améliorée
- Messages d'erreur clairs
- Logs détaillés pour le debugging

## 📋 Modifications du Dockerfile

```dockerfile
# Avant
RUN pip install --no-cache-dir -r requirements.txt

# Après
RUN pip install --no-cache-dir \
    --timeout=300 \
    --retries=5 \
    --default-timeout=300 \
    -r requirements.txt || \
    (echo "⚠️ Première tentative échouée, nouvelle tentative..." && \
     sleep 10 && \
     pip install --no-cache-dir \
         --timeout=300 \
         --retries=5 \
         --default-timeout=300 \
         -r requirements.txt)
```

## 🚀 Utilisation

Le Dockerfile est maintenant plus robuste. Si le problème persiste :

1. **Vérifier votre connexion réseau**
2. **Réessayer le build** (souvent un problème temporaire)
3. **Vérifier que PyPI est accessible**

## 🔍 Vérification

Pour tester localement :
```bash
cd backend
docker build -t rag-photographie-backend .
```

Si le problème persiste, vérifiez :
- La connexion internet
- Si PyPI est accessible : `curl https://pypi.org/simple/`
- Les logs Docker pour voir quel package pose problème

## 📝 Notes

- Le timeout de 300 secondes devrait être suffisant même pour les gros packages
- Les retries automatiques gèrent la plupart des problèmes réseau temporaires
- La nouvelle tentative automatique offre une sécurité supplémentaire

