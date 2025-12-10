<template>
  <div class="px-4 py-6 sm:px-0">
    <div class="mb-8">
      <h1 class="text-3xl font-bold text-gray-900 mb-2">Study Sessions</h1>
      <p class="text-gray-600">Track your study time and build consistency</p>
    </div>

    <!-- Timer Section -->
    <div class="bg-white rounded-lg shadow-lg p-8 mb-8">
      <div class="text-center">
        <div class="mb-6">
          <div class="text-6xl font-mono font-bold text-indigo-600 mb-4">
            {{ formatTime(timerSeconds) }}
          </div>
          <div class="flex justify-center space-x-4">
            <button
              v-if="!timerRunning"
              @click="startTimer"
              class="inline-flex items-center px-6 py-3 border border-transparent text-base font-medium rounded-md text-white bg-indigo-600 hover:bg-indigo-700"
            >
              <svg class="h-5 w-5 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M14.752 11.168l-3.197-2.132A1 1 0 0010 9.87v4.263a1 1 0 001.555.832l3.197-2.132a1 1 0 000-1.664z" />
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
              Start
            </button>
            <button
              v-else
              @click="pauseTimer"
              class="inline-flex items-center px-6 py-3 border border-transparent text-base font-medium rounded-md text-white bg-yellow-600 hover:bg-yellow-700"
            >
              <svg class="h-5 w-5 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 9v6m4-6v6m7-3a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
              Pause
            </button>
            <button
              v-if="timerRunning || timerSeconds > 0"
              @click="stopTimer"
              class="inline-flex items-center px-6 py-3 border border-gray-300 text-base font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50"
            >
              <svg class="h-5 w-5 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 10a1 1 0 011-1h4a1 1 0 011 1v4a1 1 0 01-1 1h-4a1 1 0 01-1-1v-4z" />
              </svg>
              Stop & Save
            </button>
            <button
              v-if="timerSeconds > 0 && !timerRunning"
              @click="resetTimer"
              class="inline-flex items-center px-6 py-3 border border-gray-300 text-base font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50"
            >
              Reset
            </button>
          </div>
        </div>

        <!-- Material Selection -->
        <div class="mb-4">
          <label class="block text-sm font-medium text-gray-700 mb-2">Studying Material (Optional)</label>
          <select
            v-model="selectedMaterialId"
            class="w-full max-w-md mx-auto px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-indigo-500 focus:border-indigo-500"
          >
            <option value="">None</option>
            <option v-for="material in materials" :key="material.id" :value="material.id">
              {{ material.title }}
            </option>
          </select>
        </div>

        <!-- Notes -->
        <div class="mb-4">
          <label class="block text-sm font-medium text-gray-700 mb-2">Session Notes (Optional)</label>
          <textarea
            v-model="sessionNotes"
            rows="3"
            class="w-full max-w-md mx-auto px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-indigo-500 focus:border-indigo-500"
            placeholder="What did you study today?"
          ></textarea>
        </div>
      </div>
    </div>

    <!-- Study Streak -->
    <div class="bg-gradient-to-r from-indigo-500 to-purple-600 rounded-lg shadow-lg p-6 mb-8 text-white">
      <div class="flex items-center justify-between">
        <div>
          <h2 class="text-xl font-bold mb-2">Study Streak</h2>
          <p class="text-indigo-100">Keep your learning momentum going!</p>
        </div>
        <div class="text-right">
          <div class="text-4xl font-bold">{{ streak.current_streak }}</div>
          <div class="text-sm text-indigo-100">days in a row</div>
          <div class="text-sm text-indigo-200 mt-1">Best: {{ streak.longest_streak }} days</div>
        </div>
      </div>
    </div>

    <!-- Session History -->
    <div>
      <h2 class="text-xl font-semibold text-gray-900 mb-4">Recent Sessions</h2>
      <div v-if="loading" class="text-center py-12">
        <div class="inline-block animate-spin rounded-full h-8 w-8 border-b-2 border-indigo-600"></div>
      </div>
      <div v-else-if="sessions.length === 0" class="text-center py-8 text-gray-500 bg-white rounded-lg shadow">
        No study sessions yet. Start a timer to begin tracking!
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
                  <span v-if="session.material" class="ml-2 inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-indigo-100 text-indigo-800">
                    {{ session.material.category }}
                  </span>
                </div>
                <p v-if="session.notes" class="mt-1 text-sm text-gray-500">{{ session.notes }}</p>
                <p class="mt-1 text-xs text-gray-400">
                  {{ formatDate(session.created_at) }}
                </p>
              </div>
              <div class="ml-4 text-right">
                <p class="text-lg font-semibold text-indigo-600">
                  {{ formatDuration(session.duration_minutes) }}
                </p>
              </div>
            </div>
          </li>
        </ul>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, onUnmounted } from 'vue'

