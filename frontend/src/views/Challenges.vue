<template>
  <div class="px-4 py-4 sm:py-6 sm:px-0">
    <div class="mb-6 sm:mb-8">
      <div class="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
        <div>
          <h1 class="text-2xl sm:text-3xl font-bold text-msit-dark-50 mb-2 font-serif">Coding Challenges</h1>
          <p class="text-sm sm:text-base text-msit-dark-200 font-sans">Daily and weekly coding challenges to keep your skills sharp</p>
        </div>
        <div class="text-right">
          <div class="text-xs text-msit-dark-300 font-sans">Next challenge in:</div>
          <div class="text-lg font-semibold text-msit-accent font-sans">{{ timeUntilNextChallenge }}</div>
        </div>
      </div>
    </div>

    <!-- Challenge Types -->
    <div class="grid grid-cols-1 gap-6 lg:grid-cols-2 mb-8">
      <!-- Daily Challenge -->
      <div class="bg-msit-dark-800 rounded-lg shadow border border-msit-dark-700 p-6">
        <div class="flex items-center justify-between mb-4">
          <div class="flex items-center gap-2">
            <div class="w-3 h-3 bg-msit-accent rounded-full animate-pulse"></div>
            <h2 class="text-xl font-semibold text-msit-dark-50 font-serif">Daily Challenge</h2>
          </div>
          <span class="text-xs px-2 py-1 bg-msit-accent/20 text-msit-accent rounded font-sans">Today</span>
        </div>
        
        <div v-if="dailyChallenge">
          <h3 class="text-lg font-semibold text-msit-dark-50 mb-2 font-sans">{{ dailyChallenge.title }}</h3>
          <p class="text-sm text-msit-dark-200 mb-4 font-sans">{{ dailyChallenge.description }}</p>
          
          <div class="flex items-center gap-4 mb-4 text-xs text-msit-dark-300 font-sans">
            <span class="flex items-center gap-1">
              <svg class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
              {{ dailyChallenge.estimatedTime }} min
            </span>
            <span class="flex items-center gap-1">
              <svg class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
              {{ dailyChallenge.points }} points
            </span>
            <span
              :class="[
                'px-2 py-0.5 rounded text-xs font-medium font-sans',
                dailyChallenge.difficulty === 'Easy' ? 'bg-green-500/20 text-green-400' :
                dailyChallenge.difficulty === 'Medium' ? 'bg-yellow-500/20 text-yellow-400' :
                'bg-red-500/20 text-red-400'
              ]"
            >
              {{ dailyChallenge.difficulty }}
            </span>
          </div>
          
          <button
            @click="startChallenge(dailyChallenge)"
            class="w-full inline-flex items-center justify-center px-4 py-2 border border-transparent text-sm font-semibold rounded-md text-msit-dark bg-msit-accent hover:bg-msit-accent-500 transition-colors font-sans"
          >
            Start Daily Challenge
            <svg class="ml-2 h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7" />
            </svg>
          </button>
        </div>
      </div>

      <!-- Weekly Challenge -->
      <div class="bg-msit-dark-800 rounded-lg shadow border border-msit-dark-700 p-6">
        <div class="flex items-center justify-between mb-4">
          <div class="flex items-center gap-2">
            <svg class="w-5 h-5 text-msit-accent" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
            </svg>
            <h2 class="text-xl font-semibold text-msit-dark-50 font-serif">Weekly Challenge</h2>
          </div>
          <span class="text-xs px-2 py-1 bg-yellow-500/20 text-yellow-400 rounded font-sans">This Week</span>
        </div>
        
        <div v-if="weeklyChallenge">
          <h3 class="text-lg font-semibold text-msit-dark-50 mb-2 font-sans">{{ weeklyChallenge.title }}</h3>
          <p class="text-sm text-msit-dark-200 mb-4 font-sans">{{ weeklyChallenge.description }}</p>
          
          <div class="flex items-center gap-4 mb-4 text-xs text-msit-dark-300 font-sans">
            <span class="flex items-center gap-1">
              <svg class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
              {{ weeklyChallenge.estimatedTime }} min
            </span>
            <span class="flex items-center gap-1">
              <svg class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
              {{ weeklyChallenge.points }} points
            </span>
            <span class="px-2 py-0.5 bg-red-500/20 text-red-400 rounded text-xs font-medium font-sans">
              {{ weeklyChallenge.difficulty }}
            </span>
          </div>
          
          <button
            @click="startChallenge(weeklyChallenge)"
            class="w-full inline-flex items-center justify-center px-4 py-2 border border-transparent text-sm font-semibold rounded-md text-msit-dark bg-msit-accent hover:bg-msit-accent-500 transition-colors font-sans"
          >
            Start Weekly Challenge
            <svg class="ml-2 h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7" />
            </svg>
          </button>
        </div>
      </div>
    </div>

    <!-- Challenge History -->
    <div class="bg-msit-dark-800 rounded-lg shadow border border-msit-dark-700 p-6">
      <h2 class="text-xl font-semibold text-msit-dark-50 mb-4 font-serif">Recent Challenges</h2>
      
      <div v-if="completedChallenges.length === 0" class="text-center py-8">
        <p class="text-msit-dark-300 font-sans">No challenges completed yet. Start your first challenge!</p>
      </div>
      
      <div v-else class="space-y-3">
        <div
          v-for="challenge in completedChallenges"
          :key="challenge.id"
          class="flex items-center justify-between p-4 bg-msit-dark-900 rounded-lg border border-msit-dark-700"
        >
          <div class="flex-1">
            <h3 class="text-base font-semibold text-msit-dark-50 mb-1 font-sans">{{ challenge.title }}</h3>
            <div class="flex items-center gap-3 text-xs text-msit-dark-300 font-sans">
              <span>{{ challenge.date }}</span>
              <span>•</span>
              <span>{{ challenge.points }} points earned</span>
            </div>
          </div>
          <div class="flex items-center gap-2">
            <svg class="h-5 w-5 text-msit-accent" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
            <span class="text-sm font-semibold text-msit-accent font-sans">Completed</span>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()
