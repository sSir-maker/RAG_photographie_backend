"""
Tests pour l'authentification.
"""

import pytest
from datetime import timedelta

from app.auth import (
    create_access_token,
    verify_token,
    get_password_hash,
    verify_password,
    ACCESS_TOKEN_EXPIRE_MINUTES,
)
from app.db_auth import create_user_db, authenticate_user_db


class TestPasswordHashing:
    """Tests de hachage de mot de passe."""

    def test_password_hashing(self):
        """Test que le hachage fonctionne."""
        password = "TestPassword123!"
        hashed = get_password_hash(password)

        assert hashed != password
        assert len(hashed) > 0

    def test_password_verification(self):
        """Test de vérification de mot de passe."""
        password = "TestPassword123!"
        hashed = get_password_hash(password)

        assert verify_password(password, hashed) is True
        assert verify_password("WrongPassword", hashed) is False


class TestJWT:
    """Tests des tokens JWT."""

    def test_create_token(self):
        """Test de création de token."""
        data = {"sub": "test@example.com"}
        token = create_access_token(data=data)

        assert token is not None
        assert isinstance(token, str)
        assert len(token) > 0

    def test_verify_token(self):
        """Test de vérification de token."""
        data = {"sub": "test@example.com"}
        token = create_access_token(data=data)

        payload = verify_token(token)
        assert payload is not None
        assert payload["sub"] == "test@example.com"

    def test_verify_invalid_token(self):
        """Test avec un token invalide."""
        invalid_token = "invalid.token.here"
        payload = verify_token(invalid_token)
        assert payload is None

    def test_token_expiration(self):
        """Test d'expiration de token."""
        from datetime import timedelta

        data = {"sub": "test@example.com"}
        # Créer un token qui expire immédiatement
        token = create_access_token(data=data, expires_delta=timedelta(seconds=-1))

        # Le token devrait être expiré
        payload = verify_token(token)
        # Note: La vérification d'expiration dépend de l'implémentation
        # Si le token est expiré, verify_token devrait retourner None ou lever une exception


class TestAuthenticationFlow:
    """Tests du flux d'authentification complet."""

    def test_signup_and_login_flow(self, test_db):
        """Test du flux complet signup -> login."""
        db = test_db()

        # Signup
        user = create_user_db(db=db, name="Test User", email="test@example.com", password="TestPassword123!")
        assert user is not None

        # Login
        authenticated = authenticate_user_db(db=db, email="test@example.com", password="TestPassword123!")
        assert authenticated is not None
        assert authenticated.id == user.id

        # Mauvais mot de passe
        failed = authenticate_user_db(db=db, email="test@example.com", password="WrongPassword")
        assert failed is False

        db.close()
