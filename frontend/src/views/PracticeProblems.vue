<template>
  <div class="px-4 py-4 sm:py-6 sm:px-0">
    <div class="mb-6 sm:mb-8">
      <h1 class="text-2xl sm:text-3xl font-bold text-msit-dark-50 mb-2 font-serif">Practice Problems</h1>
      <p class="text-sm sm:text-base text-msit-dark-200 font-sans">Solve coding challenges to improve your Python skills</p>
    </div>

    <!-- Search and Filter -->
    <div class="mb-6 bg-msit-dark-800 p-4 sm:p-6 rounded-lg shadow border border-msit-dark-700">
      <div class="grid grid-cols-1 gap-4 sm:grid-cols-3">
        <div>
          <label for="search" class="block text-sm font-semibold text-msit-dark-50 mb-2 font-sans">Search</label>
          <input
            id="search"
            v-model="searchQuery"
            type="text"
            placeholder="Search problems..."
            class="block w-full rounded-md border-msit-dark-600 bg-msit-dark-700 text-msit-dark-50 placeholder-msit-dark-300 shadow-sm focus:border-msit-accent focus:ring-msit-accent text-sm sm:text-base px-3 py-2.5 border font-sans"
          />
        </div>
        <div>
          <label for="difficulty" class="block text-sm font-semibold text-msit-dark-50 mb-2 font-sans">Difficulty</label>
          <select
            id="difficulty"
            v-model="selectedDifficulty"
            class="block w-full rounded-md border-msit-dark-600 bg-msit-dark-700 text-msit-dark-50 shadow-sm focus:border-msit-accent focus:ring-msit-accent text-sm sm:text-base px-3 py-2.5 border font-sans"
          >
            <option value="">All Levels</option>
            <option value="beginner">Beginner</option>
            <option value="intermediate">Intermediate</option>
            <option value="advanced">Advanced</option>
          </select>
        </div>
        <div>
          <label for="topic" class="block text-sm font-semibold text-msit-dark-50 mb-2 font-sans">Topic</label>
          <select
            id="topic"
            v-model="selectedTopic"
            class="block w-full rounded-md border-msit-dark-600 bg-msit-dark-700 text-msit-dark-50 shadow-sm focus:border-msit-accent focus:ring-msit-accent text-sm sm:text-base px-3 py-2.5 border font-sans"
          >
            <option value="">All Topics</option>
            <option v-for="topic in topics" :key="topic" :value="topic">{{ topic }}</option>
            <option v-if="loadingTopics" value="" disabled>Loading topics...</option>
          </select>
        </div>
      </div>
    </div>

    <!-- Problems Grid -->
    <div v-if="loadingProblems" class="text-center py-12">
      <p class="text-msit-dark-200 font-sans">Loading problems...</p>
    </div>
    <div v-else-if="filteredProblems.length === 0" class="text-center py-12">
      <p class="text-msit-dark-200 font-sans">No problems found</p>
    </div>

    <div v-else class="grid grid-cols-1 gap-4 sm:gap-6 lg:grid-cols-2">
      <div
        v-for="problem in filteredProblems"
        :key="problem.id"
        class="bg-msit-dark-800 overflow-hidden shadow rounded-lg hover:shadow-lg transition-shadow border border-msit-dark-700 hover:border-msit-accent"
      >
        <div class="p-4 sm:p-6">
          <div class="flex items-start justify-between mb-3">
            <div class="flex-1">
              <h3 class="text-lg sm:text-xl font-semibold text-msit-dark-50 mb-2 font-sans">
                {{ problem.title }}
              </h3>
              <div class="flex flex-wrap gap-2 mb-3">
                <span
                  :class="[
                    'inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium font-sans',
                    problem.difficulty === 'beginner' ? 'bg-green-500/20 text-green-400' :
                    problem.difficulty === 'intermediate' ? 'bg-yellow-500/20 text-yellow-400' :
                    'bg-red-500/20 text-red-400'
                  ]"
                >
                  {{ problem.difficulty }}
                </span>
                <span
                  v-for="tag in problem.tags"
                  :key="tag"
                  class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-msit-accent/20 text-msit-accent font-sans"
                >
                  {{ tag }}
                </span>
              </div>
            </div>
          </div>
          
          <p class="text-sm text-msit-dark-200 mb-4 font-sans">
            {{ problem.description }}
          </p>

          <div class="flex items-center justify-between pt-4 border-t border-msit-dark-700">
            <div class="text-xs text-msit-dark-300 font-sans">
              <span>{{ problem.points }} points</span>
              <span class="mx-2">•</span>
              <span>{{ problem.estimatedTime }} min</span>
            </div>
            <button
              @click="openProblem(problem)"
              class="inline-flex items-center px-4 py-2 border border-transparent text-sm font-semibold rounded-md text-msit-dark bg-msit-accent hover:bg-msit-accent-500 transition-colors font-sans"
            >
              Start Problem
              <svg class="ml-2 h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7" />
              </svg>
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- Problem Detail Modal -->
    <div
      v-if="selectedProblem"
      class="fixed inset-0 bg-black/50 flex items-center justify-center p-4 z-50"
      @click.self="selectedProblem = null"
    >
      <div class="bg-msit-dark-800 rounded-lg shadow-xl max-w-4xl w-full max-h-[90vh] overflow-y-auto border border-msit-dark-700">
        <div class="p-6 border-b border-msit-dark-700">
          <div class="flex items-start justify-between">
            <div class="flex-1">
              <h2 class="text-2xl font-bold text-msit-dark-50 mb-2 font-serif">{{ selectedProblem.title }}</h2>
              <div class="flex flex-wrap gap-2">
                <span
                  :class="[
                    'inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium font-sans',
                    selectedProblem.difficulty === 'beginner' ? 'bg-green-500/20 text-green-400' :
                    selectedProblem.difficulty === 'intermediate' ? 'bg-yellow-500/20 text-yellow-400' :
                    'bg-red-500/20 text-red-400'
                  ]"
                >
                  {{ selectedProblem.difficulty }}
                </span>
                <span
                  v-for="tag in selectedProblem.tags"
                  :key="tag"
                  class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-msit-accent/20 text-msit-accent font-sans"
                >
                  {{ tag }}
                </span>
              </div>
            </div>
            <button
              @click="selectedProblem = null"
              class="text-msit-dark-300 hover:text-msit-dark-50 transition-colors"
            >
              <svg class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
              </svg>
            </button>
          </div>
        </div>
        
        <div class="p-6 space-y-6">
          <div>
            <h3 class="text-lg font-semibold text-msit-dark-50 mb-2 font-sans">Description</h3>
            <p class="text-sm text-msit-dark-200 whitespace-pre-wrap font-sans">{{ selectedProblem.fullDescription }}</p>
          </div>
          
          <div v-if="selectedProblem.examples && selectedProblem.examples.length > 0">
            <h3 class="text-lg font-semibold text-msit-dark-50 mb-2 font-sans">Examples</h3>
            <div class="space-y-3">
              <div
                v-for="(example, idx) in selectedProblem.examples"
                :key="idx"
                class="bg-msit-dark-900 p-4 rounded border border-msit-dark-700"
              >
                <p class="text-sm font-semibold text-msit-dark-50 mb-2 font-sans">Example {{ idx + 1 }}:</p>
                <pre class="text-xs text-msit-dark-200 font-mono mb-2"><code>Input: {{ example.input }}</code></pre>
                <pre class="text-xs text-msit-dark-200 font-mono"><code>Output: {{ example.output }}</code></pre>
              </div>
            </div>
          </div>
          
          <div v-if="selectedProblem.constraints">
            <h3 class="text-lg font-semibold text-msit-dark-50 mb-2 font-sans">Constraints</h3>
            <ul class="list-disc list-inside text-sm text-msit-dark-200 space-y-1 font-sans">
              <li v-for="(constraint, idx) in selectedProblem.constraints" :key="idx">{{ constraint }}</li>
            </ul>
          </div>

          <!-- Code Input -->
          <div class="mt-6">
            <h3 class="text-lg font-semibold text-msit-dark-50 mb-2 font-sans">Your Solution:</h3>
            <textarea
              v-model="userCode[selectedProblem.id]"
              :placeholder="`# ${selectedProblem.title}\n# Write your solution here\n\n`"
              class="w-full bg-msit-dark-900 border border-msit-dark-700 rounded-lg p-3 text-sm text-msit-dark-50 font-mono focus:border-msit-accent focus:ring-1 focus:ring-msit-accent outline-none resize-y min-h-[200px]"
              rows="10"
            ></textarea>
          </div>

          <!-- Error Message -->
          <div v-if="testErrors[selectedProblem.id]" class="mt-6 bg-red-500/10 border border-red-500/30 rounded-lg p-4">
            <div class="flex items-center gap-2 text-red-400">
              <svg class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
              <span class="font-medium font-sans">{{ testErrors[selectedProblem.id] }}</span>
            </div>
          </div>

          <!-- Test Results -->
          <div v-if="testResults[selectedProblem.id] && testResults[selectedProblem.id].length > 0" class="mt-6">
            <div class="flex items-center justify-between mb-3">
              <h3 class="text-lg font-semibold text-msit-dark-50 font-sans">Test Results:</h3>
              <div class="flex items-center gap-3">
                <span v-if="testMethod[selectedProblem.id]" class="text-xs text-msit-dark-400 font-sans">
                  ({{ testMethod[selectedProblem.id] }})
                </span>
                <span :class="[
                  'px-3 py-1 rounded-full text-sm font-medium font-sans',
                  allTestsPassed(selectedProblem.id) ? 'bg-green-500/20 text-green-400' : 'bg-red-500/20 text-red-400'
                ]">
                  {{ passedTestsCount(selectedProblem.id) }} / {{ testResults[selectedProblem.id].length }} passed
                </span>
              </div>
            </div>
            <div class="space-y-3">
              <div
                v-for="(result, idx) in testResults[selectedProblem.id]"
                :key="idx"
                :class="[
                  'p-4 rounded-lg border font-sans',
                  result.passed ? 'bg-green-500/10 border-green-500/30' : 'bg-red-500/10 border-red-500/30'
                ]"
              >
                <div class="flex items-start gap-3">
                  <svg v-if="result.passed" class="h-6 w-6 text-green-400 shrink-0 mt-0.5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
                  </svg>
                  <svg v-else class="h-6 w-6 text-red-400 shrink-0 mt-0.5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 14l2-2m0 0l2-2m-2 2l-2-2m2 2l2 2m7-2a9 9 0 11-18 0 9 9 0 0118 0z" />
                  </svg>
                  <div class="flex-1">
                    <div class="text-sm font-mono text-msit-dark-200 mb-2">
                      <span class="font-semibold text-msit-dark-50">Test {{ idx + 1 }}:</span> {{ result.testCase.input }}
                    </div>
                    <div v-if="result.passed" class="text-sm text-green-400 font-medium">
                      ✓ Passed
                    </div>
                    <div v-else class="text-sm space-y-1">
                      <div class="text-red-400 font-medium">
                        ✗ Failed
                      </div>
                      <div class="text-msit-dark-300">
                        <span class="font-semibold">Expected:</span> <code class="bg-msit-dark-800 px-1 rounded">{{ result.expected }}</code>
                      </div>
                      <div class="text-msit-dark-300">
                        <span class="font-semibold">Got:</span> <code class="bg-msit-dark-800 px-1 rounded">{{ result.actual }}</code>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
        
        <div class="p-6 border-t border-msit-dark-700 flex flex-wrap justify-end gap-3">
          <button
            @click="selectedProblem = null"
            class="px-4 py-2 border border-msit-dark-600 text-msit-dark-50 rounded-md hover:bg-msit-dark-700 transition-colors font-sans"
          >
            Close
          </button>
          <button
            @click="runTestsForProblem(selectedProblem)"
            :disabled="!userCode[selectedProblem.id] || isLoading[selectedProblem.id]"
            class="px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 transition-colors text-sm font-semibold font-sans disabled:opacity-50 disabled:cursor-not-allowed"
          >
            <span v-if="isLoading[selectedProblem.id]" class="inline-flex items-center">
              <svg class="animate-spin h-4 w-4 mr-2" fill="none" viewBox="0 0 24 24">
                <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
              </svg>
              Running Tests...
            </span>
            <span v-else class="inline-flex items-center">
              <svg class="h-4 w-4 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
              Run Tests (Client)
            </span>
          </button>
          <button
            @click="submitToBackend(selectedProblem)"
            :disabled="!userCode[selectedProblem.id] || isSubmitting[selectedProblem.id]"
            class="px-4 py-2 bg-green-600 text-white rounded-md hover:bg-green-700 transition-colors text-sm font-semibold font-sans disabled:opacity-50 disabled:cursor-not-allowed"
          >
            <span v-if="isSubmitting[selectedProblem.id]" class="inline-flex items-center">
              <svg class="animate-spin h-4 w-4 mr-2" fill="none" viewBox="0 0 24 24">
                <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
              </svg>
              Submitting...
            </span>
            <span v-else class="inline-flex items-center">
              <svg class="h-4 w-4 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
              Submit & Validate
            </span>
          </button>
          <button
            @click="solveProblem(selectedProblem)"
            class="px-4 py-2 border border-transparent text-sm font-semibold rounded-md text-msit-dark bg-msit-accent hover:bg-msit-accent-500 transition-colors font-sans"
          >
            Solve in Compiler
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { runTests, loadPyodide, type TestCase, type TestResult } from '../utils/testRunner'

