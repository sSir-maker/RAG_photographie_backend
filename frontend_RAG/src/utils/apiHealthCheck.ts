/**
 * Vérification de santé de l'API backend
 */

import { API_ENDPOINTS } from '../config';
import { parseJSONResponse, getErrorMessageForStatus } from './responseParser';

export interface HealthCheckResult {
  isHealthy: boolean;
  message: string;
  url?: string;
}

/**
 * Teste la connexion au backend
 */
export async function checkBackendHealth(): Promise<HealthCheckResult> {
  try {
    const controller = new AbortController();
    const timeoutId = setTimeout(() => controller.abort(), 5000); // 5 secondes max

    const response = await fetch(API_ENDPOINTS.health.basic, {
      method: 'GET',
      signal: controller.signal,
      headers: {
        'Content-Type': 'application/json',
      },
    });

    clearTimeout(timeoutId);

    if (response.ok) {
      try {
        const data = await parseJSONResponse(response);
        return {
          isHealthy: true,
          message: 'Backend accessible',
          url: API_ENDPOINTS.health.basic,
        };
      } catch (parseError: any) {
        return {
          isHealthy: false,
          message: parseError.message || 'Le backend a retourné une réponse invalide',
          url: API_ENDPOINTS.health.basic,
        };
      }
    } else {
      const errorMessage = getErrorMessageForStatus(response.status, response.statusText);
      return {
        isHealthy: false,
        message: errorMessage,
        url: API_ENDPOINTS.health.basic,
      };
    }
  } catch (error: any) {
    let errorMessage = 'Erreur de connexion au backend';
    
    if (error.name === 'AbortError') {
      errorMessage = 'Le backend ne répond pas (timeout après 5 secondes)';
    } else if (error.message?.includes('Failed to fetch')) {
      errorMessage = 'Impossible de se connecter au backend. Vérifiez que le serveur est démarré.';
    } else if (error.message?.includes('NetworkError')) {
      errorMessage = 'Erreur réseau. Vérifiez votre connexion internet.';
    } else if (error.message) {
      errorMessage = error.message;
    }

    return {
      isHealthy: false,
      message: errorMessage,
      url: API_ENDPOINTS.health.basic,
    };
  }
}

/**
 * Affiche un message d'erreur détaillé pour l'utilisateur
 */
export function getErrorMessage(result: HealthCheckResult): string {
  if (result.isHealthy) {
    return '';
  }

  const baseMessage = result.message;
  const suggestions: string[] = [];

  // Suggestions selon le type d'erreur
  if (baseMessage.includes('timeout')) {
    suggestions.push('Le backend est peut-être en train de démarrer (sur Render, cela peut prendre 30-60 secondes)');
    suggestions.push('Attendez quelques secondes et réessayez');
  } else if (baseMessage.includes('Failed to fetch') || baseMessage.includes('NetworkError')) {
    suggestions.push('Vérifiez que le backend est déployé et accessible');
    suggestions.push(`Vérifiez l'URL du backend dans la console (F12)`);
  }

  if (suggestions.length > 0) {
    return `${baseMessage}\n\n💡 Suggestions:\n${suggestions.map(s => `• ${s}`).join('\n')}`;
  }

  return baseMessage;
}

