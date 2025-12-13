<template>
  <div class="px-4 py-4 sm:py-6 sm:px-0">
    <!-- Exam Selection Screen -->
    <div v-if="!examStarted && !examCompleted" class="max-w-4xl mx-auto">
      <div class="mb-6 sm:mb-8 text-center">
        <h1 class="text-3xl sm:text-4xl font-bold text-msit-dark-50 mb-2 font-serif">Python Skills Gym</h1>
        <p class="text-sm sm:text-base text-msit-dark-200 font-sans">Test your Python skills in an exam-like environment</p>
      </div>

      <div class="grid grid-cols-1 md:grid-cols-2 gap-4 sm:gap-6">
        <div
          v-for="exam in availableExams"
          :key="exam.id"
          class="bg-msit-dark-800 border border-msit-dark-700 rounded-lg p-6 hover:border-msit-accent transition-all cursor-pointer"
          @click="startExam(exam)"
        >
          <div class="flex items-start justify-between mb-4">
            <h3 class="text-xl font-semibold text-msit-dark-50 font-sans">{{ exam.name }}</h3>
            <span :class="[
              'px-2.5 py-0.5 rounded-full text-xs font-medium font-sans',
              exam.difficulty === 'Beginner' ? 'bg-green-500/20 text-green-400' :
              exam.difficulty === 'Intermediate' ? 'bg-yellow-500/20 text-yellow-400' :
              'bg-red-500/20 text-red-400'
            ]">
              {{ exam.difficulty }}
            </span>
          </div>
          <p class="text-sm text-msit-dark-200 mb-4 font-sans">{{ exam.description }}</p>
          <div class="flex items-center gap-4 text-xs text-msit-dark-300 font-sans">
            <span class="flex items-center gap-1">
              <svg class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
              </svg>
              {{ exam.questions.length }} questions
            </span>
            <span class="flex items-center gap-1">
              <svg class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
              {{ exam.timeLimit }} min
            </span>
          </div>
        </div>
      </div>
    </div>

    <!-- Exam Interface -->
    <div v-if="examStarted && !examCompleted" class="max-w-6xl mx-auto">
      <!-- Header with Timer and Progress -->
      <div class="bg-msit-dark-800 border border-msit-dark-700 rounded-lg p-4 mb-4">
        <div class="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4">
          <div>
            <h2 class="text-xl font-bold text-msit-dark-50 font-serif">{{ currentExam?.name }}</h2>
            <p class="text-sm text-msit-dark-200 font-sans">Question {{ currentQuestionIndex + 1 }} of {{ currentExam?.questions.length }}</p>
          </div>
          <div class="flex items-center gap-4">
            <div class="text-right">
              <div class="text-sm font-semibold font-sans" :class="timeRemaining <= 60 ? 'text-red-400' : 'text-msit-dark-50'">
                {{ formatTime(timeRemaining) }}
              </div>
              <div class="text-xs text-msit-dark-300 font-sans">Time Remaining</div>
            </div>
            <button
              @click="submitExam"
              class="px-4 py-2 bg-red-600 hover:bg-red-700 text-white rounded-lg text-sm font-medium transition-colors font-sans"
            >
              Submit Exam
            </button>
          </div>
        </div>
        <!-- Progress Bar -->
        <div class="mt-4 w-full bg-msit-dark-700 rounded-full h-2">
          <div
            class="bg-msit-accent h-2 rounded-full transition-all duration-300"
            :style="{ width: `${((currentQuestionIndex + 1) / (currentExam?.questions.length || 1)) * 100}%` }"
          ></div>
        </div>
      </div>

      <!-- Question Card -->
      <div class="bg-msit-dark-800 border border-msit-dark-700 rounded-lg p-6 mb-4">
        <div class="mb-4">
          <h3 class="text-lg font-semibold text-msit-dark-50 mb-3 font-sans">
            Question {{ currentQuestionIndex + 1 }}
          </h3>
          <div class="bg-msit-dark-900 border border-msit-dark-700 rounded-lg p-4 mb-4">
            <p class="text-sm text-msit-dark-200 whitespace-pre-line font-sans">{{ currentQuestion?.problem }}</p>
          </div>
          
          <!-- Examples -->
          <div v-if="currentQuestion?.examples && currentQuestion.examples.length > 0" class="mb-4">
            <h4 class="text-sm font-semibold text-msit-dark-50 mb-2 font-sans">Examples:</h4>
            <div class="space-y-2">
              <div
                v-for="(example, idx) in currentQuestion.examples"
                :key="idx"
                class="bg-msit-dark-900 border border-msit-dark-700 rounded p-3"
              >
                <pre class="text-xs text-msit-dark-200 font-mono mb-1"><code>Input: {{ example.input }}</code></pre>
                <pre class="text-xs text-msit-dark-200 font-mono"><code>Output: {{ example.output }}</code></pre>
              </div>
            </div>
          </div>

          <!-- Constraints -->
          <div v-if="currentQuestion?.constraints" class="mb-4">
            <h4 class="text-sm font-semibold text-msit-dark-50 mb-2 font-sans">Constraints:</h4>
            <ul class="list-disc list-inside text-xs text-msit-dark-200 space-y-1 font-sans">
              <li v-for="(constraint, idx) in currentQuestion.constraints" :key="idx">{{ constraint }}</li>
            </ul>
          </div>
        </div>

        <!-- Code Editor -->
        <div class="mb-4">
          <label class="block text-sm font-medium text-msit-dark-50 mb-2 font-sans">Your Solution:</label>
          <textarea
            v-model="answers[currentQuestionIndex]"
            rows="15"
            class="w-full bg-msit-dark-900 text-msit-dark-50 placeholder-msit-dark-300 rounded-md font-mono text-sm px-4 py-3 border border-msit-dark-600 focus:border-msit-accent focus:ring-1 focus:ring-msit-accent resize-y"
            :placeholder="currentQuestion?.starterCode || '# Write your solution here'"
          ></textarea>
        </div>

        <!-- Test Results -->
        <div v-if="testResults[currentQuestionIndex]" class="mb-4">
          <h4 class="text-sm font-semibold text-msit-dark-50 mb-2 font-sans">Test Results:</h4>
          <div class="space-y-2">
            <div
              v-for="(result, idx) in testResults[currentQuestionIndex]"
              :key="idx"
              :class="[
                'p-3 rounded border',
                result.passed ? 'bg-green-900/20 border-green-700' : 'bg-red-900/20 border-red-700'
              ]"
            >
              <div class="flex items-center gap-2 mb-1">
                <span v-if="result.passed" class="text-green-400">✓</span>
                <span v-else class="text-red-400">✗</span>
                <span class="text-xs font-medium font-sans" :class="result.passed ? 'text-green-300' : 'text-red-300'">
                  Test Case {{ idx + 1 }}: {{ result.passed ? 'Passed' : 'Failed' }}
                </span>
              </div>
              <div v-if="!result.passed" class="text-xs text-red-200 mt-1 font-mono">
                Expected: {{ result.expected }}, Got: {{ result.actual }}
              </div>
            </div>
          </div>
        </div>

        <!-- Navigation Buttons -->
        <div class="flex items-center justify-between gap-4">
          <button
            @click="previousQuestion"
            :disabled="currentQuestionIndex === 0"
            class="px-4 py-2 border border-msit-dark-600 text-msit-dark-50 rounded-lg hover:bg-msit-dark-700 disabled:opacity-50 disabled:cursor-not-allowed transition-colors text-sm font-medium font-sans"
          >
            ← Previous
          </button>
          <div class="flex items-center gap-2">
            <button
              @click="runTests"
              :disabled="!answers[currentQuestionIndex] || isLoading"
              class="px-4 py-2 bg-msit-accent text-msit-dark rounded-lg hover:bg-msit-accent-500 disabled:opacity-50 disabled:cursor-not-allowed transition-colors text-sm font-medium font-sans"
            >
              {{ isLoading ? 'Running...' : 'Run Tests' }}
            </button>
            <button
              @click="nextQuestion"
              :disabled="currentQuestionIndex === (currentExam?.questions.length || 0) - 1"
              class="px-4 py-2 border border-msit-dark-600 text-msit-dark-50 rounded-lg hover:bg-msit-dark-700 disabled:opacity-50 disabled:cursor-not-allowed transition-colors text-sm font-medium font-sans"
            >
              Next →
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- Results Screen -->
    <div v-if="examCompleted" class="max-w-4xl mx-auto">
      <div class="bg-msit-dark-800 border border-msit-dark-700 rounded-lg p-6 sm:p-8">
        <div class="text-center mb-6">
          <h2 class="text-3xl font-bold text-msit-dark-50 mb-2 font-serif">Exam Completed!</h2>
          <div class="text-4xl font-bold mb-4 font-sans" :class="score >= 70 ? 'text-green-400' : score >= 50 ? 'text-yellow-400' : 'text-red-400'">
            {{ score }}%
          </div>
          <p class="text-sm text-msit-dark-200 font-sans">
            You scored {{ correctAnswers }} out of {{ currentExam?.questions.length }} questions correctly
          </p>
        </div>

        <!-- Question Review -->
        <div class="space-y-4 mb-6">
          <h3 class="text-lg font-semibold text-msit-dark-50 font-sans">Question Review:</h3>
          <div
            v-for="(question, idx) in currentExam?.questions"
            :key="idx"
            class="bg-msit-dark-900 border rounded-lg p-4"
            :class="questionResults[idx] ? 'border-green-700' : 'border-red-700'"
          >
            <div class="flex items-start justify-between mb-2">
              <span class="font-medium text-sm font-sans" :class="questionResults[idx] ? 'text-green-300' : 'text-red-300'">
                Question {{ idx + 1 }}: {{ questionResults[idx] ? '✓ Correct' : '✗ Incorrect' }}
              </span>
            </div>
            <p class="text-xs text-msit-dark-200 mb-2 font-sans">{{ question.problem.substring(0, 100) }}...</p>
          </div>
        </div>

        <!-- Actions -->
        <div class="flex flex-col sm:flex-row items-center justify-center gap-4">
          <button
            @click="restartExam"
            class="px-6 py-3 bg-msit-accent text-msit-dark rounded-lg hover:bg-msit-accent-500 transition-colors font-medium font-sans"
          >
            Try Another Exam
          </button>
          <button
            @click="exportResults"
            class="px-6 py-3 border border-msit-dark-600 text-msit-dark-50 rounded-lg hover:bg-msit-dark-700 transition-colors font-medium font-sans"
          >
            Export Results
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, onUnmounted } from 'vue'

