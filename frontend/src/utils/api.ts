/**
 * API utility functions with character headers
 */

export function getCharacterHeaders(): Record<string, string> {
  const character = localStorage.getItem('character')
  if (!character) {
    return {}
  }
  
  try {
    const char = JSON.parse(character)
    return {
      'X-Character-Id': char.id || '',
      'X-Character-Name': char.name || '',
      'X-Character-Role': char.role || 'student'
    }
  } catch (e) {
    return {}
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
