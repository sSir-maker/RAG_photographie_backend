# 🚀 Guide MLOps pour RAG Photographie

Guide complet pour utiliser le pipeline MLOps du système RAG.

## 📋 Vue d'ensemble

Le pipeline MLOps automatise le cycle de vie complet du RAG :
- **Collecte** et traitement des documents
- **Monitoring** des performances
- **Feedback** utilisateur
- **Retraining** automatique

## 🎯 Architecture du Pipeline

```
┌─────────────────────────────────────────────────────────────┐
│                    PIPELINE MLOPS RAG                       │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  1. Collecte Documents  →  2. OCR Extraction               │
│         ↓                        ↓                          │
│  3. Post-traitement    →  4. Chunking Intelligent          │
│         ↓                        ↓                          │
│  5. Génération Embeddings → 6. Validation                 │
│         ↓                        ↓                          │
│  7. Monitoring & Métriques                                  │
│                                                              │
└─────────────────────────────────────────────────────────────┘
         ↓
┌─────────────────────────────────────────────────────────────┐
│              FEEDBACK LOOP & RETRAINING                    │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  Collecte Feedback → Analyse → Retraining                  │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

## 🚀 Démarrage rapide

### 1. Installation

```bash
# Installer Prefect
pip install prefect>=2.14.0

# Vérifier l'installation
prefect version
```

### 2. Premier lancement

```bash
# Exécuter le pipeline manuellement
python mlops/pipeline.py
```

### 3. Vérifier les résultats

```bash
# Voir les métriques
python mlops/monitoring.py

# Vérifier la santé du système
python -c "from mlops.monitoring import HealthChecker; import json; print(json.dumps(HealthChecker().check_health(), indent=2))"
```

## 📊 Monitoring

### Métriques collectées

Le système collecte automatiquement :

**Pipeline :**
- Nombre de documents traités
- Taux de réussite OCR
- Confiance moyenne OCR
- Temps d'exécution
- Résultats des tests de validation

**RAG :**
- Temps de réponse par requête
- Longueur des réponses
- Nombre de sources utilisées
- Ratings utilisateurs (1-5)
- Feedback textuel

### Consulter les métriques

```python
from mlops.monitoring import MetricsCollector

collector = MetricsCollector()

# Statistiques des 7 derniers jours
stats = collector.get_statistics(days=7)
print(f"Runs pipeline: {stats['pipeline_runs']}")
print(f"Requêtes RAG: {stats['rag_queries']}")
print(f"Taux de succès: {stats['pipeline']['success_rate']:.1f}%")
```

## 🔄 Feedback Loop

### Enregistrer un feedback

Dans ton API (`app/api.py`), tu peux ajouter :

```python
from mlops.feedback_loop import FeedbackCollector, UserFeedback
from datetime import datetime

@app.post("/feedback")
async def submit_feedback(
    question: str,
    answer: str,
    rating: int,
    feedback_text: Optional[str] = None,
    corrected_answer: Optional[str] = None
):
    collector = FeedbackCollector()
    
    feedback = UserFeedback(
        timestamp=datetime.now().isoformat(),
        question=question,
        answer=answer,
        sources=[],
        rating=rating,
        feedback_text=feedback_text,
        corrected_answer=corrected_answer
    )
    
    collector.save_feedback(feedback)
    return {"status": "success"}
```

### Vérifier si retraining nécessaire

```python
from mlops.feedback_loop import RetrainingPipeline

retraining = RetrainingPipeline()

if retraining.should_retrain(min_feedbacks=10, min_avg_rating=3.0):
    print("⚠️ Retraining recommandé !")
    data = retraining.prepare_retraining_data()
    print(f"📊 {data['training_examples']} exemples prêts")
```

## ⏰ Planification automatique

### Avec Prefect (recommandé)

```python
# Créer un deployment avec schedule
from prefect.deployments import Deployment
from prefect.server.schemas.schedules import CronSchedule
from mlops.pipeline import rag_mlops_pipeline

deployment = Deployment.build_from_flow(
    flow=rag_mlops_pipeline,
    name="rag-pipeline-daily",
    schedule=CronSchedule(cron="0 2 * * *"),  # Tous les jours à 2h
    work_queue_name="production"
)

if __name__ == "__main__":
    deployment.apply()
```

### Avec cron (Linux/Mac)

```bash
# Éditer crontab
crontab -e

# Ajouter (tous les jours à 2h)
0 2 * * * cd /path/to/RAG-Photographie && python mlops/pipeline.py
```

### Avec Task Scheduler (Windows)

1. Ouvrir "Planificateur de tâches"
2. Créer une tâche de base
3. Déclencheur : Quotidien à 2h
4. Action : Exécuter `python mlops/pipeline.py`

## 🧪 Tests et Validation

Le pipeline inclut des tests automatiques :

```python
# Tests de validation intégrés
validation_results = validate_pipeline_task(embedding_results)

if validation_results["all_passed"]:
    print("✅ Tous les tests passés")
else:
    print("❌ Certains tests ont échoué")
```

## 📈 Amélioration continue

### Workflow recommandé

1. **Collecte de feedback** : Les utilisateurs notent les réponses
2. **Analyse** : Le système détecte les patterns
3. **Retraining** : Quand suffisamment de feedbacks sont collectés
4. **Déploiement** : Nouveau modèle déployé
5. **Monitoring** : Suivi des performances

### Seuils recommandés

- **Retraining** : 
  - Minimum 10 feedbacks
  - Rating moyen < 3.0
  - Ou > 20% de corrections

- **Alerte** :
  - Rating moyen < 2.5
  - Taux de succès pipeline < 80%

## 🔍 Dépannage

### Pipeline échoue

```bash
# Vérifier les logs
tail -f mlops/pipeline.log

# Vérifier la santé
python -c "from mlops.monitoring import HealthChecker; print(HealthChecker().check_health())"
```

### Métriques manquantes

```bash
# Vérifier que le dossier existe
ls -la mlops/metrics/

# Vérifier les permissions
chmod -R 755 mlops/
```

## 📚 Ressources

- [Documentation Prefect](https://docs.prefect.io/)
- [MLOps Best Practices](https://ml-ops.org/)
- [Monitoring MLOps](https://neptune.ai/blog/mlops-monitoring)

## 🎓 Prochaines étapes

1. ✅ Configurer Prefect
2. ✅ Planifier des exécutions automatiques
3. ✅ Intégrer le feedback dans l'API
4. ✅ Configurer des alertes
5. ✅ Mettre en place le retraining automatique

