<template>
  <div class="px-4 py-6 sm:px-0">
    <div class="text-center">
      <h1 class="text-4xl font-extrabold text-gray-900 sm:text-5xl md:text-6xl">
        Welcome to StudyHall
      </h1>
      <p class="mt-3 max-w-md mx-auto text-base text-gray-500 sm:text-lg md:mt-5 md:text-xl md:max-w-3xl">
        Your learning platform for Python and more
      </p>
    </div>

    <div v-if="user" class="mt-12">
      <div class="grid grid-cols-1 gap-8 sm:grid-cols-2 lg:grid-cols-3">
        <router-link
          to="/materials"
          class="relative group bg-white p-6 focus-within:ring-2 focus-within:ring-inset focus-within:ring-indigo-500 rounded-lg shadow hover:shadow-lg transition-shadow"
        >
          <div>
            <span class="rounded-lg inline-flex p-3 bg-indigo-50 text-indigo-700 ring-4 ring-white">
              <svg class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5c1.747 0 3.332.477 4.5 1.253v13C19.832 18.477 18.247 18 16.5 18c-1.746 0-3.332.477-4.5 1.253" />
              </svg>
            </span>
          </div>
          <div class="mt-4">
            <h3 class="text-lg font-medium">
              <span class="absolute inset-0" aria-hidden="true"></span>
              Course Materials
            </h3>
            <p class="mt-2 text-sm text-gray-500">Access Python and other course materials</p>
          </div>
        </router-link>

        <router-link
          to="/compiler"
          class="relative group bg-white p-6 focus-within:ring-2 focus-within:ring-inset focus-within:ring-indigo-500 rounded-lg shadow hover:shadow-lg transition-shadow"
        >
          <div>
            <span class="rounded-lg inline-flex p-3 bg-indigo-50 text-indigo-700 ring-4 ring-white">
              <svg class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 20l4-16m4 4l4 4-4 4M6 16l-4-4 4-4" />
              </svg>
            </span>
          </div>
          <div class="mt-4">
            <h3 class="text-lg font-medium">
              <span class="absolute inset-0" aria-hidden="true"></span>
              Python Compiler
            </h3>
            <p class="mt-2 text-sm text-gray-500">Run Python code directly in your browser</p>
          </div>
        </router-link>
      </div>
    </div>

    <div v-else class="mt-12 text-center">
      <p class="text-lg text-gray-600">Please login or register to access course materials</p>
      <div class="mt-6 flex justify-center space-x-4">
        <router-link
          to="/login"
          class="inline-flex items-center px-6 py-3 border border-transparent text-base font-medium rounded-md text-white bg-indigo-600 hover:bg-indigo-700"
        >
          Login
        </router-link>
        <router-link
          to="/register"
          class="inline-flex items-center px-6 py-3 border border-gray-300 text-base font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50"
        >
          Register
        </router-link>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'

const user = ref<any>(null)

onMounted(async () => {
  try {
    const response = await fetch('/api/auth/me', {
      credentials: 'include'
    })
    if (response.ok) {
      user.value = await response.json()
    }
  } catch (e) {
    // Not authenticated
  }
})
</script>

