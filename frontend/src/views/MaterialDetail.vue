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
          <div class="flex items-center gap-2">
            <button
              @click="toggleBookmark"
              class="p-2 text-gray-400 hover:text-yellow-500 transition-colors"
              :class="{ 'text-yellow-500': material.is_bookmarked }"
              title="Bookmark"
            >
              <svg class="h-6 w-6" fill="currentColor" viewBox="0 0 20 20">
                <path d="M5 4a2 2 0 012-2h6a2 2 0 012 2v14l-5-2.5L5 18V4z" />
              </svg>
            </button>
            <span v-if="material.category" class="inline-flex items-center px-3 py-1 rounded-full text-sm font-medium bg-indigo-100 text-indigo-800">
              {{ material.category }}
            </span>
          </div>
        </div>
        
        <!-- Progress Section -->
        <div class="mt-4 p-4 bg-gray-50 rounded-lg">
          <div class="flex items-center justify-between mb-2">
            <span class="text-sm font-medium text-gray-700">Progress</span>
            <span class="text-sm text-gray-600">{{ material.progress.progress_percentage }}%</span>
          </div>
          <div class="bg-gray-200 rounded-full h-2 mb-3">
            <div
              class="bg-indigo-600 h-2 rounded-full transition-all duration-300"
              :style="{ width: `${material.progress.progress_percentage}%` }"
            ></div>
          </div>
          <div class="flex gap-2">
            <button
              @click="updateProgress(25)"
              class="px-3 py-1 text-xs font-medium rounded-md border border-gray-300 bg-white text-gray-700 hover:bg-gray-50"
            >
              25%
            </button>
            <button
              @click="updateProgress(50)"
              class="px-3 py-1 text-xs font-medium rounded-md border border-gray-300 bg-white text-gray-700 hover:bg-gray-50"
            >
              50%
            </button>
            <button
              @click="updateProgress(75)"
              class="px-3 py-1 text-xs font-medium rounded-md border border-gray-300 bg-white text-gray-700 hover:bg-gray-50"
            >
              75%
            </button>
            <button
              @click="markCompleted"
              class="px-3 py-1 text-xs font-medium rounded-md border border-green-300 bg-green-50 text-green-700 hover:bg-green-100"
              :class="{ 'bg-green-100 border-green-400': material.progress.is_completed }"
            >
              {{ material.progress.is_completed ? '✓ Completed' : 'Mark Complete' }}
            </button>
          </div>
        </div>
      </div>
      <div class="px-6 py-4">
        <div class="prose max-w-none" v-html="formatContent(material.content)"></div>
        <div v-if="material.notion_url" class="mt-6">
          <a
            :href="material.notion_url"
            target="_blank"
            class="inline-flex items-center px-4 py-2 border border-gray-300 shadow-sm text-sm font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50"
          >
            View in Notion
          </a>
        </div>
      </div>
      <div class="px-6 py-4 border-t border-gray-200 flex justify-between items-center">
        <router-link
          to="/materials"
          class="text-indigo-600 hover:text-indigo-500 font-medium"
        >
          ← Back to Materials
        </router-link>
        <div v-if="material.progress.is_completed" class="flex items-center text-green-600">
          <svg class="h-5 w-5 mr-1" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
          </svg>
          <span class="text-sm font-medium">Completed</span>
        </div>
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
    } else {
      error.value = 'Material not found'
    }
  } catch (e) {
    error.value = 'An error occurred'
  } finally {
    loading.value = false
  }
}

const updateProgress = async (percentage: number) => {
  try {
    const response = await fetch(`/api/progress/${route.params.id}`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      credentials: 'include',
      body: JSON.stringify({ progress_percentage: percentage })
    })
    if (response.ok) {
      const data = await response.json()
      material.value.progress = data.progress
    }
  } catch (e) {
    error.value = 'Failed to update progress'
  }
}

const markCompleted = async () => {
  try {
    const isCompleted = !material.value.progress.is_completed
    const response = await fetch(`/api/progress/${route.params.id}`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      credentials: 'include',
      body: JSON.stringify({ is_completed: isCompleted })
    })
    if (response.ok) {
      const data = await response.json()
      material.value.progress = data.progress
    }
  } catch (e) {
    error.value = 'Failed to update progress'
  }
}

const toggleBookmark = async () => {
  try {
    if (material.value.is_bookmarked) {
      await fetch(`/api/bookmarks/${route.params.id}`, {
        method: 'DELETE',
        credentials: 'include'
      })
      material.value.is_bookmarked = false
    } else {
      await fetch(`/api/bookmarks/${route.params.id}`, {
        method: 'POST',
        credentials: 'include'
      })
      material.value.is_bookmarked = true
    }
  } catch (e) {
    error.value = 'Failed to update bookmark'
  }
}

onMounted(loadMaterial)
</script>

