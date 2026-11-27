/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        ivory: {
          50: '#FDFBF7',
          100: '#F7F4EE',
          200: '#EFECE4',
          300: '#E3DFD5',
        },
        forest: {
          700: '#254A3B',
          800: '#1E3A2F',
          900: '#152921',
          950: '#0E1C16',
        },
        sage: {
          50: '#F4F7F5',
          100: '#EAF2EC',
          200: '#D2E2D6',
          400: '#8BAF99',
          500: '#6B8E7C',
          600: '#547262',
        },
        charcoal: {
          700: '#374151',
          800: '#1F2937',
          900: '#111827',
        },
        warmred: {
          500: '#C2410C',
          600: '#DC2626',
        }
      },
      fontFamily: {
        sans: ['"Plus Jakarta Sans"', 'Inter', 'system-ui', 'sans-serif'],
      },
      boxShadow: {
        'soft': '0 2px 10px rgba(30, 58, 47, 0.04)',
        'card': '0 4px 20px rgba(30, 58, 47, 0.06)',
        'card-hover': '0 8px 28px rgba(30, 58, 47, 0.09)',
      }
    },
  },
  plugins: [],
}
