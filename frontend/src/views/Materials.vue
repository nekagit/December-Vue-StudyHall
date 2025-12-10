<template>
  <div class="px-4 py-6 sm:px-0">
    <div class="flex flex-col sm:flex-row justify-between items-start sm:items-center mb-6 gap-4">
      <h1 class="text-3xl font-bold text-gray-900">Course Materials</h1>
      <div class="flex gap-2">
        <router-link
          to="/bookmarks"
          class="inline-flex items-center px-4 py-2 border border-gray-300 text-sm font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50"
        >
          <svg class="h-5 w-5 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 5a2 2 0 012-2h10a2 2 0 012 2v16l-7-3.5L5 21V5z" />
          </svg>
          Bookmarks
        </router-link>
        <button
          @click="syncNotion"
          :disabled="syncing"
          class="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md text-white bg-indigo-600 hover:bg-indigo-700 disabled:opacity-50"
        >
          {{ syncing ? 'Syncing...' : 'Sync from Notion' }}
        </button>
      </div>
    </div>

    <!-- Search and Filter Bar -->
    <div class="mb-6 bg-white p-4 rounded-lg shadow-sm">
      <div class="flex flex-col sm:flex-row gap-4">
        <div class="flex-1">
          <div class="relative">
            <div class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
              <svg class="h-5 w-5 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
              </svg>
            </div>
            <input
              v-model="searchQuery"
              @input="debouncedSearch"
              type="text"
              placeholder="Search materials..."
              class="block w-full pl-10 pr-3 py-2 border border-gray-300 rounded-md leading-5 bg-white placeholder-gray-500 focus:outline-none focus:placeholder-gray-400 focus:ring-1 focus:ring-indigo-500 focus:border-indigo-500"
            />
          </div>
        </div>
        <div class="sm:w-48">
          <select
            v-model="selectedCategory"
            @change="loadMaterials"
            class="block w-full px-3 py-2 border border-gray-300 rounded-md bg-white focus:outline-none focus:ring-indigo-500 focus:border-indigo-500"
          >
            <option value="">All Categories</option>
            <option v-for="cat in categories" :key="cat" :value="cat">{{ cat }}</option>
          </select>
        </div>
      </div>
    </div>

    <div v-if="error" class="rounded-md bg-red-50 p-4 mb-4">
      <div class="text-sm text-red-800">{{ error }}</div>
    </div>

    <div v-if="success" class="rounded-md bg-green-50 p-4 mb-4">
      <div class="text-sm text-green-800">{{ success }}</div>
    </div>

    <div v-if="loading" class="text-center py-12">
      <div class="inline-block animate-spin rounded-full h-8 w-8 border-b-2 border-indigo-600"></div>
    </div>

    <div v-else-if="materials.length === 0" class="text-center py-12">
      <p class="text-gray-500">No materials found. {{ searchQuery || selectedCategory ? 'Try adjusting your filters.' : 'Click "Sync from Notion" to import materials.' }}</p>
    </div>

    <div v-else class="grid grid-cols-1 gap-6 sm:grid-cols-2 lg:grid-cols-3">
      <div
        v-for="material in materials"
        :key="material.id"
        class="bg-white overflow-hidden shadow rounded-lg hover:shadow-lg transition-shadow relative"
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
              @click.stop="toggleBookmark(material)"
              class="ml-2 text-gray-400 hover:text-yellow-500 transition-colors"
              :class="{ 'text-yellow-500': material.is_bookmarked }"
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
            <span v-if="material.progress.is_completed" class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-green-100 text-green-800">
              Completed
            </span>
            <span v-else-if="material.progress.progress_percentage > 0" class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-blue-100 text-blue-800">
              {{ material.progress.progress_percentage }}%
            </span>
          </div>
          <p v-if="material.content" class="mt-2 text-sm text-gray-500 line-clamp-3">
            {{ material.content.substring(0, 150) }}...
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

const materials = ref<any[]>([])
const categories = ref<string[]>([])
const loading = ref(true)
const error = ref('')
const success = ref('')
const syncing = ref(false)
const searchQuery = ref('')
const selectedCategory = ref('')
let searchTimeout: ReturnType<typeof setTimeout> | null = null

const loadMaterials = async () => {
  loading.value = true
  try {
    const params = new URLSearchParams()
    if (searchQuery.value) {
      params.append('search', searchQuery.value)
    }
    if (selectedCategory.value) {
      params.append('category', selectedCategory.value)
    }
    
    const response = await fetch(`/api/materials?${params.toString()}`, {
      credentials: 'include'
    })
    if (response.ok) {
      materials.value = await response.json()
    } else {
      error.value = 'Failed to load materials'
    }
  } catch (e) {
    error.value = 'An error occurred'
  } finally {
    loading.value = false
  }
}

const loadCategories = async () => {
  try {
    const response = await fetch('/api/materials/categories', {
      credentials: 'include'
    })
    if (response.ok) {
      categories.value = await response.json()
    }
  } catch (e) {
    // Ignore errors
  }
}

const debouncedSearch = () => {
  if (searchTimeout) {
    clearTimeout(searchTimeout)
  }
  searchTimeout = setTimeout(() => {
    loadMaterials()
  }, 300)
}

const toggleBookmark = async (material: any) => {
  try {
    if (material.is_bookmarked) {
      await fetch(`/api/bookmarks/${material.id}`, {
        method: 'DELETE',
        credentials: 'include'
      })
      material.is_bookmarked = false
    } else {
      await fetch(`/api/bookmarks/${material.id}`, {
        method: 'POST',
        credentials: 'include'
      })
      material.is_bookmarked = true
    }
  } catch (e) {
    error.value = 'Failed to update bookmark'
  }
}

const syncNotion = async () => {
  syncing.value = true
  error.value = ''
  success.value = ''
  try {
    const response = await fetch('/api/materials/sync-notion', {
      method: 'POST',
      credentials: 'include'
    })
    if (response.ok) {
      const data = await response.json()
      success.value = `Synced ${data.synced} new materials!`
      await loadMaterials()
      await loadCategories()
    } else {
      const data = await response.json()
      error.value = data.error || 'Failed to sync'
    }
  } catch (e) {
    error.value = 'An error occurred while syncing'
  } finally {
    syncing.value = false
  }
}

onMounted(() => {
  loadMaterials()
  loadCategories()
})
</script>

