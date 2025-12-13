<template>
  <div class="px-4 py-4 sm:py-6 sm:px-0">
    <div class="bg-msit-dark-800 shadow rounded-lg overflow-hidden border border-msit-dark-700">
      <div class="px-4 sm:px-6 py-4 sm:py-6 border-b border-msit-dark-700">
        <h1 class="text-2xl sm:text-3xl font-bold text-msit-dark-50 font-serif">Typing Test</h1>
        <p class="mt-2 text-sm text-msit-dark-200 font-sans">Test your typing speed and accuracy</p>
      </div>
      
      <div class="px-4 sm:px-6 py-4 sm:py-6">
        <!-- Stats Bar -->
        <div class="grid grid-cols-2 md:grid-cols-4 gap-4 mb-6">
          <div class="bg-msit-dark-900 rounded-lg p-4 border border-msit-dark-700">
            <div class="text-sm text-msit-dark-300 font-sans">WPM</div>
            <div class="text-2xl font-bold text-msit-accent font-sans mt-1">{{ wpm }}</div>
          </div>
          <div class="bg-msit-dark-900 rounded-lg p-4 border border-msit-dark-700">
            <div class="text-sm text-msit-dark-300 font-sans">Accuracy</div>
            <div class="text-2xl font-bold text-msit-accent font-sans mt-1">{{ accuracy }}%</div>
          </div>
          <div class="bg-msit-dark-900 rounded-lg p-4 border border-msit-dark-700">
            <div class="text-sm text-msit-dark-300 font-sans">Time</div>
            <div class="text-2xl font-bold text-msit-accent font-sans mt-1">{{ formattedTime }}</div>
          </div>
          <div class="bg-msit-dark-900 rounded-lg p-4 border border-msit-dark-700">
            <div class="text-sm text-msit-dark-300 font-sans">Errors</div>
            <div class="text-2xl font-bold text-msit-accent font-sans mt-1">{{ errors }}</div>
          </div>
        </div>

        <!-- Text Display -->
        <div class="bg-msit-dark-900 rounded-lg p-6 mb-6 border border-msit-dark-700 min-h-[200px]">
          <div class="text-lg leading-relaxed font-mono text-msit-dark-100 select-none">
            <span
              v-for="(char, index) in textToType"
              :key="index"
              :class="getCharClass(index)"
            >
              {{ char === ' ' ? '\u00A0' : char }}
            </span>
          </div>
        </div>

        <!-- Input Area -->
        <div class="mb-6">
          <textarea
            ref="inputRef"
            v-model="userInput"
            @input="handleInput"
            @keydown="handleKeydown"
            :disabled="isFinished"
            :placeholder="isFinished ? 'Test completed! Click restart to try again.' : 'Start typing here...'"
            class="w-full bg-msit-dark-900 border border-msit-dark-700 rounded-lg p-4 text-lg font-mono text-msit-dark-50 focus:outline-none focus:ring-2 focus:ring-msit-accent focus:border-transparent resize-none min-h-[120px] disabled:opacity-50 disabled:cursor-not-allowed"
            autofocus
          ></textarea>
        </div>

        <!-- Controls -->
        <div class="flex flex-col sm:flex-row gap-4 justify-between items-center">
          <div class="flex gap-4">
            <button
              @click="restart"
              class="px-6 py-2 bg-msit-accent text-msit-dark font-semibold rounded-lg hover:bg-msit-accent-500 transition-colors font-sans"
            >
              Restart
            </button>
            <button
              @click="selectNewText"
              class="px-6 py-2 bg-msit-dark-700 text-msit-dark-50 font-semibold rounded-lg hover:bg-msit-dark-600 border border-msit-dark-600 transition-colors font-sans"
            >
              New Text
            </button>
          </div>
          
          <div v-if="isFinished" class="text-center">
            <div class="text-lg font-semibold text-msit-accent font-sans mb-2">Test Complete!</div>
            <div class="text-sm text-msit-dark-300 font-sans">
              Final WPM: {{ wpm }} | Accuracy: {{ accuracy }}%
            </div>
          </div>
        </div>

        <!-- Text Options -->
        <div class="mt-6 pt-6 border-t border-msit-dark-700">
          <div class="text-sm text-msit-dark-300 font-sans mb-3">Select text difficulty:</div>
          <div class="flex flex-wrap gap-2">
            <button
              v-for="(text, index) in textOptions"
              :key="index"
              @click="loadText(index)"
              :class="[
                'px-4 py-2 rounded-lg text-sm font-semibold transition-colors font-sans',
                currentTextIndex === index
                  ? 'bg-msit-accent text-msit-dark'
                  : 'bg-msit-dark-700 text-msit-dark-50 hover:bg-msit-dark-600'
              ]"
            >
              {{ text.name }}
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, nextTick } from 'vue'

