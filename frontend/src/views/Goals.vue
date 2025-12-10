<template>
  <div class="px-4 py-6 sm:px-0">
    <div class="mb-8">
      <div class="flex items-center justify-between mb-4">
        <div>
          <h1 class="text-3xl font-bold text-gray-900 mb-2">Study Goals</h1>
          <p class="text-gray-600">Set and track your learning objectives</p>
        </div>
        <button
          @click="showCreateModal = true"
          class="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md text-white bg-indigo-600 hover:bg-indigo-700"
        >
          <svg class="w-5 h-5 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4" />
          </svg>
          New Goal
        </button>
      </div>
    </div>

    <!-- Create/Edit Modal -->
    <div
      v-if="showCreateModal || editingGoal"
      class="fixed inset-0 bg-gray-600 bg-opacity-50 overflow-y-auto h-full w-full z-50"
      @click.self="closeModal"
    >
      <div class="relative top-20 mx-auto p-5 border w-96 shadow-lg rounded-md bg-white">
        <div class="mt-3">
          <h3 class="text-lg font-medium text-gray-900 mb-4">
            {{ editingGoal ? 'Edit Goal' : 'Create New Goal' }}
          </h3>
          <div class="space-y-4">
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">Title *</label>
              <input
                v-model="goalForm.title"
                type="text"
                class="block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500"
                placeholder="e.g., Complete Python Basics"
              />
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">Description</label>
              <textarea
                v-model="goalForm.description"
                rows="3"
                class="block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500"
                placeholder="Optional description..."
              ></textarea>
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">Target Date</label>
              <input
                v-model="goalForm.target_date"
                type="date"
                class="block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500"
              />
            </div>
            <div class="flex items-center">
              <input
                v-model="goalForm.is_completed"
                type="checkbox"
                id="completed"
                class="h-4 w-4 text-indigo-600 focus:ring-indigo-500 border-gray-300 rounded"
              />
              <label for="completed" class="ml-2 block text-sm text-gray-900">Completed</label>
            </div>
          </div>
          <div class="flex justify-end space-x-3 mt-6">
            <button
              @click="closeModal"
              class="px-4 py-2 border border-gray-300 rounded-md text-sm font-medium text-gray-700 hover:bg-gray-50"
            >
              Cancel
            </button>
            <button
              @click="saveGoal"
              :disabled="!goalForm.title.trim()"
              class="px-4 py-2 border border-transparent rounded-md text-sm font-medium text-white bg-indigo-600 hover:bg-indigo-700 disabled:opacity-50 disabled:cursor-not-allowed"
            >
              {{ editingGoal ? 'Update' : 'Create' }}
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- Loading State -->
    <div v-if="loading" class="text-center py-12">
      <div class="inline-block animate-spin rounded-full h-8 w-8 border-b-2 border-indigo-600"></div>
    </div>

    <!-- Error State -->
    <div v-else-if="error" class="rounded-md bg-red-50 p-4 mb-4">
      <div class="text-sm text-red-800">{{ error }}</div>
    </div>

    <!-- Goals List -->
    <div v-else>
      <div v-if="goals.length === 0" class="text-center py-12 bg-white rounded-lg shadow">
        <svg class="mx-auto h-12 w-12 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4M7.835 4.697a3.42 3.42 0 001.946-.806 3.42 3.42 0 014.438 0 3.42 3.42 0 001.946.806 3.42 3.42 0 013.138 3.138 3.42 3.42 0 00.806 1.946 3.42 3.42 0 010 4.438 3.42 3.42 0 00-.806 1.946 3.42 3.42 0 01-3.138 3.138 3.42 3.42 0 00-1.946.806 3.42 3.42 0 01-4.438 0 3.42 3.42 0 00-1.946-.806 3.42 3.42 0 01-3.138-3.138 3.42 3.42 0 00-.806-1.946 3.42 3.42 0 010-4.438 3.42 3.42 0 00.806-1.946 3.42 3.42 0 013.138-3.138z" />
        </svg>
        <h3 class="mt-2 text-sm font-medium text-gray-900">No goals</h3>
        <p class="mt-1 text-sm text-gray-500">Get started by creating a new study goal.</p>
        <div class="mt-6">
          <button
            @click="showCreateModal = true"
            class="inline-flex items-center px-4 py-2 border border-transparent shadow-sm text-sm font-medium rounded-md text-white bg-indigo-600 hover:bg-indigo-700"
          >
            <svg class="w-5 h-5 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4" />
            </svg>
            New Goal
          </button>
        </div>
      </div>

      <div v-else class="grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-3">
        <div
          v-for="goal in goals"
          :key="goal.id"
          class="bg-white rounded-lg shadow p-6 hover:shadow-lg transition-shadow"
          :class="{ 'opacity-75': goal.is_completed }"
        >
          <div class="flex items-start justify-between mb-3">
            <div class="flex-1">
              <h3
                class="text-lg font-medium text-gray-900"
                :class="{ 'line-through text-gray-500': goal.is_completed }"
              >
                {{ goal.title }}
              </h3>
              <p v-if="goal.description" class="mt-1 text-sm text-gray-600">
                {{ goal.description }}
              </p>
            </div>
            <div class="flex items-center space-x-2">
              <input
                type="checkbox"
                :checked="goal.is_completed"
                @change="toggleGoal(goal.id, !goal.is_completed)"
                class="h-5 w-5 text-indigo-600 focus:ring-indigo-500 border-gray-300 rounded"
              />
            </div>
          </div>

          <div v-if="goal.target_date" class="mt-3 flex items-center text-sm text-gray-500">
            <svg class="w-4 h-4 mr-1" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
            </svg>
            {{ formatDate(goal.target_date) }}
          </div>

          <div v-if="goal.completed_at" class="mt-2 text-xs text-green-600">
            Completed on {{ formatDate(goal.completed_at) }}
          </div>

          <div class="mt-4 flex items-center justify-between">
            <div class="text-xs text-gray-400">
              Created {{ formatDate(goal.created_at) }}
            </div>
            <div class="flex space-x-2">
              <button
                @click="editGoal(goal)"
                class="text-sm text-indigo-600 hover:text-indigo-800"
              >
                Edit
              </button>
              <button
                @click="deleteGoal(goal.id)"
                class="text-sm text-red-600 hover:text-red-800"
              >
                Delete
              </button>
            </div>
          </div>
        </div>
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
const editingGoal = ref<any>(null)
const goalForm = ref({
  title: '',
  description: '',
  target_date: '',
  is_completed: false
})

