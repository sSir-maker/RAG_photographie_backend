# 🏥 Configuration du Dashboard de Santé

## 📋 Vue d'ensemble

Le dashboard de santé fournit une vue d'ensemble de l'état du système en temps réel.

## 🔗 Endpoints

### Santé basique

```bash
GET /health
```

Retourne :
```json
{
  "status": "healthy",
  "timestamp": "2024-01-01T12:00:00",
  "uptime_seconds": 3600,
  "services": {
    "database": {
      "status": "healthy",
      "connected": true,
      "response_time_ms": 5.2
    },
    "cache": {
      "status": "healthy",
      "enabled": true,
      "connected": true,
      "response_time_ms": 1.5
    },
    "llm": {
      "status": "healthy",
      "available": true,
      "response_time_ms": 500.0
    }
  },
  "metrics": {
    "requests": {
      "total": 1000,
      "success": 950,
      "errors": 50,
      "error_rate": 0.05,
      "success_rate": 0.95
    }
  },
  "alerts": {
    "recent_count": 2,
    "critical_count": 0,
    "error_count": 1,
    "recent": [...]
  }
}
```

### Santé détaillée

```bash
GET /health/detailed
```

Inclut des métriques supplémentaires :
- Statistiques détaillées des timers
- Histogrammes complets
- Métriques système avancées

## 🎨 Frontend

Un composant React `HealthDashboard` est disponible dans `frontend_RAG/src/components/HealthDashboard.tsx`.

### Utilisation

```tsx
import HealthDashboard from "./components/HealthDashboard";

function App() {
  return (
    <div>
      <HealthDashboard />
    </div>
  );
}
```

## 📊 Statuts Possibles

- **healthy** : Tout fonctionne correctement
- **degraded** : Certains services sont en panne mais le système fonctionne
- **unhealthy** : Problèmes critiques détectés
- **critical** : Alertes critiques actives

## 🔍 Vérifications Effectuées

### Base de données

- Connexion active
- Temps de réponse
- Pool de connexions (PostgreSQL)
- Connexions actives

### Cache Redis

- Connexion active
- Temps de réponse
- Disponibilité

### LLM (Ollama)

- Service disponible
- Temps de réponse
- Modèles chargés

## 📈 Métriques Affichées

- **Requêtes** : Total, succès, erreurs, taux
- **Performance** : Temps de réponse, percentiles
- **Alertes** : Compteurs par niveau
- **Uptime** : Temps de fonctionnement

## 🔔 Intégration avec Alertes

Le dashboard affiche automatiquement :
- Alertes récentes (dernière heure)
- Compteurs par niveau (critical, error, warning)
- Détails des alertes

## 🚀 Monitoring Continu

Le dashboard peut être rafraîchi automatiquement :

```tsx
// Rafraîchissement toutes les 30 secondes
useEffect(() => {
  const interval = setInterval(fetchHealth, 30000);
  return () => clearInterval(interval);
}, []);
```

## ✅ Checklist

- [ ] Endpoint `/health` accessible
- [ ] Endpoint `/health/detailed` accessible
- [ ] Composant React intégré (optionnel)
- [ ] Alertes visibles dans le dashboard
- [ ] Métriques affichées correctement

---

**✅ Dashboard de santé configuré !**

