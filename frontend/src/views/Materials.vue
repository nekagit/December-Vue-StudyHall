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
        @click="$router.push(`/materials/${material.id}`)"
        class="bg-white overflow-hidden shadow rounded-lg hover:shadow-lg transition-shadow cursor-pointer"
      >
        <div class="p-6">
          <div class="flex items-center justify-between">
            <h3 class="text-lg font-medium text-gray-900">{{ material.title }}</h3>
            <span v-if="material.category" class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-indigo-100 text-indigo-800">
              {{ material.category }}
            </span>
          </div>
          <p v-if="material.content" class="mt-2 text-sm text-gray-500 line-clamp-3">
            {{ material.content.substring(0, 150) }}...
          </p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'

const materials = ref<any[]>([])
const loading = ref(true)
const error = ref('')
const success = ref('')
const syncing = ref(false)

const loadMaterials = async () => {
  loading.value = true
  try {
    const response = await fetch('/api/materials', {
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

onMounted(loadMaterials)
</script>

