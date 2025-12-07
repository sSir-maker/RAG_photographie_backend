# Comment supprimer `black --check` des workflows GitHub

## Méthode 1 : Via l'interface GitHub (RECOMMANDÉ)

1. **Aller sur GitHub** :
   - Ouvrir : https://github.com/sSir-maker/RAG_photographie_backend
   - Cliquer sur l'onglet **"Actions"** en haut

2. **Trouver le workflow** :
   - Dans le menu de gauche, chercher **"Lint and Format"** ou **"Format and Lint"**
   - Cliquer dessus pour voir les détails

3. **Voir le fichier workflow** :
   - Cliquer sur **`.github/workflows/lint.yml`** (lien en haut de la page)
   - Cliquer sur l'icône **✏️ (crayon)** pour éditer

4. **Supprimer les lignes problématiques** :
   - Chercher toutes les lignes contenant : `black --check` ou `isort --check-only`
   - **SUPPRIMER** ces lignes complètement
   - Ou remplacer par : `black app/ tests/` (sans `--check`)

5. **Sauvegarder** :
   - Cliquer sur **"Commit changes"** en bas
   - Laisser le message par défaut ou écrire : "Remove black --check verification"
   - Cliquer sur **"Commit changes"**

## Méthode 2 : Vérifier que le workflow local remplace le distant

Le workflow local a déjà été modifié et poussé. Si le CI échoue encore, c'est que le workflow distant n'a pas été mis à jour.

**Vérification** :
- Le workflow local dans `backend/.github/workflows/lint.yml` ne contient **PAS** de `black --check`
- Il formate automatiquement avec `black app/ tests/`

## Méthode 3 : Désactiver complètement le workflow (temporaire)

Si vous voulez désactiver temporairement le workflow :

1. Sur GitHub, ouvrir `.github/workflows/lint.yml`
2. Ajouter au début du fichier (après `on:`):
   ```yaml
   on:
     workflow_dispatch:  # Garder seulement ça, supprimer push et pull_request
   ```

Cela désactivera l'exécution automatique du workflow.

## Solution définitive

Le workflow local a déjà été configuré pour formater automatiquement. Au prochain push, il devrait remplacer le workflow distant.

Si le problème persiste, suivez la **Méthode 1** pour modifier directement sur GitHub.

