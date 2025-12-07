#!/bin/bash
# Script bash pour planifier les backups automatiques (Linux/Mac)
# À exécuter une fois pour configurer le cron job

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
VENV_PYTHON="$PROJECT_ROOT/venv/bin/python"
BACKUP_SCRIPT="$SCRIPT_DIR/backup_database.py"
LOG_FILE="$PROJECT_ROOT/logs/backup.log"

# Créer le répertoire de logs
mkdir -p "$PROJECT_ROOT/logs"

# Créer le cron job (backup quotidien à 2h du matin)
CRON_JOB="0 2 * * * cd $PROJECT_ROOT && $VENV_PYTHON $BACKUP_SCRIPT >> $LOG_FILE 2>&1"

# Vérifier si le cron job existe déjà
if crontab -l 2>/dev/null | grep -q "$BACKUP_SCRIPT"; then
    echo "⚠️  Le cron job existe déjà"
    read -p "Voulez-vous le remplacer? (y/n) " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        # Supprimer l'ancien cron job
        crontab -l 2>/dev/null | grep -v "$BACKUP_SCRIPT" | crontab -
    else
        echo "Annulé"
        exit 0
    fi
fi

# Ajouter le nouveau cron job
(crontab -l 2>/dev/null; echo "$CRON_JOB") | crontab -

echo "✅ Cron job créé avec succès"
echo "   - Exécution: Quotidienne à 2h du matin"
echo "   - Script: $BACKUP_SCRIPT"
echo "   - Logs: $LOG_FILE"

# Vérifier
if crontab -l 2>/dev/null | grep -q "$BACKUP_SCRIPT"; then
    echo "✅ Cron job vérifié avec succès"
    echo ""
    echo "Cron jobs actuels:"
    crontab -l | grep "$BACKUP_SCRIPT"
else
    echo "❌ Erreur lors de la création du cron job"
    exit 1
fi

