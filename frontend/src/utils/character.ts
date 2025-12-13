/**
 * Character configuration utility for localStorage management
 */

export interface CharacterConfig {
  name: string
  role: string
  id: string
}

const CHARACTER_STORAGE_KEY = 'character'

/**
 * Get character config from localStorage
 */
export function getCharacterConfig(): CharacterConfig | null {
  try {
    const stored = localStorage.getItem(CHARACTER_STORAGE_KEY)
    if (!stored) {
      return null
    }
    return JSON.parse(stored) as CharacterConfig
  } catch (e) {
    console.error('Failed to parse character config from localStorage:', e)
    return null
  }
}

/**
 * Save character config to localStorage
 */
export function saveCharacterConfig(config: CharacterConfig): void {
  try {
    localStorage.setItem(CHARACTER_STORAGE_KEY, JSON.stringify(config))
  } catch (e) {
    console.error('Failed to save character config to localStorage:', e)
    throw new Error('Failed to save character configuration')
  }
}

/**
 * Remove character config from localStorage
 */
export function removeCharacterConfig(): void {
  try {
    localStorage.removeItem(CHARACTER_STORAGE_KEY)
  } catch (e) {
    console.error('Failed to remove character config from localStorage:', e)
  }
}

/**
 * Check if character config exists
 */
export function hasCharacterConfig(): boolean {
  return localStorage.getItem(CHARACTER_STORAGE_KEY) !== null
}