const formatDate = (dateString: string): string => {
  if (!dateString) return ''
  const date = new Date(dateString)
  return date.toLocaleDateString()
}

const loadGoals = async () => {
  loading.value = true
  error.value = ''
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

const closeModal = () => {
  showCreateModal.value = false
  editingGoal.value = null
  goalForm.value = {
    title: '',
    description: '',
    target_date: '',
    is_completed: false
  }
}

const saveGoal = async () => {
  if (!goalForm.value.title.trim()) return

  try {
    const url = editingGoal.value
      ? `/api/goals/${editingGoal.value.id}`
      : '/api/goals'
    const method = editingGoal.value ? 'PUT' : 'POST'

    const body: any = {
      title: goalForm.value.title,
      description: goalForm.value.description || null,
      is_completed: goalForm.value.is_completed
    }

    if (goalForm.value.target_date) {
      body.target_date = new Date(goalForm.value.target_date).toISOString()
    }

    const response = await fetch(url, {
      method,
      headers: { 'Content-Type': 'application/json' },
      credentials: 'include',
      body: JSON.stringify(body)
    })

    if (response.ok) {
      closeModal()
      loadGoals()
    } else {
      const data = await response.json()
      error.value = data.error || 'Failed to save goal'
    }
  } catch (e) {
    error.value = 'An error occurred'
  }
}

const editGoal = (goal: any) => {
  editingGoal.value = goal
  goalForm.value = {
    title: goal.title,
    description: goal.description || '',
    target_date: goal.target_date ? goal.target_date.split('T')[0] : '',
    is_completed: goal.is_completed
  }
  showCreateModal.value = true
}

const toggleGoal = async (goalId: number, isCompleted: boolean) => {
  try {
    const goal = goals.value.find(g => g.id === goalId)
    if (!goal) return

    const response = await fetch(`/api/goals/${goalId}`, {
      method: 'PUT',
      headers: { 'Content-Type': 'application/json' },
      credentials: 'include',
      body: JSON.stringify({
        title: goal.title,
        description: goal.description,
        target_date: goal.target_date,
        is_completed: isCompleted
      })
    })

    if (response.ok) {
      loadGoals()
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
      loadGoals()
    } else {
      error.value = 'Failed to delete goal'
    }
  } catch (e) {
    error.value = 'An error occurred'
  }
}

onMounted(loadGoals)
</script>
