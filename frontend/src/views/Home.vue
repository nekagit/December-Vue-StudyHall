<template>
  <!-- Landing page for users without character configured -->
  <div v-if="!character" class="min-h-screen">
    <!-- Hero Section -->
    <div class="relative overflow-hidden bg-msit-dark">
      <div class="max-w-7xl mx-auto">
        <div class="relative z-10 pb-8 bg-msit-dark sm:pb-16 md:pb-20 lg:max-w-2xl lg:w-full lg:pb-28 xl:pb-32">
          <main class="mt-10 mx-auto max-w-7xl px-4 sm:mt-12 sm:px-6 md:mt-16 lg:mt-20 lg:px-8 xl:mt-28">
            <div class="sm:text-center lg:text-left">
              <h1 class="text-4xl tracking-tight font-serif font-bold text-msit-dark-50 sm:text-5xl md:text-6xl leading-tight">
                <span class="block xl:inline">Master Python with</span>
                <span class="block text-msit-accent xl:inline"> StudyHall</span>
              </h1>
              <p class="mt-3 text-base text-msit-dark-100 sm:mt-5 sm:text-lg sm:max-w-xl sm:mx-auto md:mt-5 md:text-xl lg:mx-0 font-sans">
                Your comprehensive learning platform for Python programming. Access course materials, run code in your browser, track your progress, and achieve your study goals.
              </p>
              <div class="mt-5 sm:mt-8 sm:flex sm:justify-center lg:justify-start gap-3">
                <router-link
                  to="/configuration"
                  class="w-full sm:w-auto flex items-center justify-center px-8 py-3 border border-transparent text-base font-semibold rounded-md text-msit-dark bg-msit-accent hover:bg-msit-accent-500 md:py-4 md:text-lg md:px-10 transition-colors font-sans"
                >
                  Get Started
                  <svg class="ml-2 h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7" />
                  </svg>
                </router-link>
              </div>
            </div>
          </main>
        </div>
      </div>
    </div>

    <!-- Features Section -->
    <div class="py-12 bg-msit-dark-900">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="lg:text-center">
          <h2 class="text-base text-msit-accent font-semibold tracking-wide uppercase font-sans">Features</h2>
          <p class="mt-2 text-3xl leading-8 font-serif font-bold tracking-tight text-msit-dark-50 sm:text-4xl">
            Everything you need to learn Python
          </p>
        </div>

        <div class="mt-10">
          <div class="space-y-10 md:space-y-0 md:grid md:grid-cols-2 md:gap-x-8 md:gap-y-10">
            <div class="relative">
              <div class="absolute flex items-center justify-center h-12 w-12 rounded-md bg-msit-accent text-msit-dark">
                <svg class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5c1.747 0 3.332.477 4.5 1.253v13C19.832 18.477 18.247 18 16.5 18c-1.746 0-3.332.477-4.5 1.253" />
                </svg>
              </div>
              <p class="ml-16 text-lg leading-6 font-semibold text-msit-dark-50 font-sans">Course Materials</p>
              <p class="mt-2 ml-16 text-base text-msit-dark-100 font-sans">
                Access comprehensive Python course materials and tutorials organized for easy learning.
              </p>
            </div>

            <div class="relative">
              <div class="absolute flex items-center justify-center h-12 w-12 rounded-md bg-msit-accent text-msit-dark">
                <svg class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 20l4-16m4 4l4 4-4 4M6 16l-4-4 4-4" />
                </svg>
              </div>
              <p class="ml-16 text-lg leading-6 font-semibold text-msit-dark-50 font-sans">Python Compiler</p>
              <p class="mt-2 ml-16 text-base text-msit-dark-100 font-sans">
                Run Python code directly in your browser. No setup required, just code and execute.
              </p>
            </div>

            <div class="relative">
              <div class="absolute flex items-center justify-center h-12 w-12 rounded-md bg-msit-accent text-msit-dark">
                <svg class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
              </div>
              <p class="ml-16 text-lg leading-6 font-semibold text-msit-dark-50 font-sans">Track Progress</p>
              <p class="mt-2 ml-16 text-base text-msit-dark-100 font-sans">
                Monitor your learning journey with study sessions, streaks, and progress tracking.
              </p>
            </div>

            <div class="relative">
              <div class="absolute flex items-center justify-center h-12 w-12 rounded-md bg-msit-accent text-msit-dark">
                <svg class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2m-6 9l2 2 4-4" />
                </svg>
              </div>
              <p class="ml-16 text-lg leading-6 font-semibold text-msit-dark-50 font-sans">Bookmarks & Notes</p>
              <p class="mt-2 ml-16 text-base text-msit-dark-100 font-sans">
                Save important materials and take notes to enhance your learning experience.
              </p>
            </div>

            <div class="relative">
              <div class="absolute flex items-center justify-center h-12 w-12 rounded-md bg-msit-accent text-msit-dark">
                <svg class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z" />
                </svg>
              </div>
              <p class="ml-16 text-lg leading-6 font-semibold text-msit-dark-50 font-sans">Study Goals</p>
              <p class="mt-2 ml-16 text-base text-msit-dark-100 font-sans">
                Set and achieve your study goals with personalized tracking and reminders.
              </p>
            </div>

            <div class="relative">
              <div class="absolute flex items-center justify-center h-12 w-12 rounded-md bg-msit-accent text-msit-dark">
                <svg class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
              </div>
              <p class="ml-16 text-lg leading-6 font-semibold text-msit-dark-50 font-sans">Study Sessions</p>
              <p class="mt-2 ml-16 text-base text-msit-dark-100 font-sans">
                Log your study sessions and build consistent learning habits with streak tracking.
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- CTA Section -->
    <div class="bg-msit-dark-800">
      <div class="max-w-2xl mx-auto text-center py-16 px-4 sm:py-20 sm:px-6 lg:px-8">
        <h2 class="text-3xl font-serif font-bold text-msit-dark-50 sm:text-4xl">
          <span class="block">Ready to start learning?</span>
          <span class="block">Join StudyHall today.</span>
        </h2>
        <p class="mt-4 text-lg leading-6 text-msit-dark-100 font-sans">
          Get access to all features and start your Python learning journey.
        </p>
        <router-link
          to="/configuration"
          class="mt-8 w-full inline-flex items-center justify-center px-5 py-3 border border-transparent text-base font-semibold rounded-md text-msit-dark bg-msit-accent hover:bg-msit-accent-500 sm:w-auto transition-colors font-sans"
        >
          Get Started
          <svg class="ml-2 h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7" />
          </svg>
        </router-link>
      </div>
    </div>
  </div>

  <!-- Dashboard view for users with character configured -->
  <div v-else class="px-4 py-6 sm:px-0">
    <div class="text-center">
      <h1 class="text-4xl font-serif font-bold text-msit-dark-50 sm:text-5xl md:text-6xl">
        Welcome back, {{ character.name }}!
      </h1>
      <p class="mt-3 max-w-md mx-auto text-base text-msit-dark-100 sm:text-lg md:mt-5 md:text-xl md:max-w-3xl font-sans">
        Continue your learning journey
      </p>
    </div>

    <div class="mt-12">
      <div class="grid grid-cols-1 gap-8 sm:grid-cols-2 lg:grid-cols-3">
        <router-link
          to="/materials"
          class="relative group bg-msit-dark-800 p-6 focus-within:ring-2 focus-within:ring-inset focus-within:ring-msit-accent rounded-lg border border-msit-dark-700 hover:border-msit-accent transition-all"
        >
          <div>
            <span class="rounded-lg inline-flex p-3 bg-msit-accent text-msit-dark ring-4 ring-msit-dark-800">
              <svg class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5c1.747 0 3.332.477 4.5 1.253v13C19.832 18.477 18.247 18 16.5 18c-1.746 0-3.332.477-4.5 1.253" />
              </svg>
            </span>
          </div>
          <div class="mt-4">
            <h3 class="text-lg font-semibold text-msit-dark-50 font-sans">
              <span class="absolute inset-0" aria-hidden="true"></span>
              Course Materials
            </h3>
            <p class="mt-2 text-sm text-msit-dark-100 font-sans">Access Python and other course materials</p>
          </div>
        </router-link>

        <router-link
          to="/compiler"
          class="relative group bg-msit-dark-800 p-6 focus-within:ring-2 focus-within:ring-inset focus-within:ring-msit-accent rounded-lg border border-msit-dark-700 hover:border-msit-accent transition-all"
        >
          <div>
            <span class="rounded-lg inline-flex p-3 bg-msit-accent text-msit-dark ring-4 ring-msit-dark-800">
              <svg class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 20l4-16m4 4l4 4-4 4M6 16l-4-4 4-4" />
              </svg>
            </span>
          </div>
          <div class="mt-4">
            <h3 class="text-lg font-semibold text-msit-dark-50 font-sans">
              <span class="absolute inset-0" aria-hidden="true"></span>
              Python Compiler
            </h3>
            <p class="mt-2 text-sm text-msit-dark-100 font-sans">Run Python code directly in your browser</p>
          </div>
        </router-link>

        <router-link
          to="/dashboard"
          class="relative group bg-msit-dark-800 p-6 focus-within:ring-2 focus-within:ring-inset focus-within:ring-msit-accent rounded-lg border border-msit-dark-700 hover:border-msit-accent transition-all"
        >
          <div>
            <span class="rounded-lg inline-flex p-3 bg-msit-accent text-msit-dark ring-4 ring-msit-dark-800">
              <svg class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
              </svg>
            </span>
          </div>
          <div class="mt-4">
            <h3 class="text-lg font-semibold text-msit-dark-50 font-sans">
              <span class="absolute inset-0" aria-hidden="true"></span>
              Dashboard
            </h3>
            <p class="mt-2 text-sm text-msit-dark-100 font-sans">View your learning progress and statistics</p>
          </div>
        </router-link>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'

const character = ref<any>(null)

const loadCharacter = () => {
  const stored = localStorage.getItem('character')
  if (stored) {
    try {
      character.value = JSON.parse(stored)
    } catch (e) {
      character.value = null
    }
  } else {
    character.value = null
  }
}

onMounted(() => {
  loadCharacter()
})
</script>

