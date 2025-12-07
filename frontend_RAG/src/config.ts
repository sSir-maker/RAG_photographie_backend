/**
 * Configuration de l'application frontend
 */

// Détection automatique de l'environnement
const isProduction = window.location.hostname !== 'localhost' && 
                     window.location.hostname !== '127.0.0.1' &&
                     !window.location.hostname.startsWith('192.168.') &&
                     !window.location.hostname.startsWith('10.0.');

// URL de l'API backend depuis les variables d'environnement
const envApiUrl = import.meta.env.VITE_API_URL;

// Détection automatique de l'URL du backend en production
function detectBackendUrl(): string {
  // 1. Utiliser la variable d'environnement si définie
  if (envApiUrl) {
    // S'assurer que l'URL commence par http:// ou https://
    if (envApiUrl.startsWith('http://') || envApiUrl.startsWith('https://')) {
      return envApiUrl;
    }
    // Si l'URL ne commence pas par http:// ou https://, l'ajouter
    return `https://${envApiUrl}`;
  }
  
  // 2. En production, toujours utiliser l'URL absolue du backend Render
  if (isProduction) {
    return 'https://rag-photographie-backend.onrender.com';
  }
  
  // 3. En développement, utiliser localhost
  return 'http://localhost:8001';
}

export const API_URL = detectBackendUrl();

// Logs de debug
console.log('🔧 API Configuration:', {
  isProduction,
  envApiUrl,
  hostname: window.location.hostname,
  finalUrl: API_URL,
});

// Configuration de l'API
export const API_CONFIG = {
  baseURL: API_URL,
  timeout: 30000, // 30 secondes
  headers: {
    'Content-Type': 'application/json',
  },
};

// Endpoints de l'API
export const API_ENDPOINTS = {
  auth: {
    login: `${API_URL}/auth/login`,
    signup: `${API_URL}/auth/signup`,
    me: `${API_URL}/auth/me`,
  },
  conversations: {
    list: `${API_URL}/conversations`,
    create: `${API_URL}/conversations`,
    get: (id: number | string) => `${API_URL}/conversations/${id}`,
    messages: (id: number | string) => `${API_URL}/conversations/${id}/messages`,
    delete: (id: number | string) => `${API_URL}/conversations/${id}`,
    export: (id: number | string, format: string = 'json') => 
      `${API_URL}/conversations/${id}/export?format=${format}`,
    share: (id: number | string) => `${API_URL}/conversations/${id}/share`,
    statistics: (id: number | string) => `${API_URL}/conversations/${id}/statistics`,
  },
  ask: {
    stream: `${API_URL}/ask/stream`,
    normal: `${API_URL}/ask`,
  },
  search: {
    messages: `${API_URL}/search/messages`,
    conversations: `${API_URL}/search/conversations`,
  },
  health: {
    basic: `${API_URL}/health`,
    detailed: `${API_URL}/health/detailed`,
  },
  metrics: `${API_URL}/metrics`,
  alerts: `${API_URL}/alerts`,
  llms: {
    list: `${API_URL}/llms`,
    get: (name: string) => `${API_URL}/llms/${name}`,
  },
};

