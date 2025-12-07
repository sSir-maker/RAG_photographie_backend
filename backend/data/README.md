# 📁 Dossier des Documents Photographie

**C'est ici que tu dois placer tous tes documents sur la photographie !**

## 📍 Emplacement

```
E:\RAG-Photographie\data\
```

## 📄 Formats de fichiers supportés

Place tous tes documents dans ce dossier (ou dans des sous-dossiers) :

### ✅ Formats supportés :

- **📝 Fichiers texte** :
  - `.txt` - Documents texte simples
  - `.md` - Fichiers Markdown

- **📚 PDFs** :
  - `.pdf` - Livres, manuels, tutoriels (texte normal)
  - PDFs scannés (avec OCR automatique)
  - **PDFs avec images intégrées** (photos, schémas, diagrammes) ✨

- **🖼️ Images** :
  - `.jpg`, `.jpeg` - Photos de documents
  - `.png` - Images de pages, captures d'écran
  - `.tif`, `.tiff` - Images haute qualité

- **📊 Données structurées** :
  - `.csv` - Tableaux de réglages, métadonnées

## 📁 Organisation recommandée

Tu peux organiser tes documents comme tu veux :

```
data/
├── livres/
│   ├── guide_photographie.pdf
│   └── technique_eclairage.pdf
├── tutoriels/
│   ├── portrait_naturel.txt
│   └── paysage_composition.md
├── fiches_techniques/
│   ├── reglages_boitiers.csv
│   └── schema_eclairage.png
└── notes/
    └── mes_notes_photo.pdf
```

Le système parcourra **récursivement** tous les fichiers dans `data/` et ses sous-dossiers.

## 🚀 Comment utiliser

1. **Ajoute tes documents** dans ce dossier (`data/`)

2. **Lance le pipeline** :
   ```bash
   python app/run_example.py
   ```

3. Le système va automatiquement :
   - Détecter tous les fichiers
   - Faire de l'OCR si nécessaire (PDFs scannés, images)
   - Créer le vector store
   - Répondre à tes questions sur la photo !

## 💡 Exemples de documents à ajouter

- 📖 Livres de photographie (PDF)
- 📝 Tutoriels et guides (TXT, MD, PDF)
- 🖼️ Photos de pages de livres scannées (JPG, PNG)
- 📊 Tableaux de réglages (CSV)
- 📋 Notes personnelles (TXT, PDF)
- 🔧 Manuels de boîtiers/appareils (PDF)

## ⚠️ Note importante

- Les documents doivent être en **français** ou **anglais** pour une meilleure qualité d'OCR
- Plus tu ajoutes de documents pertinents, meilleures seront les réponses du RAG !

