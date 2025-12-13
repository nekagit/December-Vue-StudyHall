<template>
  <div class="px-4 py-4 sm:py-6 sm:px-0">
    <div class="mb-6">
      <h1 class="text-2xl sm:text-3xl font-serif font-bold text-msit-dark-50">Course Materials</h1>
    </div>

    <!-- Search and Filter -->
    <div class="mb-6 bg-msit-dark-800 p-4 sm:p-6 rounded-lg shadow border border-msit-dark-700">
      <div class="grid grid-cols-1 gap-4 sm:grid-cols-2">
        <div>
          <label for="search" class="block text-sm font-semibold text-msit-dark-50 mb-2 font-sans">Search</label>
          <input
            id="search"
            v-model="searchQuery"
            @input="debouncedSearch"
            type="text"
            placeholder="Search materials..."
            class="block w-full rounded-md border-msit-dark-600 bg-msit-dark-700 text-msit-dark-50 placeholder-msit-dark-300 shadow-sm focus:border-msit-accent focus:ring-msit-accent text-sm sm:text-base px-3 py-2.5 border font-sans"
          />
        </div>
        <div>
          <label for="category" class="block text-sm font-semibold text-msit-dark-50 mb-2 font-sans">Category</label>
          <select
            id="category"
            v-model="selectedCategory"
            @change="loadMaterials"
            class="block w-full rounded-md border-msit-dark-600 bg-msit-dark-700 text-msit-dark-50 shadow-sm focus:border-msit-accent focus:ring-msit-accent text-sm sm:text-base px-3 py-2.5 border font-sans"
          >
            <option value="">All Categories</option>
            <option v-for="cat in categories" :key="cat" :value="cat">{{ cat }}</option>
          </select>
        </div>
      </div>
      <div v-if="searchQuery || selectedCategory" class="mt-4">
        <button
          @click="clearFilters"
          class="text-sm text-msit-accent hover:text-msit-accent-300 transition-colors font-sans"
        >
          Clear filters
        </button>
      </div>
    </div>

    <div v-if="error" class="rounded-md bg-red-900/30 border border-red-700 p-4 mb-4">
      <div class="text-sm text-red-300 font-sans">{{ error }}</div>
    </div>

    <div v-if="success" class="rounded-md bg-msit-accent/20 border border-msit-accent p-4 mb-4">
      <div class="text-sm text-msit-accent font-sans">{{ success }}</div>
    </div>

    <!-- Sync from Notion Button -->
    <div class="mb-6 flex justify-end">
      <button
        @click="syncFromNotion"
        :disabled="syncing"
        class="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md text-msit-dark bg-msit-accent hover:bg-msit-accent-500 transition-colors font-sans disabled:opacity-50 disabled:cursor-not-allowed"
      >
        <svg v-if="syncing" class="animate-spin -ml-1 mr-2 h-4 w-4" fill="none" viewBox="0 0 24 24">
          <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
          <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
        </svg>
        <svg v-else class="h-4 w-4 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
        </svg>
        {{ syncing ? 'Syncing...' : 'Sync from Notion' }}
      </button>
    </div>

    <div v-if="loading" class="text-center py-12">
      <div class="inline-block animate-spin rounded-full h-8 w-8 border-b-2 border-msit-accent"></div>
    </div>

    <div v-else-if="materials.length === 0" class="text-center py-12">
      <p class="text-msit-dark-200 font-sans">No materials found.</p>
    </div>

    <div v-else class="grid grid-cols-1 gap-4 sm:gap-6 sm:grid-cols-2 lg:grid-cols-3">
      <div
        v-for="material in materials"
        :key="material.id"
        class="bg-msit-dark-800 overflow-hidden shadow rounded-lg hover:shadow-lg transition-shadow border border-msit-dark-700 hover:border-msit-accent"
      >
        <div class="p-4 sm:p-6">
          <div class="flex flex-col sm:flex-row sm:items-start sm:justify-between gap-2 mb-2">
            <h3
              @click="$router.push(`/materials/${material.id}`)"
              class="text-base sm:text-lg font-semibold text-msit-dark-50 cursor-pointer hover:text-msit-accent transition-colors font-sans flex-1"
            >
              {{ material.title }}
            </h3>
            <span v-if="material.category" class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-msit-accent/20 text-msit-accent font-sans self-start sm:self-auto">
              {{ material.category }}
            </span>
          </div>
          <p v-if="material.content" class="mt-2 text-sm text-msit-dark-200 line-clamp-3 font-sans">
            {{ material.content.substring(0, 150) }}...
          </p>
          <div class="mt-4">
            <router-link
              :to="`/materials/${material.id}`"
              class="text-msit-accent hover:text-msit-accent-300 font-semibold text-sm transition-colors font-sans"
            >
              Read more →
            </router-link>
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
const searchQuery = ref('')
const selectedCategory = ref('')
const syncing = ref(false)
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
  loadMaterials()
}

const syncFromNotion = async () => {
  syncing.value = true
  error.value = ''
  success.value = ''
  
  try {
    const response = await fetch('/api/materials/sync-notion', {
      method: 'POST',
      credentials: 'include',
      headers: {
        'Content-Type': 'application/json'
      }
    })
    
    if (!response.ok) {
      const errorData = await response.json().catch(() => ({}))
      throw new Error(errorData.error || 'Failed to sync from Notion')
    }
    
    const result = await response.json()
    
    if (result.success) {
      success.value = `Successfully synced ${result.synced_count || 0} materials from Notion`
      // Reload materials after sync
      await loadMaterials()
      // Clear success message after 5 seconds
      setTimeout(() => {
        success.value = ''
      }, 5000)
    } else {
      throw new Error(result.error || 'Sync failed')
    }
  } catch (e: any) {
    error.value = e.message || 'An error occurred while syncing from Notion'
    console.error('Notion sync error:', e)
  } finally {
    syncing.value = false
  }
}

onMounted(() => {
  loadMaterials()
  loadCategories()
})
</script>

