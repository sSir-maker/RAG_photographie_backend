# 📝 Créer le fichier .env

## 📍 Où se trouve le fichier .env ?

Le fichier `.env` doit être créé **à la racine du projet** :
```
E:\RAG-Photographie\.env
```

## 🚀 Création rapide

### Option 1 : Copier depuis .env.example (Recommandé)

```bash
# Dans PowerShell
Copy-Item .env.example .env

# Ou manuellement :
# 1. Copier le fichier .env.example
# 2. Le renommer en .env
# 3. Éditer les valeurs
```

### Option 2 : Créer manuellement

1. Créer un nouveau fichier nommé `.env` à la racine du projet
2. Copier le contenu de `.env.example`
3. Modifier les valeurs selon tes besoins

## 🔑 Générer un SECRET_KEY

**Important** : Génère un SECRET_KEY fort pour la production !

```bash
python -c "from app.security import generate_secret_key; print(generate_secret_key())"
```

Copie le résultat et colle-le dans `.env` :
```env
SECRET_KEY=ton-secret-key-genere-ici
```

## ✅ Vérification

```bash
# Vérifier que le fichier existe
if (Test-Path .env) { Write-Host "✅ .env existe" } else { Write-Host "❌ .env n'existe pas" }

# Voir le contenu (sans afficher les secrets)
Get-Content .env | Select-String -Pattern "^[^#]" | Select-String -NotMatch "SECRET_KEY"
```

## 📋 Variables minimales requises

Pour que l'application fonctionne, tu dois au minimum configurer :

```env
# SECRET_KEY (OBLIGATOIRE pour la sécurité)
SECRET_KEY=ton-secret-key-genere

# Optionnel mais recommandé
OLLAMA_BASE_URL=http://localhost:11434
LLM_MODEL_NAME=llama3
PHOENIX_ENDPOINT=http://localhost:6006
```

## ⚠️ Sécurité

- **NE JAMAIS** commiter le fichier `.env` dans Git
- Le fichier `.env` est déjà dans `.gitignore`
- Utilise `.env.example` comme template
- Génère un SECRET_KEY différent pour chaque environnement

## 📍 Emplacement

```
E:\RAG-Photographie\
├── .env              ← ICI (à créer)
├── .env.example     ← Template (déjà créé)
├── app/
├── data/
└── ...
```

