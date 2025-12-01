# ✅ Phoenix Installation - RÉSOLU

## Problème résolu

Le package Phoenix a été installé avec succès et le code a été mis à jour pour utiliser la nouvelle API Phoenix 12.

## ✅ Installation réussie

```bash
pip install arize-phoenix>=12.0.0
pip install openinference-instrumentation-langchain>=0.1.0
```

## 🔧 Changements API Phoenix 12

Phoenix 12 utilise une nouvelle API basée sur OpenTelemetry :

### Ancienne API (Phoenix < 12)
```python
from phoenix.trace import OpenInferenceTracer
from phoenix.trace.langchain import LangChainInstrumentor
tracer = OpenInferenceTracer()
```

### Nouvelle API (Phoenix 12+)
```python
from phoenix.otel import register
from openinference.instrumentation.langchain import LangChainInstrumentor
from phoenix.trace.otel import INPUT_VALUE, OUTPUT_VALUE
from opentelemetry import trace as otel_trace

# Enregistrer Phoenix
tracer_provider = register()

# Instrumenter LangChain
instrumentor = LangChainInstrumentor()
instrumentor.instrument(tracer_provider=tracer_provider)

# Utiliser OpenTelemetry pour tracer
tracer = otel_trace.get_tracer(__name__)
with tracer.start_as_current_span("my_span") as span:
    span.set_attribute(INPUT_VALUE, "query")
    span.set_attribute(OUTPUT_VALUE, "response")
```

## 📦 Packages requis

- `arize-phoenix>=12.0.0` - Package principal
- `openinference-instrumentation-langchain>=0.1.0` - Instrumentation LangChain
- `openinference-semantic-conventions` - Inclus dans arize-phoenix

## 🚀 Utilisation

1. **Démarrer Phoenix Dashboard** :
   ```bash
   phoenix serve --port 6006
   ```
   
   **Note** : Si la commande `phoenix` n'est pas reconnue :
   ```bash
   python -m phoenix.server.main serve --port 6006
   ```

2. **Démarrer l'API** (Phoenix s'initialisera automatiquement) :
   ```bash
   python run_api.py
   ```

3. **Accéder au dashboard** : http://localhost:6006

## ✅ Vérification

```python
from app.monitoring_phoenix import get_phoenix_monitor
monitor = get_phoenix_monitor()
print(f"Phoenix activé: {monitor.enabled}")  # True
```

## 📝 Notes

- Phoenix 12+ utilise OpenTelemetry comme backend de tracing
- L'instrumentation LangChain est automatique une fois configurée
- Les traces sont envoyées au dashboard Phoenix sur le port 6006

