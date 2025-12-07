# ⚡ PostgreSQL - Démarrage Rapide

## 🚀 Configuration en 5 minutes

### 1. Installer PostgreSQL

**Windows** :
- Télécharger depuis https://www.postgresql.org/download/windows/
- Installer avec l'installateur

**Linux** :
```bash
sudo apt install postgresql postgresql-contrib
```

### 2. Créer la base de données

```bash
# Se connecter
psql -U postgres

# Dans psql
CREATE USER rag_user WITH PASSWORD 'ton-mot-de-passe-securise';
CREATE DATABASE rag_photographie OWNER rag_user;
GRANT ALL PRIVILEGES ON DATABASE rag_photographie TO rag_user;
\q
```

### 3. Configurer `.env`

```env
DATABASE_URL=postgresql://rag_user:ton-mot-de-passe-securise@localhost:5432/rag_photographie
```

### 4. Installer les dépendances

```bash
pip install psycopg2-binary alembic
```

### 5. Créer et appliquer les migrations

```bash
# Créer la migration initiale
python -m alembic revision --autogenerate -m "Initial migration"

# Appliquer
python -m alembic upgrade head
```

### 6. Vérifier

```python
from app.database import check_db_connection, IS_POSTGRESQL
print(f"PostgreSQL: {IS_POSTGRESQL}")
check_db_connection()
```

## 💾 Backup

```bash
# Backup manuel
python scripts/backup_database.py

# Backup automatisé (Windows)
.\scripts\schedule_backup.ps1

# Backup automatisé (Linux)
chmod +x scripts/schedule_backup.sh
./scripts/schedule_backup.sh
```

## 📚 Documentation complète

Voir `POSTGRESQL_SETUP.md` pour plus de détails.

