"""
Module pour exporter les conversations dans différents formats.
"""
import json
import csv
import io
from typing import List, Dict, Any, Optional
from datetime import datetime
from pathlib import Path

from .database import Conversation, Message


def export_conversation_json(conversation: Conversation, messages: List[Message]) -> str:
    """Exporte une conversation au format JSON."""
    data = {
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
        "exported_at": datetime.utcnow().isoformat(),
        "total_messages": len(messages),
    }
    return json.dumps(data, indent=2, ensure_ascii=False)


def export_conversation_csv(conversation: Conversation, messages: List[Message]) -> str:
    """Exporte une conversation au format CSV."""
    output = io.StringIO()
    writer = csv.writer(output)
    
    # En-têtes
    writer.writerow([
        "Conversation ID",
        "Conversation Title",
        "Message ID",
        "Role",
        "Content",
        "Image URL",
        "Created At"
    ])
    
    # Données
    for msg in messages:
        writer.writerow([
            conversation.id,
            conversation.title,
            msg.id,
            msg.role,
            msg.content,
            msg.image_url or "",
            msg.created_at.isoformat() if msg.created_at else "",
        ])
    
    return output.getvalue()


def export_conversation_markdown(conversation: Conversation, messages: List[Message]) -> str:
    """Exporte une conversation au format Markdown."""
    lines = [
        f"# {conversation.title}",
        "",
        f"**Conversation ID:** {conversation.id}",
        f"**Created:** {conversation.created_at.isoformat() if conversation.created_at else 'N/A'}",
        f"**Updated:** {conversation.updated_at.isoformat() if conversation.updated_at else 'N/A'}",
        "",
        "---",
        "",
    ]
    
    for msg in messages:
        role_emoji = "👤" if msg.role == "user" else "🤖"
        lines.append(f"## {role_emoji} {msg.role.capitalize()}")
        lines.append("")
        lines.append(msg.content)
        if msg.image_url:
            lines.append(f"![Image]({msg.image_url})")
        lines.append("")
        lines.append(f"*{msg.created_at.isoformat() if msg.created_at else 'N/A'}*")
        lines.append("")
        lines.append("---")
        lines.append("")
    
    return "\n".join(lines)


def export_conversation_txt(conversation: Conversation, messages: List[Message]) -> str:
    """Exporte une conversation au format texte simple."""
    lines = [
        f"Conversation: {conversation.title}",
        f"ID: {conversation.id}",
        f"Created: {conversation.created_at.isoformat() if conversation.created_at else 'N/A'}",
        f"Updated: {conversation.updated_at.isoformat() if conversation.updated_at else 'N/A'}",
        "",
        "=" * 80,
        "",
    ]
    
    for msg in messages:
        role_label = "USER" if msg.role == "user" else "ASSISTANT"
        lines.append(f"[{role_label}] {msg.created_at.isoformat() if msg.created_at else 'N/A'}")
        lines.append("-" * 80)
        lines.append(msg.content)
        if msg.image_url:
            lines.append(f"Image: {msg.image_url}")
        lines.append("")
        lines.append("=" * 80)
        lines.append("")
    
    return "\n".join(lines)


def export_conversations_bulk(
    conversations: List[Conversation],
    format_type: str = "json",
    db_session = None
) -> str:
    """
    Exporte plusieurs conversations dans un seul fichier.
    
    Args:
        conversations: Liste des conversations à exporter
        format_type: Format d'export (json, csv, markdown, txt)
        db_session: Session de base de données
    
    Returns:
        Contenu du fichier exporté
    """
    from .database import get_conversation_messages
    
    if format_type == "json":
        data = {
            "conversations": [],
            "exported_at": datetime.utcnow().isoformat(),
            "total_conversations": len(conversations),
        }
        
        for conv in conversations:
            messages = get_conversation_messages(db_session, conv.id, conv.user_id)
            data["conversations"].append({
                "conversation": {
                    "id": conv.id,
                    "title": conv.title,
                    "created_at": conv.created_at.isoformat() if conv.created_at else None,
                    "updated_at": conv.updated_at.isoformat() if conv.updated_at else None,
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
            })
        
        return json.dumps(data, indent=2, ensure_ascii=False)
    
    elif format_type == "csv":
        output = io.StringIO()
        writer = csv.writer(output)
        
        writer.writerow([
            "Conversation ID",
            "Conversation Title",
            "Message ID",
            "Role",
            "Content",
            "Image URL",
            "Created At"
        ])
        
        for conv in conversations:
            messages = get_conversation_messages(db_session, conv.id, conv.user_id)
            for msg in messages:
                writer.writerow([
                    conv.id,
                    conv.title,
                    msg.id,
                    msg.role,
                    msg.content,
                    msg.image_url or "",
                    msg.created_at.isoformat() if msg.created_at else "",
                ])
        
        return output.getvalue()
    
    else:
        raise ValueError(f"Format non supporté pour l'export bulk: {format_type}")

