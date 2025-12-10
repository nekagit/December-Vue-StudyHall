<template>
  <div class="px-4 py-6 sm:px-0">
    <div class="flex justify-between items-center mb-6">
      <h1 class="text-3xl font-bold text-gray-900">Course Materials</h1>
      <button
        @click="syncNotion"
        :disabled="syncing"
        class="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md text-white bg-indigo-600 hover:bg-indigo-700 disabled:opacity-50"
      >
        {{ syncing ? 'Syncing...' : 'Sync from Notion' }}
      </button>
    </div>

    <!-- Search and Filter -->
    <div class="mb-6 bg-white p-4 rounded-lg shadow">
      <div class="grid grid-cols-1 gap-4 sm:grid-cols-3">
        <div>
          <label for="search" class="block text-sm font-medium text-gray-700 mb-2">Search</label>
          <input
            id="search"
            v-model="searchQuery"
            @input="debouncedSearch"
            type="text"
            placeholder="Search materials..."
            class="block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm px-3 py-2 border"
          />
        </div>
        <div>
          <label for="category" class="block text-sm font-medium text-gray-700 mb-2">Category</label>
          <select
            id="category"
            v-model="selectedCategory"
            @change="loadMaterials"
            class="block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm px-3 py-2 border"
          >
            <option value="">All Categories</option>
            <option v-for="cat in categories" :key="cat" :value="cat">{{ cat }}</option>
          </select>
        </div>
        <div>
          <label for="progressStatus" class="block text-sm font-medium text-gray-700 mb-2">Progress Status</label>
          <select
            id="progressStatus"
            v-model="selectedProgressStatus"
            @change="loadMaterials"
            class="block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm px-3 py-2 border"
          >
            <option value="">All Statuses</option>
            <option value="not_started">Not Started</option>
            <option value="in_progress">In Progress</option>
            <option value="completed">Completed</option>
          </select>
        </div>
      </div>
      <div v-if="searchQuery || selectedCategory || selectedProgressStatus" class="mt-3">
        <button
          @click="clearFilters"
          class="text-sm text-indigo-600 hover:text-indigo-500"
        >
          Clear filters
        </button>
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
      <p class="text-gray-500">No materials found. Click "Sync from Notion" to import materials.</p>
    </div>

    <div v-else class="grid grid-cols-1 gap-6 sm:grid-cols-2 lg:grid-cols-3">
      <div
        v-for="material in materials"
        :key="material.id"
        class="bg-white overflow-hidden shadow rounded-lg hover:shadow-lg transition-shadow"
      >
        <div class="p-6">
          <div class="flex items-start justify-between mb-2">
            <h3
              @click="$router.push(`/materials/${material.id}`)"
              class="text-lg font-medium text-gray-900 cursor-pointer hover:text-indigo-600"
            >
              {{ material.title }}
            </h3>
            <div class="flex items-center space-x-2">
              <span v-if="material.category" class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-indigo-100 text-indigo-800">
                {{ material.category }}
              </span>
              <button
                v-if="material.is_bookmarked"
                class="text-red-500"
                title="Bookmarked"
                @click.stop="toggleBookmark(material)"
              >
                <svg class="h-5 w-5" fill="currentColor" viewBox="0 0 20 20">
                  <path fill-rule="evenodd" d="M3.172 5.172a4 4 0 015.656 0L10 6.343l1.172-1.171a4 4 0 115.656 5.656L10 17.657l-6.828-6.829a4 4 0 010-5.656z" clip-rule="evenodd" />
                </svg>
              </button>
            </div>
          </div>
          <p v-if="material.content" class="mt-2 text-sm text-gray-500 line-clamp-3">
            {{ material.content.substring(0, 150) }}...
          </p>
          <div class="mt-4 flex items-center justify-between">
            <router-link
              :to="`/materials/${material.id}`"
              class="text-indigo-600 hover:text-indigo-500 font-medium text-sm"
            >
              Read more →
            </router-link>
            <span v-if="material.reading_time_minutes" class="text-xs text-gray-400">
              ⏱ {{ material.reading_time_minutes }} min read
            </span>
          </div>
          <div v-if="material.progress_status" class="mt-2">
            <span
              class="inline-flex items-center px-2 py-0.5 rounded text-xs font-medium"
              :class="{
                'bg-green-100 text-green-800': material.progress_status === 'completed',
                'bg-blue-100 text-blue-800': material.progress_status === 'in_progress',
                'bg-gray-100 text-gray-800': material.progress_status === 'not_started'
              }"
            >
              {{ material.progress_status.replace('_', ' ') }}
            </span>
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
const selectedProgressStatus = ref('')
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
    if (selectedProgressStatus.value) {
      params.append('progress_status', selectedProgressStatus.value)
    }
    
    const url = `/api/materials${params.toString() ? '?' + params.toString() : ''}`
    const response = await fetch(url, {
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

const clearFilters = () => {
  searchQuery.value = ''
  selectedCategory.value = ''
  selectedProgressStatus.value = ''
  loadMaterials()
}

const toggleBookmark = async (material: any) => {
  try {
    if (material.is_bookmarked) {
      const response = await fetch(`/api/bookmarks/material/${material.id}`, {
        method: 'DELETE',
        credentials: 'include'
      })
      if (response.ok) {
        material.is_bookmarked = false
      }
    } else {
      const response = await fetch('/api/bookmarks', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        credentials: 'include',
        body: JSON.stringify({ material_id: material.id })
      })
      if (response.ok) {
        material.is_bookmarked = true
      }
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

