"""
Module pour gérer les conversations et messages dans la base de données.
"""

from datetime import datetime
from typing import List, Optional
from sqlalchemy.orm import Session

from .database import Conversation, Message, User


def create_conversation(db: Session, user_id: int, title: str = "New conversation") -> Conversation:
    """Crée une nouvelle conversation."""
    conversation = Conversation(
        user_id=user_id, title=title, created_at=datetime.utcnow(), updated_at=datetime.utcnow()
    )
    db.add(conversation)
    db.commit()
    db.refresh(conversation)
    return conversation


def get_user_conversations(db: Session, user_id: int) -> List[Conversation]:
    """Récupère toutes les conversations d'un utilisateur."""
    return db.query(Conversation).filter(Conversation.user_id == user_id).order_by(Conversation.updated_at.desc()).all()


def get_conversation(db: Session, conversation_id: int, user_id: int) -> Optional[Conversation]:
    """Récupère une conversation spécifique (vérifie qu'elle appartient à l'utilisateur)."""
    return db.query(Conversation).filter(Conversation.id == conversation_id, Conversation.user_id == user_id).first()


def update_conversation_title(db: Session, conversation_id: int, user_id: int, title: str) -> Optional[Conversation]:
    """Met à jour le titre d'une conversation."""
    conversation = get_conversation(db, conversation_id, user_id)
    if conversation:
        conversation.title = title
        conversation.updated_at = datetime.utcnow()
        db.commit()
        db.refresh(conversation)
    return conversation


def delete_conversation(db: Session, conversation_id: int, user_id: int) -> bool:
    """Supprime une conversation."""
    conversation = get_conversation(db, conversation_id, user_id)
    if conversation:
        db.delete(conversation)
        db.commit()
        return True
    return False


def add_message(db: Session, conversation_id: int, role: str, content: str, image_url: Optional[str] = None) -> Message:
    """Ajoute un message à une conversation."""
    message = Message(
        conversation_id=conversation_id, role=role, content=content, image_url=image_url, created_at=datetime.utcnow()
    )
    db.add(message)

    # Mettre à jour la date de modification de la conversation
    conversation = db.query(Conversation).filter(Conversation.id == conversation_id).first()
    if conversation:
        conversation.updated_at = datetime.utcnow()
        # Mettre à jour le titre si c'est le premier message utilisateur
        if role == "user" and conversation.title == "New conversation":
            conversation.title = content[:50] + ("..." if len(content) > 50 else "")

    db.commit()
    db.refresh(message)
    return message


def get_conversation_messages(db: Session, conversation_id: int, user_id: int) -> List[Message]:
    """Récupère tous les messages d'une conversation (vérifie qu'elle appartient à l'utilisateur)."""
    conversation = get_conversation(db, conversation_id, user_id)
    if not conversation:
        return []

    return db.query(Message).filter(Message.conversation_id == conversation_id).order_by(Message.created_at.asc()).all()
