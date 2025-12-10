<template>
  <div class="px-4 py-6 sm:px-0">
    <div class="flex items-center justify-between mb-6">
      <h1 class="text-3xl font-bold text-gray-900">Bookmarked Materials</h1>
      <router-link
        to="/materials"
        class="inline-flex items-center px-4 py-2 border border-gray-300 text-sm font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50"
      >
        ← Back to Materials
      </router-link>
    </div>

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
      <p class="mt-4 text-gray-500">No bookmarked materials yet.</p>
      <router-link
        to="/materials"
        class="mt-4 inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md text-white bg-indigo-600 hover:bg-indigo-700"
      >
        Browse Materials
      </router-link>
    </div>

    <div v-else class="grid grid-cols-1 gap-6 sm:grid-cols-2 lg:grid-cols-3">
      <div
        v-for="material in bookmarks"
        :key="material.id"
        class="bg-white overflow-hidden shadow rounded-lg hover:shadow-lg transition-shadow"
      >
        <div class="p-6">
          <div class="flex items-start justify-between mb-2">
            <h3 
              @click="$router.push(`/materials/${material.id}`)"
              class="text-lg font-medium text-gray-900 cursor-pointer hover:text-indigo-600 flex-1"
            >
              {{ material.title }}
            </h3>
            <button
              @click="removeBookmark(material)"
              class="ml-2 text-yellow-500 hover:text-yellow-600 transition-colors"
            >
              <svg class="h-5 w-5" fill="currentColor" viewBox="0 0 20 20">
                <path d="M5 4a2 2 0 012-2h6a2 2 0 012 2v14l-5-2.5L5 18V4z" />
              </svg>
            </button>
          </div>
          <div class="flex items-center gap-2 mb-2">
            <span v-if="material.category" class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-indigo-100 text-indigo-800">
              {{ material.category }}
            </span>
          </div>
          <p v-if="material.content" class="mt-2 text-sm text-gray-500 line-clamp-3">
            {{ material.content }}
          </p>
          <div class="mt-4">
            <button
              @click="$router.push(`/materials/${material.id}`)"
              class="text-indigo-600 hover:text-indigo-500 text-sm font-medium"
            >
              Read more →
            </button>
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

const removeBookmark = async (material: any) => {
  try {
    const response = await fetch(`/api/bookmarks/${material.id}`, {
      method: 'DELETE',
      credentials: 'include'
    })
    if (response.ok) {
      bookmarks.value = bookmarks.value.filter(b => b.id !== material.id)
    }
  } catch (e) {
    error.value = 'Failed to remove bookmark'
  }
}

onMounted(loadBookmarks)
</script>
