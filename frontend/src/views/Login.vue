<template>
  <div class="min-h-full flex items-center justify-center py-12 px-4 sm:px-6 lg:px-8">
    <div class="max-w-md w-full space-y-8">
      <div>
        <h2 class="mt-6 text-center text-3xl font-extrabold text-gray-900">
          Sign in to your account
        </h2>
      </div>
      
      <!-- Demo Accounts Section -->
      <div class="mt-6 p-4 bg-gray-50 rounded-lg border border-gray-200">
        <p class="text-sm font-medium text-gray-700 mb-3">Quick Login (Demo Accounts):</p>
        <div class="grid grid-cols-2 gap-2">
          <button
            v-for="account in demoAccounts"
            :key="account.email"
            type="button"
            @click="fillDemoAccount(account)"
            class="px-3 py-2 text-xs font-medium text-gray-700 bg-white border border-gray-300 rounded-md hover:bg-indigo-50 hover:border-indigo-300 hover:text-indigo-700 transition-colors"
          >
            {{ account.name }}
          </button>
        </div>
      </div>

      <form class="mt-8 space-y-6" @submit.prevent="handleLogin">
        <div v-if="error" class="rounded-md bg-red-50 p-4">
          <div class="text-sm text-red-800">{{ error }}</div>
        </div>
        <div class="rounded-md shadow-sm -space-y-px">
          <div>
            <label for="email" class="sr-only">Email address</label>
            <input
              id="email"
              v-model="email"
              name="email"
              type="email"
              autocomplete="email"
              required
              class="appearance-none rounded-none relative block w-full px-3 py-2 border border-gray-300 placeholder-gray-500 text-gray-900 rounded-t-md focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 focus:z-10 sm:text-sm"
              placeholder="Email address"
            />
          </div>
          <div>
            <label for="password" class="sr-only">Password</label>
            <input
              id="password"
              v-model="password"
              name="password"
              type="password"
              autocomplete="current-password"
              required
              class="appearance-none rounded-none relative block w-full px-3 py-2 border border-gray-300 placeholder-gray-500 text-gray-900 rounded-b-md focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 focus:z-10 sm:text-sm"
              placeholder="Password"
            />
          </div>
        </div>

        <div>
          <button
            type="submit"
            :disabled="loading"
            class="group relative w-full flex justify-center py-2 px-4 border border-transparent text-sm font-medium rounded-md text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 disabled:opacity-50"
          >
            {{ loading ? 'Signing in...' : 'Sign in' }}
          </button>
        </div>

        <div class="text-center">
          <router-link to="/register" class="font-medium text-indigo-600 hover:text-indigo-500">
            Don't have an account? Register here
          </router-link>
        </div>
      </form>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'

interface DemoAccount {
  email: string
  password: string
  name: string
}

const router = useRouter()
const email = ref('')
const password = ref('')
const error = ref('')
const loading = ref(false)

const demoAccounts: DemoAccount[] = [
  { email: 'student@studyhall.com', password: 'password123', name: 'Sample Student' },
  { email: 'alice@studyhall.com', password: 'demo123', name: 'Alice Johnson' },
  { email: 'bob@studyhall.com', password: 'demo123', name: 'Bob Smith' },
  { email: 'charlie@studyhall.com', password: 'demo123', name: 'Charlie Brown' },
  { email: 'diana@studyhall.com', password: 'demo123', name: 'Diana Prince' },
  { email: 'eve@studyhall.com', password: 'demo123', name: 'Eve Williams' },
]

const fillDemoAccount = (account: DemoAccount) => {
  email.value = account.email
  password.value = account.password
  error.value = ''
}

const handleLogin = async () => {
  loading.value = true
  error.value = ''
  
  try {
    const response = await fetch('/api/auth/login', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      credentials: 'include',
      body: JSON.stringify({ email: email.value, password: password.value })
    })
    
    if (response.ok) {
      router.push('/')
      window.location.reload()
    } else {
      const data = await response.json()
      error.value = data.error || 'Invalid email or password'
    }
  } catch (e) {
    error.value = 'An error occurred. Please try again.'
  } finally {
    loading.value = false
  }
}
</script>

