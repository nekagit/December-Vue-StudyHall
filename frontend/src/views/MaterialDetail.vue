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

        <!-- Rating Section -->
        <div class="mb-4">
          <div class="flex items-center space-x-2">
            <span class="text-sm font-medium text-gray-700">Rating:</span>
            <div class="flex items-center space-x-1">
              <button
                v-for="star in 5"
                :key="star"
                @click="setRating(star)"
                :class="[
                  'text-2xl',
                  star <= (userRating || 0) ? 'text-yellow-400' : 'text-gray-300'
                ]"
              >
                ★
              </button>
            </div>
            <span v-if="averageRating" class="text-sm text-gray-500 ml-2">
              ({{ averageRating }}/5.0 from {{ ratingCount }} {{ ratingCount === 1 ? 'rating' : 'ratings' }})
            </span>
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
      
      <!-- Study Timer Section -->
      <div class="px-6 py-4 border-t border-gray-200">
        <StudyTimer :material-id="material?.id" />
      </div>
      
      <!-- Notes Section -->
      <div class="px-6 py-4 border-t border-gray-200">
        <h2 class="text-xl font-semibold text-gray-900 mb-4">My Notes</h2>
        <div class="mb-4">
          <textarea
            v-model="noteContent"
            @blur="saveNote"
            rows="6"
            placeholder="Add your personal notes about this material..."
            class="block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm px-3 py-2 border"
          ></textarea>
          <div class="mt-2 flex justify-end">
            <button
              @click="saveNote"
              class="inline-flex items-center px-3 py-2 border border-transparent text-sm leading-4 font-medium rounded-md text-white bg-indigo-600 hover:bg-indigo-700"
            >
              Save Note
            </button>
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
import StudyTimer from '../components/StudyTimer.vue'

const route = useRoute()
const material = ref<any>(null)
const loading = ref(true)
const error = ref('')
const noteContent = ref('')
const noteSaving = ref(false)
const userRating = ref<number | null>(null)
const averageRating = ref<number | null>(null)
const ratingCount = ref(0)

const formatContent = (content: string) => {
  if (!content) return ''
  // Simple markdown-like formatting
  return content
    .replace(/\n/g, '<br>')
    .replace(/#{3}\s(.+)/g, '<h3>$1</h3>')
    .replace(/#{2}\s(.+)/g, '<h2>$1</h2>')
    .replace(/#{1}\s(.+)/g, '<h1>$1</h1>')
}

const loadMaterial = async () => {
  loading.value = true
  try {
    const response = await fetch(`/api/materials/${route.params.id}`, {
      credentials: 'include'
    })
    if (response.ok) {
      material.value = await response.json()
      await loadNote()
      await loadRating()
    } else {
      error.value = 'Material not found'
    }
  } catch (e) {
    error.value = 'An error occurred'
  } finally {
    loading.value = false
  }
}

const loadNote = async () => {
  if (!material.value) return
  try {
    const response = await fetch(`/api/notes/material/${material.value.id}`, {
      credentials: 'include'
    })
    if (response.ok) {
      const note = await response.json()
      noteContent.value = note.content || ''
    }
  } catch (e) {
    // Ignore errors
  }
}

const saveNote = async () => {
  if (!material.value || noteSaving.value) return
  
  noteSaving.value = true
  try {
    const response = await fetch(`/api/notes/material/${material.value.id}`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      credentials: 'include',
      body: JSON.stringify({ content: noteContent.value })
    })
    if (response.ok) {
      // Note saved successfully
    }
  } catch (e) {
    error.value = 'Failed to save note'
  } finally {
    noteSaving.value = false
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

const loadRating = async () => {
  if (!material.value) return
  try {
    const response = await fetch(`/api/ratings/material/${material.value.id}`, {
      credentials: 'include'
    })
    if (response.ok) {
      const data = await response.json()
      userRating.value = data.user_rating
      averageRating.value = data.average_rating
      ratingCount.value = data.rating_count
    }
  } catch (e) {
    // Ignore errors
  }
}

const setRating = async (rating: number) => {
  if (!material.value) return
  try {
    const response = await fetch(`/api/ratings/material/${material.value.id}`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      credentials: 'include',
      body: JSON.stringify({ rating })
    })
    if (response.ok) {
      await loadRating()
    }
  } catch (e) {
    error.value = 'Failed to set rating'
  }
}

onMounted(loadMaterial)
</script>

