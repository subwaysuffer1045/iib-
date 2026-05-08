import type { Config } from 'tailwindcss'

const config: Config = {
  content: [
    './app/**/*.{ts,tsx}',
    './components/**/*.{ts,tsx}',
    '../../packages/ui/src/**/*.{ts,tsx}',
  ],
  theme: {
    extend: {
      colors: {
        obsidian: {
          950: '#080B0F',
          900: '#0E1318',
          800: '#151D24',
          700: '#1E2A33',
          600: '#283542',
          500: '#374857',
        },
        amber: {
          300: '#FCD34D',
          400: '#FBBF24',
          500: '#F59E0B',
        },
      },
      fontFamily: {
        display: ['Instrument Serif', 'serif'],
        sans: ['DM Sans', 'sans-serif'],
        mono: ['JetBrains Mono', 'monospace'],
      },
      borderRadius: {
        sm: '6px',
        md: '10px',
        lg: '14px',
        xl: '20px',
      },
      animation: {
        'fade-up': 'fadeUp 0.4s ease forwards',
        'shimmer': 'shimmer 1.5s infinite',
        'pulse-amber': 'pulse-amber 2s infinite',
      },
    },
  },
  plugins: [],
}
export default config
