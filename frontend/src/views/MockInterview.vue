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

      <!-- Interview Tips Panel -->
      <div v-if="showInterviewTips" class="mb-6 bg-blue-500/10 border border-blue-500/30 rounded-lg p-4">
        <div class="flex items-start justify-between">
          <div class="flex-1">
            <h4 class="text-sm font-semibold text-blue-300 mb-2 font-sans flex items-center">
              <svg class="h-4 w-4 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
              Interview Tip
            </h4>
            <p class="text-xs text-blue-200 font-sans">{{ currentInterviewTip }}</p>
          </div>
          <button
            @click="showInterviewTips = false"
            class="text-blue-300 hover:text-blue-200 transition-colors"
          >
            <svg class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
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
            <div class="flex items-center gap-2">
              <button
                @click="showHints = !showHints"
                class="text-xs text-msit-accent hover:text-msit-accent-300 font-sans"
              >
                {{ showHints ? 'Hide' : 'Show' }} Hints
              </button>
              <button
                v-if="currentQuestion.testCases && currentQuestion.testCases.length > 0"
                @click="runTestsForQuestion"
                :disabled="!answers[currentQuestionIndex] || isLoadingTests"
                class="text-xs px-3 py-1 bg-green-600 hover:bg-green-700 text-white rounded transition-colors font-sans disabled:opacity-50 disabled:cursor-not-allowed"
              >
                {{ isLoadingTests ? 'Testing...' : 'Test Solution' }}
              </button>
            </div>
          </div>
          <textarea
            v-model="answers[currentQuestionIndex]"
            :placeholder="currentQuestion.starterCode || 'Write your solution here...'"
            class="w-full h-64 px-4 py-3 bg-msit-dark-900 border border-msit-dark-600 rounded-lg text-msit-dark-50 font-mono text-sm focus:border-msit-accent focus:outline-none resize-y"
          ></textarea>
          
          <!-- Test Results for Coding Questions -->
          <div v-if="testResults[currentQuestionIndex] && testResults[currentQuestionIndex].length > 0" class="mt-4">
            <div class="flex items-center justify-between mb-2">
              <h4 class="text-sm font-semibold text-msit-dark-50 font-sans">Test Results:</h4>
              <span :class="[
                'px-2 py-1 rounded text-xs font-medium font-sans',
                allTestsPassed(currentQuestionIndex) ? 'bg-green-500/20 text-green-400' : 'bg-red-500/20 text-red-400'
              ]">
                {{ passedTestsCount(currentQuestionIndex) }} / {{ testResults[currentQuestionIndex].length }} passed
              </span>
            </div>
            <div class="space-y-2">
              <div
                v-for="(result, idx) in testResults[currentQuestionIndex]"
                :key="idx"
                :class="[
                  'p-3 rounded-lg border font-sans',
                  result.passed ? 'bg-green-500/10 border-green-500/30' : 'bg-red-500/10 border-red-500/30'
                ]"
              >
                <div class="flex items-start gap-2">
                  <svg v-if="result.passed" class="h-5 w-5 text-green-400 shrink-0 mt-0.5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
                  </svg>
                  <svg v-else class="h-5 w-5 text-red-400 shrink-0 mt-0.5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 14l2-2m0 0l2-2m-2 2l-2-2m2 2l2 2m7-2a9 9 0 11-18 0 9 9 0 0118 0z" />
                  </svg>
                  <div class="flex-1">
                    <div class="text-xs font-mono text-msit-dark-200 mb-1">
                      <span class="font-semibold">Test {{ idx + 1 }}:</span> {{ result.testCase.input }}
                    </div>
                    <div v-if="result.passed" class="text-xs text-green-400">
                      ✓ Passed - Output: {{ result.actual }}
                    </div>
                    <div v-else class="text-xs space-y-1">
                      <div class="text-red-400">
                        ✗ Failed
                      </div>
                      <div class="text-msit-dark-300">
                        <span class="font-semibold">Expected:</span> {{ result.expected }}
                      </div>
                      <div class="text-msit-dark-300">
                        <span class="font-semibold">Got:</span> {{ result.actual }}
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
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
        <div class="grid grid-cols-2 sm:grid-cols-4 gap-4 mb-6">
          <div class="bg-msit-dark-900 border border-msit-dark-700 rounded-lg p-4">
            <div class="text-2xl font-bold text-msit-accent">{{ filteredQuestions.length }}</div>
            <div class="text-sm text-msit-dark-200 font-sans">Total Questions</div>
          </div>
          <div class="bg-msit-dark-900 border border-msit-dark-700 rounded-lg p-4">
            <div class="text-2xl font-bold text-msit-accent">{{ answeredCount }}</div>
            <div class="text-sm text-msit-dark-200 font-sans">Answered</div>
          </div>
          <div class="bg-msit-dark-900 border border-msit-dark-700 rounded-lg p-4">
            <div class="text-2xl font-bold" :class="codingScore >= 70 ? 'text-green-400' : codingScore >= 50 ? 'text-yellow-400' : 'text-red-400'">
              {{ codingScore }}%
            </div>
            <div class="text-sm text-msit-dark-200 font-sans">Coding Score</div>
          </div>
          <div class="bg-msit-dark-900 border border-msit-dark-700 rounded-lg p-4">
            <div class="text-2xl font-bold text-msit-accent">{{ averageTimePerQuestion }}</div>
            <div class="text-sm text-msit-dark-200 font-sans">Avg Time/Q</div>
          </div>
        </div>

        <!-- Performance Analysis -->
        <div v-if="performanceAnalysis" class="mb-6 bg-msit-dark-900 border border-msit-dark-700 rounded-lg p-4">
          <h3 class="text-lg font-semibold text-msit-dark-50 mb-3 font-sans">Performance Analysis</h3>
          <div class="space-y-3">
            <div v-for="(analysis, index) in performanceAnalysis" :key="index" class="bg-msit-dark-800 border border-msit-dark-600 rounded p-3">
              <div class="flex items-start gap-2">
                <span class="text-msit-accent text-lg">💡</span>
                <div>
                  <p class="text-sm text-msit-dark-200 font-sans">{{ analysis }}</p>
                </div>
              </div>
            </div>
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
              <div class="flex items-center gap-2">
                <span v-if="question.category === 'Coding' && question.testCases && testResults[index]" :class="[
                  'px-2 py-1 rounded text-xs font-medium font-sans',
                  allTestsPassed(index) ? 'bg-green-500/20 text-green-400' : 
                  passedTestsCount(index) > 0 ? 'bg-yellow-500/20 text-yellow-400' : 'bg-red-500/20 text-red-400'
                ]">
                  {{ passedTestsCount(index) }}/{{ testResults[index].length }} tests passed
                </span>
                <span :class="[
                  'px-2 py-1 rounded text-xs font-medium font-sans',
                  answers[index] && answers[index].trim() ? 'bg-green-500/20 text-green-400' : 'bg-red-500/20 text-red-400'
                ]">
                  {{ answers[index] && answers[index].trim() ? 'Answered' : 'Not Answered' }}
                </span>
              </div>
            </div>
            <p class="text-sm text-msit-dark-200 mb-2 font-sans">{{ question.question }}</p>
            <div v-if="answers[index] && answers[index].trim()" class="mt-2 p-3 bg-msit-dark-800 rounded border border-msit-dark-600">
              <pre class="text-sm text-msit-dark-100 whitespace-pre-wrap font-mono">{{ answers[index] }}</pre>
            </div>
            <p v-else class="text-sm text-msit-dark-300 italic font-sans">No answer provided</p>
            
            <!-- Show test results for coding questions -->
            <div v-if="question.category === 'Coding' && testResults[index] && testResults[index].length > 0" class="mt-3 space-y-2">
              <div
                v-for="(result, testIdx) in testResults[index]"
                :key="testIdx"
                :class="[
                  'p-2 rounded text-xs font-sans',
                  result.passed ? 'bg-green-500/10 border border-green-500/30' : 'bg-red-500/10 border border-red-500/30'
                ]"
              >
                <div class="flex items-center gap-2">
                  <span v-if="result.passed" class="text-green-400">✓</span>
                  <span v-else class="text-red-400">✗</span>
                  <span class="text-msit-dark-200">Test {{ testIdx + 1 }}: {{ result.passed ? 'Passed' : 'Failed' }}</span>
                </div>
                <div v-if="!result.passed" class="mt-1 text-msit-dark-300 text-xs">
                  Expected: {{ result.expected }}, Got: {{ result.actual }}
                </div>
              </div>
            </div>
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
import { runTests, loadPyodide, type TestCase, type TestResult } from '../utils/testRunner'

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
const showInterviewTips = ref(true)
const answers = ref<string[]>([])
const testResults = ref<Record<number, TestResult[]>>({})
const isLoadingTests = ref(false)
const questionStartTimes = ref<number[]>([])
const questionEndTimes = ref<number[]>([])

