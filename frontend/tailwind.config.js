/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  darkMode: 'class',
  theme: {
    extend: {
      colors: {
        'primary-sovereign': '#0F2B5B',
        'primary': '#1E3A8A',
        'surface-base': '#F5F7FA',
        'surface-elevated': '#FFFFFF',
        'surface-subtle': '#F8FAFC',
        'border-rest': '#E2E8F0',
        'border-focus': '#CBD5E1',
        'text-primary': '#0F172A',
        'text-secondary': '#334155',
        'text-tertiary': '#334155',
        'status-critical': '#DC2626',
        'status-warning': '#B45309',
        'status-healthy': '#059669',
        // Semantic aliases for compatibility
        background: '#F5F7FA',
        surface: {
          DEFAULT: '#FFFFFF',
          card: '#FFFFFF',
          subtle: '#F8FAFC',
          base: '#F5F7FA'
        },
        slateText: {
          primary: '#0F172A',
          secondary: '#334155',
          muted: '#334155',
          dim: '#334155'
        }
      },
      fontSize: {
        'h1': ['20px', { lineHeight: '28px', fontWeight: '800' }],
        'h2': ['16px', { lineHeight: '24px', fontWeight: '700' }],
        'h3': ['14px', { lineHeight: '20px', fontWeight: '600' }],
        'body': ['13px', { lineHeight: '18px', fontWeight: '400' }],
        'label': ['12px', { lineHeight: '16px', fontWeight: '500' }],
        'caption': ['11px', { lineHeight: '14px', fontWeight: '400' }],
      },
      fontFamily: {
        sans: ['Inter', 'system-ui', '-apple-system', 'sans-serif'],
        mono: ['JetBrains Mono', 'monospace'],
      },
      boxShadow: {
        'xs': '0 1px 2px 0 rgba(15, 23, 42, 0.04)',
        'sm': '0 1px 3px 0 rgba(15, 23, 42, 0.06), 0 1px 2px -1px rgba(15, 23, 42, 0.04)',
        'md': '0 4px 6px -1px rgba(15, 23, 42, 0.08), 0 2px 4px -2px rgba(15, 23, 42, 0.04)',
      }
    },
  },
  plugins: [],
}
