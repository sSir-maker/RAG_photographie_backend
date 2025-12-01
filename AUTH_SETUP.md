# 🔐 Configuration de l'Authentification

Le système d'authentification a été ajouté au serveur avec **Signup** et **Login**.

## ✅ Fonctionnalités

- **Inscription** (`/auth/signup`) : Création de nouveaux comptes utilisateurs
- **Connexion** (`/auth/login`) : Authentification des utilisateurs existants
- **Tokens JWT** : Authentification sécurisée avec tokens valides 7 jours
- **Protection des endpoints** : L'endpoint `/ask` nécessite maintenant une authentification
- **Stockage sécurisé** : Mots de passe hashés avec bcrypt, stockage dans `storage/users.json`

## 📦 Installation des dépendances

### Backend

```powershell
# Activer l'environnement virtuel
.\venv\Scripts\Activate.ps1

# Installer les nouvelles dépendances
pip install python-jose[cryptography]==3.3.0 passlib[bcrypt]==1.7.4
```

Ou simplement :

```powershell
pip install -r requirements.txt
```

### Frontend

Aucune nouvelle dépendance nécessaire, tout est déjà dans `frontend_RAG`.

## 🚀 Utilisation

### 1. Démarrer l'API

```powershell
python run_api.py
```

### 2. Démarrer le frontend

```powershell
cd frontend_RAG
npm run dev
```

### 3. Créer un compte

1. Ouvre http://localhost:3000
2. Clique sur "S'inscrire" si tu n'as pas de compte
3. Remplis le formulaire :
   - **Nom** : Ton nom complet
   - **Email** : Ton adresse email
   - **Mot de passe** : Au moins 6 caractères
4. Clique sur "Créer un compte"

### 4. Se connecter

1. Si tu as déjà un compte, utilise "Se connecter"
2. Entre ton email et mot de passe
3. Tu seras automatiquement connecté

## 🔧 Endpoints API

### POST `/auth/signup`

Inscription d'un nouvel utilisateur.

**Body** :
```json
{
  "name": "Jean Dupont",
  "email": "jean@example.com",
  "password": "monmotdepasse"
}
```

**Réponse** :
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "user": {
    "name": "Jean Dupont",
    "email": "jean@example.com",
    "created_at": "2024-01-01T12:00:00"
  }
}
```

### POST `/auth/login`

Connexion d'un utilisateur existant.

**Body** :
```json
{
  "email": "jean@example.com",
  "password": "monmotdepasse"
}
```

**Réponse** : Même format que `/auth/signup`

### GET `/auth/me`

Récupère les informations de l'utilisateur connecté.

**Headers** :
```
Authorization: Bearer <token>
```

**Réponse** :
```json
{
  "email": "jean@example.com",
  "name": "Jean Dupont"
}
```

### POST `/ask`

Pose une question au RAG (nécessite une authentification).

**Headers** :
```
Authorization: Bearer <token>
Content-Type: application/json
```

**Body** :
```json
{
  "question": "Qu'est-ce que l'ISO en photographie ?",
  "force_rebuild": false
}
```

## 🔒 Sécurité

- **Mots de passe hashés** : Utilisation de bcrypt pour le hashage
- **Tokens JWT** : Tokens signés avec une clé secrète
- **Expiration** : Tokens valides 7 jours
- **Validation** : Vérification des tokens à chaque requête protégée

## 📁 Fichiers créés/modifiés

### Backend
- `app/auth.py` : Module d'authentification (nouveau)
- `app/api.py` : Endpoints d'authentification ajoutés
- `requirements.txt` : Dépendances ajoutées
- `storage/users.json` : Stockage des utilisateurs (créé automatiquement)

### Frontend
- `frontend_RAG/src/App.tsx` : Intégration de l'authentification
- `frontend_RAG/src/components/AuthPage.tsx` : Gestion des erreurs et chargement

## ⚠️ Notes importantes

1. **Clé secrète JWT** : En production, change la clé secrète dans `app/auth.py` :
   ```python
   SECRET_KEY = os.getenv("JWT_SECRET_KEY", "your-secret-key-change-in-production")
   ```
   Utilise une variable d'environnement pour la sécurité.

2. **Stockage des utilisateurs** : Actuellement dans un fichier JSON. Pour la production, migre vers une vraie base de données (PostgreSQL, MongoDB, etc.).

3. **Tokens** : Les tokens sont stockés dans `localStorage` du navigateur. Ils persistent entre les sessions.

4. **Déconnexion** : Le bouton de déconnexion dans la sidebar supprime le token et déconnecte l'utilisateur.

## 🐛 Dépannage

### Erreur "Token invalide ou expiré"

- Le token a expiré (7 jours) ou est invalide
- Solution : Déconnecte-toi et reconnecte-toi

### Erreur "Cet email est déjà utilisé"

- Tu essaies de créer un compte avec un email existant
- Solution : Utilise un autre email ou connecte-toi avec cet email

### Erreur "Email ou mot de passe incorrect"

- Vérifie que tu utilises le bon email et mot de passe
- Solution : Réinitialise ton mot de passe (fonctionnalité à ajouter si nécessaire)

