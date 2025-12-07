"""
Script de restauration de la base de données depuis un backup.
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


def restore_postgresql(database_url: str, backup_file: Path) -> bool:
    """
    Restaure une base de données PostgreSQL depuis un backup.
    
    Args:
        database_url: URL de connexion PostgreSQL
        backup_file: Chemin vers le fichier de backup
        
    Returns:
        True si la restauration a réussi, False sinon
    """
    try:
        if not backup_file.exists():
            logger.error(f"Fichier de backup non trouvé: {backup_file}")
            return False
        
        # Parser l'URL PostgreSQL
        from urllib.parse import urlparse
        parsed = urlparse(database_url)
        
        db_name = parsed.path.lstrip('/')
        db_user = parsed.username
        db_host = parsed.hostname or 'localhost'
        db_port = parsed.port or 5432
        db_password = parsed.password
        
        # Vérifier le format du backup
        if backup_file.suffix == '.sql':
            # Format SQL (plain)
            cmd = [
                'psql',
                '-h', db_host,
                '-p', str(db_port),
                '-U', db_user,
                '-d', db_name,
                '-f', str(backup_file)
            ]
        else:
            # Format custom (compressé)
            cmd = [
                'pg_restore',
                '-h', db_host,
                '-p', str(db_port),
                '-U', db_user,
                '-d', db_name,
                '-c',  # Clean (drop) avant restauration
                str(backup_file)
            ]
        
        env = os.environ.copy()
        if db_password:
            env['PGPASSWORD'] = db_password
        
        logger.warning(f"⚠️ RESTAURATION EN COURS - La base de données sera écrasée!")
        logger.info(f"Restauration depuis: {backup_file}")
        
        result = subprocess.run(cmd, env=env, capture_output=True, text=True)
        
        if result.returncode == 0:
            logger.info("✅ Restauration PostgreSQL réussie")
            return True
        else:
            logger.error(f"❌ Erreur restauration PostgreSQL: {result.stderr}")
            return False
            
    except Exception as e:
        logger.error(f"❌ Erreur lors de la restauration PostgreSQL: {e}")
        return False


def restore_sqlite(database_path: Path, backup_file: Path) -> bool:
    """
    Restaure une base de données SQLite depuis un backup.
    
    Args:
        database_path: Chemin vers le fichier SQLite de destination
        backup_file: Chemin vers le fichier de backup
        
    Returns:
        True si la restauration a réussi, False sinon
    """
    try:
        if not backup_file.exists():
            logger.error(f"Fichier de backup non trouvé: {backup_file}")
            return False
        
        logger.warning(f"⚠️ RESTAURATION EN COURS - La base de données sera écrasée!")
        logger.info(f"Restauration depuis: {backup_file}")
        
        # Créer une sauvegarde de sécurité avant restauration
        if database_path.exists():
            safety_backup = database_path.parent / f"{database_path.name}.safety_backup"
            import shutil
            shutil.copy2(database_path, safety_backup)
            logger.info(f"Backup de sécurité créé: {safety_backup}")
        
        # Restaurer
        import shutil
        shutil.copy2(backup_file, database_path)
        
        logger.info("✅ Restauration SQLite réussie")
        return True
        
    except Exception as e:
        logger.error(f"❌ Erreur lors de la restauration SQLite: {e}")
        return False


def list_backups(backup_dir: Path):
    """Liste tous les backups disponibles."""
    if not backup_dir.exists():
        logger.warning(f"Répertoire de backup non trouvé: {backup_dir}")
        return []
    
    backups = []
    for backup_file in sorted(backup_dir.glob("*_backup_*"), reverse=True):
        if backup_file.is_file():
            try:
                file_date_str = backup_file.stem.split('_backup_')[-1]
                file_date = datetime.strptime(file_date_str, "%Y%m%d_%H%M%S")
                backups.append((backup_file, file_date))
            except (ValueError, IndexError):
                backups.append((backup_file, None))
    
    return backups


def main():
    """Fonction principale de restauration."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Restaure la base de données depuis un backup")
    parser.add_argument(
        "--backup-file",
        type=str,
        help="Chemin vers le fichier de backup (optionnel, liste les backups si non spécifié)"
    )
    parser.add_argument(
        "--latest",
        action="store_true",
        help="Utiliser le backup le plus récent"
    )
    parser.add_argument(
        "--confirm",
        action="store_true",
        help="Confirmer la restauration (requis)"
    )
    
    args = parser.parse_args()
    
    backup_dir = BASE_DIR / "backups"
    
    # Lister les backups si aucun fichier spécifié
    if not args.backup_file and not args.latest:
        backups = list_backups(backup_dir)
        if backups:
            logger.info("📋 Backups disponibles:")
            for i, (backup_file, file_date) in enumerate(backups[:10], 1):
                date_str = file_date.strftime("%Y-%m-%d %H:%M:%S") if file_date else "Date inconnue"
                logger.info(f"  {i}. {backup_file.name} ({date_str})")
        else:
            logger.warning("Aucun backup trouvé")
        return
    
    # Déterminer le fichier de backup
    if args.latest:
        backups = list_backups(backup_dir)
        if not backups:
            logger.error("Aucun backup trouvé")
            return
        backup_file = backups[0][0]
    else:
        backup_file = Path(args.backup_file)
    
    if not backup_file.exists():
        logger.error(f"Fichier de backup non trouvé: {backup_file}")
        return
    
    # Confirmation requise
    if not args.confirm:
        logger.error("⚠️ La restauration va écraser la base de données actuelle!")
        logger.error("Utilisez --confirm pour confirmer")
        return
    
    # Restaurer
    if IS_POSTGRESQL:
        success = restore_postgresql(DATABASE_URL, backup_file)
    elif IS_SQLITE:
        db_path = Path(DATABASE_URL.replace("sqlite:///", ""))
        success = restore_sqlite(db_path, backup_file)
    else:
        logger.error("Type de base de données non supporté")
        return
    
    if success:
        logger.info("✅ Restauration terminée avec succès")
    else:
        logger.error("❌ Échec de la restauration")


if __name__ == "__main__":
    main()

