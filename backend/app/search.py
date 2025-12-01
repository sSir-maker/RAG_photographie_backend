"""
Module pour rechercher dans l'historique des conversations.
"""

from typing import List, Dict, Any, Optional
from sqlalchemy.orm import Session
from sqlalchemy import or_, and_

from .database import Conversation, Message
from .db_chat import get_conversation_messages


def search_in_conversations(
    db: Session,
    user_id: int,
    query: str,
    conversation_id: Optional[int] = None,
    role_filter: Optional[str] = None,
    limit: int = 50,
) -> List[Dict[str, Any]]:
    """
    Recherche dans les conversations de l'utilisateur.

    Args:
        db: Session de base de données
        user_id: ID de l'utilisateur
        query: Terme de recherche
        conversation_id: Filtrer par conversation spécifique (optionnel)
        role_filter: Filtrer par rôle ('user' ou 'assistant')
        limit: Nombre maximum de résultats

    Returns:
        Liste de messages correspondants avec métadonnées
    """
    # Construire la requête de base
    search_filter = Message.content.ilike(f"%{query}%")

    # Filtrer par conversation si spécifié
    if conversation_id:
        search_filter = and_(search_filter, Message.conversation_id == conversation_id)

    # Filtrer par rôle si spécifié
    if role_filter:
        search_filter = and_(search_filter, Message.role == role_filter)

    # Récupérer les messages correspondants
    messages = (
        db.query(Message)
        .join(Conversation)
        .filter(and_(Conversation.user_id == user_id, search_filter))
        .order_by(Message.created_at.desc())
        .limit(limit)
        .all()
    )

    # Formater les résultats
    results = []
    for msg in messages:
        conversation = db.query(Conversation).filter(Conversation.id == msg.conversation_id).first()
        results.append(
            {
                "message_id": msg.id,
                "conversation_id": msg.conversation_id,
                "conversation_title": conversation.title if conversation else "Unknown",
                "role": msg.role,
                "content": msg.content,
                "content_preview": msg.content[:200] + "..." if len(msg.content) > 200 else msg.content,
                "created_at": msg.created_at.isoformat() if msg.created_at else None,
                "image_url": msg.image_url,
            }
        )

    return results


def search_conversations_by_title(db: Session, user_id: int, query: str, limit: int = 20) -> List[Dict[str, Any]]:
    """
    Recherche des conversations par titre.

    Args:
        db: Session de base de données
        user_id: ID de l'utilisateur
        query: Terme de recherche
        limit: Nombre maximum de résultats

    Returns:
        Liste de conversations correspondantes
    """
    conversations = (
        db.query(Conversation)
        .filter(and_(Conversation.user_id == user_id, Conversation.title.ilike(f"%{query}%")))
        .order_by(Conversation.updated_at.desc())
        .limit(limit)
        .all()
    )

    return [
        {
            "id": conv.id,
            "title": conv.title,
            "created_at": conv.created_at.isoformat() if conv.created_at else None,
            "updated_at": conv.updated_at.isoformat() if conv.updated_at else None,
        }
        for conv in conversations
    ]


def get_conversation_statistics(db: Session, user_id: int, conversation_id: Optional[int] = None) -> Dict[str, Any]:
    """
    Récupère des statistiques sur les conversations.

    Args:
        db: Session de base de données
        user_id: ID de l'utilisateur
        conversation_id: ID de conversation spécifique (optionnel)

    Returns:
        Dictionnaire avec les statistiques
    """
    if conversation_id:
        # Statistiques pour une conversation spécifique
        messages = get_conversation_messages(db, conversation_id, user_id)
        total_messages = len(messages)
        user_messages = len([m for m in messages if m.role == "user"])
        assistant_messages = len([m for m in messages if m.role == "assistant"])

        total_chars = sum(len(m.content) for m in messages)
        avg_message_length = total_chars / total_messages if total_messages > 0 else 0

        return {
            "conversation_id": conversation_id,
            "total_messages": total_messages,
            "user_messages": user_messages,
            "assistant_messages": assistant_messages,
            "total_characters": total_chars,
            "average_message_length": round(avg_message_length, 2),
        }
    else:
        # Statistiques globales pour l'utilisateur
        conversations = db.query(Conversation).filter(Conversation.user_id == user_id).all()
        total_conversations = len(conversations)

        total_messages = db.query(Message).join(Conversation).filter(Conversation.user_id == user_id).count()

        return {
            "total_conversations": total_conversations,
            "total_messages": total_messages,
        }
