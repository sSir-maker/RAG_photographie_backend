# 🎨 Frontend RAG Photographie - Guide d'utilisation

## 📋 Vue d'ensemble

Frontend React/Next.js créé pour le RAG Photographie avec un design moderne inspiré de la photographie.

## 🚀 Démarrage rapide

### 1. Installer les dépendances

```bash
cd frontend
npm install
```

### 2. Démarrer l'API backend

Dans un terminal, depuis la racine du projet :

```bash
# Activer l'environnement virtuel
.\venv\Scripts\Activate.ps1

# Démarrer l'API
python run_api.py
```

L'API sera accessible sur http://localhost:8000

### 3. Démarrer le frontend

Dans un autre terminal :

```bash
cd frontend
npm run dev
```

Le frontend sera accessible sur http://localhost:3000

## 🎨 Fonctionnalités

### Interface de chat
- Pose des questions sur la photographie
- Réponses en temps réel basées sur tes documents
- Design moderne avec dégradés et animations

### Panneau des sources
- Affiche les documents utilisés pour générer la réponse
- Extrait du contenu de chaque source
- Nombre de sources utilisées

### Design
- Interface responsive (mobile et desktop)
- Dégradés bleu/indigo inspirés de la photographie
- Animations fluides
- États de chargement

## 📁 Structure du projet

```
frontend/
├── app/
│   └── page.tsx          # Page principale
├── components/
│   ├── ChatInterface.tsx # Interface de chat principale
│   ├── MessageList.tsx   # Liste des messages
│   ├── MessageBubble.tsx  # Bulle de message
│   ├── QuestionInput.tsx # Input pour les questions
│   ├── SourcesPanel.tsx  # Panneau des sources
│   └── Header.tsx        # En-tête
├── types/
│   └── index.ts          # Types TypeScript
└── package.json
```

## 🔧 Configuration

### Changer l'URL de l'API

Si l'API est sur un autre port, modifie `frontend/components/ChatInterface.tsx` :

```typescript
const response = await fetch('http://localhost:8000/ask', {
  // ...
});
```

## 🐛 Dépannage

### L'API ne répond pas
- Vérifie que l'API est démarrée : `python run_api.py`
- Vérifie que le port 8000 est libre
- Vérifie les logs de l'API

### Erreur CORS
- L'API est configurée pour accepter les requêtes depuis localhost:3000
- Si tu utilises un autre port, modifie `app/api.py` :

```python
allow_origins=["http://localhost:3000", "http://localhost:3001"]
```

### Les sources ne s'affichent pas
- Vérifie que l'API retourne bien les sources
- Ouvre la console du navigateur (F12) pour voir les erreurs

## 📝 Notes

- Le design est inspiré de la photographie avec des couleurs bleu/indigo
- L'interface est entièrement responsive
- Les messages sont formatés avec Markdown (via prose classes Tailwind)

