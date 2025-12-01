"""
Script de backup automatisé pour la base de données.
Supporte SQLite et PostgreSQL.
"""
import os
import sys
from pathlib import Path
from datetime import datetime
import subprocess
import logging
from typing import Optional

# Ajouter le répertoire parent au PYTHONPATH
project_root = Path(__file__).resolve().parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

from app.database import DATABASE_URL, IS_POSTGRESQL, IS_SQLITE
from app.config import BASE_DIR

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def backup_postgresql(database_url: str, backup_dir: Path) -> Optional[Path]:
    """
    Backup d'une base de données PostgreSQL.
    
    Args:
        database_url: URL de connexion PostgreSQL
        backup_dir: Répertoire de destination
        
    Returns:
        Chemin du fichier de backup ou None en cas d'erreur
    """
    try:
        # Parser l'URL PostgreSQL
        # Format: postgresql://user:password@host:port/database
        from urllib.parse import urlparse
        parsed = urlparse(database_url)
        
        db_name = parsed.path.lstrip('/')
        db_user = parsed.username
        db_host = parsed.hostname or 'localhost'
        db_port = parsed.port or 5432
        db_password = parsed.password
        
        # Nom du fichier de backup
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_file = backup_dir / f"postgresql_backup_{timestamp}.sql"
        
        # Créer le répertoire de backup
        backup_dir.mkdir(parents=True, exist_ok=True)
        
        # Commande pg_dump
        # Note: PGPASSWORD doit être défini pour éviter la demande de mot de passe
        env = os.environ.copy()
        if db_password:
            env['PGPASSWORD'] = db_password
        
        cmd = [
            'pg_dump',
            '-h', db_host,
            '-p', str(db_port),
            '-U', db_user,
            '-d', db_name,
            '-F', 'c',  # Format custom (compressé)
            '-f', str(backup_file)
        ]
        
        logger.info(f"Backup PostgreSQL en cours: {db_name} -> {backup_file}")
        result = subprocess.run(cmd, env=env, capture_output=True, text=True)
        
        if result.returncode == 0:
            logger.info(f"✅ Backup PostgreSQL réussi: {backup_file}")
            return backup_file
        else:
            logger.error(f"❌ Erreur backup PostgreSQL: {result.stderr}")
            return None
            
    except Exception as e:
        logger.error(f"❌ Erreur lors du backup PostgreSQL: {e}")
        return None


def backup_sqlite(database_path: Path, backup_dir: Path) -> Optional[Path]:
    """
    Backup d'une base de données SQLite.
    
    Args:
        database_path: Chemin vers le fichier SQLite
        backup_dir: Répertoire de destination
        
    Returns:
        Chemin du fichier de backup ou None en cas d'erreur
    """
    try:
        if not database_path.exists():
            logger.warning(f"Fichier SQLite non trouvé: {database_path}")
            return None
        
        # Nom du fichier de backup
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_file = backup_dir / f"sqlite_backup_{timestamp}.db"
        
        # Créer le répertoire de backup
        backup_dir.mkdir(parents=True, exist_ok=True)
        
        # Copier le fichier SQLite
        import shutil
        shutil.copy2(database_path, backup_file)
        
        logger.info(f"✅ Backup SQLite réussi: {backup_file}")
        return backup_file
        
    except Exception as e:
        logger.error(f"❌ Erreur lors du backup SQLite: {e}")
        return None


def backup_vector_store(backup_dir: Path) -> Optional[Path]:
    """
    Backup du vector store FAISS.
    
    Args:
        backup_dir: Répertoire de destination
        
    Returns:
        Chemin de l'archive de backup ou None en cas d'erreur
    """
    try:
        from app.config import settings
        
        vector_store_dir = settings.vector_store_dir
        
        if not vector_store_dir.exists():
            logger.warning(f"Vector store non trouvé: {vector_store_dir}")
            return None
        
        # Nom de l'archive
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_file = backup_dir / f"vector_store_backup_{timestamp}.tar.gz"
        
        # Créer le répertoire de backup
        backup_dir.mkdir(parents=True, exist_ok=True)
        
        # Créer l'archive
        import tarfile
        with tarfile.open(backup_file, 'w:gz') as tar:
            tar.add(vector_store_dir, arcname='vector_store')
        
        logger.info(f"✅ Backup vector store réussi: {backup_file}")
        return backup_file
        
    except Exception as e:
        logger.error(f"❌ Erreur lors du backup vector store: {e}")
        return None


def cleanup_old_backups(backup_dir: Path, keep_days: int = 30):
    """
    Supprime les backups plus anciens que keep_days jours.
    
    Args:
        backup_dir: Répertoire des backups
        keep_days: Nombre de jours à conserver
    """
    try:
        if not backup_dir.exists():
            return
        
        from datetime import timedelta
        cutoff_date = datetime.now() - timedelta(days=keep_days)
        
        deleted_count = 0
        for backup_file in backup_dir.glob("*_backup_*"):
            if backup_file.is_file():
                # Extraire la date du nom de fichier
                try:
                    file_date_str = backup_file.stem.split('_backup_')[-1]
                    file_date = datetime.strptime(file_date_str, "%Y%m%d_%H%M%S")
                    
                    if file_date < cutoff_date:
                        backup_file.unlink()
                        deleted_count += 1
                        logger.info(f"🗑️ Backup supprimé (trop ancien): {backup_file.name}")
                except (ValueError, IndexError):
                    # Si on ne peut pas parser la date, on garde le fichier
                    pass
        
        if deleted_count > 0:
            logger.info(f"✅ {deleted_count} ancien(s) backup(s) supprimé(s)")
            
    except Exception as e:
        logger.error(f"❌ Erreur lors du nettoyage des backups: {e}")


def main():
    """Fonction principale de backup."""
    # Répertoire de backup
    backup_dir = BASE_DIR / "backups"
    backup_dir.mkdir(parents=True, exist_ok=True)
    
    logger.info("🔄 Démarrage du backup...")
    
    # Backup de la base de données
    if IS_POSTGRESQL:
        backup_file = backup_postgresql(DATABASE_URL, backup_dir)
        if backup_file:
            logger.info(f"✅ Backup DB: {backup_file.name}")
    elif IS_SQLITE:
        db_path = Path(DATABASE_URL.replace("sqlite:///", ""))
        backup_file = backup_sqlite(db_path, backup_dir)
        if backup_file:
            logger.info(f"✅ Backup DB: {backup_file.name}")
    else:
        logger.warning("Type de base de données non supporté pour le backup")
    
    # Backup du vector store
    vector_backup = backup_vector_store(backup_dir)
    if vector_backup:
        logger.info(f"✅ Backup Vector Store: {vector_backup.name}")
    
    # Nettoyage des anciens backups
    cleanup_old_backups(backup_dir, keep_days=30)
    
    logger.info("✅ Backup terminé")


if __name__ == "__main__":
    main()

