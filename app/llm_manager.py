"""
Gestionnaire multi-LLM pour supporter plusieurs modèles.
"""
import os
import logging
from typing import Optional, Dict, Any, List
from enum import Enum

logger = logging.getLogger(__name__)


class LLMProvider(Enum):
    """Fournisseurs de LLM supportés."""
    OLLAMA = "ollama"
    OPENAI = "openai"
    HUGGINGFACE = "huggingface"
    ANTHROPIC = "anthropic"


class LLMConfig:
    """Configuration pour un modèle LLM."""
    
    def __init__(
        self,
        name: str,
        provider: LLMProvider,
        model_name: str,
        base_url: Optional[str] = None,
        api_key: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: Optional[int] = None,
        **kwargs
    ):
        self.name = name
        self.provider = provider
        self.model_name = model_name
        self.base_url = base_url
        self.api_key = api_key
        self.temperature = temperature
        self.max_tokens = max_tokens
        self.extra_params = kwargs


class LLMManager:
    """Gestionnaire pour plusieurs modèles LLM."""
    
    def __init__(self):
        self.llms: Dict[str, LLMConfig] = {}
        self.default_llm: Optional[str] = None
        self._initialize_default_llms()
    
    def _initialize_default_llms(self):
        """Initialise les LLM par défaut depuis les variables d'environnement."""
        # Ollama (par défaut)
        ollama_base_url = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
        ollama_model = os.getenv("LLM_MODEL_NAME", "llama3")
        
        self.add_llm(
            "ollama_default",
            LLMProvider.OLLAMA,
            ollama_model,
            base_url=ollama_base_url
        )
        self.set_default("ollama_default")
        
        # OpenAI (si configuré)
        openai_api_key = os.getenv("OPENAI_API_KEY")
        if openai_api_key:
            openai_model = os.getenv("OPENAI_MODEL", "gpt-3.5-turbo")
            self.add_llm(
                "openai_default",
                LLMProvider.OPENAI,
                openai_model,
                api_key=openai_api_key
            )
        
        # HuggingFace (si configuré)
        hf_api_key = os.getenv("HUGGINGFACE_API_KEY")
        if hf_api_key:
            hf_model = os.getenv("HUGGINGFACE_MODEL", "mistralai/Mistral-7B-Instruct-v0.1")
            self.add_llm(
                "huggingface_default",
                LLMProvider.HUGGINGFACE,
                hf_model,
                api_key=hf_api_key
            )
    
    def add_llm(
        self,
        name: str,
        provider: LLMProvider,
        model_name: str,
        base_url: Optional[str] = None,
        api_key: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: Optional[int] = None,
        **kwargs
    ):
        """Ajoute un nouveau LLM."""
        config = LLMConfig(
            name=name,
            provider=provider,
            model_name=model_name,
            base_url=base_url,
            api_key=api_key,
            temperature=temperature,
            max_tokens=max_tokens,
            **kwargs
        )
        self.llms[name] = config
        logger.info(f"LLM ajouté: {name} ({provider.value}/{model_name})")
    
    def set_default(self, name: str):
        """Définit le LLM par défaut."""
        if name not in self.llms:
            raise ValueError(f"LLM '{name}' non trouvé")
        self.default_llm = name
        logger.info(f"LLM par défaut: {name}")
    
    def get_llm(self, name: Optional[str] = None):
        """
        Récupère une instance LangChain LLM.
        
        Args:
            name: Nom du LLM (None = utiliser le défaut)
        
        Returns:
            Instance LangChain LLM
        """
        llm_name = name or self.default_llm
        if not llm_name or llm_name not in self.llms:
            raise ValueError(f"LLM '{llm_name}' non trouvé")
        
        config = self.llms[llm_name]
        
        if config.provider == LLMProvider.OLLAMA:
            from langchain_community.llms import Ollama
            return Ollama(
                model=config.model_name,
                base_url=config.base_url,
                temperature=config.temperature,
                **config.extra_params
            )
        
        elif config.provider == LLMProvider.OPENAI:
            from langchain_openai import ChatOpenAI
            return ChatOpenAI(
                model_name=config.model_name,
                api_key=config.api_key,
                temperature=config.temperature,
                max_tokens=config.max_tokens,
                **config.extra_params
            )
        
        elif config.provider == LLMProvider.HUGGINGFACE:
            from langchain_community.llms import HuggingFaceEndpoint
            return HuggingFaceEndpoint(
                endpoint_url=f"https://api-inference.huggingface.co/models/{config.model_name}",
                huggingface_api_key=config.api_key,
                temperature=config.temperature,
                max_length=config.max_tokens or 512,
                **config.extra_params
            )
        
        elif config.provider == LLMProvider.ANTHROPIC:
            from langchain_anthropic import ChatAnthropic
            return ChatAnthropic(
                model=config.model_name,
                api_key=config.api_key,
                temperature=config.temperature,
                max_tokens=config.max_tokens,
                **config.extra_params
            )
        
        else:
            raise ValueError(f"Provider non supporté: {config.provider}")
    
    def list_llms(self) -> List[Dict[str, Any]]:
        """Liste tous les LLM disponibles."""
        return [
            {
                "name": name,
                "provider": config.provider.value,
                "model_name": config.model_name,
                "is_default": name == self.default_llm,
            }
            for name, config in self.llms.items()
        ]
    
    def get_llm_info(self, name: Optional[str] = None) -> Dict[str, Any]:
        """Récupère les informations sur un LLM."""
        llm_name = name or self.default_llm
        if not llm_name or llm_name not in self.llms:
            raise ValueError(f"LLM '{llm_name}' non trouvé")
        
        config = self.llms[llm_name]
        return {
            "name": config.name,
            "provider": config.provider.value,
            "model_name": config.model_name,
            "temperature": config.temperature,
            "max_tokens": config.max_tokens,
            "is_default": llm_name == self.default_llm,
        }


# Instance globale
_llm_manager: Optional[LLMManager] = None


def get_llm_manager() -> LLMManager:
    """Récupère l'instance globale du gestionnaire LLM."""
    global _llm_manager
    if _llm_manager is None:
        _llm_manager = LLMManager()
    return _llm_manager