const router = useRouter()
const searchQuery = ref('')
const selectedDifficulty = ref('')
const selectedTopic = ref('')
const selectedProblem = ref<any>(null)
const userCode = ref<Record<number, string>>({})
const testResults = ref<Record<number, TestResult[]>>({})
const testErrors = ref<Record<number, string>>({})
const testMethod = ref<Record<number, string>>({})
const isLoading = ref<Record<number, boolean>>({})
const isSubmitting = ref<Record<number, boolean>>({})
const problems = ref<any[]>([])
const topics = ref<string[]>([])
const loadingProblems = ref(false)
const loadingTopics = ref(false)
let pyodide: any = null

// Problems are now fetched from the API

const fetchProblems = async () => {
  loadingProblems.value = true
  try {
    const response = await fetch('/api/problems')
    if (!response.ok) {
      throw new Error('Failed to fetch problems')
    }
    const data = await response.json()
    problems.value = data
    
    // Initialize user code for each problem
    problems.value.forEach(problem => {
      if (!userCode.value[problem.id]) {
        userCode.value[problem.id] = problem.starterCode || `# ${problem.title}\n# ${problem.description}\n\n# Your solution here:\n\n`
      }
    })
  } catch (error) {
    console.error('Error fetching problems:', error)
    // Fallback to empty array on error
    problems.value = []
  } finally {
    loadingProblems.value = false
  }
}

