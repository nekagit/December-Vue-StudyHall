<template>
  <div class="px-4 py-4 sm:py-6 sm:px-0">
    <!-- Setup Screen -->
    <div v-if="!interviewStarted && !interviewCompleted" class="max-w-3xl mx-auto">
      <div class="mb-6 sm:mb-8">
        <h1 class="text-2xl sm:text-3xl font-bold text-msit-dark-50 mb-2 font-serif">Mock Interview</h1>
        <p class="text-sm sm:text-base text-msit-dark-200 font-sans">Practice your interview skills with realistic questions</p>
      </div>

      <div class="bg-msit-dark-800 border border-msit-dark-700 rounded-lg p-6">
        <h2 class="text-xl font-semibold text-msit-dark-50 mb-4 font-sans">Interview Configuration</h2>
        
        <!-- Interview Type -->
        <div class="mb-6">
          <label class="block text-sm font-medium text-msit-dark-200 mb-2 font-sans">Interview Type</label>
          <div class="grid grid-cols-1 sm:grid-cols-2 gap-3">
            <button
              v-for="type in interviewTypes"
              :key="type"
              @click="selectedType = type"
              :class="[
                'px-4 py-3 rounded-lg text-sm font-medium transition-colors font-sans text-left',
                selectedType === type
                  ? 'bg-msit-accent text-msit-dark border-2 border-msit-accent'
                  : 'bg-msit-dark-700 text-msit-dark-200 border border-msit-dark-600 hover:border-msit-accent'
              ]"
            >
              {{ type }}
            </button>
          </div>
        </div>

        <!-- Difficulty Level -->
        <div class="mb-6">
          <label class="block text-sm font-medium text-msit-dark-200 mb-2 font-sans">Difficulty Level</label>
          <div class="flex flex-wrap gap-2">
            <button
              v-for="difficulty in difficulties"
              :key="difficulty"
              @click="selectedDifficulty = difficulty"
              :class="[
                'px-4 py-2 rounded-lg text-sm font-medium transition-colors font-sans',
                selectedDifficulty === difficulty
                  ? 'bg-msit-accent text-msit-dark'
                  : 'bg-msit-dark-700 text-msit-dark-200 border border-msit-dark-600 hover:border-msit-accent'
              ]"
            >
              {{ difficulty }}
            </button>
          </div>
        </div>

        <!-- Number of Questions -->
        <div class="mb-6">
          <label class="block text-sm font-medium text-msit-dark-200 mb-2 font-sans">Number of Questions</label>
          <select
            v-model="numberOfQuestions"
            class="w-full px-4 py-2 bg-msit-dark-700 border border-msit-dark-600 rounded-lg text-msit-dark-50 focus:border-msit-accent focus:outline-none font-sans"
          >
            <option v-for="num in [5, 10, 15, 20]" :key="num" :value="num">{{ num }} questions</option>
          </select>
        </div>

        <!-- Time per Question -->
        <div class="mb-6">
          <label class="block text-sm font-medium text-msit-dark-200 mb-2 font-sans">Time per Question</label>
          <select
            v-model="timePerQuestion"
            class="w-full px-4 py-2 bg-msit-dark-700 border border-msit-dark-600 rounded-lg text-msit-dark-50 focus:border-msit-accent focus:outline-none font-sans"
          >
            <option :value="300">5 minutes</option>
            <option :value="600">10 minutes</option>
            <option :value="900">15 minutes</option>
            <option :value="0">No time limit</option>
          </select>
        </div>

        <!-- Start Button -->
        <button
          @click="startInterview"
          class="w-full px-6 py-3 bg-msit-accent text-msit-dark rounded-lg hover:bg-msit-accent-500 transition-colors font-semibold font-sans"
        >
          Start Interview
        </button>
      </div>
    </div>

    <!-- Interview Session -->
    <div v-if="interviewStarted && !interviewCompleted" class="max-w-5xl mx-auto">
      <!-- Header with Timer and Progress -->
      <div class="mb-6 bg-msit-dark-800 border border-msit-dark-700 rounded-lg p-4">
        <div class="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4">
          <div>
            <h2 class="text-xl font-semibold text-msit-dark-50 font-sans">Question {{ currentQuestionIndex + 1 }} of {{ filteredQuestions.length }}</h2>
            <p class="text-sm text-msit-dark-200 font-sans">{{ selectedType }} Interview</p>
          </div>
          <div class="flex items-center gap-4">
            <div v-if="timePerQuestion > 0" class="text-right">
              <div class="text-2xl font-bold" :class="timeRemaining <= 60 ? 'text-red-400' : 'text-msit-accent'">
                {{ formatTime(timeRemaining) }}
              </div>
              <div class="text-xs text-msit-dark-300 font-sans">Time Remaining</div>
            </div>
            <button
              @click="endInterview"
              class="px-4 py-2 bg-red-600 text-white rounded-lg hover:bg-red-700 transition-colors text-sm font-medium font-sans"
            >
              End Interview
            </button>
          </div>
        </div>
        <!-- Progress Bar -->
        <div class="mt-4">
          <div class="w-full bg-msit-dark-700 rounded-full h-2">
            <div
              class="bg-msit-accent h-2 rounded-full transition-all duration-300"
              :style="{ width: `${((currentQuestionIndex + 1) / filteredQuestions.length) * 100}%` }"
            ></div>
          </div>
        </div>
      </div>

      <!-- Current Question -->
      <div class="bg-msit-dark-800 border border-msit-dark-700 rounded-lg p-6 mb-6">
        <div class="flex items-center justify-between mb-4">
          <span :class="[
            'px-3 py-1 rounded-full text-xs font-medium font-sans',
            currentQuestion.category === 'Coding' ? 'bg-blue-500/20 text-blue-400' :
            currentQuestion.category === 'Behavioral' ? 'bg-purple-500/20 text-purple-400' :
            'bg-green-500/20 text-green-400'
          ]">
            {{ currentQuestion.category }}
          </span>
          <span :class="[
            'px-3 py-1 rounded-full text-xs font-medium font-sans',
            currentQuestion.difficulty === 'Easy' ? 'bg-green-500/20 text-green-400' :
            currentQuestion.difficulty === 'Medium' ? 'bg-yellow-500/20 text-yellow-400' :
            'bg-red-500/20 text-red-400'
          ]">
            {{ currentQuestion.difficulty }}
          </span>
        </div>

        <h3 class="text-xl font-semibold text-msit-dark-50 mb-4 font-sans">{{ currentQuestion.question }}</h3>
        
        <div v-if="currentQuestion.context" class="bg-msit-dark-900 border border-msit-dark-700 rounded-lg p-4 mb-4">
          <p class="text-sm text-msit-dark-200 whitespace-pre-line font-sans">{{ currentQuestion.context }}</p>
        </div>

        <div v-if="currentQuestion.hints && showHints" class="bg-msit-dark-900 border border-msit-accent rounded-lg p-4 mb-4">
          <h4 class="text-sm font-semibold text-msit-accent mb-2 font-sans">Hints:</h4>
          <ul class="list-disc list-inside space-y-1 text-sm text-msit-dark-200 font-sans">
            <li v-for="(hint, index) in currentQuestion.hints" :key="index">{{ hint }}</li>
          </ul>
        </div>

        <!-- Answer Area for Coding Questions -->
        <div v-if="currentQuestion.category === 'Coding'" class="mt-6">
          <div class="flex items-center justify-between mb-2">
            <label class="text-sm font-medium text-msit-dark-200 font-sans">Your Solution:</label>
            <button
              @click="showHints = !showHints"
              class="text-xs text-msit-accent hover:text-msit-accent-300 font-sans"
            >
              {{ showHints ? 'Hide' : 'Show' }} Hints
            </button>
          </div>
          <textarea
            v-model="answers[currentQuestionIndex]"
            placeholder="Write your solution here..."
            class="w-full h-48 px-4 py-3 bg-msit-dark-900 border border-msit-dark-600 rounded-lg text-msit-dark-50 font-mono text-sm focus:border-msit-accent focus:outline-none resize-none"
          ></textarea>
        </div>

        <!-- Answer Area for Other Questions -->
        <div v-else class="mt-6">
          <div class="flex items-center justify-between mb-2">
            <label class="text-sm font-medium text-msit-dark-200 font-sans">Your Answer:</label>
            <button
              @click="showHints = !showHints"
              class="text-xs text-msit-accent hover:text-msit-accent-300 font-sans"
            >
              {{ showHints ? 'Hide' : 'Show' }} Hints
            </button>
          </div>
          <textarea
            v-model="answers[currentQuestionIndex]"
            placeholder="Type your answer here..."
            class="w-full h-32 px-4 py-3 bg-msit-dark-900 border border-msit-dark-600 rounded-lg text-msit-dark-50 font-sans text-sm focus:border-msit-accent focus:outline-none resize-none"
          ></textarea>
        </div>
      </div>

      <!-- Navigation Buttons -->
      <div class="flex justify-between items-center">
        <button
          @click="previousQuestion"
          :disabled="currentQuestionIndex === 0"
          :class="[
            'px-6 py-2 rounded-lg font-medium transition-colors font-sans',
            currentQuestionIndex === 0
              ? 'bg-msit-dark-700 text-msit-dark-300 cursor-not-allowed'
              : 'bg-msit-dark-700 text-msit-dark-200 hover:bg-msit-dark-600 border border-msit-dark-600'
          ]"
        >
          ← Previous
        </button>

        <div class="flex gap-2">
          <button
            v-if="currentQuestionIndex < filteredQuestions.length - 1"
            @click="nextQuestion"
            class="px-6 py-2 bg-msit-accent text-msit-dark rounded-lg hover:bg-msit-accent-500 transition-colors font-medium font-sans"
          >
            Next →
          </button>
          <button
            v-else
            @click="completeInterview"
            class="px-6 py-2 bg-msit-accent text-msit-dark rounded-lg hover:bg-msit-accent-500 transition-colors font-medium font-sans"
          >
            Complete Interview
          </button>
        </div>
      </div>
    </div>

    <!-- Interview Summary -->
    <div v-if="interviewCompleted" class="max-w-3xl mx-auto">
      <div class="mb-6 sm:mb-8">
        <h1 class="text-2xl sm:text-3xl font-bold text-msit-dark-50 mb-2 font-serif">Interview Complete!</h1>
        <p class="text-sm sm:text-base text-msit-dark-200 font-sans">Review your performance</p>
      </div>

      <div class="bg-msit-dark-800 border border-msit-dark-700 rounded-lg p-6 mb-6">
        <h2 class="text-xl font-semibold text-msit-dark-50 mb-4 font-sans">Summary</h2>
        <div class="grid grid-cols-2 gap-4 mb-6">
          <div class="bg-msit-dark-900 border border-msit-dark-700 rounded-lg p-4">
            <div class="text-2xl font-bold text-msit-accent">{{ filteredQuestions.length }}</div>
            <div class="text-sm text-msit-dark-200 font-sans">Total Questions</div>
          </div>
          <div class="bg-msit-dark-900 border border-msit-dark-700 rounded-lg p-4">
            <div class="text-2xl font-bold text-msit-accent">{{ answeredCount }}</div>
            <div class="text-sm text-msit-dark-200 font-sans">Answered</div>
          </div>
        </div>

        <div class="space-y-4">
          <h3 class="text-lg font-semibold text-msit-dark-50 font-sans">Your Answers:</h3>
          <div
            v-for="(question, index) in filteredQuestions"
            :key="index"
            class="bg-msit-dark-900 border border-msit-dark-700 rounded-lg p-4"
          >
            <div class="flex items-center justify-between mb-2">
              <span class="text-sm font-medium text-msit-dark-200 font-sans">Question {{ index + 1 }}</span>
              <span :class="[
                'px-2 py-1 rounded text-xs font-medium font-sans',
                answers[index] && answers[index].trim() ? 'bg-green-500/20 text-green-400' : 'bg-red-500/20 text-red-400'
              ]">
                {{ answers[index] && answers[index].trim() ? 'Answered' : 'Not Answered' }}
              </span>
            </div>
            <p class="text-sm text-msit-dark-200 mb-2 font-sans">{{ question.question }}</p>
            <div v-if="answers[index] && answers[index].trim()" class="mt-2 p-3 bg-msit-dark-800 rounded border border-msit-dark-600">
              <p class="text-sm text-msit-dark-100 whitespace-pre-line font-sans">{{ answers[index] }}</p>
            </div>
            <p v-else class="text-sm text-msit-dark-300 italic font-sans">No answer provided</p>
          </div>
        </div>
      </div>

      <div class="flex gap-4">
        <button
          @click="restartInterview"
          class="flex-1 px-6 py-3 bg-msit-accent text-msit-dark rounded-lg hover:bg-msit-accent-500 transition-colors font-semibold font-sans"
        >
          Start New Interview
        </button>
        <button
          @click="exportAnswers"
          class="flex-1 px-6 py-3 bg-msit-dark-700 text-msit-dark-200 rounded-lg hover:bg-msit-dark-600 transition-colors font-semibold border border-msit-dark-600 font-sans"
        >
          Export Answers
        </button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, onUnmounted } from 'vue'

