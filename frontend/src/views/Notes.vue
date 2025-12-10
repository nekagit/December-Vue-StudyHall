<template>
  <div class="px-4 py-6 sm:px-0">
    <div class="mb-8">
      <h1 class="text-3xl font-bold text-gray-900 mb-2">My Notes</h1>
      <p class="text-gray-600">All your notes organized by material</p>
    </div>

    <div v-if="loading" class="text-center py-12">
      <div class="inline-block animate-spin rounded-full h-8 w-8 border-b-2 border-indigo-600"></div>
    </div>

    <div v-else-if="error" class="rounded-md bg-red-50 p-4 mb-4">
      <div class="text-sm text-red-800">{{ error }}</div>
    </div>

    <div v-else-if="notes.length === 0" class="text-center py-12">
      <p class="text-gray-500 mb-4">No notes yet. Start taking notes on materials!</p>
      <router-link
        to="/materials"
        class="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md text-white bg-indigo-600 hover:bg-indigo-700"
      >
        Browse Materials
      </router-link>
    </div>

    <div v-else class="space-y-6">
      <div
        v-for="note in notes"
        :key="note.id"
        class="bg-white shadow rounded-lg overflow-hidden"
      >
        <div class="px-6 py-4 border-b border-gray-200">
          <div class="flex items-center justify-between">
            <div>
              <h3 class="text-lg font-medium text-gray-900">
                <router-link
                  :to="`/materials/${note.material.id}`"
                  class="hover:text-indigo-600"
                >
                  {{ note.material.title }}
                </router-link>
              </h3>
              <p v-if="note.material.category" class="text-sm text-gray-500 mt-1">
                {{ note.material.category }}
              </p>
            </div>
            <button
              @click="deleteNote(note.id)"
              class="text-red-600 hover:text-red-800"
            >
              <svg class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
              </svg>
            </button>
          </div>
        </div>
        <div class="px-6 py-4">
          <p class="text-gray-700 whitespace-pre-wrap">{{ note.content }}</p>
          <p class="mt-4 text-xs text-gray-400">
            Created: {{ formatDate(note.created_at) }}
            <span v-if="note.updated_at && note.updated_at !== note.created_at">
              • Updated: {{ formatDate(note.updated_at) }}
            </span>
          </p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'

const notes = ref<any[]>([])
const loading = ref(true)
const error = ref('')

const formatDate = (dateString: string): string => {
  const date = new Date(dateString)
  return date.toLocaleDateString() + ' ' + date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
}

const loadNotes = async () => {
  loading.value = true
  try {
    const response = await fetch('/api/notes', {
      credentials: 'include'
    })
    if (response.ok) {
      notes.value = await response.json()
    } else {
      error.value = 'Failed to load notes'
    }
  } catch (e) {
    error.value = 'An error occurred'
  } finally {
    loading.value = false
  }
}

const deleteNote = async (noteId: number) => {
  if (!confirm('Are you sure you want to delete this note?')) return
  
  try {
    const response = await fetch(`/api/notes/${noteId}`, {
      method: 'DELETE',
      credentials: 'include'
    })
    if (response.ok) {
      loadNotes()
    } else {
      error.value = 'Failed to delete note'
    }
  } catch (e) {
    error.value = 'Failed to delete note'
  }
}

onMounted(loadNotes)
</script>
