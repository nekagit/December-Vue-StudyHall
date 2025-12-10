<template>
  <div class="min-h-full flex items-center justify-center py-12 px-4 sm:px-6 lg:px-8">
    <div class="max-w-md w-full space-y-8">
      <div>
        <h2 class="mt-6 text-center text-3xl font-serif font-bold text-msit-dark-50">
          Configure Your Character
        </h2>
        <p class="mt-2 text-center text-sm text-msit-dark-300 font-sans">
          Set up your character name and role to get started
        </p>
      </div>
      
      <form class="mt-8 space-y-6" @submit.prevent="handleConfigure">
        <div v-if="error" class="rounded-md bg-red-900/30 border border-red-700 p-4">
          <div class="text-sm text-red-300 font-sans">{{ error }}</div>
        </div>
        
        <div class="rounded-md shadow-sm space-y-4">
          <div>
            <label for="characterName" class="block text-sm font-medium text-msit-dark-50 mb-2 font-sans">
              Character Name
            </label>
            <input
              id="characterName"
              v-model="characterName"
              name="characterName"
              type="text"
              required
              class="appearance-none relative block w-full px-3 py-2 border border-msit-dark-600 bg-msit-dark-800 placeholder-msit-dark-300 text-msit-dark-50 rounded-md focus:outline-none focus:ring-msit-accent focus:border-msit-accent focus:z-10 sm:text-sm font-sans"
              placeholder="Enter your character name"
            />
          </div>
          
          <div>
            <label for="role" class="block text-sm font-medium text-msit-dark-50 mb-2 font-sans">
              Role (Optional)
            </label>
            <select
              id="role"
              v-model="role"
              name="role"
              class="appearance-none relative block w-full px-3 py-2 border border-msit-dark-600 bg-msit-dark-800 text-msit-dark-50 rounded-md focus:outline-none focus:ring-msit-accent focus:border-msit-accent focus:z-10 sm:text-sm font-sans"
            >
              <option value="student">Student</option>
              <option value="teacher">Teacher</option>
              <option value="researcher">Researcher</option>
              <option value="developer">Developer</option>
              <option value="learner">Learner</option>
            </select>
          </div>
        </div>

        <div>
          <button
            type="submit"
            :disabled="loading"
            class="group relative w-full flex justify-center py-2 px-4 border border-transparent text-sm font-semibold rounded-md text-msit-dark bg-msit-accent hover:bg-msit-accent-500 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-msit-accent disabled:opacity-50 transition-colors font-sans"
          >
            {{ loading ? 'Configuring...' : 'Start Learning' }}
          </button>
        </div>
      </form>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { getCharacterConfig, saveCharacterConfig } from '../utils/character'

const router = useRouter()
const characterName = ref('')
const role = ref('')
const error = ref('')
const loading = ref(false)

onMounted(() => {
  // Check if already configured
  const existingCharacter = getCharacterConfig()
  if (existingCharacter) {
    characterName.value = existingCharacter.name || ''
    role.value = existingCharacter.role || ''
  }
})

const handleConfigure = async () => {
  loading.value = true
  error.value = ''
  
  if (!characterName.value.trim()) {
    error.value = 'Character name is required'
    loading.value = false
    return
  }
  
  try {
    // Store character configuration in localStorage
    const character = {
      name: characterName.value.trim(),
      role: role.value || 'student', // Default to student if not provided
      id: Date.now().toString() // Simple ID generation
    }
    
    saveCharacterConfig(character)
    
    // Navigate to home/dashboard
    router.push('/')
    window.location.reload()
  } catch (e) {
    error.value = 'An error occurred. Please try again.'
  } finally {
    loading.value = false
  }
}
</script>
