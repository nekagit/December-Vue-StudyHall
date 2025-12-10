<template>
  <div class="px-4 py-6 sm:px-0">
    <div class="mb-8">
      <h1 class="text-3xl font-bold text-gray-900 mb-2">Study Goals</h1>
      <p class="text-gray-600">Set and track your learning objectives</p>
    </div>

    <!-- Create Goal Form -->
    <div class="bg-white shadow rounded-lg p-6 mb-8">
      <h2 class="text-xl font-semibold text-gray-900 mb-4">Create New Goal</h2>
      <form @submit.prevent="createGoal" class="space-y-4">
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-2">Title *</label>
          <input
            v-model="newGoal.title"
            type="text"
            required
            class="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500"
            placeholder="e.g., Complete Python Basics Course"
          />
        </div>
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-2">Description</label>
          <textarea
            v-model="newGoal.description"
            rows="3"
            class="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500"
            placeholder="Add details about your goal..."
          ></textarea>
        </div>
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-2">Target Date (Optional)</label>
          <input
            v-model="newGoal.target_date"
            type="date"
            class="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500"
          />
        </div>
        <button
          type="submit"
          class="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md text-white bg-indigo-600 hover:bg-indigo-700"
        >
          Create Goal
        </button>
      </form>
    </div>

    <!-- Goals List -->
    <div class="space-y-4">
      <div v-if="loading" class="text-center py-12">
        <div class="inline-block animate-spin rounded-full h-8 w-8 border-b-2 border-indigo-600"></div>
      </div>

      <div v-else-if="goals.length === 0" class="bg-white shadow rounded-lg p-12 text-center">
        <svg class="mx-auto h-12 w-12 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
        </svg>
        <h3 class="mt-2 text-sm font-medium text-gray-900">No goals</h3>
        <p class="mt-1 text-sm text-gray-500">Get started by creating your first study goal.</p>
      </div>

      <div v-else class="grid grid-cols-1 gap-4">
        <div
          v-for="goal in goals"
          :key="goal.id"
          class="bg-white shadow rounded-lg p-6"
          :class="{ 'opacity-75': goal.is_completed }"
        >
          <div class="flex items-start justify-between">
            <div class="flex-1">
              <div class="flex items-center">
                <input
                  type="checkbox"
                  :checked="goal.is_completed"
                  @change="toggleGoal(goal.id, !goal.is_completed)"
                  class="h-4 w-4 text-indigo-600 focus:ring-indigo-500 border-gray-300 rounded"
                />
                <h3 class="ml-3 text-lg font-medium text-gray-900" :class="{ 'line-through': goal.is_completed }">
                  {{ goal.title }}
                </h3>
              </div>
              <p v-if="goal.description" class="mt-2 text-sm text-gray-600">{{ goal.description }}</p>
              <div class="mt-3 flex items-center space-x-4 text-sm text-gray-500">
                <span v-if="goal.target_date">
                  Target: {{ formatDate(goal.target_date) }}
                  <span v-if="!goal.is_completed && isOverdue(goal.target_date)" class="text-red-600 font-medium">
                    (Overdue)
                  </span>
                </span>
                <span v-if="goal.completed_at">
                  Completed: {{ formatDate(goal.completed_at) }}
                </span>
                <span v-else>
                  Created: {{ formatDate(goal.created_at) }}
                </span>
              </div>
            </div>
            <div class="ml-4 flex space-x-2">
              <button
                @click="editGoal(goal)"
                class="text-indigo-600 hover:text-indigo-800"
              >
                <svg class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z" />
                </svg>
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
        </div>
      </div>
    </div>

    <!-- Edit Goal Modal -->
    <div v-if="editingGoal" class="fixed inset-0 bg-gray-600 bg-opacity-50 overflow-y-auto h-full w-full z-50">
      <div class="relative top-20 mx-auto p-5 border w-96 shadow-lg rounded-md bg-white">
        <div class="mt-3">
          <h3 class="text-lg font-medium text-gray-900 mb-4">Edit Goal</h3>
          <form @submit.prevent="updateGoal" class="space-y-4">
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">Title *</label>
              <input
                v-model="editingGoal.title"
                type="text"
                required
                class="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500"
              />
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">Description</label>
              <textarea
                v-model="editingGoal.description"
                rows="3"
                class="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500"
              ></textarea>
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">Target Date</label>
              <input
                v-model="editingGoal.target_date"
                type="date"
                class="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500"
              />
            </div>
            <div class="flex items-center">
              <input
                v-model="editingGoal.is_completed"
                type="checkbox"
                class="h-4 w-4 text-indigo-600 focus:ring-indigo-500 border-gray-300 rounded"
              />
              <label class="ml-2 block text-sm text-gray-900">Completed</label>
            </div>
            <div class="flex justify-end space-x-3 mt-4">
              <button
                type="button"
                @click="editingGoal = null"
                class="px-4 py-2 border border-gray-300 rounded-md text-sm font-medium text-gray-700 hover:bg-gray-50"
              >
                Cancel
              </button>
              <button
                type="submit"
                class="px-4 py-2 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-indigo-600 hover:bg-indigo-700"
              >
                Update
              </button>
            </div>
          </form>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'

const goals = ref<any[]>([])
const loading = ref(true)
const editingGoal = ref<any>(null)

const newGoal = ref({
  title: '',
  description: '',
  target_date: ''
})

const loadGoals = async () => {
  loading.value = true
  try {
    const response = await fetch('/api/goals', {
      credentials: 'include'
    })
    if (response.ok) {
      goals.value = await response.json()
    }
  } catch (e) {
    console.error('Failed to load goals', e)
  } finally {
    loading.value = false
  }
}

const createGoal = async () => {
  try {
    const response = await fetch('/api/goals', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      credentials: 'include',
      body: JSON.stringify({
        title: newGoal.value.title,
        description: newGoal.value.description || null,
        target_date: newGoal.value.target_date || null
      })
    })
    if (response.ok) {
      newGoal.value = { title: '', description: '', target_date: '' }
      await loadGoals()
    }
  } catch (e) {
    console.error('Failed to create goal', e)
  }
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
        ...goal,
        is_completed: isCompleted
      })
    })
    if (response.ok) {
      await loadGoals()
    }
  } catch (e) {
    console.error('Failed to update goal', e)
  }
}

const editGoal = (goal: any) => {
  editingGoal.value = {
    ...goal,
    target_date: goal.target_date ? goal.target_date.split('T')[0] : ''
  }
}

const updateGoal = async () => {
  if (!editingGoal.value) return
  
  try {
    const response = await fetch(`/api/goals/${editingGoal.value.id}`, {
      method: 'PUT',
      headers: { 'Content-Type': 'application/json' },
      credentials: 'include',
      body: JSON.stringify({
        title: editingGoal.value.title,
        description: editingGoal.value.description || null,
        target_date: editingGoal.value.target_date || null,
        is_completed: editingGoal.value.is_completed
      })
    })
    if (response.ok) {
      editingGoal.value = null
      await loadGoals()
    }
  } catch (e) {
    console.error('Failed to update goal', e)
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
    console.error('Failed to delete goal', e)
  }
}

const formatDate = (dateString: string): string => {
  return new Date(dateString).toLocaleDateString()
}

const isOverdue = (dateString: string): boolean => {
  if (!dateString) return false
  const targetDate = new Date(dateString)
  const today = new Date()
  today.setHours(0, 0, 0, 0)
  targetDate.setHours(0, 0, 0, 0)
  return targetDate < today
}

onMounted(loadGoals)
</script>
