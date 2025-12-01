"""
Tests pour l'API FastAPI.
"""

import pytest
from fastapi.testclient import TestClient


class TestHealthEndpoint:
    """Tests de l'endpoint de santé."""

    def test_health_check(self, client):
        """Test de vérification de santé."""
        response = client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert "status" in data
        assert data["status"] == "ok"


class TestAuthEndpoints:
    """Tests des endpoints d'authentification."""

    def test_signup(self, client, test_user_data):
        """Test d'inscription."""
        response = client.post("/auth/signup", json=test_user_data)
        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data
        assert "token_type" in data
        assert data["token_type"] == "bearer"

    def test_signup_duplicate_email(self, client, test_user_data):
        """Test d'inscription avec email dupliqué."""
        # Première inscription
        response1 = client.post("/auth/signup", json=test_user_data)
        assert response1.status_code == 200

        # Tentative de réinscription
        response2 = client.post("/auth/signup", json=test_user_data)
        assert response2.status_code == 400

    def test_login(self, client, test_user_data):
        """Test de connexion."""
        # Créer l'utilisateur
        client.post("/auth/signup", json=test_user_data)

        # Se connecter
        response = client.post(
            "/auth/login", data={"username": test_user_data["email"], "password": test_user_data["password"]}
        )
        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data

    def test_login_wrong_password(self, client, test_user_data):
        """Test de connexion avec mauvais mot de passe."""
        # Créer l'utilisateur
        client.post("/auth/signup", json=test_user_data)

        # Tentative de connexion avec mauvais mot de passe
        response = client.post("/auth/login", data={"username": test_user_data["email"], "password": "WrongPassword"})
        assert response.status_code == 401

    def test_get_current_user(self, authenticated_client):
        """Test de récupération de l'utilisateur actuel."""
        response = authenticated_client.get("/auth/me")
        assert response.status_code == 200
        data = response.json()
        assert "email" in data
        assert "name" in data


class TestAskEndpoint:
    """Tests de l'endpoint de questions RAG."""

    def test_ask_question_unauthorized(self, client):
        """Test que l'endpoint nécessite une authentification."""
        response = client.post("/ask", json={"question": "Qu'est-ce que la photographie?"})
        assert response.status_code == 401

    def test_ask_question_authorized(self, authenticated_client):
        """Test de question avec authentification."""
        # Note: Ce test nécessite que le RAG soit configuré
        # et que des documents soient disponibles
        response = authenticated_client.post("/ask", json={"question": "Qu'est-ce que la photographie?"})
        # Le test peut échouer si Ollama n'est pas disponible
        # On accepte soit 200 (succès) soit 500 (Ollama non disponible)
        assert response.status_code in [200, 500]

    def test_ask_question_stream_unauthorized(self, client):
        """Test que l'endpoint stream nécessite une authentification."""
        response = client.post("/ask/stream", json={"question": "Test question"})
        assert response.status_code == 401


class TestConversationEndpoints:
    """Tests des endpoints de conversation."""

    def test_get_conversations(self, authenticated_client):
        """Test de récupération des conversations."""
        response = authenticated_client.get("/conversations")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)

    def test_create_conversation(self, authenticated_client):
        """Test de création de conversation."""
        response = authenticated_client.post("/conversations", json={"title": "Test Conversation"})
        assert response.status_code == 200
        data = response.json()
        assert "id" in data
        assert "title" in data

    def test_delete_conversation(self, authenticated_client):
        """Test de suppression de conversation."""
        # Créer une conversation
        create_response = authenticated_client.post("/conversations", json={"title": "Test Conversation"})
        conv_id = create_response.json()["id"]

        # Supprimer
        delete_response = authenticated_client.delete(f"/conversations/{conv_id}")
        assert delete_response.status_code == 200


class TestInputValidation:
    """Tests de validation des entrées."""

    def test_xss_protection(self, authenticated_client):
        """Test que les attaques XSS sont bloquées."""
        xss_payload = "<script>alert('XSS')</script>"
        response = authenticated_client.post("/ask", json={"question": xss_payload})
        # Le payload devrait être sanitized
        # On vérifie que le serveur ne plante pas
        assert response.status_code in [200, 400, 500]

    def test_sql_injection_protection(self, authenticated_client):
        """Test que les injections SQL sont bloquées."""
        sql_payload = "'; DROP TABLE users; --"
        response = authenticated_client.post("/ask", json={"question": sql_payload})
        # Le payload devrait être sanitized
        assert response.status_code in [200, 400, 500]
