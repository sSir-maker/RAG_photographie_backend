# Script PowerShell pour planifier les backups automatiques
# À exécuter une fois pour configurer la tâche planifiée Windows

$scriptPath = Join-Path $PSScriptRoot "backup_database.py"
$projectRoot = Split-Path $PSScriptRoot -Parent
$pythonExe = Join-Path $projectRoot "venv\Scripts\python.exe"

if (-not (Test-Path $pythonExe)) {
    Write-Host "❌ Python non trouvé dans venv. Activez d'abord l'environnement virtuel."
    exit 1
}

# Créer la tâche planifiée
$taskName = "RAG-Photographie-Backup"
$taskDescription = "Backup quotidien de la base de données RAG Photographie"

# Supprimer la tâche si elle existe déjà
Unregister-ScheduledTask -TaskName $taskName -Confirm:$false -ErrorAction SilentlyContinue

# Créer la nouvelle tâche
$action = New-ScheduledTaskAction -Execute $pythonExe -Argument "`"$scriptPath`"" -WorkingDirectory $projectRoot
$trigger = New-ScheduledTaskTrigger -Daily -At 2am
$settings = New-ScheduledTaskSettingsSet -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries -StartWhenAvailable

Register-ScheduledTask -TaskName $taskName -Description $taskDescription -Action $action -Trigger $trigger -Settings $settings -RunLevel Highest

Write-Host "✅ Tâche planifiée créée: $taskName"
Write-Host "   - Exécution: Quotidienne à 2h du matin"
Write-Host "   - Script: $scriptPath"

# Vérifier
$task = Get-ScheduledTask -TaskName $taskName -ErrorAction SilentlyContinue
if ($task) {
    Write-Host "✅ Tâche vérifiée avec succès"
} else {
    Write-Host "❌ Erreur lors de la création de la tâche"
}

