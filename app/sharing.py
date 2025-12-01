"""
Module pour partager des conversations.
"""
import secrets
import hashlib
from typing import Optional, Dict, Any
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Boolean
from .database import Conversation, Message, Base
from .db_chat import get_conversation_messages


class SharedConversation(Base):
    """Modèle pour les conversations partagées."""
    __tablename__ = "shared_conversations"
    
    id = Column(Integer, primary_key=True, index=True)
    conversation_id = Column(Integer, ForeignKey("conversations.id"), nullable=False)
    share_token = Column(String, unique=True, index=True, nullable=False)
    created_by = Column(Integer, ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    expires_at = Column(DateTime, nullable=True)  # None = pas d'expiration
    is_active = Column(Boolean, default=True)
    view_count = Column(Integer, default=0)
    max_views = Column(Integer, nullable=True)  # None = illimité


def generate_share_token() -> str:
    """Génère un token unique pour le partage."""
    return secrets.token_urlsafe(32)


def create_shared_conversation(
    db: Session,
    conversation_id: int,
    user_id: int,
    expires_in_days: Optional[int] = None,
    max_views: Optional[int] = None
) -> SharedConversation:
    """
    Crée un lien de partage pour une conversation.
    
    Args:
        db: Session de base de données
        conversation_id: ID de la conversation à partager
        user_id: ID de l'utilisateur qui crée le partage
        expires_in_days: Nombre de jours avant expiration (None = pas d'expiration)
        max_views: Nombre maximum de vues (None = illimité)
    
    Returns:
        Instance SharedConversation créée
    """
    # Vérifier que la conversation appartient à l'utilisateur
    conversation = db.query(Conversation).filter(
        Conversation.id == conversation_id,
        Conversation.user_id == user_id
    ).first()
    
    if not conversation:
        raise ValueError("Conversation non trouvée ou accès refusé")
    
    # Vérifier s'il existe déjà un partage actif
    existing = db.query(SharedConversation).filter(
        SharedConversation.conversation_id == conversation_id,
        SharedConversation.is_active == True
    ).first()
    
    if existing:
        # Réactiver le partage existant
        if expires_in_days:
            existing.expires_at = datetime.utcnow() + timedelta(days=expires_in_days)
        existing.max_views = max_views
        existing.view_count = 0
        return existing
    
    # Créer un nouveau partage
    share_token = generate_share_token()
    expires_at = None
    if expires_in_days:
        expires_at = datetime.utcnow() + timedelta(days=expires_in_days)
    
    shared = SharedConversation(
        conversation_id=conversation_id,
        share_token=share_token,
        created_by=user_id,
        expires_at=expires_at,
        max_views=max_views,
    )
    
    db.add(shared)
    db.commit()
    db.refresh(shared)
    
    return shared


def get_shared_conversation(
    db: Session,
    share_token: str
) -> Optional[Dict[str, Any]]:
    """
    Récupère une conversation partagée par son token.
    
    Args:
        db: Session de base de données
        share_token: Token de partage
    
    Returns:
        Dictionnaire avec la conversation et les messages, ou None si invalide
    """
    shared = db.query(SharedConversation).filter(
        SharedConversation.share_token == share_token,
        SharedConversation.is_active == True
    ).first()
    
    if not shared:
        return None
    
    # Vérifier l'expiration
    if shared.expires_at and shared.expires_at < datetime.utcnow():
        shared.is_active = False
        db.commit()
        return None
    
    # Vérifier le nombre de vues
    if shared.max_views and shared.view_count >= shared.max_views:
        shared.is_active = False
        db.commit()
        return None
    
    # Incrémenter le compteur de vues
    shared.view_count += 1
    db.commit()
    
    # Récupérer la conversation et les messages
    conversation = db.query(Conversation).filter(
        Conversation.id == shared.conversation_id
    ).first()
    
    if not conversation:
        return None
    
    messages = get_conversation_messages(db, conversation.id, conversation.user_id)
    
    return {
        "conversation": {
            "id": conversation.id,
            "title": conversation.title,
            "created_at": conversation.created_at.isoformat() if conversation.created_at else None,
            "updated_at": conversation.updated_at.isoformat() if conversation.updated_at else None,
        },
        "messages": [
            {
                "id": msg.id,
                "role": msg.role,
                "content": msg.content,
                "image_url": msg.image_url,
                "created_at": msg.created_at.isoformat() if msg.created_at else None,
            }
            for msg in messages
        ],
        "share_info": {
            "created_at": shared.created_at.isoformat() if shared.created_at else None,
            "expires_at": shared.expires_at.isoformat() if shared.expires_at else None,
            "view_count": shared.view_count,
            "max_views": shared.max_views,
        }
    }


def revoke_shared_conversation(
    db: Session,
    conversation_id: int,
    user_id: int
) -> bool:
    """
    Révoque un partage de conversation.
    
    Args:
        db: Session de base de données
        conversation_id: ID de la conversation
        user_id: ID de l'utilisateur propriétaire
    
    Returns:
        True si révoqué avec succès
    """
    shared = db.query(SharedConversation).join(Conversation).filter(
        SharedConversation.conversation_id == conversation_id,
        Conversation.user_id == user_id,
        SharedConversation.is_active == True
    ).first()
    
    if shared:
        shared.is_active = False
        db.commit()
        return True
    
    return False


def get_user_shared_conversations(
    db: Session,
    user_id: int
) -> List[Dict[str, Any]]:
    """
    Récupère toutes les conversations partagées par un utilisateur.
    
    Args:
        db: Session de base de données
        user_id: ID de l'utilisateur
    
    Returns:
        Liste des conversations partagées
    """
    shared = db.query(SharedConversation).join(Conversation).filter(
        Conversation.user_id == user_id
    ).order_by(SharedConversation.created_at.desc()).all()
    
    return [
        {
            "id": s.id,
            "conversation_id": s.conversation_id,
            "conversation_title": db.query(Conversation).filter(
                Conversation.id == s.conversation_id
            ).first().title if db.query(Conversation).filter(
                Conversation.id == s.conversation_id
            ).first() else "Unknown",
            "share_token": s.share_token,
            "created_at": s.created_at.isoformat() if s.created_at else None,
            "expires_at": s.expires_at.isoformat() if s.expires_at else None,
            "view_count": s.view_count,
            "max_views": s.max_views,
            "is_active": s.is_active,
        }
        for s in shared
    ]

