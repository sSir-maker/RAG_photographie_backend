# 📤 Fonctionnalités d'Export

## 📋 Vue d'ensemble

Le système permet d'exporter les conversations dans plusieurs formats.

## 🔗 Endpoints

### Export d'une conversation

```bash
GET /conversations/{conversation_id}/export?format=json
GET /conversations/{conversation_id}/export?format=csv
GET /conversations/{conversation_id}/export?format=markdown
GET /conversations/{conversation_id}/export?format=txt
```

### Export en masse

```bash
POST /conversations/export/bulk
Content-Type: application/json

{
  "conversation_ids": [1, 2, 3],
  "format": "json"  # ou "csv"
}
```

## 📄 Formats Supportés

### JSON

Structure complète avec métadonnées :
```json
{
  "conversation": {
    "id": 1,
    "title": "Ma conversation",
    "created_at": "2024-01-01T12:00:00",
    "updated_at": "2024-01-01T13:00:00"
  },
  "messages": [...],
  "exported_at": "2024-01-01T14:00:00",
  "total_messages": 10
}
```

### CSV

Format tabulaire avec une ligne par message :
```csv
Conversation ID,Conversation Title,Message ID,Role,Content,Image URL,Created At
1,Ma conversation,1,user,Question...,,2024-01-01T12:00:00
```

### Markdown

Format lisible avec structure :
```markdown
# Ma conversation

**Conversation ID:** 1
**Created:** 2024-01-01T12:00:00

---

## 👤 User
Contenu du message...
```

### TXT

Format texte simple :
```
Conversation: Ma conversation
ID: 1
Created: 2024-01-01T12:00:00

================================================================================

[USER] 2024-01-01T12:00:00
--------------------------------------------------------------------------------
Contenu du message...
```

## ✅ Checklist

- [ ] Export JSON testé
- [ ] Export CSV testé
- [ ] Export Markdown testé
- [ ] Export TXT testé
- [ ] Export bulk testé

---

**✅ Fonctionnalités d'export implémentées !**