const timeUntilNextChallenge = ref('24:00:00')
let timer: ReturnType<typeof setInterval> | null = null

const dailyChallenge = {
  id: 1,
  title: 'String Manipulation Master',
  description: 'Write a function that takes a string and returns the longest word. Handle edge cases like punctuation and multiple spaces.',
  difficulty: 'Easy',
  points: 25,
  estimatedTime: 15,
  date: new Date().toISOString().split('T')[0]
}

const weeklyChallenge = {
  id: 2,
  title: 'Data Structure Challenge',
  description: 'Implement a custom data structure that efficiently stores and retrieves key-value pairs with O(1) average time complexity.',
  difficulty: 'Hard',
  points: 100,
  estimatedTime: 60,
  date: new Date().toISOString().split('T')[0]
}

const completedChallenges = ref<Array<{
  id: number
  title: string
  date: string
  points: number
}>>([])

const updateTimer = () => {
  const now = new Date()
  const tomorrow = new Date(now)
  tomorrow.setDate(tomorrow.getDate() + 1)
  tomorrow.setHours(0, 0, 0, 0)
  
  const diff = tomorrow.getTime() - now.getTime()
  const hours = Math.floor(diff / (1000 * 60 * 60))
  const minutes = Math.floor((diff % (1000 * 60 * 60)) / (1000 * 60))
  const seconds = Math.floor((diff % (1000 * 60)) / 1000)
  
  timeUntilNextChallenge.value = `${String(hours).padStart(2, '0')}:${String(minutes).padStart(2, '0')}:${String(seconds).padStart(2, '0')}`
}

const startChallenge = (challenge: any) => {
  const starterCode = `# ${challenge.title}\n# ${challenge.description}\n\ndef solution():\n    # Your code here\n    pass\n\n# Test your solution\nprint(solution())`
  localStorage.setItem('compiler_code', starterCode)
  router.push('/compiler')
}

onMounted(() => {
  updateTimer()
  timer = setInterval(updateTimer, 1000)
  
  // Load completed challenges from localStorage
  const stored = localStorage.getItem('completed_challenges')
  if (stored) {
    try {
      completedChallenges.value = JSON.parse(stored)
    } catch (e) {
      completedChallenges.value = []
    }
  }
})

onUnmounted(() => {
  if (timer) {
    clearInterval(timer)
  }
})
</script>
