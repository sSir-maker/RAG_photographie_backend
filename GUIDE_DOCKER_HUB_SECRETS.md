# Guide : Configuration des secrets Docker Hub pour GitHub Actions

## Problème

Le workflow GitHub Actions échoue avec l'erreur :
```
Error: Username and password required
```

Cela signifie que les secrets Docker Hub ne sont pas configurés dans GitHub.

## Solution : Configurer les secrets GitHub Actions

### Étape 1 : Créer un compte Docker Hub (si nécessaire)

1. Allez sur [https://hub.docker.com](https://hub.docker.com)
2. Créez un compte gratuit (si vous n'en avez pas)
3. Notez votre **username** Docker Hub

### Étape 2 : Créer un Access Token Docker Hub

1. Connectez-vous à Docker Hub
2. Allez dans **Account Settings** → **Security**
3. Cliquez sur **New Access Token**
4. Donnez un nom au token (ex: "github-actions")
5. Copiez le token généré (⚠️ **Vous ne pourrez le voir qu'une seule fois !**)

### Étape 3 : Configurer les secrets dans GitHub

1. Allez sur votre dépôt GitHub : `https://github.com/sSir-maker/RAG_photographie_backend`
2. Cliquez sur **Settings** (en haut du dépôt)
3. Dans le menu de gauche, cliquez sur **Secrets and variables** → **Actions**
4. Cliquez sur **New repository secret**

#### Secret 1 : `DOCKER_USERNAME`
- **Name** : `DOCKER_USERNAME`
- **Secret** : Votre username Docker Hub (ex: `monsieur123`)
- Cliquez sur **Add secret**

#### Secret 2 : `DOCKER_PASSWORD`
- **Name** : `DOCKER_PASSWORD`
- **Secret** : Le **Access Token** que vous avez créé à l'étape 2 (⚠️ **PAS votre mot de passe Docker Hub**)
- Cliquez sur **Add secret**

### Étape 4 : Vérifier la configuration

1. Les deux secrets doivent apparaître dans la liste :
   - `DOCKER_USERNAME`
   - `DOCKER_PASSWORD`
2. Le workflow devrait maintenant fonctionner lors du prochain push

## Alternative : Désactiver Docker Hub (si non nécessaire)

Si vous n'avez pas besoin de pousser des images Docker Hub, le workflow a été modifié pour ignorer ces étapes si les secrets ne sont pas configurés.

Les étapes Docker Hub seront automatiquement ignorées si :
- `DOCKER_USERNAME` n'est pas configuré
- Vous êtes sur une Pull Request

## Vérification

Après avoir configuré les secrets, le workflow devrait :
1. ✅ Se connecter à Docker Hub
2. ✅ Builder les images backend et frontend
3. ✅ Pousser les images vers Docker Hub

## Notes importantes

- ⚠️ **Ne partagez JAMAIS vos secrets** publiquement
- ⚠️ Utilisez un **Access Token** (pas votre mot de passe)
- ⚠️ Les secrets sont cryptés et ne peuvent pas être lus après création
- ✅ Les secrets sont disponibles uniquement pour les workflows GitHub Actions

## Dépannage

### Erreur : "Username and password required"
→ Les secrets ne sont pas configurés ou mal nommés

### Erreur : "authentication required"
→ Le token Docker Hub est invalide ou expiré

### Erreur : "denied: requested access to the resource is denied"
→ Votre username Docker Hub est incorrect ou vous n'avez pas les permissions

