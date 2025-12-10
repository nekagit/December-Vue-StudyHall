<template>
  <div class="px-4 py-6 sm:px-0">
    <div v-if="loading" class="text-center py-12">
      <div class="inline-block animate-spin rounded-full h-8 w-8 border-b-2 border-indigo-600"></div>
    </div>

    <div v-else-if="error" class="rounded-md bg-red-50 p-4">
      <div class="text-sm text-red-800">{{ error }}</div>
    </div>

    <div v-else-if="material" class="bg-white shadow rounded-lg overflow-hidden">
      <div class="px-6 py-4 border-b border-gray-200">
        <div class="flex items-center justify-between mb-4">
          <h1 class="text-3xl font-bold text-gray-900">{{ material.title }}</h1>
          <span v-if="material.category" class="inline-flex items-center px-3 py-1 rounded-full text-sm font-medium bg-indigo-100 text-indigo-800">
            {{ material.category }}
          </span>
        </div>
        
        <!-- Progress Bar -->
        <div v-if="material.progress" class="mb-4">
          <div class="flex items-center justify-between mb-2">
            <span class="text-sm font-medium text-gray-700">Progress</span>
            <span class="text-sm text-gray-500">{{ Math.round(material.progress.progress_percentage) }}%</span>
          </div>
          <div class="w-full bg-gray-200 rounded-full h-2">
            <div
              class="bg-indigo-600 h-2 rounded-full transition-all duration-300"
              :style="{ width: `${material.progress.progress_percentage}%` }"
            ></div>
          </div>
          <div class="mt-2 flex space-x-2">
            <button
              @click="updateProgress('in_progress', 25)"
              class="text-xs px-2 py-1 bg-blue-100 text-blue-800 rounded hover:bg-blue-200"
            >
              25%
            </button>
            <button
              @click="updateProgress('in_progress', 50)"
              class="text-xs px-2 py-1 bg-blue-100 text-blue-800 rounded hover:bg-blue-200"
            >
              50%
            </button>
            <button
              @click="updateProgress('in_progress', 75)"
              class="text-xs px-2 py-1 bg-blue-100 text-blue-800 rounded hover:bg-blue-200"
            >
              75%
            </button>
            <button
              @click="updateProgress('completed', 100)"
              class="text-xs px-2 py-1 bg-green-100 text-green-800 rounded hover:bg-green-200"
            >
              Complete
            </button>
          </div>
        </div>

        <!-- Action Buttons -->
        <div class="flex items-center space-x-3">
          <button
            @click="toggleBookmark"
            :class="[
              'inline-flex items-center px-4 py-2 border text-sm font-medium rounded-md',
              material.is_bookmarked
                ? 'border-red-300 text-red-700 bg-red-50 hover:bg-red-100'
                : 'border-gray-300 text-gray-700 bg-white hover:bg-gray-50'
            ]"
          >
            <svg v-if="material.is_bookmarked" class="h-5 w-5 mr-2" fill="currentColor" viewBox="0 0 20 20">
              <path fill-rule="evenodd" d="M3.172 5.172a4 4 0 015.656 0L10 6.343l1.172-1.171a4 4 0 115.656 5.656L10 17.657l-6.828-6.829a4 4 0 010-5.656z" clip-rule="evenodd" />
            </svg>
            <svg v-else class="h-5 w-5 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4.318 6.318a4.5 4.5 0 000 6.364L12 20.364l7.682-7.682a4.5 4.5 0 00-6.364-6.364L12 7.636l-1.318-1.318a4.5 4.5 0 00-6.364 0z" />
            </svg>
            {{ material.is_bookmarked ? 'Bookmarked' : 'Bookmark' }}
          </button>
          <a
            v-if="material.notion_url"
            :href="material.notion_url"
            target="_blank"
            class="inline-flex items-center px-4 py-2 border border-gray-300 shadow-sm text-sm font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50"
          >
            View in Notion
          </a>
        </div>
      </div>
      <div class="px-6 py-4">
        <div class="prose max-w-none" v-html="formatContent(material.content)"></div>
      </div>

      <!-- Rating Section -->
      <div class="px-6 py-4 border-t border-gray-200">
        <h2 class="text-lg font-medium text-gray-900 mb-4">Rate this Material</h2>
        <div class="flex items-center space-x-2 mb-2">
          <button
            v-for="star in 5"
            :key="star"
            @click="submitRating(star)"
            class="focus:outline-none"
          >
            <svg
              class="w-8 h-8"
              :class="star <= (userRating?.rating || 0) ? 'text-yellow-400' : 'text-gray-300'"
              fill="currentColor"
              viewBox="0 0 20 20"
            >
              <path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z" />
            </svg>
          </button>
          <span v-if="userRating" class="ml-2 text-sm text-gray-600">
            Your rating: {{ userRating.rating }}/5
          </span>
        </div>
        <textarea
          v-model="ratingComment"
          rows="2"
          class="block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 mb-2"
          placeholder="Add a comment (optional)"
        ></textarea>
        <button
          v-if="userRating"
          @click="deleteRating"
          class="text-sm text-red-600 hover:text-red-800"
        >
          Remove rating
        </button>
      </div>

      <!-- Notes Section -->
      <div class="px-6 py-4 border-t border-gray-200">
        <h2 class="text-lg font-medium text-gray-900 mb-4">My Notes</h2>
        
        <!-- Add Note Form -->
        <div class="mb-4">
          <textarea
            v-model="newNoteContent"
            rows="3"
            class="block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 mb-2"
            placeholder="Add a note about this material..."
          ></textarea>
          <button
            @click="createNote"
            :disabled="!newNoteContent.trim()"
            class="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md text-white bg-indigo-600 hover:bg-indigo-700 disabled:opacity-50 disabled:cursor-not-allowed"
          >
            Add Note
          </button>
        </div>

        <!-- Notes List -->
        <div v-if="notesLoading" class="text-center py-4">
          <div class="inline-block animate-spin rounded-full h-6 w-6 border-b-2 border-indigo-600"></div>
        </div>
        <div v-else-if="notes.length === 0" class="text-sm text-gray-500 py-4">
          No notes yet. Add your first note above!
        </div>
        <div v-else class="space-y-4">
          <div
            v-for="note in notes"
            :key="note.id"
            class="bg-gray-50 rounded-lg p-4"
          >
            <div class="flex items-start justify-between">
              <p class="text-sm text-gray-700 whitespace-pre-wrap">{{ note.content }}</p>
              <button
                @click="deleteNote(note.id)"
                class="ml-4 text-red-600 hover:text-red-800"
              >
                <svg class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
                </svg>
              </button>
            </div>
            <p class="mt-2 text-xs text-gray-400">
              {{ formatDate(note.created_at) }}
            </p>
          </div>
        </div>
      </div>

      <div class="px-6 py-4 border-t border-gray-200">
        <router-link
          to="/materials"
          class="text-indigo-600 hover:text-indigo-500 font-medium"
        >
          ← Back to Materials
        </router-link>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'