const inputRef = ref<HTMLTextAreaElement | null>(null)
const userInput = ref('')
const textToType = ref('')
const startTime = ref<number | null>(null)
const errors = ref(0)
const isFinished = ref(false)
const currentTextIndex = ref(0)

const textOptions = [
  {
    name: 'Easy',
    text: 'The quick brown fox jumps over the lazy dog. This is a simple sentence for beginners to practice typing. Keep your fingers on the home row and type slowly at first.'
  },
  {
    name: 'Medium',
    text: 'Programming is the art of telling a computer what to do through a series of instructions. Python is a high-level programming language known for its simplicity and readability. Many developers choose Python for web development, data science, and automation tasks.'
  },
  {
    name: 'Hard',
    text: 'The complexity of modern software systems requires developers to understand not only programming languages but also algorithms, data structures, design patterns, and system architecture. Object-oriented programming allows us to model real-world entities through classes and objects, enabling code reusability and maintainability.'
  },
  {
    name: 'Code',
    text: 'def calculate_fibonacci(n):\n    if n <= 1:\n        return n\n    return calculate_fibonacci(n - 1) + calculate_fibonacci(n - 2)\n\nresult = calculate_fibonacci(10)\nprint(f"The 10th Fibonacci number is {result}")'
  },
  {
    name: 'Long',
    text: 'In the realm of computer science, algorithms serve as the fundamental building blocks of problem-solving. They provide step-by-step procedures for accomplishing specific tasks, whether it be sorting data, searching through information, or performing complex calculations. The efficiency of an algorithm is often measured in terms of time complexity and space complexity, which help developers understand how the algorithm performs as the input size grows. Understanding these concepts is crucial for writing efficient code that can handle large-scale applications and datasets.'
  }
]

const elapsedTime = computed(() => {
  if (!startTime.value) return 0
  return Math.floor((Date.now() - startTime.value) / 1000)
})

const formattedTime = computed(() => {
  const minutes = Math.floor(elapsedTime.value / 60)
  const seconds = elapsedTime.value % 60
  return `${minutes}:${seconds.toString().padStart(2, '0')}`
})

const wpm = computed(() => {
  if (!startTime.value || elapsedTime.value === 0) return 0
  const words = userInput.value.trim().split(/\s+/).filter(w => w.length > 0).length
  const minutes = elapsedTime.value / 60
  return Math.round(words / minutes)
})

const accuracy = computed(() => {
  if (userInput.value.length === 0) return 100
  const totalChars = userInput.value.length
  const correctChars = totalChars - errors.value
  return Math.max(0, Math.round((correctChars / totalChars) * 100))
})

const getCharClass = (index: number) => {
  if (index >= userInput.value.length) {
    return 'text-msit-dark-300'
  }
  
  const userChar = userInput.value[index]
  const correctChar = textToType.value[index]
  
  if (userChar === correctChar) {
    return 'text-msit-accent bg-msit-accent/20'
  } else {
    return 'text-red-400 bg-red-400/20'
  }
}

const handleInput = () => {
  if (!startTime.value && userInput.value.length > 0) {
    startTime.value = Date.now()
  }
  
  // Check for errors
  const currentLength = userInput.value.length
  if (currentLength <= textToType.value.length) {
    const userChar = userInput.value[currentLength - 1]
    const correctChar = textToType.value[currentLength - 1]
    
    if (userChar !== correctChar) {
      errors.value++
    }
  }
  
  // Check if finished
  if (userInput.value === textToType.value) {
    isFinished.value = true
  }
  
  // Prevent typing beyond the text length
  if (userInput.value.length > textToType.value.length) {
    userInput.value = userInput.value.slice(0, textToType.value.length)
  }
}

const handleKeydown = (e: KeyboardEvent) => {
  // Prevent backspace when at start
  if (e.key === 'Backspace' && userInput.value.length === 0) {
    e.preventDefault()
  }
  
  // Prevent typing if finished
  if (isFinished.value && e.key !== 'Enter') {
    e.preventDefault()
  }
}

const loadText = (index: number) => {
  currentTextIndex.value = index
  textToType.value = textOptions[index].text
  restart()
}

const selectNewText = () => {
  const randomIndex = Math.floor(Math.random() * textOptions.length)
  loadText(randomIndex)
}

const restart = () => {
  userInput.value = ''
  startTime.value = null
  errors.value = 0
  isFinished.value = false
  
  nextTick(() => {
    inputRef.value?.focus()
  })
}

onMounted(() => {
  loadText(0)
  nextTick(() => {
    inputRef.value?.focus()
  })
})
</script>









