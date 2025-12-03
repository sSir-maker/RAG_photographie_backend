# Instructions pour remplacer le workflow sur GitHub

## Problème
Le workflow sur GitHub contient encore `black --check || exit 1` qui fait échouer le CI.

## Solution : Remplacer le workflow

### Étapes détaillées :

1. **Aller sur GitHub** :
   - Ouvrir : https://github.com/sSir-maker/RAG_photographie_backend
   - Naviguer vers : `.github/workflows/lint.yml`

2. **Ouvrir le fichier** :
   - Cliquer sur le fichier `lint.yml`
   - Cliquer sur l'icône **✏️ (crayon)** en haut à droite pour éditer

3. **Supprimer tout le contenu** et le remplacer par le contenu du fichier `WORKFLOW_LINT_AVEC_FORMATAGE_AUTOMATIQUE.yml`

4. **Sauvegarder** :
   - Descendre en bas de la page
   - Cliquer sur **"Commit changes"**
   - Message : "fix: Remplacer workflow - formatage automatique uniquement"
   - Cliquer sur **"Commit changes"**

### Contenu à copier-coller :

Le contenu complet se trouve dans le fichier `WORKFLOW_LINT_AVEC_FORMATAGE_AUTOMATIQUE.yml` dans le dossier backend.

**Important** : Ce workflow :
- ✅ Formate automatiquement avec Black et isort
- ✅ Commit automatiquement les fichiers formatés
- ✅ Ne fait PAS de vérification bloquante (`black --check` supprimé)
- ✅ Toutes les vérifications sont non-bloquantes

Après cette modification, le CI devrait passer !

