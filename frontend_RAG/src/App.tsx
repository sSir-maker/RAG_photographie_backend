import { useState, useEffect } from 'react';
import { ChatMessage } from './components/ChatMessage';
import { ChatInput } from './components/ChatInput';
import { Sidebar } from './components/Sidebar';
import { ThemeSelector } from './components/ThemeSelector';
import { AuthPage } from './components/AuthPage';
import { Menu, X } from 'lucide-react';
import { API_ENDPOINTS } from './config';
import { parseJSONResponse, getErrorMessageForStatus } from './utils/responseParser';

export interface Message {
  id: string;
  role: 'user' | 'assistant';
  content: string;
  image?: string;
  timestamp: Date;
}

export interface Conversation {
  id: number | string;  // number pour DB, string pour temporaire
  title: string;
  messages: Message[];
  createdAt: Date;
}

export type ThemeMode = 'dark' | 'light';
export type ThemeColor = 'purple' | 'yellow' | 'red' | 'blue' | 'green';

export interface Theme {
  mode: ThemeMode;
  color: ThemeColor;
}

export default function App() {
  const [theme, setTheme] = useState<Theme>({ mode: 'dark', color: 'purple' });
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [userName, setUserName] = useState('');
  const [authToken, setAuthToken] = useState<string | null>(
    localStorage.getItem('auth_token')
  );
  const [conversations, setConversations] = useState<Conversation[]>([]);
  const [currentConversationId, setCurrentConversationId] = useState<number | string | null>(null);
  const [, setIsLoadingConversations] = useState(false);
  const [isSidebarOpen, setIsSidebarOpen] = useState(false);

  const currentConversation = conversations.find((c: Conversation) => c.id === currentConversationId);

  const handleLogin = async (email: string, password: string): Promise<void> => {
    try {
      // OPTIMISATION MOBILE: Timeout plus long pour les connexions lentes
      const controller = new AbortController();
      const timeoutId = setTimeout(() => controller.abort(), 30000); // 30 secondes

      // DEBUG: Log de l'URL utilisée
      console.log('🔍 Login - API URL:', API_ENDPOINTS.auth.login);
      console.log('🔍 Login - Request body:', { email, password: '***' });
      
      const response = await fetch(API_ENDPOINTS.auth.login, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ email, password }),
        signal: controller.signal,
      });

      clearTimeout(timeoutId);

      // DEBUG: Log de la réponse
      console.log('📡 Login - Response status:', response.status, response.statusText);
      console.log('📡 Login - Response headers:', Object.fromEntries(response.headers.entries()));
      
      // Vérifier le Content-Type AVANT de parser
      const contentType = response.headers.get('content-type');
      console.log('📡 Login - Content-Type:', contentType);
      
      if (!response.ok) {
        let errorMessage = 'Erreur lors de la connexion';
        try {
          const error = await parseJSONResponse(response);
          console.error('❌ Login - Error response:', error);
          
          // Extraire le message d'erreur
          let detail = error.detail;
          
          // Si c'est un tableau d'erreurs (validation Pydantic)
          if (Array.isArray(detail)) {
            const firstError = detail[0];
            if (firstError?.msg) {
              detail = firstError.msg;
              // Traduire les erreurs de validation Pydantic
              if (firstError.type === 'value_error.email' || 
                  detail.includes('did not match the expected pattern') ||
                  detail.includes('string does not match expected pattern')) {
                detail = 'Format d\'email invalide. Veuillez vérifier que votre adresse email est correcte (exemple: votre@email.com)';
              }
            }
          }
          
          // Traduire les messages d'erreur courants
          if (typeof detail === 'string') {
            if (detail.includes('did not match the expected pattern') || 
                detail.includes('string does not match expected pattern')) {
              detail = 'Format d\'email invalide. Veuillez vérifier que votre adresse email est correcte (exemple: votre@email.com)';
            } else if (detail.includes('field required')) {
              detail = 'Veuillez remplir tous les champs requis';
            }
          }
          
          errorMessage = detail || errorMessage;
        } catch (parseError: any) {
          // Si la réponse est du HTML ou ne peut pas être parsée comme JSON
          console.error('❌ Login - Parse error:', parseError);
          if (parseError.message?.includes('HTML') || parseError.message?.includes('page d\'erreur')) {
            errorMessage = parseError.message;
          } else {
            errorMessage = getErrorMessageForStatus(response.status, response.statusText);
          }
        }
        throw new Error(errorMessage);
      }

      // Vérifier AVANT de parser si la réponse est du HTML (même avec status 200)
      const responseText = await response.clone().text();
      console.log('📡 Login - Response preview (first 200 chars):', responseText.substring(0, 200));
      console.log('📡 Login - Content-Type:', response.headers.get('content-type'));
      
      if (responseText.trim().startsWith('<!DOCTYPE') || responseText.trim().startsWith('<html')) {
        console.error('❌ Login - HTML détecté avec status 200 !');
        throw new Error(
          'Le serveur a retourné une page HTML au lieu de JSON (Status: 200). ' +
          'Le backend est peut-être en erreur ou mal configuré. ' +
          `Vérifiez que l'URL backend est correcte : ${API_ENDPOINTS.auth.login}`
        );
      }
      
      const data = await parseJSONResponse(response);
      setAuthToken(data.access_token);
      localStorage.setItem('auth_token', data.access_token);
      setUserName(data.user.name);
      setIsAuthenticated(true);
    } catch (error: any) {
      // OPTIMISATION MOBILE: Meilleure gestion des erreurs réseau
      if (error.name === 'AbortError') {
        throw new Error('La requête a pris trop de temps. Vérifiez votre connexion internet.');
      } else if (error.message?.includes('fetch')) {
        throw new Error('Impossible de se connecter au serveur. Vérifiez votre connexion internet.');
      } else if (error.message) {
        throw error;
      } else {
        throw new Error('Une erreur inattendue est survenue. Veuillez réessayer.');
      }
    }
  };

  const handleRegister = async (name: string, email: string, password: string): Promise<{ success: boolean; email: string }> => {
    try {
      // DEBUG: Log de l'URL utilisée
      console.log('🔍 Register - API URL:', API_ENDPOINTS.auth.signup);
      
      // OPTIMISATION MOBILE: Timeout plus long pour les connexions lentes
      const controller = new AbortController();
      const timeoutId = setTimeout(() => controller.abort(), 30000); // 30 secondes

      const response = await fetch(API_ENDPOINTS.auth.signup, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ name, email, password }),
        signal: controller.signal,
      });

      clearTimeout(timeoutId);

      console.log('📡 Register - Response status:', response.status, response.statusText);

      if (!response.ok) {
        let errorMessage = 'Erreur lors de l\'inscription';
        try {
          const error = await parseJSONResponse(response);
          console.error('❌ Register - Error response:', error);
          
          // Extraire le message d'erreur
          let detail = error.detail;
          
          // Si c'est un tableau d'erreurs (validation Pydantic)
          if (Array.isArray(detail)) {
            const firstError = detail[0];
            if (firstError?.msg) {
              detail = firstError.msg;
              // Traduire les erreurs de validation Pydantic
              if (firstError.type === 'value_error.email' || 
                  detail.includes('did not match the expected pattern') ||
                  detail.includes('string does not match expected pattern')) {
                detail = 'Format d\'email invalide. Veuillez vérifier que votre adresse email est correcte (exemple: votre@email.com)';
              }
            }
          }
          
          // Traduire les messages d'erreur courants
          if (typeof detail === 'string') {
            if (detail.includes('did not match the expected pattern') || 
                detail.includes('string does not match expected pattern')) {
              detail = 'Format d\'email invalide. Veuillez vérifier que votre adresse email est correcte (exemple: votre@email.com)';
            } else if (detail.includes('field required')) {
              detail = 'Veuillez remplir tous les champs requis';
            }
          }
          
          errorMessage = detail || errorMessage;
        } catch (parseError: any) {
          // Si la réponse est du HTML ou ne peut pas être parsée comme JSON
          console.error('❌ Register - Parse error:', parseError);
          if (parseError.message?.includes('HTML') || parseError.message?.includes('page d\'erreur')) {
            errorMessage = parseError.message;
          } else {
            errorMessage = getErrorMessageForStatus(response.status, response.statusText);
          }
        }
        throw new Error(errorMessage);
      }

      await parseJSONResponse(response);
      console.log('✅ Register - Success');
      
      // Après signup réussi, on ne connecte pas directement
      // On retourne juste un succès pour que AuthPage bascule vers login
      return { success: true, email };
    } catch (error: any) {
      console.error('❌ Register - Exception:', error);
      // OPTIMISATION MOBILE: Meilleure gestion des erreurs réseau
      if (error.name === 'AbortError') {
        throw new Error('La requête a pris trop de temps. Vérifiez votre connexion internet.');
      } else if (error.message?.includes('fetch') || error.message?.includes('Failed to fetch') || error.message?.includes('NetworkError')) {
        throw new Error('Impossible de se connecter au serveur. Vérifiez votre connexion internet et que le backend est accessible.');
      } else if (error.message) {
        throw error;
      } else {
        throw new Error('Une erreur inattendue est survenue. Veuillez réessayer.');
      }
    }
  };

  const toggleThemeMode = () => {
    setTheme((prev: Theme) => ({
      ...prev,
      mode: prev.mode === 'dark' ? 'light' : 'dark',
    }));
  };

  // Fonction pour charger les conversations depuis la DB
  const loadConversations = async () => {
    if (!authToken) return;
    
    setIsLoadingConversations(true);
    try {
      const response = await fetch(API_ENDPOINTS.conversations.list, {
        headers: {
          'Authorization': `Bearer ${authToken}`,
        },
      });
      
      if (response.ok) {
        const convs = await response.json();
        const conversationsWithMessages: Conversation[] = await Promise.all(
          convs.map(async (conv: any) => {
            // Charger les messages pour chaque conversation
            const messagesResponse = await fetch(
              API_ENDPOINTS.conversations.messages(conv.id),
              {
                headers: {
                  'Authorization': `Bearer ${authToken}`,
                },
              }
            );
            
            let messages: Message[] = [];
            if (messagesResponse.ok) {
              const msgs = await messagesResponse.json();
              messages = msgs.map((msg: any) => ({
                id: msg.id.toString(),
                role: msg.role,
                content: msg.content,
                image: msg.image_url,
                timestamp: new Date(msg.created_at),
              }));
            }
            
            return {
              id: conv.id,
              title: conv.title,
              messages,
              createdAt: new Date(conv.created_at),
            };
          })
        );
        
        setConversations(conversationsWithMessages);
        
        // Sélectionner la première conversation ou créer une nouvelle
        if (conversationsWithMessages.length > 0) {
          setCurrentConversationId(conversationsWithMessages[0].id);
        } else {
          // Créer une conversation par défaut
          const newConvResponse = await fetch(API_ENDPOINTS.conversations.create, {
            method: 'POST',
            headers: {
              'Authorization': `Bearer ${authToken}`,
            },
          });
          
          if (newConvResponse.ok) {
            const newConv = await newConvResponse.json();
            const welcomeMessage: Message = {
              id: '1',
              role: 'assistant',
              content: 'Hello! I\'m Dixel Bot, your AI photography assistant. I can help you with:\n\n• Camera settings and techniques\n• Photo composition and lighting advice\n• Equipment recommendations\n• Post-processing tips\n• Image analysis and feedback\n\nFeel free to ask me anything or upload a photo for detailed analysis!',
              timestamp: new Date(),
            };
            
            setConversations([{
              id: newConv.id,
              title: newConv.title,
              messages: [welcomeMessage],
              createdAt: new Date(newConv.created_at),
            }]);
            setCurrentConversationId(newConv.id);
          }
        }
      }
    } catch (error) {
      console.error('Erreur lors du chargement des conversations:', error);
    } finally {
      setIsLoadingConversations(false);
    }
  };

  // Vérifier le token au chargement (DOIT être avant tout return conditionnel)
  useEffect(() => {
    if (authToken) {
      // Vérifier que le token est valide
      fetch(API_ENDPOINTS.auth.me, {
        headers: {
          'Authorization': `Bearer ${authToken}`,
        },
      })
        .then(res => {
          if (res.ok) {
            return res.json();
          } else {
            localStorage.removeItem('auth_token');
            setAuthToken(null);
            setIsAuthenticated(false);
          }
        })
        .then(data => {
          if (data) {
            setUserName(data.name || '');
            setIsAuthenticated(true);
            // Charger les conversations après authentification
            loadConversations();
          }
        })
        .catch(() => {
          localStorage.removeItem('auth_token');
          setAuthToken(null);
          setIsAuthenticated(false);
        });
    }
  }, [authToken]);

  // Show auth page if not authenticated
  if (!isAuthenticated) {
    return (
      <AuthPage
        theme={theme}
        onThemeToggle={toggleThemeMode}
        onLogin={handleLogin}
        onRegister={handleRegister}
      />
    );
  }

  const handleSendMessage = async (content: string, image?: string) => {
    if (!authToken) return;

    // Créer une conversation si nécessaire
    let conversationId = currentConversationId;
    if (!conversationId || typeof conversationId === 'string') {
      try {
        const newConvResponse = await fetch(API_ENDPOINTS.conversations.create, {
          method: 'POST',
          headers: {
            'Authorization': `Bearer ${authToken}`,
          },
        });
        
        if (newConvResponse.ok) {
          const newConv = await newConvResponse.json();
          conversationId = newConv.id;
          setCurrentConversationId(conversationId);
          setConversations([{
            id: newConv.id,
            title: newConv.title,
            messages: [],
            createdAt: new Date(newConv.created_at),
          }]);
        }
      } catch (error) {
        console.error('Erreur lors de la création de la conversation:', error);
        return;
      }
    }

    const userMessage: Message = {
      id: Date.now().toString(),
      role: 'user',
      content,
      image,
      timestamp: new Date(),
    };

    // Ajouter le message utilisateur immédiatement
    setConversations((prev: Conversation[]) => prev.map((conv: Conversation) => {
      if (conv.id === conversationId) {
        return {
          ...conv,
          messages: [...conv.messages, userMessage],
        };
      }
      return conv;
    }));

    // Message de chargement
    const loadingMessage: Message = {
      id: (Date.now() + 1).toString(),
      role: 'assistant',
      content: 'Recherche dans tes documents...',
      timestamp: new Date(),
    };

    setConversations((prev: Conversation[]) => prev.map((conv: Conversation) => {
      if (conv.id === conversationId) {
        return {
          ...conv,
          messages: [...conv.messages, loadingMessage],
        };
      }
      return conv;
    }));

    try {
      // Créer un message assistant pour le streaming
      const streamingMessageId = (Date.now() + 1).toString();
      let streamingContent = '';
      
      // Remplacer le message de chargement par un message vide pour le streaming
      setConversations((prev: Conversation[]) => prev.map((conv: Conversation) => {
        if (conv.id === conversationId) {
          const messagesWithoutLoading = conv.messages.filter((msg: Message) => msg.id !== loadingMessage.id);
          return {
            ...conv,
            messages: [...messagesWithoutLoading, {
              id: streamingMessageId,
              role: 'assistant' as const,
              content: '',
              timestamp: new Date(),
            }],
          };
        }
        return conv;
      }));

      // Appeler l'API backend en streaming
      const response = await fetch(API_ENDPOINTS.ask.stream, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${authToken}`,
        },
        body: JSON.stringify({ 
          conversation_id: conversationId,
          question: content, 
          force_rebuild: false 
        }),
      });

      if (!response.ok) {
        throw new Error('Erreur lors de la requête');
      }

      // Lire le stream
      const reader = response.body?.getReader();
      const decoder = new TextDecoder();

      if (!reader) {
        throw new Error('Impossible de lire le stream');
      }

      while (true) {
        const { done, value } = await reader.read();
        if (done) break;

        const chunk = decoder.decode(value);
        const lines = chunk.split('\n');

        for (const line of lines) {
          if (line.startsWith('data: ')) {
            try {
              const data = JSON.parse(line.slice(6));
              
              if (data.type === 'chunk') {
                // Ajouter le chunk au contenu
                streamingContent += data.content;
                
                // Mettre à jour le message en temps réel
                setConversations((prev: Conversation[]) => prev.map((conv: Conversation) => {
                  if (conv.id === conversationId) {
                    return {
                      ...conv,
                      messages: conv.messages.map((msg: Message) => 
                        msg.id === streamingMessageId
                          ? { ...msg, content: streamingContent }
                          : msg
                      ),
                    };
                  }
                  return conv;
                }));
              } else if (data.type === 'sources') {
                // Les sources sont disponibles mais on ne les affiche pas pour l'instant
                // On pourrait les afficher dans un panneau latéral
              } else if (data.type === 'done') {
                // Le streaming est terminé, recharger depuis la DB pour avoir les IDs corrects
                if (conversationId) {
                  const messagesResponse = await fetch(
                    API_ENDPOINTS.conversations.messages(conversationId),
                    {
                      headers: {
                        'Authorization': `Bearer ${authToken}`,
                      },
                    }
                  );
                
                  if (messagesResponse.ok) {
                    const msgs = await messagesResponse.json();
                  const loadedMessages: Message[] = msgs.map((msg: any) => ({
                    id: msg.id.toString(),
                    role: msg.role,
                    content: msg.content,
                    image: msg.image_url,
                    timestamp: new Date(msg.created_at),
                  }));
                  
                  setConversations((prev: Conversation[]) => prev.map((conv: Conversation) => {
                    if (conv.id === conversationId) {
                      return {
                        ...conv,
                        messages: loadedMessages,
                      };
                    }
                    return conv;
                  }));
                  }
                }
              } else if (data.type === 'error') {
                throw new Error(data.message || 'Erreur lors du streaming');
              }
            } catch (e) {
              console.error('Erreur lors du parsing du chunk:', e);
            }
          }
        }
      }
    } catch (error) {
      // En cas d'erreur, remplacer le message de chargement par un message d'erreur
      const errorMessage: Message = {
        id: (Date.now() + 1).toString(),
        role: 'assistant',
        content: 'Erreur lors de la récupération de la réponse. Assure-toi que l\'API est démarrée (python run_api.py)',
        timestamp: new Date(),
      };

      setConversations((prev: Conversation[]) => prev.map((conv: Conversation) => {
        if (conv.id === conversationId) {
          const messagesWithoutLoading = conv.messages.filter((msg: Message) => msg.id !== loadingMessage.id);
          return {
            ...conv,
            messages: [...messagesWithoutLoading, errorMessage],
          };
        }
        return conv;
      }));
    }
  };

  const handleNewConversation = async () => {
    if (!authToken) return;
    
    try {
      const response = await fetch(API_ENDPOINTS.conversations.create, {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${authToken}`,
        },
      });
      
      if (response.ok) {
        const newConv = await response.json();
        const conversation: Conversation = {
          id: newConv.id,
          title: newConv.title,
          messages: [],
          createdAt: new Date(newConv.created_at),
        };
        setConversations((prev: Conversation[]) => [conversation, ...prev]);
        setCurrentConversationId(conversation.id);
        setIsSidebarOpen(false);
      }
    } catch (error) {
      console.error('Erreur lors de la création de la conversation:', error);
    }
  };

  const handleDeleteConversation = async (id: number | string) => {
    if (!authToken) return;
    
    try {
      const response = await fetch(API_ENDPOINTS.conversations.get(id), {
        method: 'DELETE',
        headers: {
          'Authorization': `Bearer ${authToken}`,
        },
      });
      
      if (response.ok) {
        setConversations((prev: Conversation[]) => {
          const remaining = prev.filter((c: Conversation) => c.id !== id);
          if (currentConversationId === id) {
            if (remaining.length > 0) {
              setCurrentConversationId(remaining[0].id);
            } else {
              setCurrentConversationId(null);
            }
          }
          return remaining;
        });
      }
    } catch (error) {
      console.error('Erreur lors de la suppression de la conversation:', error);
    }
  };

  const handleLogout = () => {
    setIsAuthenticated(false);
    setUserName('');
    setAuthToken(null);
    localStorage.removeItem('auth_token');
    setConversations([
      {
        id: '1',
        title: 'Welcome to Dixel Bot',
        messages: [
          {
            id: '1',
            role: 'assistant',
            content: 'Hello! I\'m Dixel Bot, your AI photography assistant. I can help you with:\n\n• Camera settings and techniques\n• Photo composition and lighting advice\n• Equipment recommendations\n• Post-processing tips\n• Image analysis and feedback\n\nFeel free to ask me anything or upload a photo for detailed analysis!',
            timestamp: new Date(),
          }
        ],
        createdAt: new Date(),
      }
    ]);
    setCurrentConversationId('1');
    setIsSidebarOpen(false);
  };

  const isDark = theme.mode === 'dark';
  const bgClass = isDark ? 'bg-[#0a0a0a]' : 'bg-white';
  const textClass = isDark ? 'text-white' : 'text-gray-900';

  return (
    <div className={`flex h-screen ${bgClass} ${textClass}`}>
      {/* Sidebar */}
      <Sidebar
        conversations={conversations}
        currentConversationId={currentConversationId?.toString() || ''}
        onSelectConversation={async (id: string | number) => {
          setCurrentConversationId(id);
          setIsSidebarOpen(false);
          
          // Charger les messages de la conversation sélectionnée
          if (authToken && typeof id === 'number') {
            try {
              const response = await fetch(
                API_ENDPOINTS.conversations.messages(id),
                {
                  headers: {
                    'Authorization': `Bearer ${authToken}`,
                  },
                }
              );
              
              if (response.ok) {
                const msgs = await response.json();
                const messages: Message[] = msgs.map((msg: any) => ({
                  id: msg.id.toString(),
                  role: msg.role,
                  content: msg.content,
                  image: msg.image_url,
                  timestamp: new Date(msg.created_at),
                }));
                
                setConversations((prev: Conversation[]) => prev.map((conv: Conversation) => {
                  if (conv.id === id) {
                    return {
                      ...conv,
                      messages,
                    };
                  }
                  return conv;
                }));
              }
            } catch (error) {
              console.error('Erreur lors du chargement des messages:', error);
            }
          }
        }}
        onNewConversation={handleNewConversation}
        onDeleteConversation={handleDeleteConversation}
        isOpen={isSidebarOpen}
        onClose={() => setIsSidebarOpen(false)}
        theme={theme}
        userName={userName}
        onLogout={handleLogout}
      />

      {/* Main Chat Area */}
      <div className="flex-1 flex flex-col">
        {/* Header */}
        <header className={`border-b ${isDark ? 'border-white/10' : 'border-gray-200'} px-4 py-4 flex items-center justify-between`}>
          <div className="flex items-center gap-3">
            <button
              onClick={() => setIsSidebarOpen(!isSidebarOpen)}
              className={`lg:hidden p-2 ${isDark ? 'hover:bg-white/5' : 'hover:bg-gray-100'} rounded-lg transition-colors`}
            >
              {isSidebarOpen ? <X className="w-5 h-5" /> : <Menu className="w-5 h-5" />}
            </button>
            <div className={`w-8 h-8 ${getGradientClass(theme.color)} rounded-lg flex items-center justify-center`}>
              <span className="text-sm">📷</span>
            </div>
            <div>
              <h1 className="text-lg">Dixel Bot</h1>
              <p className={`text-xs ${isDark ? 'text-white/50' : 'text-gray-500'}`}>Photography AI Assistant</p>
            </div>
          </div>
          
          <ThemeSelector theme={theme} onThemeChange={setTheme} />
        </header>

        {/* Messages */}
        <div className="flex-1 overflow-y-auto">
          <div className="max-w-3xl mx-auto px-4 py-8">
            {currentConversation?.messages.map((message: Message, index: number) => {
              // Détecter si c'est le dernier message de l'assistant et qu'il est en cours de streaming
              const isLastMessage = index === (currentConversation.messages.length - 1);
              const isStreaming = isLastMessage && 
                                 message.role === 'assistant' && 
                                 message.content.length > 0 &&
                                 message.content !== 'Recherche dans tes documents...';
              const isThinking = isLastMessage && 
                                 message.role === 'assistant' && 
                                 (message.content === 'Recherche dans tes documents...' || 
                                  message.content.startsWith('Recherche dans tes documents'));
              
              return (
                <ChatMessage 
                  key={message.id} 
                  message={message} 
                  theme={theme} 
                  isThinking={isStreaming || isThinking}
                />
              );
            })}
          </div>
        </div>

        {/* Input */}
        <div className={`border-t ${isDark ? 'border-white/10' : 'border-gray-200'}`}>
          <div className="max-w-3xl mx-auto px-4 py-4">
            <ChatInput onSendMessage={handleSendMessage} theme={theme} />
          </div>
        </div>
      </div>
    </div>
  );
}

function getGradientClass(color: ThemeColor): string {
  const gradients = {
    purple: 'bg-gradient-to-br from-purple-500 to-pink-500',
    yellow: 'bg-gradient-to-br from-yellow-400 to-orange-500',
    red: 'bg-gradient-to-br from-red-500 to-pink-600',
    blue: 'bg-gradient-to-br from-blue-500 to-cyan-500',
    green: 'bg-gradient-to-br from-green-500 to-emerald-600',
  };
  return gradients[color];
}

// Fonction generateMockResponse supprimée - on utilise maintenant l'API backend