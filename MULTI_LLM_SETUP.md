# 🤖 Support Multi-LLM

## 📋 Vue d'ensemble

Le système supporte plusieurs fournisseurs de LLM.

## 🔧 Fournisseurs Supportés

### 1. Ollama (par défaut)

Configuration dans `.env` :
```env
OLLAMA_BASE_URL=http://localhost:11434
LLM_MODEL_NAME=llama3
```

### 2. OpenAI

Configuration dans `.env` :
```env
OPENAI_API_KEY=sk-...
OPENAI_MODEL=gpt-3.5-turbo
```

### 3. HuggingFace

Configuration dans `.env` :
```env
HUGGINGFACE_API_KEY=hf_...
HUGGINGFACE_MODEL=mistralai/Mistral-7B-Instruct-v0.1
```

### 4. Anthropic (Claude)

Configuration dans `.env` :
```env
ANTHROPIC_API_KEY=sk-ant-...
ANTHROPIC_MODEL=claude-3-sonnet-20240229
```

## 🔗 Endpoints

### Lister les LLM disponibles

```bash
GET /llms
```

Retourne :
```json
{
  "llms": [
    {
      "name": "ollama_default",
      "provider": "ollama",
      "model_name": "llama3",
      "is_default": true
    },
    {
      "name": "openai_default",
      "provider": "openai",
      "model_name": "gpt-3.5-turbo",
      "is_default": false
    }
  ]
}
```

### Informations sur un LLM

```bash
GET /llms/{llm_name}
```

### Utiliser un LLM spécifique

```bash
POST /ask?llm_name=openai_default
```

## 🚀 Ajouter un LLM personnalisé

En Python :
```python
from app.llm_manager import get_llm_manager, LLMProvider

manager = get_llm_manager()
manager.add_llm(
    name="my_custom_llm",
    provider=LLMProvider.OLLAMA,
    model_name="mistral",
    base_url="http://localhost:11434",
    temperature=0.8
)
manager.set_default("my_custom_llm")
```

## 📊 Comparaison des Fournisseurs

| Fournisseur | Avantages | Inconvénients |
|------------|-----------|---------------|
| **Ollama** | Gratuit, local, privé | Nécessite GPU |
| **OpenAI** | Rapide, fiable | Payant, API externe |
| **HuggingFace** | Gratuit (limité), nombreux modèles | Rate limits |
| **Anthropic** | Très performant | Payant, API externe |

## ✅ Checklist

- [ ] Ollama configuré
- [ ] OpenAI configuré (optionnel)
- [ ] HuggingFace configuré (optionnel)
- [ ] Anthropic configuré (optionnel)
- [ ] Test avec différents LLM

---

**✅ Support multi-LLM implémenté !**

