<template>
  <div class="px-4 py-6 sm:px-0">
    <div class="mb-8">
      <h1 class="text-3xl font-bold text-gray-900 mb-2">My Ratings</h1>
      <p class="text-gray-600">Materials you've rated and reviewed</p>
    </div>

    <div v-if="loading" class="text-center py-12">
      <div class="inline-block animate-spin rounded-full h-8 w-8 border-b-2 border-indigo-600"></div>
    </div>

    <div v-else-if="error" class="rounded-md bg-red-50 p-4 mb-4">
      <div class="text-sm text-red-800">{{ error }}</div>
    </div>

    <div v-else-if="ratings.length === 0" class="text-center py-12">
      <p class="text-gray-500 mb-4">No ratings yet. Rate materials to help others!</p>
      <router-link
        to="/materials"
        class="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md text-white bg-indigo-600 hover:bg-indigo-700"
      >
        Browse Materials
      </router-link>
    </div>

    <div v-else class="space-y-6">
      <div
        v-for="rating in ratings"
        :key="rating.id"
        class="bg-white shadow rounded-lg overflow-hidden"
      >
        <div class="px-6 py-4 border-b border-gray-200">
          <div class="flex items-center justify-between">
            <div>
              <h3 class="text-lg font-medium text-gray-900">
                <router-link
                  :to="`/materials/${rating.material.id}`"
                  class="hover:text-indigo-600"
                >
                  {{ rating.material.title }}
                </router-link>
              </h3>
              <p v-if="rating.material.category" class="text-sm text-gray-500 mt-1">
                {{ rating.material.category }}
              </p>
            </div>
            <button
              @click="deleteRating(rating.id)"
              class="text-red-600 hover:text-red-800"
            >
              <svg class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
              </svg>
            </button>
          </div>
        </div>
        <div class="px-6 py-4">
          <div class="flex items-center mb-2">
            <div class="flex">
              <svg
                v-for="star in 5"
                :key="star"
                class="w-5 h-5"
                :class="star <= rating.rating ? 'text-yellow-400' : 'text-gray-300'"
                fill="currentColor"
                viewBox="0 0 20 20"
              >
                <path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z" />
              </svg>
            </div>
            <span class="ml-2 text-sm font-medium text-gray-700">{{ rating.rating }}/5</span>
          </div>
          <p v-if="rating.comment" class="text-gray-700 mt-2">{{ rating.comment }}</p>
          <p class="mt-4 text-xs text-gray-400">
            Rated: {{ formatDate(rating.created_at) }}
          </p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'

const ratings = ref<any[]>([])
const loading = ref(true)
const error = ref('')

const formatDate = (dateString: string): string => {
  const date = new Date(dateString)
  return date.toLocaleDateString() + ' ' + date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
}

const loadRatings = async () => {
  loading.value = true
  try {
    const response = await fetch('/api/ratings', {
      credentials: 'include'
    })
    if (response.ok) {
      ratings.value = await response.json()
    } else {
      error.value = 'Failed to load ratings'
    }
  } catch (e) {
    error.value = 'An error occurred'
  } finally {
    loading.value = false
  }
}

const deleteRating = async (ratingId: number) => {
  if (!confirm('Are you sure you want to delete this rating?')) return
  
  try {
    const response = await fetch(`/api/ratings/${ratingId}`, {
      method: 'DELETE',
      credentials: 'include'
    })
    if (response.ok) {
      loadRatings()
    } else {
      error.value = 'Failed to delete rating'
    }
  } catch (e) {
    error.value = 'Failed to delete rating'
  }
}

onMounted(loadRatings)
</script>
