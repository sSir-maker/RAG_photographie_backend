# ⚡ Optimisations RAG - Réduction de la Latence

## 🎯 Objectif
Réduire le temps de réponse moyen de **10 secondes à 2-3 secondes**.

## ✅ Optimisations Appliquées

### 1. **Réduction du nombre de documents** (gain: ~0.5-1s)
- **Avant**: 3 documents récupérés
- **Après**: 2 documents par défaut
- **Configuration**: `NUM_RETRIEVAL_DOCS=2` dans `.env`

### 2. **Optimisation des prompts** (gain: ~1-2s)
- **Avant**: Prompt long et détaillé (~300 caractères)
- **Après**: Prompt concis et optimisé (~150 caractères)
- **Impact**: Réduction du temps de traitement par le LLM

### 3. **Troncature intelligente du contexte** (gain: ~1s)
- **Avant**: Tout le contexte des documents récupérés
- **Après**: Limité à 1500 caractères maximum
- **Configuration**: `MAX_CONTEXT_LENGTH=1500` dans `.env`
- Chaque document limité à 500 caractères

### 4. **Réduction de la longueur de réponse** (gain: ~1-2s)
- **Avant**: `num_predict=512` tokens
- **Après**: `num_predict=400` tokens
- **Impact**: Génération plus rapide

### 5. **Timing détaillé** (gain: visibilité)
- Ajout de logs détaillés pour identifier les goulots d'étranglement
- Mesure séparée pour:
  - Chargement du vector store
  - Recherche vectorielle
  - Génération LLM

### 6. **Optimisation du streaming** (gain: perception)
- Délai de streaming réduit à 0ms
- Pas d'attente artificielle entre les tokens

## 📊 Résultats Attendus

| Composant | Avant | Après (attendu) |
|-----------|-------|-----------------|
| Vector store load | ~1-2s | ~0.1-0.5s (cache) |
| Recherche vectorielle | ~0.5-1s | ~0.3-0.5s |
| Génération LLM | ~5-7s | ~2-3s |
| **TOTAL** | **~10s** | **~2-3s** |

## 🔧 Configuration

Ajoutez dans votre `.env`:

```env
# Nombre de documents à récupérer (2 par défaut, plus rapide)
NUM_RETRIEVAL_DOCS=2

# Taille maximale du contexte en caractères (1500 par défaut)
MAX_CONTEXT_LENGTH=1500

# Délai de streaming en secondes (0 par défaut pour plus de rapidité)
STREAMING_DELAY=0
```

## 📝 Logs de Performance

Les logs affichent maintenant:

```
📦 Vector store chargé en 125.50ms
🔍 Recherche vectorielle en 340.20ms
⚡ RAG réponse générée en 2340.15ms (vector_store: 125.50ms, retrieval: 340.20ms, generation: 1874.45ms)
```

## 🚀 Prochaines Optimisations Possibles

1. **Cache des embeddings de requêtes** (gain: 2-3s)
   - Mettre en cache les embeddings des questions fréquentes
   - Utiliser Redis ou cache mémoire

2. **Async/Await** (gain: 1-2s)
   - Paralléliser les opérations indépendantes
   - Utiliser `asyncio.gather()` pour les opérations parallèles

3. **Modèle d'embedding plus rapide** (gain: 1-2s)
   - Utiliser un modèle plus léger comme `all-MiniLM-L6-v2` (déjà utilisé)
   - Ou un modèle quantifié

4. **Optimisation de la recherche vectorielle** (gain: 0.5-1s)
   - Utiliser un index HNSW optimisé
   - Réduire la dimension des embeddings si possible

## ⚠️ Notes

- Ces optimisations réduisent légèrement la qualité des réponses (moins de contexte)
- Le compromis vitesse/qualité peut être ajusté via les variables d'environnement
- Surveillez les logs pour identifier d'autres goulots d'étranglement
