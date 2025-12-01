"""
Module de sécurité : sanitization, validation, secrets management.
"""

import os
import re
import html
import secrets
from typing import Optional, Dict, Any, Tuple
from pathlib import Path
import json
import logging

try:
    from cryptography.fernet import Fernet

    CRYPTOGRAPHY_AVAILABLE = True
except ImportError:
    CRYPTOGRAPHY_AVAILABLE = False
    Fernet = None

logger = logging.getLogger(__name__)


class SecretsManager:
    """Gestionnaire centralisé des secrets."""

    def __init__(self, secrets_file: Optional[Path] = None):
        """
        Initialise le gestionnaire de secrets.

        Args:
            secrets_file: Chemin vers le fichier de secrets (optionnel)
        """
        self.secrets_file = secrets_file or Path(__file__).parent.parent / ".secrets"
        self._secrets: Dict[str, str] = {}
        self._cipher: Optional[Fernet] = None
        self._load_secrets()

    def _get_encryption_key(self) -> Optional[bytes]:
        """Génère ou récupère la clé de chiffrement."""
        if not CRYPTOGRAPHY_AVAILABLE:
            return None

        key_file = self.secrets_file.parent / ".encryption_key"

        if key_file.exists():
            return key_file.read_bytes()
        else:
            # Générer une nouvelle clé
            key = Fernet.generate_key()
            key_file.write_bytes(key)
            try:
                key_file.chmod(0o600)  # Permissions restrictives (Unix)
            except:
                pass  # Windows n'a pas chmod
            return key

    def _load_secrets(self):
        """Charge les secrets depuis le fichier ou les variables d'environnement."""
        # Priorité 1: Variables d'environnement
        self._secrets = {
            "SECRET_KEY": os.getenv("SECRET_KEY"),
            "DATABASE_URL": os.getenv("DATABASE_URL"),
            "JWT_SECRET": os.getenv("JWT_SECRET") or os.getenv("SECRET_KEY"),
        }

        # Priorité 2: Fichier .secrets (si existe)
        if self.secrets_file.exists() and CRYPTOGRAPHY_AVAILABLE:
            try:
                key = self._get_encryption_key()
                if key:
                    self._cipher = Fernet(key)

                    encrypted_data = self.secrets_file.read_bytes()
                    decrypted_data = self._cipher.decrypt(encrypted_data)
                    file_secrets = json.loads(decrypted_data.decode())

                    # Merger avec les secrets existants (env prend priorité)
                    for k, v in file_secrets.items():
                        if k not in self._secrets or self._secrets[k] is None:
                            self._secrets[k] = v
            except Exception as e:
                logger.warning(f"Impossible de charger les secrets depuis le fichier: {e}")

    def get(self, key: str, default: Optional[str] = None) -> Optional[str]:
        """Récupère un secret."""
        return self._secrets.get(key, default)

    def set(self, key: str, value: str, save: bool = False):
        """Définit un secret (optionnellement sauvegardé)."""
        self._secrets[key] = value
        if save:
            self._save_secrets()

    def _save_secrets(self):
        """Sauvegarde les secrets dans le fichier chiffré."""
        if not CRYPTOGRAPHY_AVAILABLE:
            logger.warning("Cryptography non disponible, secrets non chiffrés")
            return

        if not self._cipher:
            key = self._get_encryption_key()
            if key:
                self._cipher = Fernet(key)
            else:
                logger.warning("Impossible de générer la clé de chiffrement")
                return

        encrypted_data = self._cipher.encrypt(json.dumps(self._secrets).encode())
        self.secrets_file.write_bytes(encrypted_data)
        try:
            self.secrets_file.chmod(0o600)  # Permissions restrictives (Unix)
        except:
            pass  # Windows n'a pas chmod


# Instance globale
_secrets_manager: Optional[SecretsManager] = None


def get_secrets_manager() -> SecretsManager:
    """Récupère l'instance globale du gestionnaire de secrets."""
    global _secrets_manager
    if _secrets_manager is None:
        _secrets_manager = SecretsManager()
    return _secrets_manager


class InputSanitizer:
    """Classe pour sanitizer et valider les entrées utilisateur."""

    # Patterns dangereux
    DANGEROUS_PATTERNS = [
        (r"<script[^>]*>.*?</script>", "Script tags"),
        (r"javascript:", "JavaScript protocol"),
        (r"on\w+\s*=", "Event handlers"),
        (r"data:text/html", "Data URI HTML"),
        (r"vbscript:", "VBScript protocol"),
    ]

    # Caractères SQL injection courants
    SQL_INJECTION_PATTERNS = [
        (r"('|(\\')|(;)|(--)|(\*)|(\%))", "SQL injection attempt"),
    ]

    @staticmethod
    def sanitize_text(text: str, max_length: Optional[int] = None) -> str:
        """
        Nettoie et sanitize un texte.

        Args:
            text: Texte à nettoyer
            max_length: Longueur maximale (optionnel)

        Returns:
            Texte nettoyé
        """
        if not isinstance(text, str):
            text = str(text)

        # Échapper les caractères HTML
        text = html.escape(text)

        # Supprimer les patterns dangereux
        for pattern, description in InputSanitizer.DANGEROUS_PATTERNS:
            text = re.sub(pattern, "", text, flags=re.IGNORECASE | re.DOTALL)

        # Supprimer les tentatives SQL injection
        for pattern, description in InputSanitizer.SQL_INJECTION_PATTERNS:
            text = re.sub(pattern, "", text, flags=re.IGNORECASE)

        # Normaliser les espaces
        text = re.sub(r"\s+", " ", text).strip()

        # Limiter la longueur
        if max_length and len(text) > max_length:
            text = text[:max_length]
            logger.warning(f"Texte tronqué à {max_length} caractères")

        return text

    @staticmethod
    def sanitize_email(email: str) -> str:
        """Sanitize une adresse email."""
        email = email.strip().lower()
        # Validation basique
        if not re.match(r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$", email):
            raise ValueError("Format d'email invalide")
        return email

    @staticmethod
    def sanitize_question(question: str) -> str:
        """Sanitize une question pour le RAG."""
        # Nettoyer mais garder la structure
        question = InputSanitizer.sanitize_text(question, max_length=1000)

        # Vérifier qu'il reste du contenu
        if len(question.strip()) < 3:
            raise ValueError("La question est trop courte")

        return question

    @staticmethod
    def validate_password(password: str) -> Tuple[bool, Optional[str]]:
        """
        Valide un mot de passe.

        Returns:
            (is_valid, error_message)
        """
        if len(password) < 8:
            return False, "Le mot de passe doit contenir au moins 8 caractères"

        if len(password) > 72:  # Limite bcrypt
            return False, "Le mot de passe est trop long (max 72 caractères)"

        if not re.search(r"[A-Za-z]", password):
            return False, "Le mot de passe doit contenir au moins une lettre"

        if not re.search(r"[0-9]", password):
            return False, "Le mot de passe doit contenir au moins un chiffre"

        return True, None


def generate_secret_key(length: int = 32) -> str:
    """Génère une clé secrète sécurisée."""
    return secrets.token_urlsafe(length)


# Instance globale du sanitizer
input_sanitizer = InputSanitizer()
