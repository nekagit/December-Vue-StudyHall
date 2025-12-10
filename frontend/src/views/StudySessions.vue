<template>
  <div class="px-4 py-6 sm:px-0">
    <div class="mb-8">
      <h1 class="text-3xl font-bold text-gray-900 mb-2">Study Sessions</h1>
      <p class="text-gray-600">Track your study time and build consistency</p>
    </div>

    <!-- Active Session Timer -->
    <div v-if="activeSession" class="bg-white shadow rounded-lg p-6 mb-8">
      <h2 class="text-xl font-semibold text-gray-900 mb-4">Active Session</h2>
      <div class="text-center">
        <div class="text-5xl font-mono font-bold text-indigo-600 mb-4">
          {{ formatTime(elapsedTime) }}
        </div>
        <div class="flex justify-center space-x-4">
          <button
            @click="stopSession"
            class="inline-flex items-center px-6 py-3 border border-transparent text-base font-medium rounded-md text-white bg-red-600 hover:bg-red-700"
          >
            Stop Session
          </button>
        </div>
        <div v-if="activeSession.material" class="mt-4 text-sm text-gray-600">
          Studying: {{ activeSession.material.title }}
        </div>
      </div>
    </div>

    <!-- Start New Session -->
    <div v-else class="bg-white shadow rounded-lg p-6 mb-8">
      <h2 class="text-xl font-semibold text-gray-900 mb-4">Start New Session</h2>
      <form @submit.prevent="startSession" class="space-y-4">
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-2">
            Material (Optional)
          </label>
          <select
            v-model="newSession.material_id"
            class="block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500"
          >
            <option :value="null">General Study</option>
            <option v-for="material in materials" :key="material.id" :value="material.id">
              {{ material.title }}
            </option>
          </select>
        </div>
        <button
          type="submit"
          class="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md text-white bg-indigo-600 hover:bg-indigo-700"
        >
          Start Session
        </button>
      </form>
    </div>

    <!-- Sessions List -->
    <div v-if="loading" class="text-center py-12">
      <div class="inline-block animate-spin rounded-full h-8 w-8 border-b-2 border-indigo-600"></div>
    </div>

    <div v-else-if="error" class="rounded-md bg-red-50 p-4 mb-4">
      <div class="text-sm text-red-800">{{ error }}</div>
    </div>

    <div v-else>
      <div class="mb-4 flex items-center justify-between">
        <h2 class="text-xl font-semibold text-gray-900">Session History</h2>
        <div class="text-sm text-gray-600">
          Total: {{ totalMinutes }} minutes
        </div>
      </div>

      <div v-if="sessions.length === 0" class="text-center py-12 text-gray-500">
        No study sessions yet. Start your first session above!
      </div>

      <div v-else class="space-y-4">
        <div
          v-for="session in sessions"
          :key="session.id"
          class="bg-white shadow rounded-lg p-6"
        >
          <div class="flex items-start justify-between">
            <div class="flex-1">
              <h3 class="text-lg font-medium text-gray-900">
                {{ session.material ? session.material.title : 'General Study' }}
              </h3>
              <p v-if="session.material && session.material.category" class="text-sm text-gray-500 mt-1">
                {{ session.material.category }}
              </p>
              <div class="mt-2 flex items-center text-sm text-gray-600 space-x-4">
                <span>
                  <svg class="w-4 h-4 inline mr-1" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
                  </svg>
                  {{ Math.round(session.duration_minutes) }} minutes
                </span>
                <span>
                  <svg class="w-4 h-4 inline mr-1" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
                  </svg>
                  {{ formatDate(session.started_at) }}
                </span>
              </div>
              <p v-if="session.notes" class="mt-2 text-sm text-gray-700">
                {{ session.notes }}
              </p>
            </div>
            <button
              @click="deleteSession(session.id)"
              class="ml-4 text-red-600 hover:text-red-800"
            >
              <svg class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
              </svg>
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, onUnmounted } from 'vue'

const sessions = ref<any[]>([])
const materials = ref<any[]>([])
const loading = ref(true)
const error = ref('')
const activeSession = ref<any>(null)
const elapsedTime = ref(0)
const timerInterval = ref<any>(null)
const newSession = ref({
  material_id: null as number | null
})

const formatDate = (dateString: string): string => {
  const date = new Date(dateString)
  return date.toLocaleDateString() + ' ' + date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
}

const formatTime = (seconds: number): string => {
  const hours = Math.floor(seconds / 3600)
  const minutes = Math.floor((seconds % 3600) / 60)
  const secs = seconds % 60
  return `${hours.toString().padStart(2, '0')}:${minutes.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')}`
}

const loadSessions = async () => {
  loading.value = true
  try {
    const response = await fetch('/api/sessions', {
      credentials: 'include'
    })
    if (response.ok) {
      sessions.value = await response.json()
    } else {
      error.value = 'Failed to load sessions'
    }
  } catch (e) {
    error.value = 'An error occurred'
  } finally {
    loading.value = false
  }
}

const loadMaterials = async () => {
  try {
    const response = await fetch('/api/materials', {
      credentials: 'include'
    })
    if (response.ok) {
      materials.value = await response.json()
    }
  } catch (e) {
    // Ignore errors
  }
}

const startSession = async () => {
  try {
    const response = await fetch('/api/sessions', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      credentials: 'include',
      body: JSON.stringify({
        material_id: newSession.value.material_id || null,
        started_at: new Date().toISOString(),
        duration_minutes: 0
      })
    })

    if (response.ok) {
      const data = await response.json()
      activeSession.value = data.session || data
      elapsedTime.value = 0
      newSession.value.material_id = null
      
      // Start timer
      timerInterval.value = setInterval(() => {
        elapsedTime.value += 1
      }, 1000)
      
      loadSessions()
    } else {
      const errorData = await response.json()
      error.value = errorData.error || 'Failed to start session'
    }
  } catch (e) {
    error.value = 'An error occurred while starting the session'
  }
}

const stopSession = async () => {
  if (!activeSession.value) return

  try {
    const durationMinutes = elapsedTime.value / 60
    
    const response = await fetch(`/api/sessions/${activeSession.value.id}`, {
      method: 'PUT',
      headers: { 'Content-Type': 'application/json' },
      credentials: 'include',
      body: JSON.stringify({
        duration_minutes: durationMinutes,
        ended_at: new Date().toISOString()
      })
    })

    if (response.ok) {
      if (timerInterval.value) {
        clearInterval(timerInterval.value)
        timerInterval.value = null
      }
      activeSession.value = null
      elapsedTime.value = 0
      loadSessions()
    } else {
      error.value = 'Failed to stop session'
    }
  } catch (e) {
    error.value = 'An error occurred while stopping the session'
  }
}

const deleteSession = async (sessionId: number) => {
  if (!confirm('Are you sure you want to delete this session?')) return

  try {
    const response = await fetch(`/api/sessions/${sessionId}`, {
      method: 'DELETE',
      credentials: 'include'
    })

    if (response.ok) {
      loadSessions()
    } else {
      error.value = 'Failed to delete session'
    }
  } catch (e) {
    error.value = 'An error occurred'
  }
}

const totalMinutes = computed(() => {
  return sessions.value.reduce((sum, s) => sum + (s.duration_minutes || 0), 0)
})

onMounted(() => {
  loadSessions()
  loadMaterials()
})

onUnmounted(() => {
  if (timerInterval.value) {
    clearInterval(timerInterval.value)
  }
})
</script>
