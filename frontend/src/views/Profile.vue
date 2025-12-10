<template>
  <div class="px-4 py-6 sm:px-0">
    <div class="max-w-3xl mx-auto">
      <h1 class="text-3xl font-bold text-gray-900 mb-6">Profile</h1>

      <div v-if="loading" class="text-center py-12">
        <div class="inline-block animate-spin rounded-full h-8 w-8 border-b-2 border-indigo-600"></div>
      </div>

      <div v-else-if="error" class="rounded-md bg-red-50 p-4 mb-4">
        <div class="text-sm text-red-800">{{ error }}</div>
      </div>

      <div v-else-if="profile" class="bg-white shadow rounded-lg overflow-hidden">
        <!-- Stats Section -->
        <div class="px-6 py-4 bg-indigo-50 border-b border-indigo-100">
          <h2 class="text-lg font-semibold text-gray-900 mb-4">Statistics</h2>
          <div class="grid grid-cols-2 gap-4">
            <div>
              <p class="text-sm text-gray-600">Total Materials</p>
              <p class="text-2xl font-bold text-indigo-600">{{ profile.stats.total_materials }}</p>
            </div>
            <div>
              <p class="text-sm text-gray-600">Completed</p>
              <p class="text-2xl font-bold text-green-600">{{ profile.stats.completed_materials }}</p>
            </div>
            <div>
              <p class="text-sm text-gray-600">Bookmarks</p>
              <p class="text-2xl font-bold text-yellow-600">{{ profile.stats.bookmarks_count }}</p>
            </div>
            <div>
              <p class="text-sm text-gray-600">Completion Rate</p>
              <p class="text-2xl font-bold text-indigo-600">{{ profile.stats.completion_rate }}%</p>
            </div>
          </div>
        </div>

        <!-- Edit Form -->
        <div class="px-6 py-4">
          <h2 class="text-lg font-semibold text-gray-900 mb-4">Edit Profile</h2>
          <form @submit.prevent="updateProfile" class="space-y-4">
            <div>
              <label for="name" class="block text-sm font-medium text-gray-700">Name</label>
              <input
                id="name"
                v-model="formData.name"
                type="text"
                required
                class="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500"
              />
            </div>
            <div>
              <label for="email" class="block text-sm font-medium text-gray-700">Email</label>
              <input
                id="email"
                v-model="formData.email"
                type="email"
                required
                class="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500"
              />
            </div>
            <div>
              <label for="password" class="block text-sm font-medium text-gray-700">New Password (leave blank to keep current)</label>
              <input
                id="password"
                v-model="formData.password"
                type="password"
                class="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500"
              />
            </div>
            <div v-if="updateSuccess" class="rounded-md bg-green-50 p-4">
              <div class="text-sm text-green-800">Profile updated successfully!</div>
            </div>
            <div class="flex justify-end">
              <button
                type="submit"
                :disabled="updating"
                class="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md text-white bg-indigo-600 hover:bg-indigo-700 disabled:opacity-50"
              >
                {{ updating ? 'Updating...' : 'Update Profile' }}
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

const profile = ref<any>(null)
const loading = ref(true)
const error = ref('')
const updating = ref(false)
const updateSuccess = ref(false)
const formData = ref({
  name: '',
  email: '',
  password: ''
})

const loadProfile = async () => {
  loading.value = true
  try {
    const response = await fetch('/api/profile', {
      credentials: 'include'
    })
    if (response.ok) {
      profile.value = await response.json()
      formData.value.name = profile.value.name
      formData.value.email = profile.value.email
    } else {
      error.value = 'Failed to load profile'
    }
  } catch (e) {
    error.value = 'An error occurred'
  } finally {
    loading.value = false
  }
}

const updateProfile = async () => {
  updating.value = true
  updateSuccess.value = false
  error.value = ''
  try {
    const payload: any = {
      name: formData.value.name,
      email: formData.value.email
    }
    if (formData.value.password) {
      payload.password = formData.value.password
    }
    
    const response = await fetch('/api/profile', {
      method: 'PUT',
      headers: {
        'Content-Type': 'application/json'
      },
      credentials: 'include',
      body: JSON.stringify(payload)
    })
    
    if (response.ok) {
      updateSuccess.value = true
      await loadProfile()
      formData.value.password = ''
      setTimeout(() => {
        updateSuccess.value = false
      }, 3000)
    } else {
      const data = await response.json()
      error.value = data.error || 'Failed to update profile'
    }
  } catch (e) {
    error.value = 'An error occurred'
  } finally {
    updating.value = false
  }
}

onMounted(loadProfile)
</script>
