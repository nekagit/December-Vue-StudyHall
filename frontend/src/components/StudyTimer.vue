<template>
  <div class="bg-white shadow rounded-lg p-6">
    <h3 class="text-lg font-medium text-gray-900 mb-4">Study Timer</h3>
    
    <div class="text-center mb-6">
      <div class="text-4xl font-bold text-indigo-600 mb-2">
        {{ formatTime(elapsedSeconds) }}
      </div>
      <div class="text-sm text-gray-500">Elapsed Time</div>
    </div>
    
    <div class="flex justify-center space-x-4 mb-4">
      <button
        v-if="!isRunning"
        @click="startTimer"
        class="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md text-white bg-green-600 hover:bg-green-700"
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
        class="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md text-white bg-yellow-600 hover:bg-yellow-700"
      >
        <svg class="h-5 w-5 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 9v6m4-6v6m7-3a9 9 0 11-18 0 9 9 0 0118 0z" />
        </svg>
        Pause
      </button>
      <button
        v-if="elapsedSeconds > 0"
        @click="stopTimer"
        class="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md text-white bg-red-600 hover:bg-red-700"
      >
        <svg class="h-5 w-5 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 10h6v4H9z" />
        </svg>
        Stop & Save
      </button>
    </div>
    
    <div v-if="materialId" class="mt-4 text-sm text-gray-500 text-center">
      Tracking study time for this material
    </div>
    
    <div v-if="saving" class="mt-4 text-center text-sm text-indigo-600">
      Saving session...
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, onUnmounted } from 'vue'

interface Props {
  materialId?: number
}

const props = defineProps<Props>()

const isRunning = ref(false)
const elapsedSeconds = ref(0)
const intervalId = ref<ReturnType<typeof setInterval> | null>(null)
const saving = ref(false)

const formatTime = (seconds: number) => {
  const hrs = Math.floor(seconds / 3600)
  const mins = Math.floor((seconds % 3600) / 60)
  const secs = seconds % 60
  return `${String(hrs).padStart(2, '0')}:${String(mins).padStart(2, '0')}:${String(secs).padStart(2, '0')}`
}

const startTimer = () => {
  if (!isRunning.value) {
    isRunning.value = true
    intervalId.value = setInterval(() => {
      elapsedSeconds.value++
    }, 1000)
  }
}

const pauseTimer = () => {
  if (isRunning.value && intervalId.value) {
    isRunning.value = false
    clearInterval(intervalId.value)
    intervalId.value = null
  }
}

const stopTimer = async () => {
  pauseTimer()
  
  if (elapsedSeconds.value > 0) {
    saving.value = true
    try {
      const durationMinutes = elapsedSeconds.value / 60
      const response = await fetch('/api/study-sessions', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        credentials: 'include',
        body: JSON.stringify({
          duration_minutes: durationMinutes,
          material_id: props.materialId || null
        })
      })
      
      if (response.ok) {
        elapsedSeconds.value = 0
      }
    } catch (e) {
      console.error('Failed to save study session', e)
    } finally {
      saving.value = false
    }
  }
}

onUnmounted(() => {
  if (intervalId.value) {
    clearInterval(intervalId.value)
  }
})
</script>
