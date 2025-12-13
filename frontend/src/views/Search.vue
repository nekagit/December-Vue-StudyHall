<template>
  <div class="px-4 py-4 sm:py-6 sm:px-0">
    <div class="mb-6 sm:mb-8">
      <h1 class="text-2xl sm:text-3xl font-bold text-msit-dark-50 mb-2 font-serif">Global Search</h1>
      <p class="text-sm sm:text-base text-msit-dark-200 font-sans">Search across all content: materials, snippets, problems, and resources</p>
    </div>

    <!-- Search Input -->
    <div class="mb-6 bg-msit-dark-800 p-4 sm:p-6 rounded-lg shadow border border-msit-dark-700">
      <div class="relative">
        <input
          v-model="searchQuery"
          @input="performSearch"
          type="text"
          placeholder="Search everything..."
          class="block w-full rounded-md border-msit-dark-600 bg-msit-dark-700 text-msit-dark-50 placeholder-msit-dark-300 shadow-sm focus:border-msit-accent focus:ring-msit-accent text-sm sm:text-base px-4 py-3 pl-10 border font-sans"
        />
        <svg
          class="absolute left-3 top-3.5 h-5 w-5 text-msit-dark-300"
          fill="none"
          viewBox="0 0 24 24"
          stroke="currentColor"
        >
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
        </svg>
      </div>
      
      <!-- Filter Tabs -->
      <div class="mt-4 flex flex-wrap gap-2">
        <button
          v-for="filter in filters"
          :key="filter"
          @click="toggleFilter(filter)"
          :class="[
            'px-3 py-1 rounded-md text-sm font-medium transition-colors font-sans',
            activeFilters.includes(filter)
              ? 'bg-msit-accent text-msit-dark'
              : 'bg-msit-dark-700 text-msit-dark-200 border border-msit-dark-600 hover:border-msit-accent'
          ]"
        >
          {{ filter }}
        </button>
      </div>
    </div>

    <!-- Results -->
    <div v-if="searchQuery && results.length === 0 && !loading" class="text-center py-12">
      <p class="text-msit-dark-200 font-sans">No results found</p>
    </div>

    <div v-if="loading" class="text-center py-12">
      <div class="inline-block animate-spin rounded-full h-8 w-8 border-b-2 border-msit-accent"></div>
    </div>

    <div v-if="results.length > 0" class="space-y-4">
      <!-- Group by type -->
      <div v-for="type in resultTypes" :key="type">
        <div v-if="getResultsByType(type).length > 0" class="mb-6">
          <h2 class="text-xl font-semibold text-msit-dark-50 mb-4 font-sans capitalize">{{ type }}</h2>
          <div class="grid grid-cols-1 gap-4 sm:gap-6 lg:grid-cols-2">
            <div
              v-for="result in getResultsByType(type)"
              :key="result.id"
              class="bg-msit-dark-800 overflow-hidden shadow rounded-lg hover:shadow-lg transition-shadow border border-msit-dark-700 hover:border-msit-accent cursor-pointer"
              @click="navigateToResult(result)"
            >
              <div class="p-4 sm:p-6">
                <div class="flex items-start justify-between mb-2">
                  <h3 class="text-lg font-semibold text-msit-dark-50 font-sans">{{ result.title }}</h3>
                  <span class="inline-flex items-center px-2 py-0.5 rounded text-xs font-medium bg-msit-accent/20 text-msit-accent font-sans">
                    {{ result.type }}
                  </span>
                </div>
                <p class="text-sm text-msit-dark-200 mb-2 font-sans line-clamp-2">{{ result.description }}</p>
                <div class="text-xs text-msit-dark-300 font-sans">
                  {{ result.category || 'General' }}
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Empty State -->
    <div v-if="!searchQuery" class="text-center py-12">
      <svg
        class="mx-auto h-12 w-12 text-msit-dark-400"
        fill="none"
        viewBox="0 0 24 24"
        stroke="currentColor"
      >
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
      </svg>
      <p class="mt-4 text-msit-dark-200 font-sans">Enter a search query to find content across the platform</p>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()
const searchQuery = ref('')
const activeFilters = ref<string[]>(['materials', 'snippets', 'problems', 'resources'])
const loading = ref(false)
const results = ref<any[]>([])

