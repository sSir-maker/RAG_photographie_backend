/**
 * Utilitaires pour parser les réponses du backend
 */

/**
 * Vérifie si la réponse est du HTML au lieu de JSON
 */
export async function checkResponseType(response: Response): Promise<boolean> {
  const contentType = response.headers.get('content-type');
  return contentType?.includes('text/html') || false;
}

/**
 * Parse une réponse JSON avec gestion des erreurs pour HTML
 */
export async function parseJSONResponse(response: Response): Promise<any> {
  const text = await response.text();
  
  // Vérifier si c'est du HTML (erreur du serveur)
  if (text.trim().startsWith('<!DOCTYPE') || text.trim().startsWith('<html')) {
    throw new Error(
      'Le serveur a retourné une page d\'erreur HTML au lieu d\'une réponse JSON. ' +
      'Le backend est peut-être en erreur ou l\'endpoint n\'existe pas. ' +
      `Status: ${response.status} ${response.statusText}`
    );
  }
  
  // Essayer de parser le JSON
  try {
    return JSON.parse(text);
  } catch (error: any) {
    throw new Error(
      `Impossible de parser la réponse du serveur comme JSON. ` +
      `Le serveur a peut-être retourné une erreur. ` +
      `Status: ${response.status} ${response.statusText}`
    );
  }
}

/**
 * Obtient un message d'erreur approprié selon le statut HTTP
 */
export function getErrorMessageForStatus(status: number, statusText: string): string {
  switch (status) {
    case 404:
      return 'Endpoint introuvable. Vérifiez que le backend est correctement déployé et que l\'URL est correcte.';
    case 500:
      return 'Erreur interne du serveur. Le backend a rencontré une erreur. Vérifiez les logs du backend.';
    case 503:
      return 'Service indisponible. Le backend est peut-être en train de démarrer ou est surchargé.';
    case 502:
      return 'Bad Gateway. Le serveur proxy a reçu une réponse invalide du backend.';
    case 504:
      return 'Gateway Timeout. Le backend a pris trop de temps à répondre.';
    default:
      return `Erreur ${status}: ${statusText}. Vérifiez que le backend est accessible et fonctionne correctement.`;
  }
}

