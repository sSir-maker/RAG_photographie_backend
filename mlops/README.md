# 🚀 Pipeline MLOps pour RAG Photographie

Pipeline MLOps complet pour automatiser, monitorer et améliorer le système RAG.

## 📋 Structure

```
mlops/
├── pipeline.py          # Pipeline principal avec Prefect
├── monitoring.py         # Système de monitoring et métriques
├── feedback_loop.py      # Boucle de feedback utilisateur
├── deploy.py            # Scripts de déploiement
├── tests/               # Tests automatisés
└── metrics/             # Métriques historiques
```

## 🔧 Installation

### 1. Installer Prefect

```bash
pip install prefect
```

### 2. Initialiser Prefect (optionnel, pour UI)

```bash
prefect server start
```

Ou utiliser Prefect Cloud (gratuit) :
```bash
prefect cloud login
```

## 🎯 Utilisation

### Exécuter le pipeline manuellement

```bash
python mlops/pipeline.py
```

### Exécuter avec Prefect

```bash
# Créer un flow
prefect deployment build mlops/pipeline.py:rag_mlops_pipeline -n rag-pipeline

# Appliquer le deployment
prefect deployment apply rag_mlops_pipeline-deployment.yaml

# Exécuter le flow
prefect deployment run rag-mlops-pipeline/rag-pipeline
```

### Planifier des exécutions automatiques

```python
# Dans pipeline.py, ajouter un schedule
from prefect.server.schemas.schedules import CronSchedule

deployment = Deployment.build_from_flow(
    flow=rag_mlops_pipeline,
    name="rag-pipeline-scheduled",
    schedule=CronSchedule(cron="0 2 * * *")  # Tous les jours à 2h
)
```

## 📊 Monitoring

### Vérifier les métriques

```bash
python mlops/monitoring.py
```

### Vérifier la santé du système

```python
from mlops.monitoring import HealthChecker

checker = HealthChecker()
health = checker.check_health()
print(health)
```

## 🔄 Feedback Loop

### Enregistrer un feedback utilisateur

```python
from mlops.feedback_loop import FeedbackCollector, UserFeedback
from datetime import datetime

collector = FeedbackCollector()

feedback = UserFeedback(
    timestamp=datetime.now().isoformat(),
    question="Qu'est-ce que l'ISO ?",
    answer="L'ISO est...",
    sources=["document1.pdf"],
    rating=4,
    feedback_text="Bonne réponse mais pourrait être plus détaillée",
    corrected_answer="L'ISO (International Organization for Standardization) est..."
)

collector.save_feedback(feedback)
```

### Vérifier si un retraining est nécessaire

```python
from mlops.feedback_loop import RetrainingPipeline

retraining = RetrainingPipeline()
if retraining.should_retrain():
    print("Retraining recommandé !")
    data = retraining.prepare_retraining_data()
```

## 📈 Métriques collectées

### Métriques Pipeline
- Nombre de documents traités
- Taux de réussite OCR
- Confiance moyenne OCR
- Temps d'exécution
- Validation des tests

### Métriques RAG
- Temps de réponse
- Longueur des réponses
- Nombre de sources utilisées
- Ratings utilisateurs
- Feedback textuel

## 🔍 Logs

Les logs sont enregistrés dans :
- `mlops/pipeline.log` : Logs du pipeline
- `mlops/metrics/` : Métriques JSON
- `mlops/feedback/` : Feedbacks utilisateurs

## 🧪 Tests

```bash
# Exécuter les tests
pytest mlops/tests/
```

## 📝 Workflow complet

1. **Collecte** : Détection automatique de nouveaux documents
2. **OCR** : Extraction de texte avec monitoring de qualité
3. **Post-traitement** : Correction et nettoyage
4. **Chunking** : Découpage intelligent
5. **Embeddings** : Génération et stockage
6. **Validation** : Tests automatiques
7. **Monitoring** : Enregistrement des métriques
8. **Feedback** : Collecte des retours utilisateurs
9. **Retraining** : Amélioration continue

## 🚀 Déploiement

### Local
```bash
python mlops/pipeline.py
```

### Production (avec Prefect)
```bash
prefect deployment apply rag_mlops_pipeline-deployment.yaml
```

### CI/CD
Intégrer dans GitHub Actions / GitLab CI pour exécution automatique.

## 📚 Documentation

- [Prefect Documentation](https://docs.prefect.io/)
- [MLOps Best Practices](https://ml-ops.org/)

