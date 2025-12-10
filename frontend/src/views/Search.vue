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

    // Search snippets (from local data)
    if (activeFilters.value.includes('snippets')) {
      const snippets = [
        { id: 1, name: 'Hello World', category: 'Basics', description: 'Basic print statement', code: 'print("Hello, World!")' },
        { id: 2, name: 'Variables and Types', category: 'Basics', description: 'Variable assignment and type checking' },
        { id: 3, name: 'Lists Operations', category: 'Data Structures', description: 'Common list operations' },
        { id: 4, name: 'List Methods', category: 'Data Structures', description: 'Adding, removing, and modifying list elements' },
        { id: 5, name: 'For Loops', category: 'Control Flow', description: 'Iterating with for loops' },
        { id: 6, name: 'While Loops', category: 'Control Flow', description: 'Conditional iteration' },
        { id: 7, name: 'If-Else Statements', category: 'Control Flow', description: 'Conditional logic' },
        { id: 8, name: 'Functions', category: 'Functions', description: 'Define and call functions' },
        { id: 9, name: 'Lambda Functions', category: 'Functions', description: 'Anonymous functions' },
        { id: 10, name: 'Dictionaries', category: 'Data Structures', description: 'Key-value pairs' }
      ]

      snippets.forEach(s => {
        if (s.name.toLowerCase().includes(query) || s.description.toLowerCase().includes(query) || s.category.toLowerCase().includes(query)) {
          searchResults.push({
            id: s.id,
            title: s.name,
            description: s.description,
            type: 'snippets',
            category: s.category,
            route: '/snippets'
          })
        }
      })
    }

    // Search problems (from local data)
    if (activeFilters.value.includes('problems')) {
      const problems = [
        { id: 1, title: 'Sum of Two Numbers', difficulty: 'beginner', category: 'Basics', description: 'Write a function that takes two numbers as arguments and returns their sum.' },
        { id: 2, title: 'Find Maximum in List', difficulty: 'beginner', category: 'Data Structures', description: 'Write a function that finds the maximum value in a list without using the built-in max() function.' },
        { id: 3, title: 'Reverse a String', difficulty: 'beginner', category: 'Strings', description: 'Write a function that reverses a string without using the built-in reversed() function or slicing.' },
        { id: 4, title: 'Count Vowels', difficulty: 'beginner', category: 'Strings', description: 'Write a function that counts the number of vowels (a, e, i, o, u) in a string.' },
        { id: 5, title: 'Factorial', difficulty: 'intermediate', category: 'Recursion', description: 'Write a function that calculates the factorial of a number using recursion.' },
        { id: 6, title: 'Check Palindrome', difficulty: 'intermediate', category: 'Strings', description: 'Write a function that checks if a string is a palindrome (reads the same forwards and backwards).' }
      ]

      problems.forEach(p => {
        if (p.title.toLowerCase().includes(query) || p.description.toLowerCase().includes(query) || p.category.toLowerCase().includes(query)) {
          searchResults.push({
            id: p.id,
            title: p.title,
            description: p.description,
            type: 'problems',
            category: p.category,
            route: '/practice-problems'
          })
        }
      })
    }

    // Search resources (from local data)
    if (activeFilters.value.includes('resources')) {
      const resources = [
        { id: 1, title: 'Python Official Documentation', category: 'Documentation', description: 'Comprehensive official documentation for Python programming language.' },
        { id: 2, title: 'Real Python', category: 'Tutorials', description: 'High-quality Python tutorials, articles, and courses for developers of all skill levels.' },
        { id: 3, title: 'Python.org Tutorial', category: 'Tutorials', description: 'Official Python tutorial covering basics to advanced topics. Perfect for beginners.' },
        { id: 4, title: 'LeetCode', category: 'Practice', description: 'Practice coding problems and improve your problem-solving skills with Python.' }
      ]

      resources.forEach(r => {
        if (r.title.toLowerCase().includes(query) || r.description.toLowerCase().includes(query) || r.category.toLowerCase().includes(query)) {
          searchResults.push({
            id: r.id,
            title: r.title,
            description: r.description,
            type: 'resources',
            category: r.category,
            route: '/resources'
          })
        }
      })
    }

    // Search cheat sheets (from local data)
    if (activeFilters.value.includes('cheatsheets')) {
      const sheets = [
        { id: 1, title: 'Python Basics', description: 'Essential Python syntax and operations' },
        { id: 2, title: 'Strings', description: 'String operations and methods' },
        { id: 3, title: 'Lists', description: 'List operations and methods' },
        { id: 4, title: 'Dictionaries', description: 'Dictionary operations and methods' },
        { id: 5, title: 'Control Flow', description: 'If statements, loops, and control structures' },
        { id: 6, title: 'Functions', description: 'Function definition and usage' }
      ]

      sheets.forEach(s => {
        if (s.title.toLowerCase().includes(query) || s.description.toLowerCase().includes(query)) {
          searchResults.push({
            id: s.id,
            title: s.title,
            description: s.description,
            type: 'cheatsheets',
            category: 'Reference',
            route: '/cheat-sheets'
          })
        }
      })
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
