# 🔌 Intégration API Backend

Le frontend a été modifié pour utiliser l'API backend RAG au lieu des réponses mockées.

## ✅ Modifications apportées

**Fichier modifié : `src/App.tsx`**
- La fonction `handleSendMessage` appelle maintenant l'API backend (`http://localhost:8000/ask`)
- Suppression de la fonction `generateMockResponse` (plus utilisée)
- Ajout de la gestion des erreurs et des états de chargement

**Design : AUCUNE modification** - Le design reste exactement le même.

## 🚀 Utilisation

### 1. Démarrer l'API backend

Dans un terminal, depuis la racine du projet :

```bash
# Activer l'environnement virtuel
.\venv\Scripts\Activate.ps1

# Démarrer l'API
python run_api.py
```

L'API sera accessible sur http://localhost:8001

### 2. Démarrer le frontend

Dans un autre terminal :

```bash
cd frontend_RAG
npm run dev
```

Le frontend sera accessible sur http://localhost:3000

## 🔧 Configuration

L'API utilise le port **8001** par défaut. Si tu veux changer le port :

1. Modifie `run_api.py` :
```python
uvicorn.run("app.api:app", host="0.0.0.0", port=8002, reload=True)  # Change le port ici
```

2. Modifie `frontend_RAG/src/App.tsx` ligne ~131 :
```typescript
const response = await fetch('http://localhost:8002/ask', {  // Même port que ci-dessus
  // ...
});
```

## 📝 Notes

- Le design et tous les composants UI restent inchangés
- Seule la logique d'appel API a été modifiée
- Les fonctionnalités (thèmes, sidebar, upload d'images) fonctionnent toujours

