<template>
  <div class="px-4 py-6 sm:px-0">
    <div class="flex justify-between items-center mb-6">
      <h1 class="text-3xl font-bold text-gray-900">Study Sessions</h1>
      <select
        v-model="daysFilter"
        @change="loadSessions"
        class="block rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm px-3 py-2 border"
      >
        <option :value="7">Last 7 days</option>
        <option :value="30">Last 30 days</option>
        <option :value="90">Last 90 days</option>
        <option :value="365">Last year</option>
      </select>
    </div>

    <div v-if="loading" class="text-center py-12">
      <div class="inline-block animate-spin rounded-full h-8 w-8 border-b-2 border-indigo-600"></div>
    </div>

    <div v-else-if="error" class="rounded-md bg-red-50 p-4 mb-4">
      <div class="text-sm text-red-800">{{ error }}</div>
    </div>

    <div v-else>
      <!-- Summary Stats -->
      <div class="grid grid-cols-1 gap-5 sm:grid-cols-3 mb-8">
        <div class="bg-white overflow-hidden shadow rounded-lg">
          <div class="p-5">
            <div class="flex items-center">
              <div class="flex-shrink-0">
                <svg class="h-6 w-6 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
              </div>
              <div class="ml-5 w-0 flex-1">
                <dl>
                  <dt class="text-sm font-medium text-gray-500 truncate">Total Sessions</dt>
                  <dd class="text-lg font-medium text-gray-900">{{ summary.total_sessions }}</dd>
                </dl>
              </div>
            </div>
          </div>
        </div>

        <div class="bg-white overflow-hidden shadow rounded-lg">
          <div class="p-5">
            <div class="flex items-center">
              <div class="flex-shrink-0">
                <svg class="h-6 w-6 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
              </div>
              <div class="ml-5 w-0 flex-1">
                <dl>
                  <dt class="text-sm font-medium text-gray-500 truncate">Total Hours</dt>
                  <dd class="text-lg font-medium text-gray-900">{{ summary.total_hours }}</dd>
                </dl>
              </div>
            </div>
          </div>
        </div>

        <div class="bg-white overflow-hidden shadow rounded-lg">
          <div class="p-5">
            <div class="flex items-center">
              <div class="flex-shrink-0">
                <svg class="h-6 w-6 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
                </svg>
              </div>
              <div class="ml-5 w-0 flex-1">
                <dl>
                  <dt class="text-sm font-medium text-gray-500 truncate">Total Minutes</dt>
                  <dd class="text-lg font-medium text-gray-900">{{ summary.total_minutes }}</dd>
                </dl>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Sessions List -->
      <div v-if="sessions.length === 0" class="text-center py-12 bg-white rounded-lg shadow">
        <svg class="mx-auto h-12 w-12 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
        </svg>
        <h3 class="mt-2 text-sm font-medium text-gray-900">No study sessions</h3>
        <p class="mt-1 text-sm text-gray-500">Start studying materials to track your time!</p>
      </div>

      <div v-else class="bg-white shadow rounded-lg overflow-hidden">
        <ul class="divide-y divide-gray-200">
          <li v-for="session in sessions" :key="session.id" class="px-6 py-4 hover:bg-gray-50">
            <div class="flex items-center justify-between">
              <div class="flex-1">
                <div class="flex items-center">
                  <p class="text-sm font-medium text-gray-900">
                    {{ session.material ? session.material.title : 'General Study' }}
                  </p>
                </div>
                <div class="mt-2 flex items-center text-sm text-gray-500">
                  <svg class="flex-shrink-0 mr-1.5 h-5 w-5 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
                  </svg>
                  {{ formatDuration(session.duration_minutes) }}
                  <span class="mx-2">•</span>
                  {{ formatDate(session.started_at) }}
                </div>
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

const sessions = ref<any[]>([])
const summary = ref({
  total_sessions: 0,
  total_minutes: 0,
  total_hours: 0
})
const loading = ref(true)
const error = ref('')
const daysFilter = ref(30)

const formatDuration = (minutes: number) => {
  const hrs = Math.floor(minutes / 60)
  const mins = Math.round(minutes % 60)
  if (hrs > 0) {
    return `${hrs}h ${mins}m`
  }
  return `${mins}m`
}

const formatDate = (dateString: string) => {
  if (!dateString) return ''
  const date = new Date(dateString)
  return date.toLocaleDateString('en-US', { 
    year: 'numeric', 
    month: 'short', 
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  })
}

const loadSessions = async () => {
  loading.value = true
  try {
    const response = await fetch(`/api/study-sessions?days=${daysFilter.value}`, {
      credentials: 'include'
    })
    if (response.ok) {
      const data = await response.json()
      sessions.value = data.sessions || []
      summary.value = {
        total_sessions: data.sessions?.length || 0,
        total_minutes: Math.round(data.total_minutes || 0),
        total_hours: data.total_hours || 0
      }
    } else {
      error.value = 'Failed to load study sessions'
    }
  } catch (e) {
    error.value = 'An error occurred'
  } finally {
    loading.value = false
  }
}

onMounted(loadSessions)
</script>
