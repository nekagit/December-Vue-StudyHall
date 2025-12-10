<template>
  <div class="px-4 py-4 sm:py-6 sm:px-0">
    <div class="flex flex-col sm:flex-row sm:justify-between sm:items-center gap-4 mb-6">
      <h1 class="text-2xl sm:text-3xl font-serif font-bold text-msit-dark-50">Course Materials</h1>
      <button
        @click="syncNotion"
        :disabled="syncing"
        class="w-full sm:w-auto inline-flex items-center justify-center px-4 py-2 border border-transparent text-sm font-semibold rounded-md text-msit-dark bg-msit-accent hover:bg-msit-accent-500 disabled:opacity-50 transition-colors font-sans"
      >
        {{ syncing ? 'Syncing...' : 'Sync from Notion' }}
      </button>
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

    <div v-if="loading" class="text-center py-12">
      <div class="inline-block animate-spin rounded-full h-8 w-8 border-b-2 border-msit-accent"></div>
    </div>

    <div v-else-if="materials.length === 0" class="text-center py-12">
      <p class="text-msit-dark-200 font-sans">No materials found. Click "Sync from Notion" to import materials.</p>
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