interface TestCase {
  input: string
  output: string
}

interface Question {
  id: number
  problem: string
  examples?: TestCase[]
  constraints?: string[]
  testCases: TestCase[]
  starterCode?: string
}

interface Exam {
  id: number
  name: string
  description: string
  difficulty: string
  timeLimit: number
  questions: Question[]
}

const examStarted = ref(false)
const examCompleted = ref(false)
const currentExam = ref<Exam | null>(null)
const currentQuestionIndex = ref(0)
const answers = ref<string[]>([])
const testResults = ref<Record<number, Array<{ passed: boolean; expected: string; actual: string }>>>({})
const questionResults = ref<boolean[]>([])
const timeRemaining = ref(0)
const isLoading = ref(false)
let timerInterval: ReturnType<typeof setInterval> | null = null
let pyodide: any = null

const availableExams: Exam[] = [
  {
    id: 1,
    name: 'Python Basics',
    description: 'Fundamental Python concepts and syntax',
    difficulty: 'Beginner',
    timeLimit: 30,
    questions: [
      {
        id: 1,
        problem: 'Write a function called `add_numbers` that takes two parameters `a` and `b` and returns their sum.',
        examples: [
          { input: 'add_numbers(5, 3)', output: '8' },
          { input: 'add_numbers(-1, 1)', output: '0' }
        ],
        constraints: ['Both inputs are integers', 'Result should be an integer'],
        testCases: [
          { input: 'add_numbers(5, 3)', output: '8' },
          { input: 'add_numbers(-1, 1)', output: '0' },
          { input: 'add_numbers(10, -5)', output: '5' },
          { input: 'add_numbers(0, 0)', output: '0' }
        ],
        starterCode: 'def add_numbers(a, b):\n    # Your code here\n    pass'
      },
      {
        id: 2,
        problem: 'Write a function `find_max` that takes a list of numbers and returns the maximum value. Do not use Python\'s built-in `max()` function.',
        examples: [
          { input: 'find_max([1, 5, 3, 9, 2])', output: '9' },
          { input: 'find_max([-5, -2, -10])', output: '-2' }
        ],
        constraints: ['List contains at least one element', 'All elements are numbers'],
        testCases: [
          { input: 'find_max([1, 5, 3, 9, 2])', output: '9' },
          { input: 'find_max([-5, -2, -10])', output: '-2' },
          { input: 'find_max([42])', output: '42' },
          { input: 'find_max([1, 1, 1])', output: '1' }
        ],
        starterCode: 'def find_max(numbers):\n    # Your code here\n    pass'
      },
      {
        id: 3,
        problem: 'Write a function `count_vowels` that takes a string and returns the count of vowels (a, e, i, o, u). The function should be case-insensitive.',
        examples: [
          { input: 'count_vowels("Hello")', output: '2' },
          { input: 'count_vowels("Python Programming")', output: '5' }
        ],
        constraints: ['Input is a string', 'Case-insensitive matching'],
        testCases: [
          { input: 'count_vowels("Hello")', output: '2' },
          { input: 'count_vowels("Python Programming")', output: '5' },
          { input: 'count_vowels("xyz")', output: '0' },
          { input: 'count_vowels("AEIOU")', output: '5' }
        ],
        starterCode: 'def count_vowels(text):\n    # Your code here\n    pass'
      },
      {
        id: 4,
        problem: 'Write a function `reverse_string` that takes a string and returns it reversed. Do not use Python\'s built-in string reversal methods like `[::-1]` or `reversed()`.',
        examples: [
          { input: 'reverse_string("hello")', output: '"olleh"' },
          { input: 'reverse_string("Python")', output: '"nohtyP"' }
        ],
        constraints: ['Input is a non-empty string'],
        testCases: [
          { input: 'reverse_string("hello")', output: '"olleh"' },
          { input: 'reverse_string("Python")', output: '"nohtyP"' },
          { input: 'reverse_string("a")', output: '"a"' },
          { input: 'reverse_string("123")', output: '"321"' }
        ],
        starterCode: 'def reverse_string(text):\n    # Your code here\n    pass'
      },
      {
        id: 5,
        problem: 'Write a function `is_palindrome` that takes a string and returns True if it is a palindrome, False otherwise. Ignore case and non-alphanumeric characters.',
        examples: [
          { input: 'is_palindrome("racecar")', output: 'True' },
          { input: 'is_palindrome("Hello")', output: 'False' }
        ],
        constraints: ['Ignore case', 'Ignore spaces and punctuation'],
        testCases: [
          { input: 'is_palindrome("racecar")', output: 'True' },
          { input: 'is_palindrome("Hello")', output: 'False' },
          { input: 'is_palindrome("A man a plan a canal Panama")', output: 'True' },
          { input: 'is_palindrome("python")', output: 'False' }
        ],
        starterCode: 'def is_palindrome(text):\n    # Your code here\n    pass'
      }
    ]
  },
  {
    id: 2,
    name: 'Intermediate Python',
    description: 'More challenging problems requiring algorithms and data structures',
    difficulty: 'Intermediate',
    timeLimit: 45,
    questions: [
      {
        id: 1,
        problem: 'Write a function `fibonacci` that takes an integer n and returns a list containing the first n Fibonacci numbers. The Fibonacci sequence starts with 0 and 1.',
        examples: [
          { input: 'fibonacci(5)', output: '[0, 1, 1, 2, 3]' },
          { input: 'fibonacci(10)', output: '[0, 1, 1, 2, 3, 5, 8, 13, 21, 34]' }
        ],
        constraints: ['n is a positive integer', 'n >= 1'],
        testCases: [
          { input: 'fibonacci(5)', output: '[0, 1, 1, 2, 3]' },
          { input: 'fibonacci(10)', output: '[0, 1, 1, 2, 3, 5, 8, 13, 21, 34]' },
          { input: 'fibonacci(1)', output: '[0]' },
          { input: 'fibonacci(2)', output: '[0, 1]' }
        ],
        starterCode: 'def fibonacci(n):\n    # Your code here\n    pass'
      },
      {
        id: 2,
        problem: 'Write a function `two_sum` that takes a list of integers and a target integer. Return the indices of the two numbers that add up to the target. You may assume that each input has exactly one solution.',
        examples: [
          { input: 'two_sum([2, 7, 11, 15], 9)', output: '[0, 1]' },
          { input: 'two_sum([3, 2, 4], 6)', output: '[1, 2]' }
        ],
        constraints: ['Each input has exactly one solution', 'Cannot use the same element twice'],
        testCases: [
          { input: 'two_sum([2, 7, 11, 15], 9)', output: '[0, 1]' },
          { input: 'two_sum([3, 2, 4], 6)', output: '[1, 2]' },
          { input: 'two_sum([3, 3], 6)', output: '[0, 1]' },
          { input: 'two_sum([1, 2, 3, 4], 7)', output: '[2, 3]' }
        ],
        starterCode: 'def two_sum(nums, target):\n    # Your code here\n    pass'
      },
      {
        id: 3,
        problem: 'Write a function `are_anagrams` that takes two strings and returns True if they are anagrams (contain the same characters in different order), False otherwise. The function should be case-insensitive.',
        examples: [
          { input: 'are_anagrams("listen", "silent")', output: 'True' },
          { input: 'are_anagrams("hello", "world")', output: 'False' }
        ],
        constraints: ['Case-insensitive', 'Ignore spaces'],
        testCases: [
          { input: 'are_anagrams("listen", "silent")', output: 'True' },
          { input: 'are_anagrams("hello", "world")', output: 'False' },
          { input: 'are_anagrams("rail safety", "fairy tales")', output: 'True' },
          { input: 'are_anagrams("python", "typhon")', output: 'True' }
        ],
        starterCode: 'def are_anagrams(s1, s2):\n    # Your code here\n    pass'
      },
      {
        id: 4,
        problem: 'Write a function `merge_sorted` that takes two sorted lists and returns a new sorted list containing all elements from both lists.',
        examples: [
          { input: 'merge_sorted([1, 3, 5], [2, 4, 6])', output: '[1, 2, 3, 4, 5, 6]' },
          { input: 'merge_sorted([1, 2], [3, 4])', output: '[1, 2, 3, 4]' }
        ],
        constraints: ['Both input lists are sorted', 'Result should be sorted'],
        testCases: [
          { input: 'merge_sorted([1, 3, 5], [2, 4, 6])', output: '[1, 2, 3, 4, 5, 6]' },
          { input: 'merge_sorted([1, 2], [3, 4])', output: '[1, 2, 3, 4]' },
          { input: 'merge_sorted([], [1, 2])', output: '[1, 2]' },
          { input: 'merge_sorted([1, 2], [])', output: '[1, 2]' }
        ],
        starterCode: 'def merge_sorted(list1, list2):\n    # Your code here\n    pass'
      }
    ]
  }
]

