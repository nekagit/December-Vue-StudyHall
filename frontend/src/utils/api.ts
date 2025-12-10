/**
 * API utility functions with character headers
 */

import { getCharacterConfig } from './character'

export function getCharacterHeaders(): Record<string, string> {
  const character = getCharacterConfig()
  if (!character) {
    return {}
  }
  
  return {
    'X-Character-Id': character.id || '',
    'X-Character-Name': character.name || '',
    'X-Character-Role': character.role || 'student'
  }
}

export async function apiFetch(url: string, options: RequestInit = {}): Promise<Response> {
  const headers = {
    'Content-Type': 'application/json',
    ...getCharacterHeaders(),
    ...(options.headers || {})
  }
  
  return fetch(url, {
    ...options,
    headers,
    credentials: 'include'
  })
}