const route = useRoute()
const material = ref<any>(null)
const loading = ref(true)
const error = ref('')
const notes = ref<any[]>([])
const notesLoading = ref(false)
const newNoteContent = ref('')
const userRating = ref<any>(null)
const ratingComment = ref('')

const formatContent = (content: string) => {
  if (!content) return ''
  // Simple markdown-like formatting
  return content
    .replace(/\n/g, '<br>')
    .replace(/#{3}\s(.+)/g, '<h3>$1</h3>')
    .replace(/#{2}\s(.+)/g, '<h2>$1</h2>')
    .replace(/#{1}\s(.+)/g, '<h1>$1</h1>')
}

const formatDate = (dateString: string): string => {
  const date = new Date(dateString)
  return date.toLocaleDateString() + ' ' + date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
}

const loadMaterial = async () => {
  loading.value = true
  try {
    const response = await fetch(`/api/materials/${route.params.id}`, {
      credentials: 'include'
    })
    if (response.ok) {
      material.value = await response.json()
      loadRating()
      loadNotes()
    } else {
      error.value = 'Material not found'
    }
  } catch (e) {
    error.value = 'An error occurred'
  } finally {
    loading.value = false
  }
}

const loadRating = async () => {
  if (!material.value) return
  try {
    const response = await fetch(`/api/materials/${material.value.id}/rating`, {
      credentials: 'include'
    })
    if (response.ok) {
      const data = await response.json()
      userRating.value = data.user_rating
      ratingComment.value = data.user_rating?.comment || ''
    }
  } catch (e) {
    // Ignore errors
  }
}

const loadNotes = async () => {
  if (!material.value) return
  notesLoading.value = true
  try {
    const response = await fetch(`/api/materials/${material.value.id}/notes`, {
      credentials: 'include'
    })
    if (response.ok) {
      notes.value = await response.json()
    }
  } catch (e) {
    // Ignore errors
  } finally {
    notesLoading.value = false
  }
}

const submitRating = async (rating: number) => {
  if (!material.value) return
  try {
    const response = await fetch(`/api/materials/${material.value.id}/rating`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      credentials: 'include',
      body: JSON.stringify({
        rating: rating,
        comment: ratingComment.value || null
      })
    })
    if (response.ok) {
      await loadRating()
    }
  } catch (e) {
    error.value = 'Failed to submit rating'
  }
}

const deleteRating = async () => {
  if (!userRating.value || !material.value) return
  try {
    // Set rating to null by sending a DELETE request or setting rating to 0
    // Since we don't have a DELETE endpoint, we'll just clear it locally
    // In a real app, you'd want a DELETE endpoint
    userRating.value = null
    ratingComment.value = ''
  } catch (e) {
    error.value = 'Failed to delete rating'
  }
}

const createNote = async () => {
  if (!material.value || !newNoteContent.value.trim()) return
  try {
    const response = await fetch(`/api/materials/${material.value.id}/notes`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      credentials: 'include',
      body: JSON.stringify({
        content: newNoteContent.value,
        title: null
      })
    })
    if (response.ok) {
      newNoteContent.value = ''
      await loadNotes()
    } else {
      error.value = 'Failed to create note'
    }
  } catch (e) {
    error.value = 'Failed to create note'
  }
}

const deleteNote = async (noteId: number) => {
  try {
    const response = await fetch(`/api/notes/${noteId}`, {
      method: 'DELETE',
      credentials: 'include'
    })
    if (response.ok) {
      await loadNotes()
    } else {
      error.value = 'Failed to delete note'
    }
  } catch (e) {
    error.value = 'Failed to delete note'
  }
}

const toggleBookmark = async () => {
  if (!material.value) return
  
  try {
    if (material.value.is_bookmarked) {
      // Remove bookmark
      const response = await fetch(`/api/bookmarks/material/${material.value.id}`, {
        method: 'DELETE',
        credentials: 'include'
      })
      if (response.ok) {
        material.value.is_bookmarked = false
        material.value.bookmark_id = null
      }
    } else {
      // Add bookmark
      const response = await fetch('/api/bookmarks', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        credentials: 'include',
        body: JSON.stringify({ material_id: material.value.id })
      })
      if (response.ok) {
        const data = await response.json()
        material.value.is_bookmarked = true
        material.value.bookmark_id = data.bookmark.id
      }
    }
  } catch (e) {
    error.value = 'Failed to update bookmark'
  }
}

const updateProgress = async (status: string, percentage: number) => {
  if (!material.value) return
  
  try {
    const response = await fetch(`/api/progress/material/${material.value.id}`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      credentials: 'include',
      body: JSON.stringify({ status, progress_percentage: percentage })
    })
    if (response.ok) {
      const data = await response.json()
      if (material.value.progress) {
        material.value.progress.status = data.progress.status
        material.value.progress.progress_percentage = data.progress.progress_percentage
      } else {
        material.value.progress = {
          status: data.progress.status,
          progress_percentage: data.progress.progress_percentage
        }
      }
    }
  } catch (e) {
    error.value = 'Failed to update progress'
  }
}

onMounted(loadMaterial)
</script>

