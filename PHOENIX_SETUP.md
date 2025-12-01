# 🔥 Guide d'Installation et Configuration Phoenix

Guide complet pour installer et configurer Arize Phoenix pour le monitoring du RAG.

## 📋 Prérequis

- Python 3.11 ou 3.12
- Environnement virtuel activé
- Projet RAG opérationnel

## 🚀 Installation

### Option 1 : Installation Python (Recommandé)

```bash
# Activer l'environnement virtuel
.\venv\Scripts\Activate.ps1  # Windows
# ou
source venv/bin/activate     # Linux/Mac

# Installer Phoenix
pip install phoenix>=3.0.0 openinference-semantic-conventions>=1.0.0

# Vérifier l'installation
python -c "import phoenix; print('Phoenix installé!')"
```

### Option 2 : Installation via Docker

```bash
# Lancer Phoenix avec Docker
docker-compose -f docker-compose.monitoring.yml up -d

# Vérifier que c'est lancé
docker ps | grep phoenix
```

## ⚙️ Configuration

### 1. Variables d'environnement (optionnel)

Créer un fichier `.env` à la racine :

```env
# Phoenix Configuration
PHOENIX_ENDPOINT=http://localhost:6006
PHOENIX_PORT=6006
```

### 2. Démarrage du Dashboard

#### Mode Développement (Python)

```bash
# Dans un terminal séparé
phoenix serve --port 6006
```

**Note** : Si la commande `phoenix` n'est pas reconnue, utilisez :
```bash
python -m phoenix.server.main serve --port 6006
```

Le dashboard sera accessible sur : **http://localhost:6006**

#### Mode Production (Docker)

```bash
docker-compose -f docker-compose.monitoring.yml up -d
```

## 🔧 Intégration dans le Code

### L'instrumentation est automatique !

Le code est déjà configuré pour utiliser Phoenix :

1. **Au démarrage de l'API** (`app/api.py`) :
   - Phoenix s'initialise automatiquement
   - L'instrumentation LangChain est activée

2. **Dans le pipeline RAG** (`app/rag_pipeline.py`) :
   - Tracing automatique des appels LangChain
   - Tracing manuel pour les phases custom

3. **Dans le pipeline MLOps** (`mlops/pipeline.py`) :
   - Monitoring des exécutions de pipeline

### Vérifier que ça fonctionne

1. Démarrer Phoenix :
   ```bash
   python -m phoenix.server.main --port 6006
   ```

2. Démarrer l'API :
   ```bash
   python run_api.py
   ```

3. Faire une requête test :
   ```bash
   curl -X POST http://localhost:8001/ask \
     -H "Content-Type: application/json" \
     -H "Authorization: Bearer <token>" \
     -d '{"question": "Qu'est-ce que l'ISO ?", "conversation_id": 1}'
   ```

4. Vérifier dans Phoenix :
   - Ouvrir http://localhost:6006
   - Vous devriez voir les traces apparaître !

## 📊 Utilisation du Dashboard

### Vue d'ensemble

Le dashboard Phoenix affiche :

1. **Traces** : Toutes les requêtes RAG avec détails
2. **Performance** : Temps d'exécution par phase
3. **Embeddings** : Visualisation 2D/3D des embeddings
4. **Qualité** : Scores de qualité automatiques

### Fonctionnalités principales

#### 1. Explorer les Traces

- Cliquer sur une trace pour voir les détails
- Voir les phases : retrieval → generation → response
- Analyser les métriques par phase

#### 2. Analyser les Performances

- Graphiques de latence
- Comparaison historique
- Identification des bottlenecks

#### 3. Visualiser les Embeddings

- Clustering des documents
- Similarité entre requêtes
- Détection d'anomalies

#### 4. Évaluer la Qualité

- Scores de pertinence
- Détection d'hallucinations
- Comparaison des réponses

## 🔍 Métriques Disponibles

### Métriques Retrieval

- `retrieval.documents_count` : Nombre de documents récupérés
- `retrieval.avg_score` : Score de similarité moyen
- `retrieval.duration_ms` : Temps de retrieval

### Métriques Génération

- `generation.duration_ms` : Temps de génération
- `generation.tokens_used` : Nombre de tokens
- `generation.model` : Modèle LLM utilisé

### Métriques Pipeline

- `pipeline.duration_seconds` : Durée totale
- `pipeline.documents_processed` : Documents traités
- `pipeline.success` : Succès/échec

## 🐛 Dépannage

### Phoenix ne démarre pas

```bash
# Vérifier que le port est libre
netstat -ano | findstr :6006  # Windows
lsof -i :6006                 # Linux/Mac

# Changer le port si nécessaire
python -m phoenix.server.main --port 6007
```

### Pas de traces visibles

1. Vérifier que Phoenix est démarré
2. Vérifier que l'API est démarrée
3. Vérifier les logs de l'API pour les erreurs Phoenix
4. Vérifier que `PHOENIX_ENDPOINT` est correct

### Erreur d'import

```bash
# Réinstaller Phoenix
pip uninstall arize-phoenix
pip install arize-phoenix>=7.5.0
```

## 📚 Ressources

- [Documentation Phoenix](https://docs.arize.com/phoenix)
- [OpenInference Standard](https://github.com/Arize-ai/openinference)
- [LangChain Integration](https://docs.arize.com/phoenix/integrations/langchain)

## ✅ Checklist de Vérification

- [ ] Phoenix installé (`pip list | grep phoenix`)
- [ ] Dashboard accessible (http://localhost:6006)
- [ ] API démarrée avec Phoenix activé
- [ ] Traces visibles après une requête test
- [ ] Métriques affichées correctement

## 🎯 Prochaines Étapes

1. ✅ Installer Phoenix
2. ✅ Démarrer le dashboard
3. ✅ Faire des requêtes test
4. ✅ Explorer les traces
5. ✅ Configurer des alertes (optionnel)
6. ✅ Intégrer dans CI/CD (optionnel)

**Votre monitoring est maintenant opérationnel ! 🚀**

