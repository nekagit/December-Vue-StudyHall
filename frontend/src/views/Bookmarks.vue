<template>
  <div class="px-4 py-6 sm:px-0">
    <h1 class="text-3xl font-bold text-gray-900 mb-6">My Bookmarks</h1>

    <div v-if="loading" class="text-center py-12">
      <div class="inline-block animate-spin rounded-full h-8 w-8 border-b-2 border-indigo-600"></div>
    </div>

    <div v-else-if="error" class="rounded-md bg-red-50 p-4 mb-4">
      <div class="text-sm text-red-800">{{ error }}</div>
    </div>

    <div v-else-if="bookmarks.length === 0" class="text-center py-12">
      <svg class="mx-auto h-12 w-12 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 5a2 2 0 012-2h10a2 2 0 012 2v16l-7-3.5L5 21V5z" />
      </svg>
      <h3 class="mt-2 text-sm font-medium text-gray-900">No bookmarks</h3>
      <p class="mt-1 text-sm text-gray-500">Get started by bookmarking materials you want to save for later.</p>
      <div class="mt-6">
        <router-link
          to="/materials"
          class="inline-flex items-center px-4 py-2 border border-transparent shadow-sm text-sm font-medium rounded-md text-white bg-indigo-600 hover:bg-indigo-700"
        >
          Browse Materials
        </router-link>
      </div>
    </div>

    <div v-else class="grid grid-cols-1 gap-6 sm:grid-cols-2 lg:grid-cols-3">
      <div
        v-for="bookmark in bookmarks"
        :key="bookmark.id"
        class="bg-white overflow-hidden shadow rounded-lg hover:shadow-lg transition-shadow"
      >
        <div class="p-6">
          <div class="flex items-center justify-between mb-3">
            <span v-if="bookmark.material.category" class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-indigo-100 text-indigo-800">
              {{ bookmark.material.category }}
            </span>
            <button
              @click="removeBookmark(bookmark.id)"
              class="text-red-600 hover:text-red-800"
              title="Remove bookmark"
            >
              <svg class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
              </svg>
            </button>
          </div>
          <h3 class="text-lg font-medium text-gray-900 mb-2">{{ bookmark.material.title }}</h3>
          <div class="flex items-center justify-between mt-4">
            <router-link
              :to="`/materials/${bookmark.material.id}`"
              class="text-indigo-600 hover:text-indigo-500 font-medium text-sm"
            >
              View Material →
            </router-link>
            <span class="text-xs text-gray-500">
              {{ formatDate(bookmark.created_at) }}
            </span>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'

const bookmarks = ref<any[]>([])
const loading = ref(true)
const error = ref('')

const formatDate = (dateString: string) => {
  if (!dateString) return ''
  const date = new Date(dateString)
  return date.toLocaleDateString('en-US', { year: 'numeric', month: 'short', day: 'numeric' })
}

const loadBookmarks = async () => {
  loading.value = true
  try {
    const response = await fetch('/api/bookmarks', {
      credentials: 'include'
    })
    if (response.ok) {
      bookmarks.value = await response.json()
    } else {
      error.value = 'Failed to load bookmarks'
    }
  } catch (e) {
    error.value = 'An error occurred'
  } finally {
    loading.value = false
  }
}

const removeBookmark = async (bookmarkId: number) => {
  try {
    const response = await fetch(`/api/bookmarks/${bookmarkId}`, {
      method: 'DELETE',
      credentials: 'include'
    })
    if (response.ok) {
      bookmarks.value = bookmarks.value.filter(b => b.id !== bookmarkId)
    } else {
      error.value = 'Failed to remove bookmark'
    }
  } catch (e) {
    error.value = 'An error occurred'
  }
}

onMounted(loadBookmarks)
</script>
