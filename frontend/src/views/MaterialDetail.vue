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
        <div class="flex items-center justify-between">
          <h1 class="text-3xl font-bold text-gray-900">{{ material.title }}</h1>
          <span v-if="material.category" class="inline-flex items-center px-3 py-1 rounded-full text-sm font-medium bg-indigo-100 text-indigo-800">
            {{ material.category }}
          </span>
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

onMounted(loadMaterial)
</script>

