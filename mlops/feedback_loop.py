"""
Boucle de feedback pour améliorer le RAG.
Collecte les retours utilisateurs et prépare les données pour le retraining.
"""
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any, Optional
import json
import logging
from dataclasses import dataclass, asdict

logger = logging.getLogger(__name__)


@dataclass
class UserFeedback:
    """Feedback d'un utilisateur sur une réponse RAG."""
    timestamp: str
    question: str
    answer: str
    sources: List[str]
    rating: int  # 1-5
    feedback_text: Optional[str] = None
    corrected_answer: Optional[str] = None
    user_id: Optional[str] = None


class FeedbackCollector:
    """Collecte et gère les feedbacks utilisateurs."""
    
    def __init__(self, feedback_dir: Path = None):
        if feedback_dir is None:
            feedback_dir = Path("mlops/feedback")
        self.feedback_dir = feedback_dir
        self.feedback_dir.mkdir(parents=True, exist_ok=True)
        
        self.feedback_file = self.feedback_dir / "user_feedback.jsonl"
        self.training_data_file = self.feedback_dir / "training_data.jsonl"
    
    def save_feedback(self, feedback: UserFeedback):
        """Sauvegarde un feedback utilisateur."""
        with open(self.feedback_file, 'a', encoding='utf-8') as f:
            f.write(json.dumps(asdict(feedback), ensure_ascii=False) + '\n')
        logger.info(f"Feedback enregistré: rating={feedback.rating}")
    
    def get_feedback(self, min_rating: int = None) -> List[Dict[str, Any]]:
        """Récupère les feedbacks (optionnellement filtrés par rating minimum)."""
        feedbacks = []
        
        if not self.feedback_file.exists():
            return feedbacks
        
        with open(self.feedback_file, 'r', encoding='utf-8') as f:
            for line in f:
                try:
                    feedback = json.loads(line)
                    if min_rating is None or feedback.get("rating", 0) >= min_rating:
                        feedbacks.append(feedback)
                except Exception as e:
                    logger.warning(f"Erreur lecture feedback: {e}")
        
        return feedbacks
    
    def prepare_training_data(self) -> List[Dict[str, Any]]:
        """Prépare les données de training à partir des feedbacks."""
        training_data = []
        
        # Récupérer les feedbacks avec corrections
        feedbacks = self.get_feedback()
        
        for feedback in feedbacks:
            if feedback.get("corrected_answer"):
                # Créer une paire question-réponse corrigée
                training_data.append({
                    "question": feedback["question"],
                    "answer": feedback["corrected_answer"],
                    "original_answer": feedback["answer"],
                    "rating": feedback["rating"],
                    "sources": feedback.get("sources", []),
                    "timestamp": feedback["timestamp"]
                })
        
        # Sauvegarder les données de training
        with open(self.training_data_file, 'w', encoding='utf-8') as f:
            for item in training_data:
                f.write(json.dumps(item, ensure_ascii=False) + '\n')
        
        logger.info(f"{len(training_data)} exemples de training préparés")
        return training_data
    
    def get_statistics(self) -> Dict[str, Any]:
        """Calcule les statistiques sur les feedbacks."""
        feedbacks = self.get_feedback()
        
        if not feedbacks:
            return {
                "total_feedbacks": 0,
                "avg_rating": 0.0,
                "with_corrections": 0
            }
        
        ratings = [f.get("rating", 0) for f in feedbacks if f.get("rating")]
        corrections = [f for f in feedbacks if f.get("corrected_answer")]
        
        return {
            "total_feedbacks": len(feedbacks),
            "avg_rating": sum(ratings) / len(ratings) if ratings else 0.0,
            "min_rating": min(ratings) if ratings else 0,
            "max_rating": max(ratings) if ratings else 0,
            "with_corrections": len(corrections),
            "correction_rate": len(corrections) / len(feedbacks) * 100 if feedbacks else 0.0
        }


class RetrainingPipeline:
    """Pipeline de retraining basé sur les feedbacks."""
    
    def __init__(self):
        self.feedback_collector = FeedbackCollector()
    
    def should_retrain(self, min_feedbacks: int = 10, min_avg_rating: float = 3.0) -> bool:
        """Détermine si un retraining est nécessaire."""
        stats = self.feedback_collector.get_statistics()
        
        if stats["total_feedbacks"] < min_feedbacks:
            return False
        
        if stats["avg_rating"] < min_avg_rating:
            return True
        
        # Si beaucoup de corrections, retraining recommandé
        if stats["correction_rate"] > 20.0:  # Plus de 20% de corrections
            return True
        
        return False
    
    def prepare_retraining_data(self) -> Dict[str, Any]:
        """Prépare les données pour le retraining."""
        training_data = self.feedback_collector.prepare_training_data()
        
        return {
            "training_examples": len(training_data),
            "data_file": str(self.feedback_collector.training_data_file),
            "ready_for_training": len(training_data) > 0
        }


if __name__ == "__main__":
    # Test du système de feedback
    collector = FeedbackCollector()
    stats = collector.get_statistics()
    print("Statistiques feedback:")
    print(json.dumps(stats, indent=2, ensure_ascii=False))
    
    retraining = RetrainingPipeline()
    should_retrain = retraining.should_retrain()
    print(f"\nRetraining nécessaire: {should_retrain}")
    
    if should_retrain:
        retraining_data = retraining.prepare_retraining_data()
        print("Données de retraining:")
        print(json.dumps(retraining_data, indent=2, ensure_ascii=False))

