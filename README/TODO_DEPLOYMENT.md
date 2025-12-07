# ✅ TODO - Déploiement Production

## 🔴 Priorité HAUTE (15% - 15-20h)

### 1. Rate Limiting ⏱️ 2h
```bash
pip install slowapi
```
- [ ] Ajouter slowapi dans requirements.txt
- [ ] Implémenter rate limiting dans app/api.py
- [ ] Configurer limites par endpoint
- [ ] Tester avec plusieurs requêtes

### 2. PostgreSQL ⏱️ 4h
- [ ] Installer psycopg2 dans requirements.txt
- [ ] Créer fichier .env avec DATABASE_URL PostgreSQL
- [ ] Modifier app/database.py pour supporter PostgreSQL
- [ ] Créer script de migration
- [ ] Tester la connexion
- [ ] Migrer les données depuis SQLite

### 3. Tests Critiques ⏱️ 6h
- [ ] Tests unitaires pour auth (2h)
- [ ] Tests unitaires pour RAG pipeline (2h)
- [ ] Tests d'intégration API (2h)
- [ ] Configurer pytest
- [ ] Ajouter coverage

### 4. HTTPS/SSL ⏱️ 2h
- [ ] Configurer certificat SSL (Let's Encrypt)
- [ ] Configurer reverse proxy (Nginx/Traefik)
- [ ] Rediriger HTTP vers HTTPS
- [ ] Tester la connexion sécurisée

### 5. Backup Automatisé ⏱️ 2h
- [ ] Script de backup base de données
- [ ] Script de backup vector store
- [ ] Configurer cron job / scheduled task
- [ ] Tester la restauration

---

## 🟡 Priorité MOYENNE (7% - 10-15h)

### 6. Cache Redis ⏱️ 4h
- [ ] Installer redis dans requirements.txt
- [ ] Configurer connexion Redis
- [ ] Implémenter cache pour embeddings
- [ ] Implémenter cache pour réponses fréquentes
- [ ] Tester les performances

### 7. CI/CD Pipeline ⏱️ 5h
- [ ] Créer .github/workflows/ci.yml
- [ ] Configurer tests automatisés
- [ ] Configurer linting (black, flake8)
- [ ] Configurer déploiement automatique
- [ ] Tester le pipeline

### 8. Monitoring Avancé ⏱️ 3h
- [ ] Configurer alertes Phoenix
- [ ] Ajouter métriques custom
- [ ] Dashboard de santé
- [ ] Configurer notifications (email/Slack)

### 9. Optimisations Performance ⏱️ 3h
- [ ] Database connection pooling
- [ ] Optimiser les requêtes SQL
- [ ] Lazy loading des embeddings
- [ ] Compression des réponses

---

## 🟢 Priorité BASSE (3% - Variable)

### 10. Features Additionnelles
- [ ] Export conversations (PDF/JSON)
- [ ] Recherche dans historique
- [ ] Partage de conversations
- [ ] Multi-LLM support
- [ ] Thèmes personnalisables

---

## 📝 Checklist Déploiement

### Avant le déploiement :
- [ ] Tous les tests passent
- [ ] Rate limiting activé
- [ ] PostgreSQL configuré
- [ ] HTTPS configuré
- [ ] Secrets dans variables d'environnement
- [ ] Backup configuré
- [ ] Monitoring actif
- [ ] Documentation à jour

### Après le déploiement :
- [ ] Vérifier que l'API répond
- [ ] Vérifier que le frontend se connecte
- [ ] Vérifier Phoenix monitoring
- [ ] Tester l'authentification
- [ ] Tester une requête RAG
- [ ] Vérifier les logs
- [ ] Vérifier les métriques

---

## 🎯 Objectif : MVP Production Ready

**Temps estimé** : 12-15 heures  
**Priorité** : Phase 1 uniquement

Une fois ces 5 tâches critiques complétées, le projet sera prêt pour un déploiement MVP en production.