const interviewTypes = ['Technical', 'Behavioral', 'Mixed']
const difficulties = ['Easy', 'Medium', 'Hard', 'All Levels']

const selectedType = ref('Technical')
const selectedDifficulty = ref('All Levels')
const numberOfQuestions = ref(10)
const timePerQuestion = ref(600) // 10 minutes default

const interviewStarted = ref(false)
const interviewCompleted = ref(false)
const currentQuestionIndex = ref(0)
const timeRemaining = ref(600)
const showHints = ref(false)
const answers = ref<string[]>([])

let timerInterval: number | null = null

const questions = [
  // Technical - Easy
  {
    category: 'Coding',
    difficulty: 'Easy',
    question: 'Reverse a string without using built-in reverse methods.',
    context: 'Write a function that takes a string and returns it reversed.\n\nExample:\nInput: "hello"\nOutput: "olleh"',
    hints: ['Use a loop to iterate through the string', 'Build the reversed string character by character', 'Start from the end']
  },
  {
    category: 'Technical',
    difficulty: 'Easy',
    question: 'What is the difference between a list and a tuple in Python?',
    hints: ['Think about mutability', 'Consider use cases', 'Memory efficiency']
  },
  {
    category: 'Coding',
    difficulty: 'Easy',
    question: 'Find the maximum element in an array.',
    context: 'Write a function that finds the largest number in an array.\n\nExample:\nInput: [3, 7, 2, 9, 1]\nOutput: 9',
    hints: ['Iterate through the array', 'Keep track of the maximum value', 'Compare each element']
  },
  {
    category: 'Technical',
    difficulty: 'Easy',
    question: 'Explain what a dictionary is in Python and when you would use it.',
    hints: ['Key-value pairs', 'Fast lookups', 'Unordered collection']
  },
  {
    category: 'Coding',
    difficulty: 'Easy',
    question: 'Check if a number is even or odd.',
    context: 'Write a function that returns True if a number is even, False otherwise.\n\nExample:\nInput: 4\nOutput: True',
    hints: ['Use the modulo operator (%)', 'Check if remainder is 0']
  },
  
  // Technical - Medium
  {
    category: 'Coding',
    difficulty: 'Medium',
    question: 'Implement a function to check if a string is a palindrome.',
    context: 'A palindrome reads the same forwards and backwards.\n\nExample:\nInput: "racecar"\nOutput: True\nInput: "hello"\nOutput: False',
    hints: ['Compare characters from start and end', 'Move towards the center', 'Handle edge cases']
  },
  {
    category: 'Technical',
    difficulty: 'Medium',
    question: 'What is the time complexity of binary search? Explain why.',
    hints: ['Think about how the search space reduces', 'Each step eliminates half the possibilities', 'Logarithmic relationship']
  },
  {
    category: 'Coding',
    difficulty: 'Medium',
    question: 'Find the two numbers in an array that add up to a target sum.',
    context: 'Given an array of integers and a target sum, find two numbers that add up to the target.\n\nExample:\nInput: [2, 7, 11, 15], target = 9\nOutput: [2, 7]',
    hints: ['Use a hash map/dictionary', 'Store complements', 'Single pass solution']
  },
  {
    category: 'Technical',
    difficulty: 'Medium',
    question: 'Explain the difference between a stack and a queue. Give examples of when to use each.',
    hints: ['LIFO vs FIFO', 'Think about order of operations', 'Real-world applications']
  },
  {
    category: 'Coding',
    difficulty: 'Medium',
    question: 'Implement a function to find the factorial of a number using recursion.',
    context: 'Write a recursive function to calculate n!.\n\nExample:\nInput: 5\nOutput: 120',
    hints: ['Base case: factorial(0) = 1', 'Recursive case: n * factorial(n-1)', 'Handle edge cases']
  },
  
  // Technical - Hard
  {
    category: 'Coding',
    difficulty: 'Hard',
    question: 'Implement a function to find the longest common subsequence between two strings.',
    context: 'A subsequence is a sequence that appears in the same relative order, but not necessarily contiguous.\n\nExample:\nInput: "ABCDGH", "AEDFHR"\nOutput: 3 (ADH)',
    hints: ['Use dynamic programming', 'Create a 2D table', 'Build solution bottom-up']
  },
  {
    category: 'Technical',
    difficulty: 'Hard',
    question: 'Explain how garbage collection works in Python. What are the advantages and disadvantages?',
    hints: ['Reference counting', 'Cyclic reference detection', 'Performance implications']
  },
  {
    category: 'Coding',
    difficulty: 'Hard',
    question: 'Design a data structure that supports insert, delete, and getRandom in O(1) time.',
    context: 'All operations should be O(1) average time complexity.',
    hints: ['Use a combination of data structures', 'HashMap and Array', 'Swap and pop technique']
  },
  
  // Behavioral
  {
    category: 'Behavioral',
    difficulty: 'Easy',
    question: 'Tell me about yourself.',
    hints: ['Keep it professional', 'Highlight relevant experience', 'Connect to the role']
  },
  {
    category: 'Behavioral',
    difficulty: 'Easy',
    question: 'Why do you want to work here?',
    hints: ['Research the company', 'Show genuine interest', 'Connect your values']
  },
  {
    category: 'Behavioral',
    difficulty: 'Medium',
    question: 'Describe a time when you had to work under pressure. How did you handle it?',
    hints: ['Use STAR method', 'Be specific', 'Show positive outcome']
  },
  {
    category: 'Behavioral',
    difficulty: 'Medium',
    question: 'Tell me about a challenging project you worked on. What was your role and what did you learn?',
    hints: ['Focus on your contribution', 'Show problem-solving skills', 'Highlight learning']
  },
  {
    category: 'Behavioral',
    difficulty: 'Medium',
    question: 'How do you handle conflicts in a team setting?',
    hints: ['Show communication skills', 'Focus on resolution', 'Be diplomatic']
  },
  {
    category: 'Behavioral',
    difficulty: 'Hard',
    question: 'Describe a time when you failed. What did you learn from it?',
    hints: ['Be honest', 'Show growth mindset', 'Focus on learning']
  },
  {
    category: 'Behavioral',
    difficulty: 'Hard',
    question: 'Tell me about a time when you had to learn something new quickly. How did you approach it?',
    hints: ['Show learning ability', 'Be specific about methods', 'Demonstrate adaptability']
  }
]