let timerInterval: number | null = null
let pyodide: any = null

const questions = [
  // Technical - Easy
  {
    category: 'Coding',
    difficulty: 'Easy',
    question: 'Reverse a string without using built-in reverse methods.',
    context: 'Write a function that takes a string and returns it reversed.\n\nExample:\nInput: "hello"\nOutput: "olleh"',
    hints: ['Use a loop to iterate through the string', 'Build the reversed string character by character', 'Start from the end'],
    starterCode: 'def reverse_string(text):\n    # Your code here\n    pass',
    testCases: [
      { input: 'reverse_string("hello")', output: '"olleh"' },
      { input: 'reverse_string("Python")', output: '"nohtyP"' },
      { input: 'reverse_string("a")', output: '"a"' },
      { input: 'reverse_string("123")', output: '"321"' }
    ]
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
    hints: ['Iterate through the array', 'Keep track of the maximum value', 'Compare each element'],
    starterCode: 'def find_max(numbers):\n    # Your code here\n    pass',
    testCases: [
      { input: 'find_max([3, 7, 2, 9, 1])', output: '9' },
      { input: 'find_max([-5, -2, -10])', output: '-2' },
      { input: 'find_max([42])', output: '42' },
      { input: 'find_max([1, 1, 1])', output: '1' }
    ]
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
    hints: ['Use the modulo operator (%)', 'Check if remainder is 0'],
    starterCode: 'def is_even(number):\n    # Your code here\n    pass',
    testCases: [
      { input: 'is_even(4)', output: 'True' },
      { input: 'is_even(5)', output: 'False' },
      { input: 'is_even(0)', output: 'True' },
      { input: 'is_even(-2)', output: 'True' }
    ]
  },
  
  // Technical - Medium
  {
    category: 'Coding',
    difficulty: 'Medium',
    question: 'Implement a function to check if a string is a palindrome.',
    context: 'A palindrome reads the same forwards and backwards.\n\nExample:\nInput: "racecar"\nOutput: True\nInput: "hello"\nOutput: False',
    hints: ['Compare characters from start and end', 'Move towards the center', 'Handle edge cases'],
    starterCode: 'def is_palindrome(text):\n    # Your code here\n    pass',
    testCases: [
      { input: 'is_palindrome("racecar")', output: 'True' },
      { input: 'is_palindrome("hello")', output: 'False' },
      { input: 'is_palindrome("a")', output: 'True' },
      { input: 'is_palindrome("madam")', output: 'True' }
    ]
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
    hints: ['Use a hash map/dictionary', 'Store complements', 'Single pass solution'],
    starterCode: 'def two_sum(numbers, target):\n    # Your code here\n    pass',
    testCases: [
      { input: 'two_sum([2, 7, 11, 15], 9)', output: '[2, 7]' },
      { input: 'two_sum([3, 2, 4], 6)', output: '[2, 4]' },
      { input: 'two_sum([3, 3], 6)', output: '[3, 3]' }
    ]
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
    hints: ['Base case: factorial(0) = 1', 'Recursive case: n * factorial(n-1)', 'Handle edge cases'],
    starterCode: 'def factorial(n):\n    # Your code here\n    pass',
    testCases: [
      { input: 'factorial(5)', output: '120' },
      { input: 'factorial(0)', output: '1' },
      { input: 'factorial(1)', output: '1' },
      { input: 'factorial(3)', output: '6' }
    ]
  },
  
  // Technical - Hard
  {
    category: 'Coding',
    difficulty: 'Hard',
    question: 'Implement a function to find the longest common subsequence between two strings.',
    context: 'A subsequence is a sequence that appears in the same relative order, but not necessarily contiguous.\n\nExample:\nInput: "ABCDGH", "AEDFHR"\nOutput: 3 (ADH)',
    hints: ['Use dynamic programming', 'Create a 2D table', 'Build solution bottom-up'],
    starterCode: 'def longest_common_subsequence(s1, s2):\n    # Your code here\n    pass',
    testCases: [
      { input: 'longest_common_subsequence("ABCDGH", "AEDFHR")', output: '3' },
      { input: 'longest_common_subsequence("AGGTAB", "GXTXAYB")', output: '4' },
      { input: 'longest_common_subsequence("", "ABC")', output: '0' }
    ]
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
    question: 'Count the number of vowels in a string.',
    context: 'Write a function that counts vowels (a, e, i, o, u) in a string. Case-insensitive.\n\nExample:\nInput: "Hello"\nOutput: 2',
    hints: ['Convert to lowercase', 'Check each character', 'Use a set or string of vowels'],
    starterCode: 'def count_vowels(text):\n    # Your code here\n    pass',
    testCases: [
      { input: 'count_vowels("Hello")', output: '2' },
      { input: 'count_vowels("Python")', output: '1' },
      { input: 'count_vowels("AEIOU")', output: '5' },
      { input: 'count_vowels("xyz")', output: '0' }
    ]
  },
  {
    category: 'Coding',
    difficulty: 'Easy',
    question: 'Sum all numbers in a list.',
    context: 'Write a function that sums all numbers in a list.\n\nExample:\nInput: [1, 2, 3, 4]\nOutput: 10',
    hints: ['Use a loop', 'Initialize sum to 0', 'Add each number'],
    starterCode: 'def sum_list(numbers):\n    # Your code here\n    pass',
    testCases: [
      { input: 'sum_list([1, 2, 3, 4])', output: '10' },
      { input: 'sum_list([5, -3, 2])', output: '4' },
      { input: 'sum_list([0])', output: '0' },
      { input: 'sum_list([-1, -2, -3])', output: '-6' }
    ]
  },
  {
    category: 'Coding',
    difficulty: 'Medium',
    question: 'Find duplicates in a list.',
    context: 'Write a function that returns a list of duplicate elements.\n\nExample:\nInput: [1, 2, 2, 3, 4, 4, 5]\nOutput: [2, 4]',
    hints: ['Use a dictionary to count', 'Track elements that appear more than once', 'Return unique duplicates'],
    starterCode: 'def find_duplicates(lst):\n    # Your code here\n    pass',
    testCases: [
      { input: 'find_duplicates([1, 2, 2, 3, 4, 4, 5])', output: '[2, 4]' },
      { input: 'find_duplicates([1, 2, 3])', output: '[]' },
      { input: 'find_duplicates([1, 1, 1, 2, 2])', output: '[1, 2]' }
    ]
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

const codingScore = computed(() => {
  const codingQuestions = filteredQuestions.value.filter(q => q.category === 'Coding' && q.testCases)
  if (codingQuestions.length === 0) return 0
  
  let totalTests = 0
  let passedTests = 0
  
  codingQuestions.forEach((question, index) => {
    const questionIndex = filteredQuestions.value.indexOf(question)
    if (testResults.value[questionIndex]) {
      totalTests += testResults.value[questionIndex].length
      passedTests += testResults.value[questionIndex].filter(r => r.passed).length
    }
  })
  
  return totalTests > 0 ? Math.round((passedTests / totalTests) * 100) : 0
})

const averageTimePerQuestion = computed(() => {
  if (questionStartTimes.value.length === 0) return '0:00'
  const totalTime = questionEndTimes.value.reduce((sum, end, idx) => {
    const start = questionStartTimes.value[idx] || 0
    return sum + (end - start)
  }, 0)
  const avgSeconds = Math.round(totalTime / questionStartTimes.value.length)
  return formatTime(avgSeconds)
})

const performanceAnalysis = computed(() => {
  if (!interviewCompleted.value) return []
  
  const analysis: string[] = []
  const codingQuestions = filteredQuestions.value.filter(q => q.category === 'Coding')
  const behavioralQuestions = filteredQuestions.value.filter(q => q.category === 'Behavioral')
  
  // Coding performance
  if (codingQuestions.length > 0) {
    const codingAnswered = codingQuestions.filter((q, idx) => {
      const questionIndex = filteredQuestions.value.indexOf(q)
      return answers.value[questionIndex] && answers.value[questionIndex].trim()
    }).length
    
    if (codingScore.value >= 80) {
      analysis.push(`Excellent coding performance! You passed ${codingScore.value}% of test cases.`)
    } else if (codingScore.value >= 60) {
      analysis.push(`Good coding performance. You passed ${codingScore.value}% of test cases. Consider practicing more edge cases.`)
    } else if (codingScore.value > 0) {
      analysis.push(`You're on the right track! You passed ${codingScore.value}% of test cases. Review your solutions and test them thoroughly.`)
    } else if (codingAnswered > 0) {
      analysis.push(`You attempted ${codingAnswered} coding questions but none passed tests. Review the test cases and debug your solutions.`)
    }
  }
  
  // Answer completeness
  const completionRate = Math.round((answeredCount.value / filteredQuestions.value.length) * 100)
  if (completionRate === 100) {
    analysis.push('Great job answering all questions! This shows good time management.')
  } else if (completionRate >= 80) {
    analysis.push(`You answered ${completionRate}% of questions. Try to answer all questions, even briefly.`)
  } else {
    analysis.push(`You answered ${completionRate}% of questions. Practice managing your time better to answer more questions.`)
  }
  
  // Behavioral questions
  if (behavioralQuestions.length > 0) {
    const behavioralAnswered = behavioralQuestions.filter((q, idx) => {
      const questionIndex = filteredQuestions.value.indexOf(q)
      return answers.value[questionIndex] && answers.value[questionIndex].trim()
    }).length
    
    if (behavioralAnswered === behavioralQuestions.length) {
      analysis.push('You answered all behavioral questions. Remember to use the STAR method (Situation, Task, Action, Result) for structured responses.')
    }
  }
  
  return analysis
})

const currentInterviewTip = computed(() => {
  const tips = [
    'Take a moment to understand the question before jumping into coding. Ask clarifying questions if needed.',
    'For coding questions, start with a simple approach, then optimize if time permits.',
    'Use the test button to verify your solution works before moving on.',
    'For behavioral questions, use the STAR method: Situation, Task, Action, Result.',
    'Don\'t panic if you don\'t know the answer immediately. Think out loud and show your problem-solving process.',
    'Time management is crucial. Don\'t spend too long on one question.',
    'Write clean, readable code. Interviewers value code quality over clever tricks.',
    'Test your code with edge cases: empty inputs, single elements, negative numbers, etc.',
    'Explain your thought process as you code. Communication is as important as coding skills.',
    'If stuck, use hints but try to solve it yourself first. Practice makes perfect.'
  ]
  
  const tipIndex = currentQuestionIndex.value % tips.length
  return tips[tipIndex]
})

const passedTestsCount = (questionIndex: number): number => {
  if (!testResults.value[questionIndex]) return 0
  return testResults.value[questionIndex].filter(r => r.passed).length
}

const allTestsPassed = (questionIndex: number): boolean => {
  if (!testResults.value[questionIndex] || testResults.value[questionIndex].length === 0) return false
  return testResults.value[questionIndex].every(r => r.passed)
}

const startInterview = async () => {
  interviewStarted.value = true
  interviewCompleted.value = false
  currentQuestionIndex.value = 0
  answers.value = new Array(filteredQuestions.value.length).fill('')
  testResults.value = {}
  timeRemaining.value = timePerQuestion.value
  showHints.value = false
  showInterviewTips.value = true
  questionStartTimes.value = []
  questionEndTimes.value = []
  
  // Initialize starter code for coding questions
  filteredQuestions.value.forEach((q, idx) => {
    if (q.category === 'Coding' && q.starterCode) {
      answers.value[idx] = q.starterCode
    }
  })
  
  // Load Pyodide for code execution
  if (!pyodide) {
    try {
      pyodide = await loadPyodide()
    } catch (error) {
      console.error('Failed to load Pyodide:', error)
    }
  }
  
  // Record start time for first question
  questionStartTimes.value[0] = Date.now()
  
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
  // Record end time for current question
  questionEndTimes.value[currentQuestionIndex.value] = Date.now()
  
  if (currentQuestionIndex.value < filteredQuestions.value.length - 1) {
    currentQuestionIndex.value++
    timeRemaining.value = timePerQuestion.value
    showHints.value = false
    
    // Record start time for new question
    questionStartTimes.value[currentQuestionIndex.value] = Date.now()
  }
}

const previousQuestion = () => {
  // Record end time for current question
  questionEndTimes.value[currentQuestionIndex.value] = Date.now()
  
  if (currentQuestionIndex.value > 0) {
    currentQuestionIndex.value--
    timeRemaining.value = timePerQuestion.value
    showHints.value = false
    
    // Record start time for previous question (if not already recorded)
    if (!questionStartTimes.value[currentQuestionIndex.value]) {
      questionStartTimes.value[currentQuestionIndex.value] = Date.now()
    }
  }
}

const runTestsForQuestion = async () => {
  const question = currentQuestion.value
  if (!question || question.category !== 'Coding' || !question.testCases || !answers.value[currentQuestionIndex.value] || !pyodide) {
    return
  }
  
  isLoadingTests.value = true
  
  try {
    const results = await runTests(pyodide, answers.value[currentQuestionIndex.value], question.testCases)
    testResults.value[currentQuestionIndex.value] = results
  } catch (error: any) {
    console.error('Test execution error:', error)
    testResults.value[currentQuestionIndex.value] = question.testCases.map((testCase: TestCase) => ({
      passed: false,
      expected: testCase.output,
      actual: `Error: ${error.message || String(error)}`,
      testCase
    }))
  } finally {
    isLoadingTests.value = false
  }
}

const completeInterview = () => {
  // Record end time for current question
  questionEndTimes.value[currentQuestionIndex.value] = Date.now()
  
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

onMounted(async () => {
  // Preload Pyodide
  try {
    pyodide = await loadPyodide()
  } catch (error) {
    console.error('Failed to load Pyodide:', error)
  }
})

onUnmounted(() => {
  if (timerInterval) {
    clearInterval(timerInterval)
  }
})
</script>



