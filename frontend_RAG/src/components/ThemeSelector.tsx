import { Theme, ThemeMode, ThemeColor } from '../App';
import { Sun, Moon, Palette } from 'lucide-react';
import { useState } from 'react';

interface ThemeSelectorProps {
  theme: Theme;
  onThemeChange: (theme: Theme) => void;
}

export function ThemeSelector({ theme, onThemeChange }: ThemeSelectorProps) {
  const [showColorPicker, setShowColorPicker] = useState(false);
  const isDark = theme.mode === 'dark';

  const colors: { name: ThemeColor; label: string; class: string }[] = [
    { name: 'purple', label: 'Purple', class: 'bg-gradient-to-br from-purple-500 to-pink-500' },
    { name: 'yellow', label: 'Yellow', class: 'bg-gradient-to-br from-yellow-400 to-orange-500' },
    { name: 'red', label: 'Red', class: 'bg-gradient-to-br from-red-500 to-pink-600' },
    { name: 'blue', label: 'Blue', class: 'bg-gradient-to-br from-blue-500 to-cyan-500' },
    { name: 'green', label: 'Green', class: 'bg-gradient-to-br from-green-500 to-emerald-600' },
  ];

  const toggleMode = () => {
    onThemeChange({
      ...theme,
      mode: theme.mode === 'dark' ? 'light' : 'dark',
    });
  };

  const selectColor = (color: ThemeColor) => {
    onThemeChange({
      ...theme,
      color,
    });
    setShowColorPicker(false);
  };

  return (
    <div className="flex items-center gap-2">
      {/* Mode Toggle */}
      <button
        onClick={toggleMode}
        className={`p-2 rounded-lg transition-colors ${
          isDark ? 'hover:bg-white/5' : 'hover:bg-gray-100'
        }`}
        title={`Switch to ${isDark ? 'light' : 'dark'} mode`}
      >
        {isDark ? <Sun className="w-5 h-5" /> : <Moon className="w-5 h-5" />}
      </button>

      {/* Color Picker */}
      <div className="relative">
        <button
          onClick={() => setShowColorPicker(!showColorPicker)}
          className={`p-2 rounded-lg transition-colors ${
            isDark ? 'hover:bg-white/5' : 'hover:bg-gray-100'
          }`}
          title="Change accent color"
        >
          <Palette className="w-5 h-5" />
        </button>

        {showColorPicker && (
          <>
            {/* Backdrop */}
            <div
              className="fixed inset-0 z-40"
              onClick={() => setShowColorPicker(false)}
            />

            {/* Color picker dropdown */}
            <div
              className={`absolute right-0 mt-2 p-3 rounded-xl shadow-2xl z-50 ${
                isDark ? 'bg-[#1a1a1a] border border-white/10' : 'bg-white border border-gray-200'
              }`}
            >
              <p className={`text-xs mb-3 ${isDark ? 'text-white/60' : 'text-gray-600'}`}>
                Accent Color
              </p>
              <div className="flex gap-2">
                {colors.map((color) => (
                  <button
                    key={color.name}
                    onClick={() => selectColor(color.name)}
                    className={`w-10 h-10 rounded-lg ${color.class} transition-transform hover:scale-110 ${
                      theme.color === color.name ? 'ring-2 ring-offset-2 ' + (isDark ? 'ring-white ring-offset-[#1a1a1a]' : 'ring-gray-900 ring-offset-white') : ''
                    }`}
                    title={color.label}
                  />
                ))}
              </div>
            </div>
          </>
        )}
      </div>
    </div>
  );
}
