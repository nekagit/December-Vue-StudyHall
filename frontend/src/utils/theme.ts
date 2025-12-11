/**
 * Theme management utility for color theme switching
 */

export interface Theme {
  id: string
  name: string
  description: string
  colors: {
    dark: string
    dark50: string
    dark100: string
    dark200: string
    dark300: string
    dark600: string
    dark700: string
    dark800: string
    dark900: string
    accent: string
    accent300: string
    accent500: string
  }
}

export const themes: Theme[] = [
  {
    id: 'msit-green',
    name: 'MSIT Green',
    description: 'Default green theme inspired by nature',
    colors: {
      dark: '#1A312B',
      dark50: '#E0EADD',
      dark100: '#D4E3D0',
      dark200: '#C2D5BC',
      dark300: '#B0C7A8',
      dark600: '#6B8A63',
      dark700: '#4A6946',
      dark800: '#2A3F35',
      dark900: '#0F1D19',
      accent: '#83E65B',
      accent300: '#A2ED87',
      accent500: '#6BD945',
    },
  },
  {
    id: 'ocean-blue',
    name: 'Ocean Blue',
    description: 'Calm and professional blue theme',
    colors: {
      dark: '#1A2332',
      dark50: '#E0E8F0',
      dark100: '#D4DEE8',
      dark200: '#C2D0DE',
      dark300: '#B0C2D4',
      dark600: '#6B8AA3',
      dark700: '#4A6B8A',
      dark800: '#2A3F52',
      dark900: '#0F1A26',
      accent: '#5B9FE6',
      accent300: '#87B2ED',
      accent500: '#4589D9',
    },
  },
  {
    id: 'purple-dream',
    name: 'Purple Dream',
    description: 'Modern and vibrant purple theme',
    colors: {
      dark: '#2A1A32',
      dark50: '#F0E0F0',
      dark100: '#E8D4E8',
      dark200: '#DEC2DE',
      dark300: '#D4B0D4',
      dark600: '#A36BA3',
      dark700: '#8A4A8A',
      dark800: '#522A52',
      dark900: '#260F26',
      accent: '#E65BE6',
      accent300: '#ED87ED',
      accent500: '#D945D9',
    },
  },
  {
    id: 'amber-warm',
    name: 'Amber Warm',
    description: 'Warm and cozy amber theme',
    colors: {
      dark: '#322A1A',
      dark50: '#F0E8E0',
      dark100: '#E8DED4',
      dark200: '#DED2C2',
      dark300: '#D4C6B0',
      dark600: '#A38B6B',
      dark700: '#8A6F4A',
      dark800: '#52422A',
      dark900: '#261F0F',
      accent: '#E6A35B',
      accent300: '#EDB887',
      accent500: '#D98F45',
    },
  },
  {
    id: 'crimson-bold',
    name: 'Crimson Bold',
    description: 'Bold and energetic red theme',
    colors: {
      dark: '#321A1A',
      dark50: '#F0E0E0',
      dark100: '#E8D4D4',
      dark200: '#DEC2C2',
      dark300: '#D4B0B0',
      dark600: '#A36B6B',
      dark700: '#8A4A4A',
      dark800: '#522A2A',
      dark900: '#260F0F',
      accent: '#E65B5B',
      accent300: '#ED8787',
      accent500: '#D94545',
    },
  },
  {
    id: 'indigo-classic',
    name: 'Indigo Classic',
    description: 'Classic and elegant indigo theme',
    colors: {
      dark: '#1A1F32',
      dark50: '#E0E2F0',
      dark100: '#D4D7E8',
      dark200: '#C2C6DE',
      dark300: '#B0B5D4',
      dark600: '#6B73A3',
      dark700: '#4A548A',
      dark800: '#2A3252',
      dark900: '#0F1326',
      accent: '#5B6BE6',
      accent300: '#878FED',
      accent500: '#4555D9',
    },
  },
  {
    id: 'slate-minimal',
    name: 'Slate Minimal',
    description: 'Minimalist gray theme',
    colors: {
      dark: '#1F1F23',
      dark50: '#E8E8EA',
      dark100: '#DCDCDE',
      dark200: '#CACACC',
      dark300: '#B8B8BA',
      dark600: '#6B6B6F',
      dark700: '#4A4A4E',
      dark800: '#2F2F33',
      dark900: '#141418',
      accent: '#8B8B8F',
      accent300: '#A3A3A7',
      accent500: '#737377',
    },
  },
  {
    id: 'emerald-fresh',
    name: 'Emerald Fresh',
    description: 'Fresh and vibrant emerald theme',
    colors: {
      dark: '#1A2B26',
      dark50: '#E0F0EA',
      dark100: '#D4E8E0',
      dark200: '#C2DED4',
      dark300: '#B0D4C8',
      dark600: '#6BA38B',
      dark700: '#4A8A6F',
      dark800: '#2A5242',
      dark900: '#0F261F',
      accent: '#5BE6A3',
      accent300: '#87EDB8',
      accent500: '#45D98F',
    },
  },
]

const THEME_STORAGE_KEY = 'theme'
const DEFAULT_THEME_ID = 'msit-green'

/**
 * Get current theme from localStorage
 */
export function getCurrentTheme(): string {
  try {
    const stored = localStorage.getItem(THEME_STORAGE_KEY)
    return stored || DEFAULT_THEME_ID
  } catch (e) {
    console.error('Failed to get theme from localStorage:', e)
    return DEFAULT_THEME_ID
  }
}

/**
 * Save theme to localStorage
 */
export function saveTheme(themeId: string): void {
  try {
    localStorage.setItem(THEME_STORAGE_KEY, themeId)
  } catch (e) {
    console.error('Failed to save theme to localStorage:', e)
    throw new Error('Failed to save theme')
  }
}

/**
 * Get theme by ID
 */
export function getThemeById(themeId: string): Theme | undefined {
  return themes.find((theme) => theme.id === themeId)
}

/**
 * Apply theme to the document
 */
export function applyTheme(theme: Theme): void {
  const root = document.documentElement
  root.style.setProperty('--msit-dark', theme.colors.dark)
  root.style.setProperty('--msit-dark-50', theme.colors.dark50)
  root.style.setProperty('--msit-dark-100', theme.colors.dark100)
  root.style.setProperty('--msit-dark-200', theme.colors.dark200)
  root.style.setProperty('--msit-dark-300', theme.colors.dark300)
  root.style.setProperty('--msit-dark-600', theme.colors.dark600)
  root.style.setProperty('--msit-dark-700', theme.colors.dark700)
  root.style.setProperty('--msit-dark-800', theme.colors.dark800)
  root.style.setProperty('--msit-dark-900', theme.colors.dark900)
  root.style.setProperty('--msit-accent', theme.colors.accent)
  root.style.setProperty('--msit-accent-300', theme.colors.accent300)
  root.style.setProperty('--msit-accent-500', theme.colors.accent500)
}

/**
 * Initialize theme on app load
 */
export function initializeTheme(): void {
  const themeId = getCurrentTheme()
  const theme = getThemeById(themeId) || getThemeById(DEFAULT_THEME_ID)!
  applyTheme(theme)
}