// Fetch topics from API endpoint
const fetchTopics = async () => {
  loadingTopics.value = true
  try {
    const response = await fetch('/api/problems/topics')
    if (!response.ok) {
      throw new Error('Failed to fetch topics')
    }
    const data = await response.json()
    topics.value = Array.isArray(data) ? data.sort() : []
  } catch (error) {
    console.error('Error fetching topics:', error)
    // Fallback to computing from problems
    const topicSet = new Set<string>()
    problems.value.forEach(p => {
      if (p.tags) {
        p.tags.forEach((tag: string) => topicSet.add(tag))
      }
    })
    topics.value = Array.from(topicSet).sort()
  } finally {
    loadingTopics.value = false
  }
}

const filteredProblems = computed(() => {
  let result = problems.value
  
  if (selectedDifficulty.value) {
    result = result.filter(p => p.difficulty === selectedDifficulty.value)
  }
  
  if (selectedTopic.value) {
    result = result.filter(p => p.tags && p.tags.includes(selectedTopic.value))
  }
  
  if (searchQuery.value) {
    const query = searchQuery.value.toLowerCase()
    result = result.filter(p => 
      p.title.toLowerCase().includes(query) ||
      p.description.toLowerCase().includes(query) ||
      (p.tags && p.tags.some((tag: string) => tag.toLowerCase().includes(query)))
    )
  }
  
  return result
})

