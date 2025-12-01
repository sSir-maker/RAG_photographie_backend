import { Message } from '../App';
import { Theme } from '../App';
import { ImageWithFallback } from './figma/ImageWithFallback';
import { ThinkingIndicator } from './ThinkingIndicator';

interface ChatMessageProps {
  message: Message;
  theme: Theme;
  isThinking?: boolean;
}

export function ChatMessage({ message, theme, isThinking = false }: ChatMessageProps) {
  const isUser = message.role === 'user';
  const isDark = theme.mode === 'dark';

  const getGradientClass = () => {
    const gradients = {
      purple: 'bg-gradient-to-br from-purple-500 to-pink-500',
      yellow: 'bg-gradient-to-br from-yellow-400 to-orange-500',
      red: 'bg-gradient-to-br from-red-500 to-pink-600',
      blue: 'bg-gradient-to-br from-blue-500 to-cyan-500',
      green: 'bg-gradient-to-br from-green-500 to-emerald-600',
    };
    return gradients[theme.color];
  };

  return (
    <div className={`flex gap-4 mb-8 ${isUser ? 'justify-end' : 'justify-start'}`}>
      {!isUser && (
        <div className={`w-8 h-8 rounded-full ${getGradientClass()} flex items-center justify-center flex-shrink-0`}>
          <span className="text-sm">📷</span>
        </div>
      )}
      
      <div className={`flex flex-col gap-2 max-w-[85%] ${isUser ? 'items-end' : 'items-start'}`}>
        <div className={`rounded-2xl px-4 py-3 ${
          isUser 
            ? isDark ? 'bg-white/10 backdrop-blur-sm' : 'bg-gray-100'
            : 'bg-transparent'
        }`}>
          {message.image && (
            <div className="mb-3 rounded-lg overflow-hidden">
              <ImageWithFallback
                src={message.image}
                alt="Uploaded image"
                className="max-w-full h-auto max-h-96 object-cover"
              />
            </div>
          )}
          <div className={`whitespace-pre-wrap ${isDark ? 'text-white/90' : 'text-gray-900'}`}>
            {isThinking && !isUser ? (
              <ThinkingIndicator 
                text={message.content}
                speed={25}
                streaming={message.content.length > 0 && message.content !== 'Recherche dans tes documents...'}
              />
            ) : (
              message.content
            )}
          </div>
          <style>{`
            .thinking-text {
              display: inline;
            }
            .cursor {
              display: inline-block;
              margin-left: 2px;
              animation: blink 1s infinite;
            }
            @keyframes blink {
              0%, 50% { opacity: 1; }
              51%, 100% { opacity: 0; }
            }
          `}</style>
        </div>
        <span className={`text-xs ${isDark ? 'text-white/40' : 'text-gray-500'} px-2`}>
          {message.timestamp.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
        </span>
      </div>

      {isUser && (
        <div className={`w-8 h-8 rounded-full ${isDark ? 'bg-white/10' : 'bg-gray-200'} flex items-center justify-center flex-shrink-0`}>
          <span className="text-sm">👤</span>
        </div>
      )}
    </div>
  );
}