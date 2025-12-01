"""
Tests pour la base de données.
"""

import pytest
from sqlalchemy.orm import Session
from datetime import datetime

from app.database import User, Conversation, Message, init_db, check_db_connection
from app.db_auth import create_user_db, authenticate_user_db, get_user_by_email
from app.db_chat import (
    create_conversation,
    get_user_conversations,
    get_conversation,
    delete_conversation,
    add_message,
    get_conversation_messages,
)


class TestDatabaseConnection:
    """Tests de connexion à la base de données."""

    def test_check_db_connection(self, test_db):
        """Test de vérification de connexion."""
        assert check_db_connection() is True


class TestUserModel:
    """Tests du modèle User."""

    def test_create_user(self, test_db):
        """Test de création d'utilisateur."""
        db = test_db()
        user = create_user_db(db=db, name="Test User", email="test@example.com", password="TestPassword123!")
        assert user is not None
        assert user.id is not None
        assert user.email == "test@example.com"
        assert user.name == "Test User"
        db.close()

    def test_authenticate_user(self, test_db):
        """Test d'authentification utilisateur."""
        db = test_db()
        # Créer l'utilisateur
        user = create_user_db(db=db, name="Test User", email="test@example.com", password="TestPassword123!")

        # Authentifier
        authenticated = authenticate_user_db(db=db, email="test@example.com", password="TestPassword123!")
        assert authenticated is not None
        assert authenticated.id == user.id

        # Mauvais mot de passe
        failed = authenticate_user_db(db=db, email="test@example.com", password="WrongPassword")
        assert failed is False
        db.close()

    def test_get_user_by_email(self, test_db):
        """Test de récupération d'utilisateur par email."""
        db = test_db()
        user = create_user_db(db=db, name="Test User", email="test@example.com", password="TestPassword123!")

        found_user = get_user_by_email(db=db, email="test@example.com")
        assert found_user is not None
        assert found_user.id == user.id

        # Utilisateur inexistant
        not_found = get_user_by_email(db=db, email="nonexistent@example.com")
        assert not_found is None
        db.close()

    def test_duplicate_email(self, test_db):
        """Test que l'email doit être unique."""
        db = test_db()
        create_user_db(db=db, name="Test User 1", email="test@example.com", password="TestPassword123!")

        # Tentative de créer un utilisateur avec le même email
        with pytest.raises(Exception):  # SQLAlchemy devrait lever une exception
            create_user_db(db=db, name="Test User 2", email="test@example.com", password="TestPassword123!")
        db.close()


class TestConversationModel:
    """Tests du modèle Conversation."""

    def test_create_conversation(self, test_db):
        """Test de création de conversation."""
        db = test_db()
        # Créer un utilisateur
        user = create_user_db(db=db, name="Test User", email="test@example.com", password="TestPassword123!")

        # Créer une conversation
        conversation = create_conversation(db=db, user_id=user.id, title="Test Conversation")
        assert conversation is not None
        assert conversation.id is not None
        assert conversation.user_id == user.id
        assert conversation.title == "Test Conversation"
        db.close()

    def test_get_user_conversations(self, test_db):
        """Test de récupération des conversations d'un utilisateur."""
        db = test_db()
        user = create_user_db(db=db, name="Test User", email="test@example.com", password="TestPassword123!")

        # Créer plusieurs conversations
        conv1 = create_conversation(db=db, user_id=user.id, title="Conv 1")
        conv2 = create_conversation(db=db, user_id=user.id, title="Conv 2")

        conversations = get_user_conversations(db=db, user_id=user.id)
        assert len(conversations) == 2
        assert conv1.id in [c.id for c in conversations]
        assert conv2.id in [c.id for c in conversations]

        # Vérifier l'ordre (plus récent en premier)
        assert conversations[0].updated_at >= conversations[1].updated_at
        db.close()

    def test_delete_conversation(self, test_db):
        """Test de suppression de conversation."""
        db = test_db()
        user = create_user_db(db=db, name="Test User", email="test@example.com", password="TestPassword123!")

        conversation = create_conversation(db=db, user_id=user.id, title="Test Conversation")
        conv_id = conversation.id

        # Supprimer
        delete_conversation(db=db, conversation_id=conv_id, user_id=user.id)

        # Vérifier qu'elle n'existe plus
        found = get_conversation(db=db, conversation_id=conv_id, user_id=user.id)
        assert found is None
        db.close()


class TestMessageModel:
    """Tests du modèle Message."""

    def test_add_message(self, test_db):
        """Test d'ajout de message."""
        db = test_db()
        user = create_user_db(db=db, name="Test User", email="test@example.com", password="TestPassword123!")

        conversation = create_conversation(db=db, user_id=user.id, title="Test Conversation")

        # Ajouter un message
        message = add_message(db=db, conversation_id=conversation.id, role="user", content="Test message")
        assert message is not None
        assert message.id is not None
        assert message.role == "user"
        assert message.content == "Test message"
        db.close()

    def test_get_conversation_messages(self, test_db):
        """Test de récupération des messages d'une conversation."""
        db = test_db()
        user = create_user_db(db=db, name="Test User", email="test@example.com", password="TestPassword123!")

        conversation = create_conversation(db=db, user_id=user.id, title="Test Conversation")

        # Ajouter plusieurs messages
        msg1 = add_message(db=db, conversation_id=conversation.id, role="user", content="Message 1")
        msg2 = add_message(db=db, conversation_id=conversation.id, role="assistant", content="Message 2")

        messages = get_conversation_messages(db=db, conversation_id=conversation.id, user_id=user.id)
        assert len(messages) == 2
        assert msg1.id in [m.id for m in messages]
        assert msg2.id in [m.id for m in messages]
        # Vérifier l'ordre (plus ancien en premier)
        assert messages[0].created_at <= messages[1].created_at
        db.close()

    def test_cascade_delete(self, test_db):
        """Test que la suppression d'une conversation supprime ses messages."""
        db = test_db()
        user = create_user_db(db=db, name="Test User", email="test@example.com", password="TestPassword123!")

        conversation = create_conversation(db=db, user_id=user.id, title="Test Conversation")

        # Ajouter un message
        message = add_message(db=db, conversation_id=conversation.id, role="user", content="Test message")
        msg_id = message.id

        # Supprimer la conversation
        delete_conversation(db=db, conversation_id=conversation.id)

        # Vérifier que le message n'existe plus
        from app.database import Message

        found_message = db.query(Message).filter(Message.id == msg_id).first()
        assert found_message is None
        db.close()
