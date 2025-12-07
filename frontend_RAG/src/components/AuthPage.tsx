import { useState, useEffect } from 'react';
import { Theme } from '../App';
import { Camera, Mail, Lock, User, Sun, Moon } from 'lucide-react';
import { checkBackendHealth, getErrorMessage } from '../utils/apiHealthCheck';
import { API_URL } from '../config';

interface AuthPageProps {
  theme: Theme;
  onThemeToggle: () => void;
  onLogin: (email: string, password: string) => Promise<void>;
  onRegister: (name: string, email: string, password: string) => Promise<{ success: boolean; email: string }>;
}

export function AuthPage({ theme, onThemeToggle, onLogin, onRegister }: AuthPageProps) {
  const [isLogin, setIsLogin] = useState(true);
  const [name, setName] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');

  const isDark = theme.mode === 'dark';

  const getGradientClass = () => {
    const gradients = {
      purple: 'from-purple-500 to-pink-500',
      yellow: 'from-yellow-400 to-orange-500',
      red: 'from-red-500 to-pink-600',
      blue: 'from-blue-500 to-cyan-500',
      green: 'from-green-500 to-emerald-600',
    };
    return gradients[theme.color];
  };

  const [isLoading, setIsLoading] = useState(false);
  const [successMessage, setSuccessMessage] = useState('');
  const [backendHealth, setBackendHealth] = useState<{ checked: boolean; isHealthy: boolean; message: string }>({
    checked: false,
    isHealthy: true,
    message: '',
  });

  // Vérifier la santé du backend au chargement
  useEffect(() => {
    const checkHealth = async () => {
      console.log('🔍 Vérification de la connexion au backend...');
      console.log('🔗 URL backend configurée:', API_URL);
      
      const result = await checkBackendHealth();
      console.log('📊 Résultat du health check:', result);
      
      const errorMessage = !result.isHealthy ? getErrorMessage(result) : '';
      
      setBackendHealth({
        checked: true,
        isHealthy: result.isHealthy,
        message: errorMessage || result.message,
      });

      if (!result.isHealthy) {
        console.error('❌ Backend inaccessible:', result.message);
      }
    };

    checkHealth();
  }, []);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');
    setSuccessMessage('');
    setIsLoading(true);

    try {
      if (isLogin) {
        if (!email || !password) {
          setError('Veuillez remplir tous les champs');
          setIsLoading(false);
          return;
        }
        
        // Validation de l'email côté client
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        if (!emailRegex.test(email)) {
          setError('Format d\'email invalide. Veuillez vérifier votre adresse email (exemple: votre@email.com)');
          setIsLoading(false);
          return;
        }
        
        await onLogin(email, password);
        // Si onLogin réussit, l'utilisateur sera automatiquement authentifié
        // et redirigé vers le bot (géré dans App.tsx)
      } else {
        if (!name || !email || !password) {
          setError('Veuillez remplir tous les champs');
          setIsLoading(false);
          return;
        }
        
        // Validation de l'email côté client
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        if (!emailRegex.test(email)) {
          setError('Format d\'email invalide. Veuillez vérifier votre adresse email (exemple: votre@email.com)');
          setIsLoading(false);
          return;
        }
        
        if (password.length < 6) {
          setError('Le mot de passe doit contenir au moins 6 caractères');
          setIsLoading(false);
          return;
        }
        const result = await onRegister(name, email, password);
        if (result && result.success) {
          // Afficher un message de succès et basculer vers login
          setSuccessMessage('Compte créé avec succès ! Connecte-toi maintenant.');
          setIsLogin(true);
          // Pré-remplir l'email dans le formulaire de login
          setName('');
          setPassword('');
          // Le champ email reste rempli
        }
      }
    } catch (err: any) {
      console.error('❌ AuthPage - Error:', err);
      // Afficher un message d'erreur plus détaillé
      let errorMessage = err.message || 'Une erreur est survenue';
      
      // Traduire les messages d'erreur Pydantic en français
      if (errorMessage.includes('did not match the expected pattern') || 
          errorMessage.includes('string does not match expected pattern')) {
        errorMessage = 'Format d\'email invalide. Veuillez vérifier que votre adresse email est correcte (exemple: votre@email.com)';
      } else if (errorMessage.includes('field required')) {
        errorMessage = 'Veuillez remplir tous les champs requis';
      } else if (errorMessage.includes('validation error')) {
        errorMessage = 'Les données saisies ne sont pas valides. Veuillez vérifier vos informations.';
      }
      
      console.error('❌ AuthPage - Error message:', errorMessage);
      setError(errorMessage);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className={`min-h-screen flex items-center justify-center px-4 auth-container ${
      isDark ? 'bg-[#0a0a0a]' : 'bg-gray-50'
    }`}>
      {/* Theme Toggle */}
      <button
        onClick={onThemeToggle}
        className={`fixed top-6 right-6 p-3 rounded-full transition-colors ${
          isDark ? 'bg-white/10 hover:bg-white/20' : 'bg-white hover:bg-gray-100 shadow-lg'
        }`}
      >
        {isDark ? (
          <Sun className="w-5 h-5 text-white" />
        ) : (
          <Moon className="w-5 h-5 text-gray-900" />
        )}
      </button>

      <div className="w-full max-w-md">
        {/* Logo and Title */}
        <div className="text-center mb-8">
          <div className={`w-16 h-16 mx-auto mb-4 bg-gradient-to-br ${getGradientClass()} rounded-2xl flex items-center justify-center shadow-lg`}>
            <Camera className="w-8 h-8 text-white" />
          </div>
          <h1 className={`text-3xl mb-2 ${isDark ? 'text-white' : 'text-gray-900'}`}>
            Dixel Bot
          </h1>
          <p className={`${isDark ? 'text-white/60' : 'text-gray-600'}`}>
            Your AI Photography Assistant
          </p>
        </div>

        {/* Auth Card */}
        <div className={`rounded-2xl p-8 shadow-2xl ${
          isDark ? 'bg-[#1a1a1a] border border-white/10' : 'bg-white border border-gray-200'
        }`}>
          <div className="mb-6">
            <h2 className={`text-2xl mb-2 ${isDark ? 'text-white' : 'text-gray-900'}`}>
              {isLogin ? 'Bon retour' : 'Créer un compte'}
            </h2>
            <p className={`text-sm ${isDark ? 'text-white/60' : 'text-gray-600'}`}>
              {isLogin 
                ? 'Connecte-toi pour continuer ton parcours photographique'
                : 'Commence ton parcours photographique avec l\'assistance IA'
              }
            </p>
          </div>

          <form onSubmit={handleSubmit} className="space-y-4">
            {!isLogin && (
              <div>
                <label className={`block text-sm mb-2 ${isDark ? 'text-white/80' : 'text-gray-700'}`}>
                  Full Name
                </label>
                <div className={`flex items-center gap-3 px-4 py-3 rounded-xl border transition-colors ${
                  isDark 
                    ? 'bg-white/5 border-white/10 focus-within:border-white/30' 
                    : 'bg-gray-50 border-gray-200 focus-within:border-gray-400'
                }`}>
                  <User className={`w-5 h-5 ${isDark ? 'text-white/40' : 'text-gray-400'}`} />
                  <input
                    type="text"
                    value={name}
                    onChange={(e) => setName(e.target.value)}
                    placeholder="Jean Dupont"
                    autoComplete="name"
                    className={`flex-1 bg-transparent outline-none ${
                      isDark ? 'text-white placeholder-white/40' : 'text-gray-900 placeholder-gray-500'
                    }`}
                    style={{ fontSize: '16px' }}
                  />
                </div>
              </div>
            )}

            <div>
              <label className={`block text-sm mb-2 ${isDark ? 'text-white/80' : 'text-gray-700'}`}>
                Email
              </label>
              <div className={`flex items-center gap-3 px-4 py-3 rounded-xl border transition-colors ${
                isDark 
                  ? 'bg-white/5 border-white/10 focus-within:border-white/30' 
                  : 'bg-gray-50 border-gray-200 focus-within:border-gray-400'
              }`}>
                <Mail className={`w-5 h-5 ${isDark ? 'text-white/40' : 'text-gray-400'}`} />
                <input
                  type="email"
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                  placeholder="vous@exemple.com"
                  autoComplete="email"
                  className={`flex-1 bg-transparent outline-none ${
                    isDark ? 'text-white placeholder-white/40' : 'text-gray-900 placeholder-gray-500'
                  }`}
                  style={{ fontSize: '16px' }}
                />
              </div>
            </div>

            <div>
              <label className={`block text-sm mb-2 ${isDark ? 'text-white/80' : 'text-gray-700'}`}>
                Password
              </label>
              <div className={`flex items-center gap-3 px-4 py-3 rounded-xl border transition-colors ${
                isDark 
                  ? 'bg-white/5 border-white/10 focus-within:border-white/30' 
                  : 'bg-gray-50 border-gray-200 focus-within:border-gray-400'
              }`}>
                <Lock className={`w-5 h-5 ${isDark ? 'text-white/40' : 'text-gray-400'}`} />
                <input
                  type="password"
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  placeholder="••••••••"
                  autoComplete={isLogin ? 'current-password' : 'new-password'}
                  className={`flex-1 bg-transparent outline-none ${
                    isDark ? 'text-white placeholder-white/40' : 'text-gray-900 placeholder-gray-500'
                  }`}
                  style={{ fontSize: '16px' }}
                />
              </div>
            </div>

            {!backendHealth.checked && (
              <div className="px-4 py-3 rounded-xl bg-blue-500/10 border border-blue-500/20">
                <p className="text-sm text-blue-500">
                  🔍 Vérification de la connexion au backend...
                </p>
              </div>
            )}

            {backendHealth.checked && !backendHealth.isHealthy && (
              <div 
                className="px-4 py-3 rounded-xl bg-red-500/10 border border-red-500/20"
                data-load-failed={true}
              >
                <p className="text-sm text-red-500 whitespace-pre-line">
                  ❌ {backendHealth.message}
                </p>
                <p className="text-xs text-red-400 mt-2">
                  🔗 Backend: {API_URL}
                </p>
              </div>
            )}

            {error && backendHealth.isHealthy && (
              <div 
                className="px-4 py-3 rounded-xl bg-red-500/10 border border-red-500/20"
                data-load-failed={error.includes('Load failed') || error.includes('Failed to fetch') || error.includes('NetworkError')}
              >
                <p className="text-sm text-red-500">
                  {error.includes('Load failed') || error.includes('Failed to fetch') || error.includes('NetworkError')
                    ? '❌ Erreur de connexion. Vérifiez votre connexion internet et réessayez.'
                    : error}
                </p>
              </div>
            )}

            {successMessage && (
              <div className="px-4 py-3 rounded-xl bg-green-500/10 border border-green-500/20">
                <p className="text-sm text-green-500">{successMessage}</p>
              </div>
            )}

            <button
              type="submit"
              disabled={isLoading}
              className={`w-full py-3 rounded-xl bg-gradient-to-r ${getGradientClass()} text-white transition-transform hover:scale-[1.02] active:scale-[0.98] disabled:opacity-50 disabled:cursor-not-allowed`}
            >
              {isLoading ? (
                <span className="flex items-center justify-center gap-2">
                  <span className="animate-spin rounded-full h-4 w-4 border-b-2 border-white"></span>
                  {isLogin ? 'Connexion...' : 'Inscription...'}
                </span>
              ) : (
                isLogin ? 'Se connecter' : 'Créer un compte'
              )}
            </button>
          </form>

          <div className="mt-6 text-center">
            <p className={`text-sm ${isDark ? 'text-white/60' : 'text-gray-600'}`}>
              {isLogin ? "Vous n'avez pas de compte ? " : "Vous avez déjà un compte ? "}
              <button
                onClick={() => {
                  setIsLogin(!isLogin);
                  setError('');
                  setSuccessMessage('');
                  setName('');
                  setEmail('');
                  setPassword('');
                }}
                className={`bg-gradient-to-r ${getGradientClass()} bg-clip-text text-transparent hover:underline`}
              >
                {isLogin ? "S'inscrire" : 'Se connecter'}
              </button>
            </p>
          </div>
        </div>
      </div>
    </div>
  );
}