const openProblem = (problem: any) => {
  selectedProblem.value = problem
}

const solveProblem = (problem: any) => {
  const code = userCode.value[problem.id] || `# ${problem.title}\n# ${problem.description}\n\ndef solution():\n    # Your code here\n    pass\n\n# Test your solution\nprint(solution())`
  localStorage.setItem('compiler_code', code)
  selectedProblem.value = null
  router.push('/compiler')
}

const runTestsForProblem = async (problem: any) => {
  if (!userCode.value[problem.id] || !problem.testCases) return

  isLoading.value[problem.id] = true
  testErrors.value[problem.id] = ''
  testResults.value[problem.id] = []
  testMethod.value[problem.id] = ''

  // First, try server-side submission (more reliable)
  try {
    const response = await fetch(`/api/problems/${problem.id}/submit`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        code: userCode.value[problem.id],
      }),
    })

    if (!response.ok) {
      const errorData = await response.json().catch(() => ({}))
      throw new Error(errorData.error || 'Server submission failed')
    }

    const data = await response.json()
    
    if (data.success) {
      // Convert server response to TestResult format
      testResults.value[problem.id] = data.results.map((r: any) => ({
        passed: r.passed,
        expected: r.expected || '',
        actual: r.actual || '',
        testCase: {
          input: r.input || '',
          output: r.expected || ''
        }
      }))
      testMethod.value[problem.id] = 'Server'
      return
    } else {
      throw new Error(data.error || 'Submission failed')
    }
  } catch (serverError: any) {
    console.warn('Server-side test failed, trying client-side:', serverError)
    
    // Fallback to client-side Pyodide
    try {
      if (!pyodide) {
        pyodide = await loadPyodide()
      }

      const results = await runTests(pyodide, userCode.value[problem.id], problem.testCases)
      testResults.value[problem.id] = results
      testMethod.value[problem.id] = 'Client (Pyodide)'
    } catch (clientError: any) {
      console.error('Client-side test execution error:', clientError)
      testErrors.value[problem.id] = `Both server and client-side testing failed. ${clientError.message || String(clientError)}`
      testResults.value[problem.id] = problem.testCases.map((testCase: TestCase) => ({
        passed: false,
        expected: testCase.output,
        actual: `Error: ${clientError.message || String(clientError)}`,
        testCase
      }))
    }
  } finally {
    isLoading.value[problem.id] = false
  }
}

