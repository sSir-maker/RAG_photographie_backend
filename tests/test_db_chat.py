"""
Tests supplémentaires pour les fonctions de chat de la base de données.
"""
import pytest
from app.db_chat import (
    get_user_conversations,
    get_conversation,
    create_conversation,
    delete_conversation,
    add_message,
    get_conversation_messages,
    update_conversation_title,
)
from app.db_auth import create_user_db


class TestConversationManagement:
    """Tests de gestion des conversations."""
    
    def test_get_user_conversations_empty(self, test_db):
        """Test de récupération des conversations d'un utilisateur sans conversations."""
        db = test_db()
        user = create_user_db(
            db=db,
            name="Test User",
            email="test@example.com",
            password="TestPassword123!"
        )
        
        conversations = get_user_conversations(db=db, user_id=user.id)
        assert conversations == []
        db.close()
    
    def test_get_conversation_nonexistent(self, test_db):
        """Test de récupération d'une conversation inexistante."""
        db = test_db()
        conversation = get_conversation(db=db, conversation_id=99999)
        assert conversation is None
        db.close()
    
    def test_update_conversation_title(self, test_db):
        """Test de mise à jour du titre d'une conversation."""
        db = test_db()
        user = create_user_db(
            db=db,
            name="Test User",
            email="test@example.com",
            password="TestPassword123!"
        )
        
        conversation = create_conversation(
            db=db,
            user_id=user.id,
            title="Original Title"
        )
        
        # Mettre à jour le titre
        updated = update_conversation_title(
            db=db,
            conversation_id=conversation.id,
            user_id=user.id,
            title="Updated Title"
        )
        assert updated is not None
        assert updated.title == "Updated Title"
        
        # Vérifier que c'est bien mis à jour
        found = get_conversation(db=db, conversation_id=conversation.id, user_id=user.id)
        assert found.title == "Updated Title"
        db.close()
    
    def test_add_message_with_image(self, test_db):
        """Test d'ajout de message avec image."""
        db = test_db()
        user = create_user_db(
            db=db,
            name="Test User",
            email="test@example.com",
            password="TestPassword123!"
        )
        
        conversation = create_conversation(
            db=db,
            user_id=user.id,
            title="Test Conversation"
        )
        
        # Ajouter un message avec image
        message = add_message(
            db=db,
            conversation_id=conversation.id,
            role="user",
            content="Regarde cette photo",
            image_url="https://example.com/image.jpg"
        )
        assert message is not None
        assert message.image_url == "https://example.com/image.jpg"
        db.close()
    
    def test_get_conversation_messages_empty(self, test_db):
        """Test de récupération des messages d'une conversation vide."""
        db = test_db()
        user = create_user_db(
            db=db,
            name="Test User",
            email="test@example.com",
            password="TestPassword123!"
        )
        
        conversation = create_conversation(
            db=db,
            user_id=user.id,
            title="Empty Conversation"
        )
        
        messages = get_conversation_messages(db=db, conversation_id=conversation.id, user_id=user.id)
        assert messages == []
        db.close()
    
    def test_delete_nonexistent_conversation(self, test_db):
        """Test de suppression d'une conversation inexistante."""
        db = test_db()
        user = create_user_db(
            db=db,
            name="Test User",
            email="test@example.com",
            password="TestPassword123!"
        )
        # Ne devrait pas lever d'exception
        result = delete_conversation(db=db, conversation_id=99999, user_id=user.id)
        # La fonction retourne False si la conversation n'existe pas
        assert result is False
        db.close()
    
    def test_get_conversation_with_wrong_user(self, test_db):
        """Test de récupération d'une conversation avec un mauvais utilisateur."""
        db = test_db()
        user1 = create_user_db(
            db=db,
            name="User 1",
            email="user1@example.com",
            password="TestPassword123!"
        )
        user2 = create_user_db(
            db=db,
            name="User 2",
            email="user2@example.com",
            password="TestPassword123!"
        )
        
        conversation = create_conversation(
            db=db,
            user_id=user1.id,
            title="User 1 Conversation"
        )
        
        # User2 ne devrait pas pouvoir accéder à la conversation de User1
        found = get_conversation(db=db, conversation_id=conversation.id, user_id=user2.id)
        assert found is None
        db.close()

