# 🔍 Fonctionnalités de Recherche

## 📋 Vue d'ensemble

Le système permet de rechercher dans l'historique des conversations.

## 🔗 Endpoints

### Recherche dans les messages

```bash
GET /search/messages?query=photographie&conversation_id=1&role=user&limit=50
```

Paramètres :
- `query` (requis) : Terme de recherche
- `conversation_id` (optionnel) : Filtrer par conversation
- `role` (optionnel) : `user` ou `assistant`
- `limit` (optionnel) : Nombre max de résultats (1-100, défaut: 50)

### Recherche de conversations par titre

```bash
GET /search/conversations?query=photo&limit=20
```

Paramètres :
- `query` (requis) : Terme de recherche
- `limit` (optionnel) : Nombre max de résultats (1-50, défaut: 20)

### Statistiques d'une conversation

```bash
GET /conversations/{conversation_id}/statistics
```

Retourne :
- Nombre total de messages
- Messages utilisateur vs assistant
- Nombre total de caractères
- Longueur moyenne des messages

## 📊 Exemples

### Recherche simple

```bash
curl -H "Authorization: Bearer TOKEN" \
  "http://localhost:8001/search/messages?query=photographie"
```

### Recherche avec filtres

```bash
curl -H "Authorization: Bearer TOKEN" \
  "http://localhost:8001/search/messages?query=photo&conversation_id=1&role=assistant"
```

### Statistiques

```bash
curl -H "Authorization: Bearer TOKEN" \
  "http://localhost:8001/conversations/1/statistics"
```

## ✅ Checklist

- [ ] Recherche dans messages testée
- [ ] Recherche par titre testée
- [ ] Statistiques testées
- [ ] Filtres testés

---

**✅ Fonctionnalités de recherche implémentées !**

