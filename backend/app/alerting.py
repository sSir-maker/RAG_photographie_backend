"""
Système d'alertes pour le monitoring.
"""

import logging
import os
import smtplib
import json
from typing import List, Dict, Any, Optional
from datetime import datetime, timedelta
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from enum import Enum

logger = logging.getLogger(__name__)


class AlertLevel(Enum):
    """Niveaux d'alerte."""

    INFO = "info"
    WARNING = "warning"
    ERROR = "error"
    CRITICAL = "critical"


class AlertChannel(Enum):
    """Canaux d'alerte."""

    LOG = "log"
    EMAIL = "email"
    WEBHOOK = "webhook"
    SLACK = "slack"  # Pour extension future


class Alert:
    """Représente une alerte."""

    def __init__(
        self,
        title: str,
        message: str,
        level: AlertLevel = AlertLevel.INFO,
        source: str = "system",
        metadata: Optional[Dict[str, Any]] = None,
    ):
        self.title = title
        self.message = message
        self.level = level
        self.source = source
        self.metadata = metadata or {}
        self.timestamp = datetime.utcnow()
        self.id = f"{self.timestamp.isoformat()}-{self.source}-{self.level.value}"


class AlertManager:
    """Gestionnaire d'alertes."""

    def __init__(self):
        self.alert_history: List[Alert] = []
        self.max_history = int(os.getenv("ALERT_MAX_HISTORY", "1000"))
        self.enabled_channels = self._load_enabled_channels()
        self.alert_thresholds = self._load_thresholds()
        self.last_alert_times: Dict[str, datetime] = {}
        self.alert_cooldown = timedelta(minutes=int(os.getenv("ALERT_COOLDOWN_MINUTES", "5")))

    def _load_enabled_channels(self) -> List[AlertChannel]:
        """Charge les canaux d'alerte activés."""
        channels_str = os.getenv("ALERT_CHANNELS", "log")
        channels = []
        for ch in channels_str.split(","):
            ch = ch.strip().lower()
            try:
                channels.append(AlertChannel(ch))
            except ValueError:
                logger.warning(f"Canal d'alerte inconnu: {ch}")
        return channels

    def _load_thresholds(self) -> Dict[str, Dict[str, float]]:
        """Charge les seuils d'alerte."""
        return {
            "error_rate": {
                "warning": float(os.getenv("ALERT_ERROR_RATE_WARNING", "0.05")),  # 5%
                "critical": float(os.getenv("ALERT_ERROR_RATE_CRITICAL", "0.10")),  # 10%
            },
            "response_time": {
                "warning": float(os.getenv("ALERT_RESPONSE_TIME_WARNING", "5.0")),  # 5s
                "critical": float(os.getenv("ALERT_RESPONSE_TIME_CRITICAL", "10.0")),  # 10s
            },
            "database_connections": {
                "warning": float(os.getenv("ALERT_DB_CONN_WARNING", "80")),  # 80%
                "critical": float(os.getenv("ALERT_DB_CONN_CRITICAL", "90")),  # 90%
            },
            "cache_hit_rate": {
                "warning": float(os.getenv("ALERT_CACHE_HIT_WARNING", "0.50")),  # 50%
                "critical": float(os.getenv("ALERT_CACHE_HIT_CRITICAL", "0.30")),  # 30%
            },
        }

    def send_alert(
        self,
        title: str,
        message: str,
        level: AlertLevel = AlertLevel.INFO,
        source: str = "system",
        metadata: Optional[Dict[str, Any]] = None,
    ) -> bool:
        """
        Envoie une alerte via les canaux configurés.

        Returns:
            True si l'alerte a été envoyée, False sinon
        """
        alert = Alert(title, message, level, source, metadata)

        # Vérifier le cooldown
        alert_key = f"{source}-{level.value}"
        if alert_key in self.last_alert_times:
            time_since_last = datetime.utcnow() - self.last_alert_times[alert_key]
            if time_since_last < self.alert_cooldown:
                logger.debug(f"Alerte en cooldown: {alert_key}")
                return False

        # Ajouter à l'historique
        self.alert_history.append(alert)
        if len(self.alert_history) > self.max_history:
            self.alert_history.pop(0)

        # Mettre à jour le timestamp
        self.last_alert_times[alert_key] = datetime.utcnow()

        # Envoyer via les canaux
        success = True
        for channel in self.enabled_channels:
            try:
                if channel == AlertChannel.LOG:
                    self._send_to_log(alert)
                elif channel == AlertChannel.EMAIL:
                    self._send_to_email(alert)
                elif channel == AlertChannel.WEBHOOK:
                    self._send_to_webhook(alert)
            except Exception as e:
                logger.error(f"Erreur envoi alerte via {channel.value}: {e}")
                success = False

        return success

    def _send_to_log(self, alert: Alert):
        """Envoie l'alerte aux logs."""
        log_level = {
            AlertLevel.INFO: logging.INFO,
            AlertLevel.WARNING: logging.WARNING,
            AlertLevel.ERROR: logging.ERROR,
            AlertLevel.CRITICAL: logging.CRITICAL,
        }.get(alert.level, logging.INFO)

        logger.log(
            log_level,
            f"[ALERT {alert.level.value.upper()}] {alert.title}: {alert.message}",
            extra={"alert_metadata": alert.metadata},
        )

    def _send_to_email(self, alert: Alert):
        """Envoie l'alerte par email."""
        smtp_host = os.getenv("SMTP_HOST")
        smtp_port = int(os.getenv("SMTP_PORT", "587"))
        smtp_user = os.getenv("SMTP_USER")
        smtp_password = os.getenv("SMTP_PASSWORD")
        alert_email_to = os.getenv("ALERT_EMAIL_TO", "").split(",")

        if not all([smtp_host, smtp_user, smtp_password, alert_email_to]):
            logger.warning("Configuration email incomplète. Alerte non envoyée.")
            return

        try:
            msg = MIMEMultipart()
            msg["From"] = smtp_user
            msg["To"] = ", ".join(alert_email_to)
            msg["Subject"] = f"[{alert.level.value.upper()}] {alert.title}"

            body = f"""
            Alerte: {alert.title}
            
            Message: {alert.message}
            
            Source: {alert.source}
            Niveau: {alert.level.value}
            Timestamp: {alert.timestamp.isoformat()}
            
            Métadonnées:
            {json.dumps(alert.metadata, indent=2)}
            """

            msg.attach(MIMEText(body, "plain"))

            with smtplib.SMTP(smtp_host, smtp_port) as server:
                server.starttls()
                server.login(smtp_user, smtp_password)
                server.send_message(msg)

            logger.info(f"Alerte envoyée par email: {alert.title}")
        except Exception as e:
            logger.error(f"Erreur envoi email: {e}")
            raise

    def _send_to_webhook(self, alert: Alert):
        """Envoie l'alerte à un webhook."""
        webhook_url = os.getenv("ALERT_WEBHOOK_URL")
        if not webhook_url:
            return

        try:
            import requests

            payload = {
                "title": alert.title,
                "message": alert.message,
                "level": alert.level.value,
                "source": alert.source,
                "timestamp": alert.timestamp.isoformat(),
                "metadata": alert.metadata,
            }

            response = requests.post(webhook_url, json=payload, timeout=5)
            response.raise_for_status()

            logger.info(f"Alerte envoyée au webhook: {alert.title}")
        except Exception as e:
            logger.error(f"Erreur envoi webhook: {e}")
            raise

    def check_thresholds(self, metrics: Dict[str, float]) -> List[Alert]:
        """
        Vérifie les seuils et génère des alertes si nécessaire.

        Args:
            metrics: Dictionnaire de métriques (ex: {"error_rate": 0.15, "response_time": 8.5})

        Returns:
            Liste des alertes générées
        """
        alerts = []

        for metric_name, value in metrics.items():
            if metric_name not in self.alert_thresholds:
                continue

            thresholds = self.alert_thresholds[metric_name]

            # Déterminer le niveau d'alerte
            level = None
            if "critical" in thresholds and value >= thresholds["critical"]:
                level = AlertLevel.CRITICAL
            elif "warning" in thresholds and value >= thresholds["warning"]:
                level = AlertLevel.WARNING

            if level:
                alert = Alert(
                    title=f"Seuil dépassé: {metric_name}",
                    message=f"La métrique {metric_name} a atteint {value} (seuil {level.value}: {thresholds.get(level.value, 'N/A')})",
                    level=level,
                    source="threshold_monitor",
                    metadata={"metric": metric_name, "value": value, "thresholds": thresholds},
                )
                alerts.append(alert)
                self.send_alert(alert.title, alert.message, alert.level, alert.source, alert.metadata)

        return alerts

    def get_recent_alerts(self, hours: int = 24, level: Optional[AlertLevel] = None) -> List[Alert]:
        """Récupère les alertes récentes."""
        cutoff = datetime.utcnow() - timedelta(hours=hours)
        alerts = [a for a in self.alert_history if a.timestamp >= cutoff]

        if level:
            alerts = [a for a in alerts if a.level == level]

        return sorted(alerts, key=lambda x: x.timestamp, reverse=True)


# Instance globale
_alert_manager: Optional[AlertManager] = None


def get_alert_manager() -> AlertManager:
    """Récupère l'instance globale du gestionnaire d'alertes."""
    global _alert_manager
    if _alert_manager is None:
        _alert_manager = AlertManager()
    return _alert_manager
