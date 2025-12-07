# ⚡ Démarrage Rapide - Configuration .env

## 🎯 Créer le fichier .env en 3 étapes

### Étape 1 : Créer le fichier

```bash
# Copier le template
Copy-Item .env.example .env
```

### Étape 2 : Générer un SECRET_KEY

```bash
python -c "from app.security import generate_secret_key; print(generate_secret_key())"
```

### Étape 3 : Éditer .env

Ouvre le fichier `.env` et remplace :
```env
SECRET_KEY=change-me-in-production-generate-a-strong-secret
```

Par le SECRET_KEY généré à l'étape 2.

## 📍 Emplacement

Le fichier `.env` doit être ici :
```
E:\RAG-Photographie\.env
```

## ✅ Vérifier

```bash
# Vérifier que le fichier existe
Test-Path .env
```

## 🔒 Important

- Le fichier `.env` est dans `.gitignore` (ne sera pas commité)
- Ne partage JAMAIS ton fichier `.env`
- Utilise `.env.example` comme template pour les autres développeurs