const submitToBackend = async (problem: any) => {
  if (!userCode.value[problem.id]) return

  isSubmitting.value[problem.id] = true
  testErrors.value[problem.id] = ''

  try {
    const response = await fetch(`/api/problems/${problem.id}/submit`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ code: userCode.value[problem.id] })
    })

    const result = await response.json()
    
    if (result.success) {
      // Convert backend results to frontend format
      testResults.value[problem.id] = result.results.map((r: any) => ({
        passed: r.passed,
        expected: r.expected,
        actual: r.actual,
        testCase: {
          input: r.input,
          output: r.expected
        }
      }))
      testMethod.value[problem.id] = 'Server (Backend)'
      
      // Show success message if all tests passed
      if (result.allPassed) {
        alert(`🎉 All ${result.totalTests} tests passed!`)
      }
    } else {
      testErrors.value[problem.id] = result.error || 'Submission failed'
    }
  } catch (error: any) {
    console.error('Backend submission error:', error)
    testErrors.value[problem.id] = `Error submitting solution: ${error.message || 'Network error'}`
  } finally {
    isSubmitting.value[problem.id] = false
  }
}

const passedTestsCount = (problemId: number): number => {
  if (!testResults.value[problemId]) return 0
  return testResults.value[problemId].filter(r => r.passed).length
}

const allTestsPassed = (problemId: number): boolean => {
  if (!testResults.value[problemId] || testResults.value[problemId].length === 0) return false
  return testResults.value[problemId].every(r => r.passed)
}

onMounted(async () => {
  // Fetch problems and topics from API
  await Promise.all([fetchProblems(), fetchTopics()])
  
  // Preload Pyodide
  try {
    pyodide = await loadPyodide()
  } catch (error) {
    console.error('Failed to load Pyodide:', error)
  }
})
</script>