const filteredQuestions = computed(() => {
  let filtered = questions

  // Filter by type
  if (selectedType.value === 'Technical') {
    filtered = filtered.filter(q => q.category === 'Technical' || q.category === 'Coding')
  } else if (selectedType.value === 'Behavioral') {
    filtered = filtered.filter(q => q.category === 'Behavioral')
  }
  // Mixed keeps all

  // Filter by difficulty
  if (selectedDifficulty.value !== 'All Levels') {
    filtered = filtered.filter(q => q.difficulty === selectedDifficulty.value)
  }

  // Shuffle and limit
  const shuffled = [...filtered].sort(() => Math.random() - 0.5)
  return shuffled.slice(0, numberOfQuestions.value)
})

const currentQuestion = computed(() => {
  return filteredQuestions.value[currentQuestionIndex.value]
})

const answeredCount = computed(() => {
  return answers.value.filter(a => a && a.trim()).length
})

const startInterview = () => {
  interviewStarted.value = true
  interviewCompleted.value = false
  currentQuestionIndex.value = 0
  answers.value = new Array(filteredQuestions.value.length).fill('')
  timeRemaining.value = timePerQuestion.value
  showHints.value = false
  
  if (timePerQuestion.value > 0) {
    startTimer()
  }
}

const startTimer = () => {
  if (timerInterval) {
    clearInterval(timerInterval)
  }
  
  timerInterval = window.setInterval(() => {
    if (timeRemaining.value > 0) {
      timeRemaining.value--
    } else {
      // Auto-advance to next question or complete if last
      if (currentQuestionIndex.value < filteredQuestions.value.length - 1) {
        nextQuestion()
      } else {
        completeInterview()
      }
    }
  }, 1000)
}

