import { useState, useRef } from 'react';
import { Send, ImagePlus, X } from 'lucide-react';
import { Theme } from '../App';

interface ChatInputProps {
  onSendMessage: (content: string, image?: string) => void;
  theme: Theme;
}

export function ChatInput({ onSendMessage, theme }: ChatInputProps) {
  const [message, setMessage] = useState('');
  const [selectedImage, setSelectedImage] = useState<string | null>(null);
  const fileInputRef = useRef<HTMLInputElement>(null);
  const isDark = theme.mode === 'dark';

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (message.trim() || selectedImage) {
      onSendMessage(message.trim() || 'Please analyze this image', selectedImage || undefined);
      setMessage('');
      setSelectedImage(null);
    }
  };

  const handleImageSelect = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (file) {
      const reader = new FileReader();
      reader.onloadend = () => {
        setSelectedImage(reader.result as string);
      };
      reader.readAsDataURL(file);
    }
  };

  return (
    <form onSubmit={handleSubmit} className="relative">
      {selectedImage && (
        <div className="mb-3 relative inline-block">
          <img
            src={selectedImage}
            alt="Selected"
            className="h-24 rounded-lg object-cover"
          />
          <button
            type="button"
            onClick={() => setSelectedImage(null)}
            className="absolute -top-2 -right-2 w-6 h-6 bg-red-500 rounded-full flex items-center justify-center hover:bg-red-600 transition-colors"
          >
            <X className="w-4 h-4" />
          </button>
        </div>
      )}
      
      <div className={`relative flex items-end gap-2 rounded-2xl border transition-colors ${
        isDark 
          ? 'bg-white/5 border-white/10 focus-within:border-white/20' 
          : 'bg-gray-50 border-gray-200 focus-within:border-gray-300'
      }`}>
        <button
          type="button"
          onClick={() => fileInputRef.current?.click()}
          className={`p-3 rounded-xl transition-colors flex-shrink-0 ${
            isDark ? 'hover:bg-white/5' : 'hover:bg-gray-100'
          }`}
          title="Upload image"
        >
          <ImagePlus className={`w-5 h-5 ${isDark ? 'text-white/60' : 'text-gray-600'}`} />
        </button>
        
        <input
          type="file"
          ref={fileInputRef}
          onChange={handleImageSelect}
          accept="image/*"
          className="hidden"
        />
        
        <textarea
          value={message}
          onChange={(e) => setMessage(e.target.value)}
          onKeyDown={(e) => {
            if (e.key === 'Enter' && !e.shiftKey) {
              e.preventDefault();
              handleSubmit(e);
            }
          }}
          placeholder="Ask about photography techniques, camera settings, or upload an image..."
          rows={1}
          className={`flex-1 bg-transparent px-2 py-3 outline-none resize-none max-h-32 overflow-y-auto ${
            isDark ? 'text-white placeholder-white/40' : 'text-gray-900 placeholder-gray-500'
          }`}
          style={{ minHeight: '24px' }}
        />
        
        <button
          type="submit"
          disabled={!message.trim() && !selectedImage}
          className={`p-3 rounded-xl transition-colors disabled:opacity-40 disabled:cursor-not-allowed flex-shrink-0 ${
            isDark ? 'hover:bg-white/5' : 'hover:bg-gray-100'
          }`}
          title="Send message"
        >
          <Send className={`w-5 h-5 ${isDark ? 'text-white/60' : 'text-gray-600'}`} />
        </button>
      </div>
      
      <p className={`text-xs mt-2 text-center ${isDark ? 'text-white/30' : 'text-gray-400'}`}>
        Dixel Bot can make mistakes. Consider checking important photography information.
      </p>
    </form>
  );
}