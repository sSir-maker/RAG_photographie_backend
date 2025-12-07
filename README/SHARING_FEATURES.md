# 🔗 Fonctionnalités de Partage

## 📋 Vue d'ensemble

Le système permet de partager des conversations via des liens publics.

## 🔗 Endpoints

### Créer un partage

```bash
POST /conversations/{conversation_id}/share?expires_in_days=7&max_views=10
```

Paramètres :
- `expires_in_days` (optionnel) : Nombre de jours avant expiration (1-365)
- `max_views` (optionnel) : Nombre maximum de vues

### Récupérer une conversation partagée

```bash
GET /shared/{share_token}
```

**Note** : Pas d'authentification requise (public)

### Révoquer un partage

```bash
DELETE /conversations/{conversation_id}/share
```

### Lister les partages de l'utilisateur

```bash
GET /conversations/shared
```

## 🔐 Sécurité

- Tokens uniques et sécurisés (32 caractères)
- Expiration optionnelle
- Limite de vues optionnelle
- Révocable à tout moment
- Seul le propriétaire peut créer/révoquer

## 📊 Exemples

### Créer un partage permanent

```bash
curl -X POST \
  -H "Authorization: Bearer TOKEN" \
  "http://localhost:8001/conversations/1/share"
```

### Créer un partage avec expiration

```bash
curl -X POST \
  -H "Authorization: Bearer TOKEN" \
  "http://localhost:8001/conversations/1/share?expires_in_days=7&max_views=10"
```

### Accéder à une conversation partagée

```bash
curl "http://localhost:8001/shared/TOKEN_ICI"
```

### Révoquer un partage

```bash
curl -X DELETE \
  -H "Authorization: Bearer TOKEN" \
  "http://localhost:8001/conversations/1/share"
```

## ✅ Checklist

- [ ] Création de partage testée
- [ ] Accès public testé
- [ ] Expiration testée
- [ ] Limite de vues testée
- [ ] Révocation testée

---

**✅ Fonctionnalités de partage implémentées !**

