import { Conversation } from '../App';
import { Theme } from '../App';
import { Plus, MessageSquare, Trash2, LogOut } from 'lucide-react';

interface SidebarProps {
  conversations: Conversation[];
  currentConversationId: string;
  onSelectConversation: (id: string) => void;
  onNewConversation: () => void;
  onDeleteConversation: (id: string) => void;
  isOpen: boolean;
  onClose: () => void;
  theme: Theme;
  userName: string;
  onLogout: () => void;
}

export function Sidebar({
  conversations,
  currentConversationId,
  onSelectConversation,
  onNewConversation,
  onDeleteConversation,
  isOpen,
  onClose,
  theme,
  userName,
  onLogout,
}: SidebarProps) {
  const isDark = theme.mode === 'dark';

  return (
    <>
      {/* Overlay for mobile */}
      {isOpen && (
        <div
          className="fixed inset-0 bg-black/50 lg:hidden z-40"
          onClick={onClose}
        />
      )}

      {/* Sidebar */}
      <aside
        className={`
          fixed lg:static inset-y-0 left-0 z-50
          w-72 border-r
          ${isDark ? 'bg-[#0f0f0f] border-white/10' : 'bg-gray-50 border-gray-200'}
          transform transition-transform duration-200 ease-in-out
          ${isOpen ? 'translate-x-0' : '-translate-x-full lg:translate-x-0'}
          flex flex-col
        `}
      >
        {/* Header */}
        <div className={`p-4 border-b ${isDark ? 'border-white/10' : 'border-gray-200'}`}>
          <button
            onClick={onNewConversation}
            className={`w-full flex items-center justify-center gap-2 px-4 py-3 rounded-xl transition-colors ${
              isDark ? 'bg-white/5 hover:bg-white/10' : 'bg-white hover:bg-gray-100 border border-gray-200'
            }`}
          >
            <Plus className="w-5 h-5" />
            <span>New Chat</span>
          </button>
        </div>

        {/* Conversations List */}
        <div className="flex-1 overflow-y-auto p-3">
          <div className="space-y-1">
            {conversations.map((conv) => (
              <div
                key={conv.id}
                className={`
                  group relative flex items-center gap-3 px-3 py-3 rounded-lg cursor-pointer transition-colors
                  ${currentConversationId === conv.id 
                    ? isDark ? 'bg-white/10' : 'bg-white border border-gray-200'
                    : isDark ? 'hover:bg-white/5' : 'hover:bg-white'
                  }
                `}
                onClick={() => onSelectConversation(conv.id)}
              >
                <MessageSquare className={`w-4 h-4 flex-shrink-0 ${isDark ? 'text-white/50' : 'text-gray-500'}`} />
                <div className="flex-1 min-w-0">
                  <p className={`text-sm truncate ${isDark ? 'text-white/90' : 'text-gray-900'}`}>
                    {conv.title}
                  </p>
                  <p className={`text-xs ${isDark ? 'text-white/40' : 'text-gray-500'}`}>
                    {conv.messages.length} message{conv.messages.length !== 1 ? 's' : ''}
                  </p>
                </div>
                <button
                  onClick={(e) => {
                    e.stopPropagation();
                    onDeleteConversation(conv.id);
                  }}
                  className={`opacity-0 group-hover:opacity-100 p-1.5 rounded transition-all ${
                    isDark ? 'hover:bg-white/10' : 'hover:bg-gray-100'
                  }`}
                  title="Delete conversation"
                >
                  <Trash2 className="w-4 h-4 text-red-400" />
                </button>
              </div>
            ))}
          </div>
        </div>

        {/* Footer */}
        <div className={`p-4 border-t ${isDark ? 'border-white/10' : 'border-gray-200'}`}>
          {/* User Info */}
          <div className={`flex items-center gap-3 p-3 rounded-lg mb-3 ${
            isDark ? 'bg-white/5' : 'bg-white border border-gray-200'
          }`}>
            <div className={`w-10 h-10 rounded-full flex items-center justify-center ${
              isDark ? 'bg-white/10' : 'bg-gray-200'
            }`}>
              <span className="text-lg">👤</span>
            </div>
            <div className="flex-1 min-w-0">
              <p className={`text-sm truncate ${isDark ? 'text-white/90' : 'text-gray-900'}`}>
                {userName}
              </p>
              <p className={`text-xs ${isDark ? 'text-white/40' : 'text-gray-500'}`}>
                Premium User
              </p>
            </div>
            <button
              onClick={onLogout}
              className={`p-2 rounded-lg transition-colors ${
                isDark ? 'hover:bg-white/10' : 'hover:bg-gray-100'
              }`}
              title="Logout"
            >
              <LogOut className={`w-4 h-4 ${isDark ? 'text-white/60' : 'text-gray-600'}`} />
            </button>
          </div>

          <div className={`text-xs space-y-1 ${isDark ? 'text-white/40' : 'text-gray-500'}`}>
            <p>Dixel Bot v1.0</p>
            <p>Your AI Photography Assistant</p>
          </div>
        </div>
      </aside>
    </>
  );
}