interface Material {
  id: number
  title: string
  category?: string
}

interface Session {
  id: number
  material_id?: number
  material?: Material
  duration_minutes: number
  notes?: string
  created_at: string
}

const timerSeconds = ref(0)
const timerRunning = ref(false)
const timerInterval = ref<number | null>(null)
const selectedMaterialId = ref<number | null>(null)
const sessionNotes = ref('')
const sessions = ref<Session[]>([])
const materials = ref<Material[]>([])
const loading = ref(true)
const streak = ref({
  current_streak: 0,
  longest_streak: 0,
  last_study_date: null
})
const sessionStartTime = ref<Date | null>(null)

const startTimer = () => {
  if (!timerRunning.value) {
    timerRunning.value = true
    sessionStartTime.value = new Date()
    timerInterval.value = window.setInterval(() => {
      timerSeconds.value++
    }, 1000)
  }
}

const pauseTimer = () => {
  if (timerRunning.value && timerInterval.value) {
    timerRunning.value = false
    clearInterval(timerInterval.value)
    timerInterval.value = null
  }
}

const resetTimer = () => {
  pauseTimer()
  timerSeconds.value = 0
  selectedMaterialId.value = null
  sessionNotes.value = ''
  sessionStartTime.value = null
}

const stopTimer = async () => {
  if (timerSeconds.value === 0) return
  
  pauseTimer()
  const durationMinutes = timerSeconds.value / 60
  
  try {
    const response = await fetch('/api/sessions', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      credentials: 'include',
      body: JSON.stringify({
        material_id: selectedMaterialId.value || null,
        duration_minutes: durationMinutes,
        notes: sessionNotes.value || null,
        started_at: sessionStartTime.value?.toISOString(),
        ended_at: new Date().toISOString()
      })
    })
    
    if (response.ok) {
      resetTimer()
      loadSessions()
      loadStreak()
    } else {
      alert('Failed to save session')
    }
  } catch (e) {
    alert('An error occurred')
  }
}

const formatTime = (seconds: number) => {
  const hrs = Math.floor(seconds / 3600)
  const mins = Math.floor((seconds % 3600) / 60)
  const secs = seconds % 60
  return `${String(hrs).padStart(2, '0')}:${String(mins).padStart(2, '0')}:${String(secs).padStart(2, '0')}`
}

const formatDuration = (minutes: number) => {
  const hrs = Math.floor(minutes / 60)
  const mins = Math.floor(minutes % 60)
  if (hrs > 0) {
    return `${hrs}h ${mins}m`
  }
  return `${mins}m`
}

const formatDate = (dateString: string) => {
  const date = new Date(dateString)
  return date.toLocaleDateString('en-US', {
    month: 'short',
    day: 'numeric',
    year: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  })
}

const loadSessions = async () => {
  loading.value = true
  try {
    const response = await fetch('/api/sessions', {
      credentials: 'include'
    })
    if (response.ok) {
      sessions.value = await response.json()
    }
  } catch (e) {
    // Error handling
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
    // Error handling
  }
}

const loadStreak = async () => {
  try {
    const response = await fetch('/api/streak', {
      credentials: 'include'
    })
    if (response.ok) {
      streak.value = await response.json()
    }
  } catch (e) {
    // Error handling
  }
}

onMounted(() => {
  loadSessions()
  loadMaterials()
  loadStreak()
})

onUnmounted(() => {
  if (timerInterval.value) {
    clearInterval(timerInterval.value)
  }
})
</script>
