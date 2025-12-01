# 🗄️ Configuration de la Base de Données

Le système utilise maintenant **SQLite** avec **SQLAlchemy** pour stocker toutes les données de manière persistante.

## ✅ Fonctionnalités

- **Utilisateurs** : Stockage sécurisé dans la base de données (migration depuis JSON)
- **Conversations** : Chaque utilisateur a ses propres conversations
- **Messages** : Historique complet de tous les messages sauvegardé
- **Persistance** : Toutes les données sont conservées entre les sessions

## 📦 Structure de la Base de Données

### Table `users`
- `id` : Identifiant unique
- `name` : Nom de l'utilisateur
- `email` : Email (unique)
- `hashed_password` : Mot de passe hashé avec bcrypt
- `created_at` : Date de création

### Table `conversations`
- `id` : Identifiant unique
- `user_id` : Référence à l'utilisateur
- `title` : Titre de la conversation
- `created_at` : Date de création
- `updated_at` : Date de dernière modification

### Table `messages`
- `id` : Identifiant unique
- `conversation_id` : Référence à la conversation
- `role` : 'user' ou 'assistant'
- `content` : Contenu du message
- `image_url` : URL de l'image (optionnel)
- `created_at` : Date de création

## 🚀 Initialisation

La base de données est automatiquement créée au démarrage de l'API dans `storage/database.db`.

### Première utilisation

1. **Démarrer l'API** :
   ```powershell
   python run_api.py
   ```

2. La base de données sera créée automatiquement dans `storage/database.db`

3. **Créer un compte** via le frontend

## 📡 Endpoints API

### Conversations

- **GET `/conversations`** : Liste toutes les conversations de l'utilisateur
- **POST `/conversations`** : Crée une nouvelle conversation
- **GET `/conversations/{id}/messages`** : Récupère tous les messages d'une conversation
- **DELETE `/conversations/{id}`** : Supprime une conversation

### Messages

Les messages sont automatiquement sauvegardés lors de l'appel à `/ask`.

## 🔄 Migration depuis JSON

Les utilisateurs existants dans `storage/users.json` ne seront pas automatiquement migrés. Pour migrer :

1. Les nouveaux utilisateurs seront créés dans la base de données
2. Les anciens utilisateurs devront se réinscrire (ou créer un script de migration)

## 📝 Notes

- La base de données SQLite est locale et stockée dans `storage/database.db`
- Pour la production, considère migrer vers PostgreSQL ou MySQL
- Les données sont persistantes : elles restent même après redémarrage
- Chaque utilisateur ne voit que ses propres conversations

## 🔧 Maintenance

### Sauvegarder la base de données

```powershell
# Copier le fichier
Copy-Item storage\database.db storage\database.db.backup
```

### Réinitialiser la base de données

```powershell
# Supprimer le fichier (ATTENTION : perte de toutes les données)
Remove-Item storage\database.db
# Redémarrer l'API pour recréer
```

## 🐛 Dépannage

### Erreur "database is locked"

- Ferme tous les processus qui utilisent la base de données
- Redémarre l'API

### Base de données corrompue

- Supprime `storage/database.db`
- Redémarre l'API pour recréer

### Données perdues

- Vérifie que le fichier `storage/database.db` existe
- Vérifie les permissions d'écriture dans le dossier `storage/`

