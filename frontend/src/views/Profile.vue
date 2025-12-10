<template>
  <div class="px-4 py-6 sm:px-0">
    <h1 class="text-3xl font-bold text-gray-900 mb-6">Profile</h1>

    <div v-if="loading" class="text-center py-12">
      <div class="inline-block animate-spin rounded-full h-8 w-8 border-b-2 border-indigo-600"></div>
    </div>

    <div v-else-if="error" class="rounded-md bg-red-50 p-4 mb-4">
      <div class="text-sm text-red-800">{{ error }}</div>
    </div>

    <div v-else-if="character" class="max-w-3xl">
      <div class="bg-white shadow rounded-lg">
        <div class="px-6 py-4 border-b border-gray-200">
          <h2 class="text-lg font-medium text-gray-900">Character Information</h2>
        </div>
        <div class="px-6 py-4">
          <dl class="grid grid-cols-1 gap-x-4 gap-y-6 sm:grid-cols-2">
            <div>
              <dt class="text-sm font-medium text-gray-500">Name</dt>
              <dd class="mt-1 text-sm text-gray-900">{{ character.name }}</dd>
            </div>
            <div>
              <dt class="text-sm font-medium text-gray-500">Role</dt>
              <dd class="mt-1 text-sm text-gray-900">{{ character.role || 'student' }}</dd>
            </div>
            <div>
              <dt class="text-sm font-medium text-gray-500">Character ID</dt>
              <dd class="mt-1 text-sm text-gray-900">{{ character.id }}</dd>
            </div>
          </dl>
        </div>
      </div>

      <!-- Progress Summary -->
      <div class="mt-6 bg-white shadow rounded-lg">
        <div class="px-6 py-4 border-b border-gray-200">
          <h2 class="text-lg font-medium text-gray-900">Learning Progress</h2>
        </div>
        <div class="px-6 py-4">
          <div v-if="progressLoading" class="text-center py-4">
            <div class="inline-block animate-spin rounded-full h-6 w-6 border-b-2 border-indigo-600"></div>
          </div>
          <div v-else-if="progressError" class="text-sm text-red-600">{{ progressError }}</div>
          <div v-else>
            <div class="grid grid-cols-1 gap-4 sm:grid-cols-3">
              <div class="text-center">
                <div class="text-2xl font-bold text-gray-900">{{ progressStats.completed }}</div>
                <div class="text-sm text-gray-500">Completed</div>
              </div>
              <div class="text-center">
                <div class="text-2xl font-bold text-blue-600">{{ progressStats.in_progress }}</div>
                <div class="text-sm text-gray-500">In Progress</div>
              </div>
              <div class="text-center">
                <div class="text-2xl font-bold text-gray-600">{{ progressStats.total }}</div>
                <div class="text-sm text-gray-500">Total Materials</div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'

const character = ref<any>(null)
const loading = ref(true)
const error = ref('')

const progressStats = ref({
  completed: 0,
  in_progress: 0,
  total: 0
})
const progressLoading = ref(false)
const progressError = ref('')

const loadCharacter = () => {
  loading.value = true
  try {
    const stored = localStorage.getItem('character')
    if (stored) {
      character.value = JSON.parse(stored)
      loadProgress()
    } else {
      error.value = 'Character not configured'
    }
  } catch (e) {
    error.value = 'Failed to load character information'
  } finally {
    loading.value = false
  }
}

const loadProgress = async () => {
  progressLoading.value = true
  try {
    const response = await fetch('/api/progress')
    if (response.ok) {
      const progress = await response.json()
      progressStats.value = {
        completed: progress.filter((p: any) => p.status === 'completed').length,
        in_progress: progress.filter((p: any) => p.status === 'in_progress').length,
        total: progress.length
      }
    } else {
      progressError.value = 'Failed to load progress'
    }
  } catch (e) {
    progressError.value = 'An error occurred'
  } finally {
    progressLoading.value = false
  }
}

onMounted(loadCharacter)
</script>
