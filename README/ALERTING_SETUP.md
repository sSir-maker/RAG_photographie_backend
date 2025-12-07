# 🚨 Configuration du Système d'Alertes

## 📋 Vue d'ensemble

Le système d'alertes permet de notifier automatiquement en cas de problèmes ou de seuils dépassés.

## 🔧 Configuration

### Variables d'environnement

Dans `.env` :

```env
# Canaux d'alerte (séparés par virgule)
ALERT_CHANNELS=log,email,webhook

# Cooldown entre alertes (minutes)
ALERT_COOLDOWN_MINUTES=5

# Seuils d'alerte
ALERT_ERROR_RATE_WARNING=0.05    # 5%
ALERT_ERROR_RATE_CRITICAL=0.10   # 10%
ALERT_RESPONSE_TIME_WARNING=5.0  # 5 secondes
ALERT_RESPONSE_TIME_CRITICAL=10.0 # 10 secondes
ALERT_DB_CONN_WARNING=80         # 80% du pool
ALERT_DB_CONN_CRITICAL=90        # 90% du pool
ALERT_CACHE_HIT_WARNING=0.50     # 50%
ALERT_CACHE_HIT_CRITICAL=0.30    # 30%

# Email (si ALERT_CHANNELS contient "email")
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=ton-email@gmail.com
SMTP_PASSWORD=ton-mot-de-passe-app
ALERT_EMAIL_TO=admin@example.com,dev@example.com

# Webhook (si ALERT_CHANNELS contient "webhook")
ALERT_WEBHOOK_URL=https://hooks.slack.com/services/YOUR/WEBHOOK/URL
```

## 📧 Configuration Email

### Gmail

1. Activer l'authentification à deux facteurs
2. Générer un mot de passe d'application :
   - https://myaccount.google.com/apppasswords
3. Utiliser ce mot de passe dans `SMTP_PASSWORD`

### Autres providers

- **Outlook** : `smtp-mail.outlook.com:587`
- **SendGrid** : `smtp.sendgrid.net:587`
- **Mailgun** : `smtp.mailgun.org:587`

## 🔗 Configuration Webhook

### Slack

1. Créer un webhook : https://api.slack.com/messaging/webhooks
2. Copier l'URL dans `ALERT_WEBHOOK_URL`

### Discord

1. Créer un webhook dans les paramètres du serveur
2. Utiliser l'URL du webhook

### Custom

Le webhook doit accepter un POST JSON avec :
```json
{
  "title": "Titre de l'alerte",
  "message": "Message",
  "level": "error",
  "source": "rag_api",
  "timestamp": "2024-01-01T12:00:00",
  "metadata": {}
}
```

## 🚀 Utilisation

### Envoyer une alerte manuellement

```python
from app.alerting import get_alert_manager, AlertLevel

alerts = get_alert_manager()
alerts.send_alert(
    title="Problème détecté",
    message="Description du problème",
    level=AlertLevel.ERROR,
    source="mon_module",
    metadata={"key": "value"}
)
```

### Vérifier les seuils automatiquement

```python
from app.alerting import get_alert_manager

alerts = get_alert_manager()
metrics = {
    "error_rate": 0.15,  # 15% d'erreurs
    "response_time": 8.5,  # 8.5 secondes
}

# Génère automatiquement des alertes si seuils dépassés
alerts.check_thresholds(metrics)
```

### Récupérer les alertes récentes

```python
from app.alerting import get_alert_manager, AlertLevel

alerts = get_alert_manager()
recent = alerts.get_recent_alerts(hours=24, level=AlertLevel.ERROR)
```

## 📊 Niveaux d'Alerte

- **INFO** : Information générale
- **WARNING** : Avertissement (seuil warning dépassé)
- **ERROR** : Erreur (seuil critical dépassé, erreur système)
- **CRITICAL** : Critique (système down, données perdues)

## ✅ Checklist

- [ ] Variables d'environnement configurées
- [ ] Email configuré (si utilisé)
- [ ] Webhook configuré (si utilisé)
- [ ] Seuils ajustés selon les besoins
- [ ] Test d'envoi d'alerte réussi

---

**✅ Système d'alertes configuré !**

