<template>
  <div class="px-4 py-6 sm:px-0">
    <div class="flex justify-between items-center mb-6">
      <h1 class="text-3xl font-bold text-gray-900">Study Goals</h1>
      <button
        @click="showCreateModal = true"
        class="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md text-white bg-indigo-600 hover:bg-indigo-700"
      >
        + New Goal
      </button>
    </div>

    <div v-if="loading" class="text-center py-12">
      <div class="inline-block animate-spin rounded-full h-8 w-8 border-b-2 border-indigo-600"></div>
    </div>

    <div v-else-if="error" class="rounded-md bg-red-50 p-4 mb-4">
      <div class="text-sm text-red-800">{{ error }}</div>
    </div>

    <div v-else-if="goals.length === 0" class="text-center py-12">
      <p class="text-gray-500 mb-4">No goals yet. Create your first study goal!</p>
    </div>

    <div v-else class="grid grid-cols-1 gap-6 md:grid-cols-2 lg:grid-cols-3">
      <div
        v-for="goal in goals"
        :key="goal.id"
        :class="[
          'bg-white shadow rounded-lg p-6',
          goal.is_completed ? 'opacity-75' : ''
        ]"
      >
        <div class="flex items-start justify-between mb-4">
          <h3 :class="['text-lg font-semibold', goal.is_completed ? 'line-through text-gray-500' : 'text-gray-900']">
            {{ goal.title }}
          </h3>
          <div class="flex items-center space-x-2">
            <button
              @click="toggleGoal(goal)"
              :class="[
                'px-2 py-1 text-xs font-medium rounded',
                goal.is_completed
                  ? 'bg-green-100 text-green-800'
                  : 'bg-gray-100 text-gray-800'
              ]"
            >
              {{ goal.is_completed ? '✓ Done' : 'Mark Done' }}
            </button>
            <button
              @click="deleteGoal(goal.id)"
              class="text-red-600 hover:text-red-800"
            >
              <svg class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
              </svg>
            </button>
          </div>
        </div>
        
        <p v-if="goal.description" class="text-sm text-gray-600 mb-4">{{ goal.description }}</p>
        
        <div v-if="goal.target_date" class="text-sm text-gray-500">
          <span>Target: {{ formatDate(goal.target_date) }}</span>
        </div>
        
        <div v-if="goal.is_completed && goal.completed_at" class="mt-2 text-sm text-green-600">
          Completed: {{ formatDate(goal.completed_at) }}
        </div>
      </div>
    </div>

    <!-- Create/Edit Modal -->
    <div
      v-if="showCreateModal"
      class="fixed inset-0 bg-gray-600 bg-opacity-50 overflow-y-auto h-full w-full z-50"
      @click.self="showCreateModal = false"
    >
      <div class="relative top-20 mx-auto p-5 border w-96 shadow-lg rounded-md bg-white">
        <h3 class="text-lg font-bold text-gray-900 mb-4">New Study Goal</h3>
        <form @submit.prevent="createGoal" class="space-y-4">
          <div>
            <label for="title" class="block text-sm font-medium text-gray-700">Title *</label>
            <input
              id="title"
              v-model="goalForm.title"
              type="text"
              required
              class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm px-3 py-2 border"
            />
          </div>
          <div>
            <label for="description" class="block text-sm font-medium text-gray-700">Description</label>
            <textarea
              id="description"
              v-model="goalForm.description"
              rows="3"
              class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm px-3 py-2 border"
            ></textarea>
          </div>
          <div>
            <label for="target_date" class="block text-sm font-medium text-gray-700">Target Date</label>
            <input
              id="target_date"
              v-model="goalForm.target_date"
              type="date"
              class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm px-3 py-2 border"
            />
          </div>
          <div class="flex justify-end space-x-3">
            <button
              type="button"
              @click="showCreateModal = false"
              class="px-4 py-2 border border-gray-300 rounded-md text-sm font-medium text-gray-700 hover:bg-gray-50"
            >
              Cancel
            </button>
            <button
              type="submit"
              :disabled="creating"
              class="px-4 py-2 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-indigo-600 hover:bg-indigo-700 disabled:opacity-50"
            >
              {{ creating ? 'Creating...' : 'Create Goal' }}
            </button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'

const goals = ref<any[]>([])
const loading = ref(true)
const error = ref('')
const showCreateModal = ref(false)
const creating = ref(false)
const goalForm = ref({
  title: '',
  description: '',
  target_date: ''
})

const formatDate = (dateStr: string) => {
  if (!dateStr) return ''
  const date = new Date(dateStr)
  return date.toLocaleDateString()
}

const loadGoals = async () => {
  loading.value = true
  try {
    const response = await fetch('/api/goals', {
      credentials: 'include'
    })
    if (response.ok) {
      goals.value = await response.json()
    } else {
      error.value = 'Failed to load goals'
    }
  } catch (e) {
    error.value = 'An error occurred'
  } finally {
    loading.value = false
  }
}

const createGoal = async () => {
  creating.value = true
  try {
    const response = await fetch('/api/goals', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      credentials: 'include',
      body: JSON.stringify({
        title: goalForm.value.title,
        description: goalForm.value.description,
        target_date: goalForm.value.target_date || null
      })
    })
    if (response.ok) {
      showCreateModal.value = false
      goalForm.value = { title: '', description: '', target_date: '' }
      await loadGoals()
    } else {
      const data = await response.json()
      error.value = data.error || 'Failed to create goal'
    }
  } catch (e) {
    error.value = 'An error occurred'
  } finally {
    creating.value = false
  }
}

const toggleGoal = async (goal: any) => {
  try {
    const response = await fetch(`/api/goals/${goal.id}`, {
      method: 'PUT',
      headers: { 'Content-Type': 'application/json' },
      credentials: 'include',
      body: JSON.stringify({ is_completed: !goal.is_completed })
    })
    if (response.ok) {
      await loadGoals()
    }
  } catch (e) {
    error.value = 'Failed to update goal'
  }
}

const deleteGoal = async (goalId: number) => {
  if (!confirm('Are you sure you want to delete this goal?')) return
  
  try {
    const response = await fetch(`/api/goals/${goalId}`, {
      method: 'DELETE',
      credentials: 'include'
    })
    if (response.ok) {
      await loadGoals()
    }
  } catch (e) {
    error.value = 'Failed to delete goal'
  }
}

onMounted(loadGoals)
</script>