const currentQuestion = computed(() => {
  return currentExam.value?.questions[currentQuestionIndex.value]
})

const correctAnswers = computed(() => {
  return questionResults.value.filter(r => r).length
})

const score = computed(() => {
  if (!currentExam.value) return 0
  return Math.round((correctAnswers.value / currentExam.value.questions.length) * 100)
})

const startExam = (exam: Exam) => {
  currentExam.value = exam
  examStarted.value = true
  examCompleted.value = false
  currentQuestionIndex.value = 0
  answers.value = new Array(exam.questions.length).fill('')
  testResults.value = {}
  questionResults.value = new Array(exam.questions.length).fill(false)
  timeRemaining.value = exam.timeLimit * 60 // Convert to seconds
  
  startTimer()
  loadPyodide()
}

const startTimer = () => {
  if (timerInterval) {
    clearInterval(timerInterval)
  }
  
  timerInterval = setInterval(() => {
    timeRemaining.value--
    if (timeRemaining.value <= 0) {
      submitExam()
    }
  }, 1000)
}

const formatTime = (seconds: number): string => {
  const mins = Math.floor(seconds / 60)
  const secs = seconds % 60
  return `${mins}:${secs.toString().padStart(2, '0')}`
}

const nextQuestion = () => {
  if (currentExam.value && currentQuestionIndex.value < currentExam.value.questions.length - 1) {
    currentQuestionIndex.value++
  }
}

