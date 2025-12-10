<template>
  <div class="px-4 py-6 sm:px-0">
    <h1 class="text-3xl font-bold text-gray-900 mb-6">Dashboard</h1>

    <div v-if="loading" class="text-center py-12">
      <div class="inline-block animate-spin rounded-full h-8 w-8 border-b-2 border-indigo-600"></div>
    </div>

    <div v-else-if="error" class="rounded-md bg-red-50 p-4 mb-4">
      <div class="text-sm text-red-800">{{ error }}</div>
    </div>

    <div v-else-if="stats">
      <!-- Stats Cards -->
      <div class="grid grid-cols-1 gap-5 sm:grid-cols-2 lg:grid-cols-4 mb-8">
        <div class="bg-white overflow-hidden shadow rounded-lg">
          <div class="p-5">
            <div class="flex items-center">
              <div class="flex-shrink-0">
                <svg class="h-6 w-6 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5c1.747 0 3.332.477 4.5 1.253v13C19.832 18.477 18.247 18 16.5 18c-1.746 0-3.332.477-4.5 1.253" />
                </svg>
              </div>
              <div class="ml-5 w-0 flex-1">
                <dl>
                  <dt class="text-sm font-medium text-gray-500 truncate">Total Materials</dt>
                  <dd class="text-lg font-medium text-gray-900">{{ stats.total_materials }}</dd>
                </dl>
              </div>
            </div>
          </div>
        </div>

        <div class="bg-white overflow-hidden shadow rounded-lg">
          <div class="p-5">
            <div class="flex items-center">
              <div class="flex-shrink-0">
                <svg class="h-6 w-6 text-green-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
              </div>
              <div class="ml-5 w-0 flex-1">
                <dl>
                  <dt class="text-sm font-medium text-gray-500 truncate">Completed</dt>
                  <dd class="text-lg font-medium text-gray-900">{{ stats.completed_materials }}</dd>
                </dl>
              </div>
            </div>
          </div>
        </div>

        <div class="bg-white overflow-hidden shadow rounded-lg">
          <div class="p-5">
            <div class="flex items-center">
              <div class="flex-shrink-0">
                <svg class="h-6 w-6 text-blue-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
              </div>
              <div class="ml-5 w-0 flex-1">
                <dl>
                  <dt class="text-sm font-medium text-gray-500 truncate">In Progress</dt>
                  <dd class="text-lg font-medium text-gray-900">{{ stats.in_progress_materials }}</dd>
                </dl>
              </div>
            </div>
          </div>
        </div>

        <div class="bg-white overflow-hidden shadow rounded-lg">
          <div class="p-5">
            <div class="flex items-center">
              <div class="flex-shrink-0">
                <svg class="h-6 w-6 text-yellow-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 5a2 2 0 012-2h10a2 2 0 012 2v16l-7-3.5L5 21V5z" />
                </svg>
              </div>
              <div class="ml-5 w-0 flex-1">
                <dl>
                  <dt class="text-sm font-medium text-gray-500 truncate">Bookmarks</dt>
                  <dd class="text-lg font-medium text-gray-900">{{ stats.bookmarks_count }}</dd>
                </dl>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Progress Bar -->
      <div class="bg-white shadow rounded-lg p-6 mb-8">
        <h2 class="text-lg font-semibold text-gray-900 mb-4">Overall Progress</h2>
        <div class="flex items-center">
          <div class="flex-1">
            <div class="bg-gray-200 rounded-full h-4">
              <div
                class="bg-indigo-600 h-4 rounded-full transition-all duration-300"
                :style="{ width: `${stats.completion_rate}%` }"
              ></div>
            </div>
          </div>
          <span class="ml-4 text-sm font-medium text-gray-700">{{ stats.completion_rate }}%</span>
        </div>
      </div>

      <!-- Recent Activity -->
      <div class="bg-white shadow rounded-lg overflow-hidden">
        <div class="px-6 py-4 border-b border-gray-200">
          <h2 class="text-lg font-semibold text-gray-900">Recent Activity</h2>
        </div>
        <div v-if="stats.recent_activity.length === 0" class="px-6 py-4 text-center text-gray-500">
          No recent activity
        </div>
        <ul v-else class="divide-y divide-gray-200">
          <li
            v-for="activity in stats.recent_activity"
            :key="activity.id"
            class="px-6 py-4 hover:bg-gray-50 cursor-pointer"
            @click="$router.push(`/materials/${activity.id}`)"
          >
            <div class="flex items-center justify-between">
              <div class="flex-1">
                <p class="text-sm font-medium text-gray-900">{{ activity.title }}</p>
                <p v-if="activity.category" class="text-sm text-gray-500">{{ activity.category }}</p>
              </div>
              <div class="flex items-center gap-4">
                <div class="text-right">
                  <p class="text-sm font-medium text-gray-900">
                    {{ activity.is_completed ? 'Completed' : `${activity.progress_percentage}%` }}
                  </p>
                  <p class="text-xs text-gray-500">
                    {{ formatDate(activity.last_accessed_at) }}
                  </p>
                </div>
                <svg class="h-5 w-5 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7" />
                </svg>
              </div>
            </div>
          </li>
        </ul>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'

const stats = ref<any>(null)
const loading = ref(true)
const error = ref('')

const formatDate = (dateString: string) => {
  if (!dateString) return ''
  const date = new Date(dateString)
  const now = new Date()
  const diffMs = now.getTime() - date.getTime()
  const diffMins = Math.floor(diffMs / 60000)
  const diffHours = Math.floor(diffMs / 3600000)
  const diffDays = Math.floor(diffMs / 86400000)

  if (diffMins < 1) return 'Just now'
  if (diffMins < 60) return `${diffMins} minute${diffMins > 1 ? 's' : ''} ago`
  if (diffHours < 24) return `${diffHours} hour${diffHours > 1 ? 's' : ''} ago`
  if (diffDays < 7) return `${diffDays} day${diffDays > 1 ? 's' : ''} ago`
  return date.toLocaleDateString()
}

const loadStats = async () => {
  loading.value = true
  try {
    const response = await fetch('/api/dashboard/stats', {
      credentials: 'include'
    })
    if (response.ok) {
      stats.value = await response.json()
    } else {
      error.value = 'Failed to load dashboard stats'
    }
  } catch (e) {
    error.value = 'An error occurred'
  } finally {
    loading.value = false
  }
}

onMounted(loadStats)
</script>