const nextQuestion = () => {
  if (currentQuestionIndex.value < filteredQuestions.value.length - 1) {
    currentQuestionIndex.value++
    timeRemaining.value = timePerQuestion.value
    showHints.value = false
  }
}

const previousQuestion = () => {
  if (currentQuestionIndex.value > 0) {
    currentQuestionIndex.value--
    timeRemaining.value = timePerQuestion.value
    showHints.value = false
  }
}

const completeInterview = () => {
  if (timerInterval) {
    clearInterval(timerInterval)
    timerInterval = null
  }
  interviewCompleted.value = true
  interviewStarted.value = false
}

const endInterview = () => {
  if (confirm('Are you sure you want to end the interview? Your progress will be saved.')) {
    completeInterview()
  }
}

const restartInterview = () => {
  interviewStarted.value = false
  interviewCompleted.value = false
  currentQuestionIndex.value = 0
  answers.value = []
  timeRemaining.value = timePerQuestion.value
  showHints.value = false
}

const exportAnswers = () => {
  const exportData = {
    type: selectedType.value,
    difficulty: selectedDifficulty.value,
    totalQuestions: filteredQuestions.value.length,
    answered: answeredCount.value,
    answers: filteredQuestions.value.map((q, index) => ({
      question: q.question,
      answer: answers.value[index] || 'Not answered',
      category: q.category,
      difficulty: q.difficulty
    }))
  }

  const blob = new Blob([JSON.stringify(exportData, null, 2)], { type: 'application/json' })
  const url = URL.createObjectURL(blob)
  const a = document.createElement('a')
  a.href = url
  a.download = `interview-answers-${new Date().toISOString().split('T')[0]}.json`
  document.body.appendChild(a)
  a.click()
  document.body.removeChild(a)
  URL.revokeObjectURL(url)
}

const formatTime = (seconds: number): string => {
  const mins = Math.floor(seconds / 60)
  const secs = seconds % 60
  return `${mins}:${secs.toString().padStart(2, '0')}`
}

onUnmounted(() => {
  if (timerInterval) {
    clearInterval(timerInterval)
  }
})
</script>
