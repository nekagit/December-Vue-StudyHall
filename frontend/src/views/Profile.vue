<template>
  <div class="px-4 py-6 sm:px-0">
    <h1 class="text-3xl font-bold text-gray-900 mb-6">Profile</h1>

    <div v-if="loading" class="text-center py-12">
      <div class="inline-block animate-spin rounded-full h-8 w-8 border-b-2 border-indigo-600"></div>
    </div>

    <div v-else-if="error" class="rounded-md bg-red-50 p-4 mb-4">
      <div class="text-sm text-red-800">{{ error }}</div>
    </div>

    <div v-else-if="user" class="max-w-3xl">
      <div class="bg-white shadow rounded-lg">
        <div class="px-6 py-4 border-b border-gray-200">
          <h2 class="text-lg font-medium text-gray-900">Account Information</h2>
        </div>
        <div class="px-6 py-4">
          <dl class="grid grid-cols-1 gap-x-4 gap-y-6 sm:grid-cols-2">
            <div>
              <dt class="text-sm font-medium text-gray-500">Name</dt>
              <dd class="mt-1 text-sm text-gray-900">{{ user.name }}</dd>
            </div>
            <div>
              <dt class="text-sm font-medium text-gray-500">Email</dt>
              <dd class="mt-1 text-sm text-gray-900">{{ user.email }}</dd>
            </div>
            <div>
              <dt class="text-sm font-medium text-gray-500">User ID</dt>
              <dd class="mt-1 text-sm text-gray-900">{{ user.id }}</dd>
            </div>
          </dl>
        </div>
      </div>

      <!-- Learning Streak -->
      <div class="mt-6 bg-gradient-to-r from-indigo-500 to-purple-600 shadow rounded-lg">
        <div class="px-6 py-4">
          <h2 class="text-lg font-medium text-white mb-4">Learning Streak 🔥</h2>
          <div class="flex items-baseline space-x-6">
            <div>
              <div class="text-3xl font-bold text-white">{{ streak.current_streak_days }}</div>
              <div class="text-sm text-white/90">Current Streak (days)</div>
            </div>
            <div>
              <div class="text-2xl font-semibold text-white">{{ streak.longest_streak_days }}</div>
              <div class="text-sm text-white/90">Best Streak (days)</div>
            </div>
          </div>
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

      <!-- Password Change -->
      <div class="mt-6 bg-white shadow rounded-lg">
        <div class="px-6 py-4 border-b border-gray-200">
          <h2 class="text-lg font-medium text-gray-900">Change Password</h2>
        </div>
        <div class="px-6 py-4">
          <div v-if="passwordError" class="rounded-md bg-red-50 p-4 mb-4">
            <div class="text-sm text-red-800">{{ passwordError }}</div>
          </div>
          <div v-if="passwordSuccess" class="rounded-md bg-green-50 p-4 mb-4">
            <div class="text-sm text-green-800">{{ passwordSuccess }}</div>
          </div>
          <form @submit.prevent="changePassword" class="space-y-4">
            <div>
              <label for="current_password" class="block text-sm font-medium text-gray-700">Current Password</label>
              <input
                id="current_password"
                v-model="passwordForm.current_password"
                type="password"
                required
                class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm px-3 py-2 border"
              />
            </div>
            <div>
              <label for="new_password" class="block text-sm font-medium text-gray-700">New Password</label>
              <input
                id="new_password"
                v-model="passwordForm.new_password"
                type="password"
                required
                minlength="6"
                class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm px-3 py-2 border"
              />
            </div>
            <div>
              <button
                type="submit"
                :disabled="passwordChanging"
                class="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md text-white bg-indigo-600 hover:bg-indigo-700 disabled:opacity-50"
              >
                {{ passwordChanging ? 'Changing...' : 'Change Password' }}
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

const user = ref<any>(null)
const loading = ref(true)
const error = ref('')

const progressStats = ref({
  completed: 0,
  in_progress: 0,
  total: 0
})
const progressLoading = ref(false)
const progressError = ref('')
const streak = ref<any>({
  current_streak_days: 0,
  longest_streak_days: 0,
  last_study_date: null
})
const passwordForm = ref({
  current_password: '',
  new_password: ''
})
const passwordChanging = ref(false)
const passwordError = ref('')
const passwordSuccess = ref('')

const loadStreak = async () => {
  try {
    const response = await fetch('/api/learning-streak', {
      credentials: 'include'
    })
    if (response.ok) {
      streak.value = await response.json()
    }
  } catch (e) {
    // Ignore errors
  }
}

const loadUser = async () => {
  loading.value = true
  try {
    const response = await fetch('/api/auth/me', {
      credentials: 'include'
    })
    if (response.ok) {
      user.value = await response.json()
      await loadProgress()
      await loadStreak()
    } else {
      error.value = 'Failed to load user information'
    }
  } catch (e) {
    error.value = 'An error occurred'
  } finally {
    loading.value = false
  }
}

const loadProgress = async () => {
  progressLoading.value = true
  try {
    const response = await fetch('/api/progress', {
      credentials: 'include'
    })
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

const changePassword = async () => {
  passwordChanging.value = true
  passwordError.value = ''
  passwordSuccess.value = ''
  
  try {
    const response = await fetch('/api/auth/change-password', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      credentials: 'include',
      body: JSON.stringify(passwordForm.value)
    })
    
    if (response.ok) {
      passwordSuccess.value = 'Password changed successfully!'
      passwordForm.value = { current_password: '', new_password: '' }
    } else {
      const data = await response.json()
      passwordError.value = data.error || 'Failed to change password'
    }
  } catch (e) {
    passwordError.value = 'An error occurred'
  } finally {
    passwordChanging.value = false
  }
}

onMounted(loadUser)
</script>