const filters = ['materials', 'snippets', 'problems', 'resources', 'cheatsheets']

const toggleFilter = (filter: string) => {
  const index = activeFilters.value.indexOf(filter)
  if (index > -1) {
    activeFilters.value.splice(index, 1)
  } else {
    activeFilters.value.push(filter)
  }
  if (searchQuery.value) {
    performSearch()
  }
}

const resultTypes = computed(() => {
  const types = new Set(results.value.map(r => r.type))
  return Array.from(types)
})

const getResultsByType = (type: string) => {
  return results.value.filter(r => r.type === type)
}

const performSearch = async () => {
  if (!searchQuery.value.trim()) {
    results.value = []
    return
  }

  loading.value = true
  results.value = []

  try {
    const query = searchQuery.value.toLowerCase()
    const searchResults: any[] = []

    // Search materials
    if (activeFilters.value.includes('materials')) {
      try {
        const response = await fetch(`/api/materials?search=${encodeURIComponent(searchQuery.value)}`, {
          credentials: 'include'
        })
        if (response.ok) {
          const materials = await response.json()
          materials.forEach((m: any) => {
            searchResults.push({
              id: m.id,
              title: m.title,
              description: m.content?.substring(0, 200) || '',
              type: 'materials',
              category: m.category,
              route: `/materials/${m.id}`
            })
          })
        }
      } catch (e) {
        // Ignore errors
      }
    }

    // Search snippets from API
    if (activeFilters.value.includes('snippets')) {
      try {
        const response = await fetch(`/api/snippets?search=${encodeURIComponent(searchQuery.value)}`, {
          credentials: 'include'
        })
        if (response.ok) {
          const snippets = await response.json()
          snippets.forEach((s: any) => {
            searchResults.push({
              id: s.id,
              title: s.name,
              description: s.description,
              type: 'snippets',
              category: s.category,
              route: '/snippets'
            })
          })
        }
      } catch (e) {
        console.error('Error fetching snippets:', e)
      }
    }

    // Search problems (from API)
    if (activeFilters.value.includes('problems')) {
      try {
        const response = await fetch(`/api/problems?search=${encodeURIComponent(searchQuery.value)}`, {
          credentials: 'include'
        })
        if (response.ok) {
          const problems = await response.json()
          problems.forEach((p: any) => {
            searchResults.push({
              id: p.id,
              title: p.title,
              description: p.description || p.fullDescription || '',
              type: 'problems',
              category: p.category || p.difficulty || 'General',
              route: '/practice-problems'
            })
          })
        }
      } catch (e) {
        // Ignore errors, continue with other searches
        console.error('Error fetching problems:', e)
      }
    }

    // Search resources from API
    if (activeFilters.value.includes('resources')) {
      try {
        const response = await fetch(`/api/resources?search=${encodeURIComponent(searchQuery.value)}`, {
          credentials: 'include'
        })
        if (response.ok) {
          const resources = await response.json()
          resources.forEach((r: any) => {
            searchResults.push({
              id: r.id,
              title: r.title,
              description: r.description,
              type: 'resources',
              category: r.category,
              route: '/resources'
            })
          })
        }
      } catch (e) {
        console.error('Error fetching resources:', e)
      }
    }

    // Search cheat sheets from API
    if (activeFilters.value.includes('cheatsheets')) {
      try {
        const response = await fetch(`/api/cheat-sheets?search=${encodeURIComponent(searchQuery.value)}`, {
          credentials: 'include'
        })
        if (response.ok) {
          const sheets = await response.json()
          sheets.forEach((s: any) => {
            searchResults.push({
              id: s.id,
              title: s.title,
              description: s.description,
              type: 'cheatsheets',
              category: 'Reference',
              route: '/cheat-sheets'
            })
          })
        }
      } catch (e) {
        console.error('Error fetching cheat sheets:', e)
      }
    }

    results.value = searchResults
  } catch (e) {
    console.error('Search error:', e)
  } finally {
    loading.value = false
  }
}

const navigateToResult = (result: any) => {
  if (result.route) {
    router.push(result.route)
  }
}

onMounted(() => {
  // Focus search input on mount
  const input = document.querySelector('input[type="text"]') as HTMLInputElement
  if (input) {
    input.focus()
  }
})
</script>
