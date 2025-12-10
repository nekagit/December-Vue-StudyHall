<template>
  <div class="min-h-screen bg-msit-dark text-msit-dark-50">
    <nav v-if="character" class="bg-msit-dark border-b border-msit-dark-700">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="flex justify-between h-16">
          <div class="flex">
            <div class="flex-shrink-0 flex items-center">
              <router-link to="/" class="text-xl font-bold text-msit-accent">StudyHall</router-link>
            </div>
            <div class="hidden sm:ml-6 sm:flex sm:space-x-8">
              <router-link
                to="/"
                class="border-transparent inline-flex items-center px-1 pt-1 border-b-2 text-sm font-medium transition-colors"
                style="color: #E0EADD; font-family: 'Inter', sans-serif;"
                active-class="border-msit-accent"
                :style="$route.path === '/' ? 'border-color: #83E65B; color: #83E65B;' : ''"
                @mouseover="$event.target.style.color='#83E65B'"
                @mouseleave="$route.path === '/' ? $event.target.style.color='#83E65B' : $event.target.style.color='#E0EADD'"
              >
                Home
              </router-link>
              <router-link
                v-if="character"
                to="/dashboard"
                class="border-transparent inline-flex items-center px-1 pt-1 border-b-2 text-sm font-medium transition-colors"
                style="color: #E0EADD; font-family: 'Inter', sans-serif;"
                :style="$route.path === '/dashboard' ? 'border-color: #83E65B; color: #83E65B;' : ''"
                @mouseover="$event.target.style.color='#83E65B'"
                @mouseleave="$route.path === '/dashboard' ? $event.target.style.color='#83E65B' : $event.target.style.color='#E0EADD'"
              >
                Dashboard
              </router-link>
              <router-link
                v-if="character"
                to="/materials"
                class="border-transparent inline-flex items-center px-1 pt-1 border-b-2 text-sm font-medium transition-colors"
                style="color: #E0EADD; font-family: 'Inter', sans-serif;"
                :style="$route.path.startsWith('/materials') ? 'border-color: #83E65B; color: #83E65B;' : ''"
                @mouseover="$event.target.style.color='#83E65B'"
                @mouseleave="$route.path.startsWith('/materials') ? $event.target.style.color='#83E65B' : $event.target.style.color='#E0EADD'"
              >
                Materials
              </router-link>
              <router-link
                v-if="character"
                to="/bookmarks"
                class="border-transparent inline-flex items-center px-1 pt-1 border-b-2 text-sm font-medium transition-colors"
                style="color: #E0EADD; font-family: 'Inter', sans-serif;"
                :style="$route.path === '/bookmarks' ? 'border-color: #83E65B; color: #83E65B;' : ''"
                @mouseover="$event.target.style.color='#83E65B'"
                @mouseleave="$route.path === '/bookmarks' ? $event.target.style.color='#83E65B' : $event.target.style.color='#E0EADD'"
              >
                Bookmarks
              </router-link>
              <router-link
                v-if="character"
                to="/compiler"
                class="border-transparent inline-flex items-center px-1 pt-1 border-b-2 text-sm font-medium transition-colors"
                style="color: #E0EADD; font-family: 'Inter', sans-serif;"
                :style="$route.path === '/compiler' ? 'border-color: #83E65B; color: #83E65B;' : ''"
                @mouseover="$event.target.style.color='#83E65B'"
                @mouseleave="$route.path === '/compiler' ? $event.target.style.color='#83E65B' : $event.target.style.color='#E0EADD'"
              >
                Compiler
              </router-link>
              <router-link
                v-if="character"
                to="/goals"
                class="border-transparent inline-flex items-center px-1 pt-1 border-b-2 text-sm font-medium transition-colors"
                style="color: #E0EADD; font-family: 'Inter', sans-serif;"
                :style="$route.path === '/goals' ? 'border-color: #83E65B; color: #83E65B;' : ''"
                @mouseover="$event.target.style.color='#83E65B'"
                @mouseleave="$route.path === '/goals' ? $event.target.style.color='#83E65B' : $event.target.style.color='#E0EADD'"
              >
                Goals
              </router-link>
              <router-link
                v-if="character"
                to="/study-sessions"
                class="border-transparent inline-flex items-center px-1 pt-1 border-b-2 text-sm font-medium transition-colors"
                style="color: #E0EADD; font-family: 'Inter', sans-serif;"
                :style="$route.path === '/study-sessions' ? 'border-color: #83E65B; color: #83E65B;' : ''"
                @mouseover="$event.target.style.color='#83E65B'"
                @mouseleave="$route.path === '/study-sessions' ? $event.target.style.color='#83E65B' : $event.target.style.color='#E0EADD'"
              >
                Study Sessions
              </router-link>
              <router-link
                v-if="character"
                to="/notes"
                class="border-transparent inline-flex items-center px-1 pt-1 border-b-2 text-sm font-medium transition-colors"
                style="color: #E0EADD; font-family: 'Inter', sans-serif;"
                :style="$route.path === '/notes' ? 'border-color: #83E65B; color: #83E65B;' : ''"
                @mouseover="$event.target.style.color='#83E65B'"
                @mouseleave="$route.path === '/notes' ? $event.target.style.color='#83E65B' : $event.target.style.color='#E0EADD'"
              >
                Notes
              </router-link>
              <router-link
                v-if="character"
                to="/ratings"
                class="border-transparent inline-flex items-center px-1 pt-1 border-b-2 text-sm font-medium transition-colors"
                style="color: #E0EADD; font-family: 'Inter', sans-serif;"
                :style="$route.path === '/ratings' ? 'border-color: #83E65B; color: #83E65B;' : ''"
                @mouseover="$event.target.style.color='#83E65B'"
                @mouseleave="$route.path === '/ratings' ? $event.target.style.color='#83E65B' : $event.target.style.color='#E0EADD'"
              >
                Ratings
              </router-link>
            </div>
          </div>
          <div class="flex items-center">
            <div v-if="character" class="flex items-center space-x-4">
              <router-link
                to="/profile"
                class="font-medium transition-colors"
                style="color: #E0EADD; font-family: 'Inter', sans-serif;"
                @mouseover="$event.target.style.color='#83E65B'"
                @mouseleave="$event.target.style.color='#E0EADD'"
              >
                {{ character.name }}
              </router-link>
              <span class="text-msit-dark-300 text-sm font-sans">({{ character.role }})</span>
              <button
                @click="resetConfiguration"
                class="inline-flex items-center px-4 py-2 border border-transparent text-sm font-semibold rounded-md transition-colors"
                style="color: #1A312B; background-color: #83E65B; font-family: 'Inter', sans-serif;"
                @mouseover="$event.target.style.backgroundColor='#6BD945'"
                @mouseleave="$event.target.style.backgroundColor='#83E65B'"
              >
                Reset Character
              </button>
            </div>
          </div>
        </div>
      </div>
    </nav>

    <main class="max-w-7xl mx-auto py-6 sm:px-6 lg:px-8">
      <router-view />
    </main>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()
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

const resetConfiguration = () => {
  if (confirm('Are you sure you want to reset your character configuration?')) {
    localStorage.removeItem('character')
    character.value = null
    router.push('/configuration')
  }
}

onMounted(() => {
  loadCharacter()
  router.afterEach(() => {
    loadCharacter()
  })
})
</script>
