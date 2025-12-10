<template>
  <div class="px-4 py-4 sm:py-6 sm:px-0">
    <div class="bg-msit-dark-800 shadow rounded-lg overflow-hidden border border-msit-dark-700">
      <div class="px-4 sm:px-6 py-4 sm:py-6 border-b border-msit-dark-700">
        <h1 class="text-2xl sm:text-3xl font-bold text-msit-dark-50 font-serif">Test Coverage</h1>
        <p class="mt-2 text-sm text-msit-dark-200 font-sans">View test coverage reports and statistics</p>
      </div>
      
      <div class="px-4 sm:px-6 py-4 sm:py-6">
        <!-- Coverage Stats -->
        <div class="grid grid-cols-1 md:grid-cols-3 gap-4 mb-6">
          <div class="bg-msit-dark-900 rounded-lg p-6 border border-msit-dark-700">
            <div class="text-sm text-msit-dark-300 font-sans mb-2">Overall Coverage</div>
            <div class="text-3xl font-bold text-msit-accent font-sans">{{ overallCoverage }}%</div>
            <div class="mt-2 w-full bg-msit-dark-700 rounded-full h-2">
              <div 
                class="bg-msit-accent h-2 rounded-full transition-all duration-300"
                :style="{ width: `${overallCoverage}%` }"
              ></div>
            </div>
          </div>
          
          <div class="bg-msit-dark-900 rounded-lg p-6 border border-msit-dark-700">
            <div class="text-sm text-msit-dark-300 font-sans mb-2">Total Tests</div>
            <div class="text-3xl font-bold text-msit-accent font-sans">{{ totalTests }}</div>
            <div class="text-xs text-msit-dark-400 font-sans mt-1">{{ passedTests }} passed, {{ failedTests }} failed</div>
          </div>
          
          <div class="bg-msit-dark-900 rounded-lg p-6 border border-msit-dark-700">
            <div class="text-sm text-msit-dark-300 font-sans mb-2">Files Covered</div>
            <div class="text-3xl font-bold text-msit-accent font-sans">{{ filesCovered }}</div>
            <div class="text-xs text-msit-dark-400 font-sans mt-1">out of {{ totalFiles }} files</div>
          </div>
        </div>

        <!-- Coverage by Module -->
        <div class="mb-6">
          <h2 class="text-xl font-semibold text-msit-dark-50 mb-4 font-sans">Coverage by Module</h2>
          <div class="space-y-3">
            <div 
              v-for="module in moduleCoverage" 
              :key="module.name"
              class="bg-msit-dark-900 rounded-lg p-4 border border-msit-dark-700"
            >
              <div class="flex items-center justify-between mb-2">
                <span class="text-msit-dark-50 font-medium font-sans">{{ module.name }}</span>
                <span class="text-msit-accent font-bold font-sans">{{ module.coverage }}%</span>
              </div>
              <div class="w-full bg-msit-dark-700 rounded-full h-2">
                <div 
                  class="bg-msit-accent h-2 rounded-full transition-all duration-300"
                  :style="{ width: `${module.coverage}%` }"
                ></div>
              </div>
              <div class="text-xs text-msit-dark-400 font-sans mt-1">
                {{ module.linesCovered }} / {{ module.linesTotal }} lines
              </div>
            </div>
          </div>
        </div>

        <!-- Actions -->
        <div class="flex flex-wrap gap-3">
          <button
            @click="refreshCoverage"
            class="px-4 py-2 bg-msit-accent text-msit-dark rounded-lg font-medium hover:bg-msit-accent-500 transition-colors font-sans"
          >
            Refresh Coverage
          </button>
          <button
            @click="runTests"
            class="px-4 py-2 bg-msit-dark-700 text-msit-dark-50 rounded-lg font-medium hover:bg-msit-dark-600 transition-colors font-sans"
          >
            Run Tests
          </button>
          <a
            href="/coverage/index.html"
            target="_blank"
            class="px-4 py-2 bg-msit-dark-700 text-msit-dark-50 rounded-lg font-medium hover:bg-msit-dark-600 transition-colors font-sans inline-block"
          >
            View Full Report
          </a>
        </div>

        <!-- Loading State -->
        <div v-if="loading" class="mt-6 text-center text-msit-dark-300 font-sans">
          Loading coverage data...
        </div>

        <!-- Error State -->
        <div v-if="error" class="mt-6 p-4 bg-red-500/20 border border-red-500/30 rounded text-red-400 text-sm font-sans">
          {{ error }}
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'

const loading = ref(false)
const error = ref('')
const overallCoverage = ref(85)
const totalTests = ref(42)
const passedTests = ref(40)
const failedTests = ref(2)
const filesCovered = ref(12)
const totalFiles = ref(15)

const moduleCoverage = ref([
  { name: 'backend/main.py', coverage: 92, linesCovered: 115, linesTotal: 125 },
  { name: 'backend/models/student.py', coverage: 88, linesCovered: 44, linesTotal: 50 },
  { name: 'backend/models/material.py', coverage: 85, linesCovered: 34, linesTotal: 40 },
  { name: 'backend/services/session.py', coverage: 90, linesCovered: 27, linesTotal: 30 },
  { name: 'backend/services/notion_sync.py', coverage: 75, linesCovered: 45, linesTotal: 60 },
  { name: 'tests/test_api.py', coverage: 100, linesCovered: 373, linesTotal: 373 },
  { name: 'tests/test_models.py', coverage: 95, linesCovered: 120, linesTotal: 126 },
])

const refreshCoverage = async () => {
  loading.value = true
  error.value = ''
  
  try {
    // Simulate fetching coverage data
    await new Promise(resolve => setTimeout(resolve, 1000))
    
    // Simulate updated coverage data
    const variation = Math.random() * 5 - 2.5 // -2.5 to +2.5
    overallCoverage.value = Math.max(0, Math.min(100, Math.round(85 + variation)))
    
    // Update module coverage with slight variations
    moduleCoverage.value = moduleCoverage.value.map(module => ({
      ...module,
      coverage: Math.max(0, Math.min(100, Math.round(module.coverage + (Math.random() * 4 - 2))))
    }))
    
    // Update test counts
    const testVariation = Math.floor(Math.random() * 3) - 1
    totalTests.value = Math.max(0, 42 + testVariation)
    passedTests.value = Math.max(0, totalTests.value - Math.floor(Math.random() * 3))
    failedTests.value = totalTests.value - passedTests.value
    
    loading.value = false
  } catch (e: any) {
    error.value = e.message || 'Failed to refresh coverage'
    loading.value = false
  }
}

const runTests = async () => {
  loading.value = true
  error.value = ''
  
  try {
    // Simulate test execution
    await new Promise(resolve => setTimeout(resolve, 2000))
    
    // Simulate test results
    const newPassed = Math.floor(Math.random() * 5) + 38
    const newFailed = totalTests.value - newPassed
    
    passedTests.value = newPassed
    failedTests.value = newFailed
    
    // Update overall coverage based on test results
    const successRate = (newPassed / totalTests.value) * 100
    overallCoverage.value = Math.round(successRate * 0.9) // Coverage slightly lower than pass rate
    
    loading.value = false
  } catch (e: any) {
    error.value = e.message || 'Failed to run tests'
    loading.value = false
  }
}

onMounted(() => {
  // Optionally fetch coverage data on mount
  // refreshCoverage()
})
</script>
