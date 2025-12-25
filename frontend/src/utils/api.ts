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

export interface ApiError {
  message: string
  status?: number
  error?: string
  traceback?: string
}

export async function apiFetchWithErrorHandling<T = any>(
  url: string,
  options: RequestInit = {}
): Promise<T> {
  try {
    const response = await apiFetch(url, options)
    const data = await response.json()
    
    if (!response.ok) {
      const error: ApiError = {
        message: data.error || data.message || `HTTP ${response.status}: ${response.statusText}`,
        status: response.status,
        error: data.error,
        traceback: data.traceback
      }
      throw error
    }
    
    return data
  } catch (error: any) {
    if (error instanceof TypeError && error.message === 'Failed to fetch') {
      throw {
        message: 'Network error: Unable to connect to the server. Please check your connection.',
        status: 0
      } as ApiError
    }
    throw error
  }
}

export function formatApiError(error: ApiError | Error | unknown): string {
  if (typeof error === 'object' && error !== null) {
    if ('message' in error) {
      return (error as ApiError).message || 'An unknown error occurred'
    }
  }
  if (error instanceof Error) {
    return error.message
  }
  return 'An unknown error occurred'
}