const previousQuestion = () => {
  if (currentQuestionIndex.value > 0) {
    currentQuestionIndex.value--
  }
}

const loadPyodide = async () => {
  if (pyodide) return
  
  try {
    // @ts-ignore - Pyodide is loaded dynamically
    if ((window as any).loadPyodide) {
      // @ts-ignore
      pyodide = await (window as any).loadPyodide()
    } else {
      await new Promise((resolve) => {
        const script = document.createElement('script')
        script.src = "https://cdn.jsdelivr.net/pyodide/v0.25.0/full/pyodide.js"
        script.onload = async () => {
          // @ts-ignore
          pyodide = await window.loadPyodide()
          resolve(null)
        }
        document.head.appendChild(script)
      })
    }
  } catch (e) {
    console.error('Failed to load Pyodide:', e)
  }
}

const runTests = async () => {
  if (!pyodide || !currentQuestion.value || !answers.value[currentQuestionIndex.value]) return
  
  isLoading.value = true
  const question = currentQuestion.value
  const code = answers.value[currentQuestionIndex.value]
  const results: Array<{ passed: boolean; expected: string; actual: string }> = []
  
  try {
    // Execute the user's code first to define functions
    await pyodide.runPythonAsync(code)
    
    // Run each test case
    for (const testCase of question.testCases) {
      try {
        // Capture stdout
        let output = ''
        pyodide.setStdout({ batched: (msg: string) => {
          output += msg
        }})
        
        // Execute the test case and capture result
        const testCode = `
import json
import sys

# Execute the test case
try:
    result = ${testCase.input}
    # Convert result to JSON-like string representation
    if isinstance(result, bool):
        result_str = str(result)
    elif isinstance(result, (int, float)):
        result_str = str(result)
    elif isinstance(result, str):
        result_str = repr(result)  # Use repr to preserve quotes
    elif isinstance(result, (list, tuple)):
        result_str = str(result).replace("'", '"') if isinstance(result, tuple) else str(result)
    elif isinstance(result, dict):
        result_str = str(result)
    else:
        result_str = str(result)
    sys.stdout.write("RESULT:" + result_str + "\\n")
except Exception as e:
    sys.stdout.write("ERROR:" + str(e) + "\\n")
`
        
        await pyodide.runPythonAsync(testCode)
        
        // Extract result from output
        let actualStr = ''
        if (output.includes('RESULT:')) {
          actualStr = output.split('RESULT:')[1].split('\n')[0].trim()
        } else if (output.includes('ERROR:')) {
          const errorMsg = output.split('ERROR:')[1].split('\n')[0].trim()
          results.push({
            passed: false,
            expected: testCase.output,
            actual: `Error: ${errorMsg}`
          })
          continue
        } else {
          results.push({
            passed: false,
            expected: testCase.output,
            actual: 'No output produced'
          })
          continue
        }
        
        const expectedStr = testCase.output.trim()
        
        // Normalize comparison - handle different representations
        const normalize = (str: string) => {
          // Remove extra quotes, normalize whitespace
          return str.replace(/^['"]|['"]$/g, '').replace(/\s+/g, ' ').trim()
        }
        
        const normalizedActual = normalize(actualStr)
        const normalizedExpected = normalize(expectedStr)
        
        // Compare: try exact match, normalized match, and whitespace-ignored match
        const passed = actualStr === expectedStr || 
                      normalizedActual === normalizedExpected ||
                      actualStr.replace(/\s/g, '') === expectedStr.replace(/\s/g, '') ||
                      JSON.stringify(actualStr) === JSON.stringify(expectedStr)
        
        results.push({
          passed,
          expected: expectedStr,
          actual: actualStr
        })
      } catch (e: any) {
        results.push({
          passed: false,
          expected: testCase.output,
          actual: `Error: ${e.message || String(e)}`
        })
      }
    }
    
    testResults.value[currentQuestionIndex.value] = results
    questionResults.value[currentQuestionIndex.value] = results.every(r => r.passed)
  } catch (e: any) {
    // Code execution error
    const errorMsg = e.message || String(e)
    question.testCases.forEach(() => {
      results.push({
        passed: false,
        expected: 'Valid output',
        actual: `Error: ${errorMsg}`
      })
    })
    testResults.value[currentQuestionIndex.value] = results
    questionResults.value[currentQuestionIndex.value] = false
  } finally {
    isLoading.value = false
    // Reset stdout
    pyodide.setStdout({ batched: () => {} })
  }
}

const submitExam = () => {
  if (timerInterval) {
    clearInterval(timerInterval)
    timerInterval = null
  }
  
  examCompleted.value = true
  examStarted.value = false
}

const restartExam = () => {
  examStarted.value = false
  examCompleted.value = false
  currentExam.value = null
  currentQuestionIndex.value = 0
  answers.value = []
  testResults.value = {}
  questionResults.value = []
  timeRemaining.value = 0
}

const exportResults = () => {
  if (!currentExam.value) return
  
  const results = {
    examName: currentExam.value.name,
    score: score.value,
    correctAnswers: correctAnswers.value,
    totalQuestions: currentExam.value.questions.length,
    timeSpent: formatTime((currentExam.value.timeLimit * 60) - timeRemaining.value),
    questions: currentExam.value.questions.map((q, idx) => ({
      question: q.problem,
      passed: questionResults.value[idx],
      answer: answers.value[idx]
    }))
  }
  
  const blob = new Blob([JSON.stringify(results, null, 2)], { type: 'application/json' })
  const url = URL.createObjectURL(blob)
  const a = document.createElement('a')
  a.href = url
  a.download = `exam-results-${new Date().toISOString().split('T')[0]}.json`
  document.body.appendChild(a)
  a.click()
  document.body.removeChild(a)
  URL.revokeObjectURL(url)
}

onMounted(() => {
  loadPyodide()
})

onUnmounted(() => {
  if (timerInterval) {
    clearInterval(timerInterval)
  }
})
</script>









