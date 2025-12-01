import { useState, useEffect, useRef } from 'react';

// Configuration du simulateur d'écriture
const writingSimulator = {
  enabled: true,
  speed: 'natural', // ~25-50ms par caractère
  pauses: {
    thinking: 500,    // Pause avant de commencer
    sentences: 200,   // Pause entre les phrases  
    paragraphs: 400   // Pause entre les paragraphes
  },
  effects: {
    typos: false,     // Fautes de frappe simulées
    corrections: true, // Auto-corrections
    hesitation: true   // Ralentissements naturels
  }
};

// Fonction pour calculer la vitesse naturelle avec hésitations
const getNaturalSpeed = (char: string, baseSpeed: number): number => {
  if (!writingSimulator.effects.hesitation) {
    return baseSpeed;
  }

  // Ralentir légèrement après les virgules
  if (char === ',') {
    return baseSpeed + 50;
  }

  // Ralentir après les deux-points
  if (char === ':') {
    return baseSpeed + 100;
  }

  // Hésitation aléatoire (10% de chance de ralentir)
  if (Math.random() < 0.1) {
    return baseSpeed + Math.random() * 100;
  }

  // Variation naturelle de vitesse
  return baseSpeed + (Math.random() * 20 - 10); // ±10ms
};

// Fonction pour détecter les phrases
const isEndOfSentence = (char: string): boolean => {
  return char === '.' || char === '!' || char === '?';
};

// Fonction pour détecter les paragraphes
const isEndOfParagraph = (char: string, nextChar: string | undefined): boolean => {
  return char === '\n' && (nextChar === '\n' || nextChar === undefined);
};

interface ThinkingIndicatorProps {
  text: string;
  speed?: number;
  onComplete?: () => void;
  streaming?: boolean; // Mode streaming : affiche le texte directement sans animation
}

export function ThinkingIndicator({ text, speed = 30, onComplete, streaming = false }: ThinkingIndicatorProps) {
  const [displayedText, setDisplayedText] = useState('');
  const [showCursor, setShowCursor] = useState(true);
  const currentIndexRef = useRef(0);
  const hasStartedRef = useRef(false);
  const timeoutRef = useRef<NodeJS.Timeout | null>(null);
  
  // Vérifier si le texte est complet pour cacher le curseur
  const isComplete = streaming ? displayedText === text && text.length > 0 : currentIndexRef.current >= text.length;

  // Mode streaming : afficher le texte directement
  useEffect(() => {
    if (streaming) {
      setDisplayedText(text);
      // Cacher le curseur quand le texte est complet en mode streaming
      if (text.length > 0 && displayedText === text) {
        setShowCursor(false);
        if (onComplete) {
          const timer = setTimeout(() => {
            onComplete();
          }, 100);
          return () => clearTimeout(timer);
        }
      } else if (text.length === 0) {
        setShowCursor(true);
      }
      return;
    }
  }, [text, streaming, onComplete, displayedText]);

  useEffect(() => {
    // Mode streaming : ne pas utiliser l'animation
    if (streaming) {
      return;
    }

    // Nettoyer les timeouts précédents
    if (timeoutRef.current) {
      clearTimeout(timeoutRef.current);
    }

    // Si le texte est complet
    if (currentIndexRef.current >= text.length) {
      // Cacher le curseur quand le texte est complet
      setShowCursor(false);
      if (onComplete) {
        onComplete();
      }
      return;
    }

    // Pause de réflexion avant de commencer (seulement la première fois)
    if (!hasStartedRef.current && writingSimulator.enabled) {
      hasStartedRef.current = true;
      timeoutRef.current = setTimeout(() => {
        // Après la pause, commencer l'écriture
        if (currentIndexRef.current < text.length) {
          const char = text[currentIndexRef.current];
          const nextChar = text[currentIndexRef.current + 1];
          let delay = getNaturalSpeed(char, speed);
          
          // Pause supplémentaire après les phrases
          if (isEndOfSentence(char)) {
            delay += writingSimulator.pauses.sentences;
          }
          
          // Pause supplémentaire après les paragraphes
          if (isEndOfParagraph(char, nextChar)) {
            delay += writingSimulator.pauses.paragraphs;
          }

          timeoutRef.current = setTimeout(() => {
            setDisplayedText(prev => prev + char);
            currentIndexRef.current++;
          }, delay);
        }
      }, writingSimulator.pauses.thinking);
      
      return () => {
        if (timeoutRef.current) clearTimeout(timeoutRef.current);
      };
    }

    // Continuer l'écriture
    if (hasStartedRef.current && currentIndexRef.current < text.length) {
      const char = text[currentIndexRef.current];
      const nextChar = text[currentIndexRef.current + 1];
      
      // Calculer le délai avec pauses naturelles
      let delay = getNaturalSpeed(char, speed);
      
      // Pause supplémentaire après les phrases
      if (isEndOfSentence(char)) {
        delay += writingSimulator.pauses.sentences;
      }
      
      // Pause supplémentaire après les paragraphes
      if (isEndOfParagraph(char, nextChar)) {
        delay += writingSimulator.pauses.paragraphs;
      }

      timeoutRef.current = setTimeout(() => {
        setDisplayedText(prev => prev + char);
        currentIndexRef.current++;
      }, delay);
      
      return () => {
        if (timeoutRef.current) clearTimeout(timeoutRef.current);
      };
    }
  }, [displayedText, text, speed, onComplete]);

  // Clignotement du curseur
  useEffect(() => {
    const cursorInterval = setInterval(() => {
      setShowCursor(prev => !prev);
    }, 500);
    
    return () => clearInterval(cursorInterval);
  }, []);

  // Réinitialiser quand le texte change (seulement en mode non-streaming)
  useEffect(() => {
    if (!streaming) {
      setDisplayedText('');
      currentIndexRef.current = 0;
      hasStartedRef.current = false;
      setShowCursor(true); // Réafficher le curseur au début
      if (timeoutRef.current) {
        clearTimeout(timeoutRef.current);
        timeoutRef.current = null;
      }
    } else {
      // En mode streaming, réafficher le curseur si le texte change (nouveau message)
      if (text.length === 0) {
        setShowCursor(true);
      }
    }
  }, [text, streaming]);
  
  // Vérifier si le texte est complet pour cacher le curseur (mode streaming)
  useEffect(() => {
    if (streaming && text.length > 0 && displayedText === text) {
      // Petit délai avant de cacher le curseur pour un effet plus naturel
      const timer = setTimeout(() => {
        setShowCursor(false);
      }, 300);
      return () => clearTimeout(timer);
    }
  }, [streaming, text, displayedText]);

  // Ne pas afficher le curseur si le texte est complet
  const shouldShowCursor = showCursor && !isComplete;
  
  return (
    <span className="thinking-text">
      {displayedText}
      {shouldShowCursor && <span className="cursor animate-pulse">|</span>}
    </span>
  );
}

