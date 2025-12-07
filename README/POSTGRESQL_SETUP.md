# 🐘 Configuration PostgreSQL pour Production

## 📋 Table des matières

1. [Installation PostgreSQL](#installation-postgresql)
2. [Création de la base de données](#création-de-la-base-de-données)
3. [Configuration de l'application](#configuration-de-lapplication)
4. [Migrations avec Alembic](#migrations-avec-alembic)
5. [Backup automatisé](#backup-automatisé)
6. [Migration depuis SQLite](#migration-depuis-sqlite)

---

## 🔧 Installation PostgreSQL

### Windows

1. **Télécharger PostgreSQL** :
   - https://www.postgresql.org/download/windows/
   - Installer avec l'installateur officiel

2. **Vérifier l'installation** :
   ```powershell
   psql --version
   ```

### Linux (Ubuntu/Debian)

```bash
sudo apt update
sudo apt install postgresql postgresql-contrib
sudo systemctl start postgresql
sudo systemctl enable postgresql
```

### macOS

```bash
brew install postgresql
brew services start postgresql
```

---

## 🗄️ Création de la base de données

### 1. Se connecter à PostgreSQL

```bash
# Windows (si installé avec l'installateur)
psql -U postgres

# Linux
sudo -u postgres psql
```

### 2. Créer la base de données et l'utilisateur

```sql
-- Créer l'utilisateur
CREATE USER rag_user WITH PASSWORD 'ton-mot-de-passe-securise';

-- Créer la base de données
CREATE DATABASE rag_photographie OWNER rag_user;

-- Donner les permissions
GRANT ALL PRIVILEGES ON DATABASE rag_photographie TO rag_user;

-- Se connecter à la nouvelle base
\c rag_photographie

-- Donner les permissions sur le schéma public
GRANT ALL ON SCHEMA public TO rag_user;
```

### 3. Vérifier

```sql
\l  -- Lister les bases de données
\du -- Lister les utilisateurs
```

---

## ⚙️ Configuration de l'application

### 1. Installer les dépendances

```bash
pip install psycopg2-binary alembic
```

### 2. Configurer `.env`

```env
# PostgreSQL (Production)
DATABASE_URL=postgresql://rag_user:ton-mot-de-passe-securise@localhost:5432/rag_photographie

# Ou avec psycopg2 explicitement
# DATABASE_URL=postgresql+psycopg2://rag_user:ton-mot-de-passe-securise@localhost:5432/rag_photographie
```

**Format de l'URL** :
```
postgresql://[user]:[password]@[host]:[port]/[database]
```

### 3. Vérifier la connexion

```python
from app.database import check_db_connection, IS_POSTGRESQL
print(f"PostgreSQL: {IS_POSTGRESQL}")
check_db_connection()
```

---

## 🔄 Migrations avec Alembic

### 1. Créer la migration initiale

```bash
# Activer l'environnement virtuel
.\venv\Scripts\Activate.ps1

# Créer la migration initiale
python -m alembic revision --autogenerate -m "Initial migration"

# Appliquer les migrations
python -m alembic upgrade head
```

### 2. Commandes Alembic courantes

```bash
# Voir l'état actuel
python -m alembic current

# Voir l'historique
python -m alembic history

# Créer une nouvelle migration
python -m alembic revision --autogenerate -m "Description de la migration"

# Appliquer toutes les migrations en attente
python -m alembic upgrade head

# Revenir à une version précédente
python -m alembic downgrade -1

# Revenir à une version spécifique
python -m alembic downgrade <revision_id>
```

### 3. Structure des migrations

```
alembic/
├── versions/
│   ├── 001_initial_migration.py
│   ├── 002_add_new_column.py
│   └── ...
├── env.py
└── script.py.mako
```

---

## 💾 Backup automatisé

### 1. Backup manuel

```bash
# Backup de la base de données
python scripts/backup_database.py
```

### 2. Backup automatisé (Windows Task Scheduler)

1. Ouvrir le Planificateur de tâches
2. Créer une tâche de base
3. Déclencheur : Quotidien à 2h du matin
4. Action : Exécuter un programme
   - Programme : `python`
   - Arguments : `E:\RAG-Photographie\scripts\backup_database.py`
   - Démarrer dans : `E:\RAG-Photographie`

### 3. Backup automatisé (Linux Cron)

```bash
# Éditer le crontab
crontab -e

# Ajouter (backup quotidien à 2h du matin)
0 2 * * * cd /chemin/vers/RAG-Photographie && /chemin/vers/venv/bin/python scripts/backup_database.py >> logs/backup.log 2>&1
```

### 4. Restauration depuis un backup

```bash
# Lister les backups disponibles
python scripts/restore_database.py

# Restaurer le backup le plus récent
python scripts/restore_database.py --latest --confirm

# Restaurer un backup spécifique
python scripts/restore_database.py --backup-file backups/postgresql_backup_20240101_020000.sql --confirm
```

---

## 🔄 Migration depuis SQLite vers PostgreSQL

### Option 1 : Script de migration automatique

```python
# scripts/migrate_sqlite_to_postgresql.py
from app.database import engine as postgres_engine, Base
from sqlalchemy import create_engine
import sqlite3

# Connexion SQLite
sqlite_path = "storage/database.db"
sqlite_conn = sqlite3.connect(sqlite_path)

# Créer les tables dans PostgreSQL
Base.metadata.create_all(bind=postgres_engine)

# Migrer les données (exemple simplifié)
# Note: Utiliser un outil comme pgloader pour une migration complète
```

### Option 2 : Utiliser pgloader (Recommandé)

```bash
# Installer pgloader
# Windows: https://github.com/dimitri/pgloader/releases
# Linux: sudo apt install pgloader

# Migrer
pgloader sqlite:///storage/database.db postgresql://rag_user:password@localhost/rag_photographie
```

### Option 3 : Export/Import manuel

```bash
# 1. Exporter depuis SQLite
sqlite3 storage/database.db .dump > dump.sql

# 2. Adapter le dump pour PostgreSQL (supprimer les commandes SQLite spécifiques)

# 3. Importer dans PostgreSQL
psql -U rag_user -d rag_photographie -f dump.sql
```

---

## 📊 Vérification

### Tester la connexion

```python
from app.database import check_db_connection, IS_POSTGRESQL, engine

print(f"PostgreSQL activé: {IS_POSTGRESQL}")
check_db_connection()

# Vérifier les tables
from sqlalchemy import inspect
inspector = inspect(engine)
tables = inspector.get_table_names()
print(f"Tables: {tables}")
```

### Vérifier les données

```sql
-- Se connecter
psql -U rag_user -d rag_photographie

-- Voir les tables
\dt

-- Compter les utilisateurs
SELECT COUNT(*) FROM users;

-- Voir les conversations
SELECT id, title, created_at FROM conversations LIMIT 10;
```

---

## 🔒 Sécurité

### Bonnes pratiques

1. **Mot de passe fort** :
   ```python
   from app.security import generate_secret_key
   print(generate_secret_key())  # Utiliser pour le mot de passe DB
   ```

2. **Permissions limitées** :
   ```sql
   -- Ne donner que les permissions nécessaires
   GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA public TO rag_user;
   ```

3. **Connexion SSL** (production) :
   ```env
   DATABASE_URL=postgresql://user:pass@host:5432/db?sslmode=require
   ```

4. **Firewall** :
   - Limiter l'accès PostgreSQL au serveur uniquement
   - Ne pas exposer le port 5432 publiquement

---

## 🐳 Docker (Optionnel)

### docker-compose.yml avec PostgreSQL

```yaml
version: '3.8'

services:
  postgres:
    image: postgres:15-alpine
    container_name: rag-postgres
    environment:
      POSTGRES_USER: rag_user
      POSTGRES_PASSWORD: ${POSTGRES_PASSWORD}
      POSTGRES_DB: rag_photographie
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data
    networks:
      - rag-network

  backend:
    # ... configuration existante ...
    environment:
      - DATABASE_URL=postgresql://rag_user:${POSTGRES_PASSWORD}@postgres:5432/rag_photographie
    depends_on:
      - postgres

volumes:
  postgres_data:

networks:
  rag-network:
    driver: bridge
```

---

## 📚 Commandes utiles

### PostgreSQL

```bash
# Se connecter
psql -U rag_user -d rag_photographie

# Backup manuel
pg_dump -U rag_user -d rag_photographie -F c -f backup.dump

# Restauration manuelle
pg_restore -U rag_user -d rag_photographie -c backup.dump

# Voir la taille de la base
psql -U rag_user -d rag_photographie -c "SELECT pg_size_pretty(pg_database_size('rag_photographie'));"
```

### Alembic

```bash
# État actuel
python -m alembic current

# Historique
python -m alembic history

# Créer migration
python -m alembic revision --autogenerate -m "Description"

# Appliquer
python -m alembic upgrade head

# Revenir en arrière
python -m alembic downgrade -1
```

---

## ✅ Checklist

- [ ] PostgreSQL installé
- [ ] Base de données créée
- [ ] Utilisateur créé avec permissions
- [ ] `DATABASE_URL` configuré dans `.env`
- [ ] `psycopg2-binary` installé
- [ ] Migration initiale créée et appliquée
- [ ] Backup automatisé configuré
- [ ] Test de connexion réussi
- [ ] Données migrées (si migration depuis SQLite)

---

**✅ PostgreSQL est maintenant configuré pour la production !**

