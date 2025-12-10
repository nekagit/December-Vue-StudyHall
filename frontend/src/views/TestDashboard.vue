<template>
  <div class="min-h-screen bg-gray-50 py-8">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      <div class="mb-8">
        <h1 class="text-3xl font-bold text-gray-900">Test Dashboard</h1>
        <p class="mt-2 text-sm text-gray-600">View test results and coverage for backend and frontend</p>
      </div>

      <!-- Action Buttons -->
      <div class="mb-6 flex gap-4">
        <button
          @click="runBackendTests"
          :disabled="runningBackend"
          class="px-4 py-2 bg-indigo-600 text-white rounded-md hover:bg-indigo-700 disabled:opacity-50 disabled:cursor-not-allowed"
        >
          {{ runningBackend ? 'Running...' : 'Run Backend Tests' }}
        </button>
        <button
          @click="runFrontendTests"
          :disabled="runningFrontend"
          class="px-4 py-2 bg-indigo-600 text-white rounded-md hover:bg-indigo-700 disabled:opacity-50 disabled:cursor-not-allowed"
        >
          {{ runningFrontend ? 'Running...' : 'Run Frontend Tests' }}
        </button>
        <button
          @click="refreshCoverage"
          :disabled="loading"
          class="px-4 py-2 bg-gray-600 text-white rounded-md hover:bg-gray-700 disabled:opacity-50 disabled:cursor-not-allowed"
        >
          Refresh Coverage
        </button>
      </div>

      <!-- Coverage Summary -->
      <div class="grid grid-cols-1 md:grid-cols-2 gap-6 mb-8">
        <!-- Backend Coverage -->
        <div class="bg-white rounded-lg shadow p-6">
          <h2 class="text-xl font-semibold text-gray-900 mb-4">Backend Coverage</h2>
          <div v-if="backendCoverage.available" class="space-y-4">
            <div class="flex items-center justify-between">
              <span class="text-sm font-medium text-gray-700">Overall Coverage</span>
              <span class="text-2xl font-bold" :class="getCoverageColor(backendCoverage.coverage_percent)">
                {{ backendCoverage.coverage_percent }}%
              </span>
            </div>
            <div class="w-full bg-gray-200 rounded-full h-4">
              <div
                class="h-4 rounded-full transition-all"
                :class="getCoverageBarColor(backendCoverage.coverage_percent)"
                :style="{ width: `${backendCoverage.coverage_percent}%` }"
              ></div>
            </div>
            <div class="text-sm text-gray-600">
              {{ backendCoverage.covered_lines }} / {{ backendCoverage.total_lines }} lines covered
            </div>
            <div v-if="Object.keys(backendCoverage.files || {}).length > 0" class="mt-4">
              <h3 class="text-sm font-medium text-gray-700 mb-2">File Coverage</h3>
              <div class="space-y-2 max-h-64 overflow-y-auto">
                <div
                  v-for="(file, path) in backendCoverage.files"
                  :key="path"
                  class="flex items-center justify-between text-xs p-2 bg-gray-50 rounded"
                >
                  <span class="truncate flex-1 mr-2">{{ path }}</span>
                  <span :class="getCoverageColor(file.coverage_percent)">
                    {{ file.coverage_percent }}%
                  </span>
                </div>
              </div>
            </div>
          </div>
          <div v-else class="text-gray-500 text-sm">
            {{ backendCoverage.message || 'Coverage data not available' }}
          </div>
        </div>

        <!-- Frontend Coverage -->
        <div class="bg-white rounded-lg shadow p-6">
          <h2 class="text-xl font-semibold text-gray-900 mb-4">Frontend Coverage</h2>
          <div v-if="frontendCoverage.available" class="space-y-4">
            <div class="flex items-center justify-between">
              <span class="text-sm font-medium text-gray-700">Overall Coverage</span>
              <span class="text-2xl font-bold" :class="getCoverageColor(frontendCoverage.coverage_percent)">
                {{ frontendCoverage.coverage_percent }}%
              </span>
            </div>
            <div class="w-full bg-gray-200 rounded-full h-4">
              <div
                class="h-4 rounded-full transition-all"
                :class="getCoverageBarColor(frontendCoverage.coverage_percent)"
                :style="{ width: `${frontendCoverage.coverage_percent}%` }"
              ></div>
            </div>
            <div class="text-sm text-gray-600">
              {{ frontendCoverage.covered_lines }} / {{ frontendCoverage.total_lines }} lines covered
            </div>
            <div v-if="Object.keys(frontendCoverage.files || {}).length > 0" class="mt-4">
              <h3 class="text-sm font-medium text-gray-700 mb-2">File Coverage</h3>
              <div class="space-y-2 max-h-64 overflow-y-auto">
                <div
                  v-for="(file, path) in frontendCoverage.files"
                  :key="path"
                  class="flex items-center justify-between text-xs p-2 bg-gray-50 rounded"
                >
                  <span class="truncate flex-1 mr-2">{{ path }}</span>
                  <span :class="getCoverageColor(file.coverage_percent)">
                    {{ file.coverage_percent }}%
                  </span>
                </div>
              </div>
            </div>
          </div>
          <div v-else class="text-gray-500 text-sm">
            {{ frontendCoverage.message || 'Coverage data not available' }}
          </div>
        </div>
      </div>

      <!-- Test Results -->
      <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
        <!-- Backend Test Results -->
        <div class="bg-white rounded-lg shadow p-6">
          <h2 class="text-xl font-semibold text-gray-900 mb-4">Backend Tests</h2>
          <div v-if="backendTestResults" class="space-y-4">
            <div class="flex items-center gap-4">
              <div class="flex items-center gap-2">
                <span class="text-green-600 font-semibold">
                  ✓ {{ backendTestResults.report?.summary?.passed || 0 }} passed
                </span>
                <span class="text-red-600 font-semibold">
                  ✗ {{ backendTestResults.report?.summary?.failed || 0 }} failed
                </span>
                <span class="text-gray-600">
                  ⊘ {{ backendTestResults.report?.summary?.skipped || 0 }} skipped
                </span>
              </div>
            </div>
            <div class="text-sm text-gray-700">
              Total: {{ backendTestResults.report?.summary?.total || 0 }} tests
            </div>
            <div v-if="backendTestResults.success === false" class="text-red-600 text-sm">
              {{ backendTestResults.error || 'Tests failed' }}
            </div>
            <div v-if="backendTestResults.report?.tests" class="mt-4 space-y-2 max-h-96 overflow-y-auto">
              <div
                v-for="test in backendTestResults.report.tests"
                :key="test.nodeid"
                class="p-2 rounded text-xs"
                :class="{
                  'bg-green-50 text-green-800': test.outcome === 'passed',
                  'bg-red-50 text-red-800': test.outcome === 'failed',
                  'bg-gray-50 text-gray-800': test.outcome === 'skipped'
                }"
              >
                <div class="font-medium">{{ test.nodeid }}</div>
                <div v-if="test.outcome === 'failed' && test.call" class="mt-1 text-red-600">
                  {{ test.call.longrepr }}
                </div>
              </div>
            </div>
          </div>
          <div v-else class="text-gray-500 text-sm">
            No test results available. Run tests to see results.
          </div>
        </div>

        <!-- Frontend Test Results -->
        <div class="bg-white rounded-lg shadow p-6">
          <h2 class="text-xl font-semibold text-gray-900 mb-4">Frontend Tests</h2>
          <div v-if="frontendTestResults" class="space-y-4">
            <div class="flex items-center gap-4">
              <div class="flex items-center gap-2">
                <span class="text-green-600 font-semibold">
                  ✓ {{ frontendTestResults.report?.numPassedTests || 0 }} passed
                </span>
                <span class="text-red-600 font-semibold">
                  ✗ {{ frontendTestResults.report?.numFailedTests || 0 }} failed
                </span>
                <span class="text-gray-600">
                  ⊘ {{ frontendTestResults.report?.numSkippedTests || 0 }} skipped
                </span>
              </div>
            </div>
            <div class="text-sm text-gray-700">
              Total: {{ frontendTestResults.report?.numTotalTests || 0 }} tests
            </div>
            <div v-if="frontendTestResults.success === false" class="text-red-600 text-sm">
              {{ frontendTestResults.error || 'Tests failed' }}
            </div>
            <div v-if="frontendTestResults.report?.testResults" class="mt-4 space-y-2 max-h-96 overflow-y-auto">
              <div
                v-for="testResult in frontendTestResults.report.testResults"
                :key="testResult.name"
                class="mb-4"
              >
                <div class="font-medium text-sm mb-2">{{ testResult.name }}</div>
                <div class="space-y-1">
                  <div
                    v-for="test in testResult.assertionResults || []"
                    :key="test.fullName"
                    class="p-2 rounded text-xs"
                    :class="{
                      'bg-green-50 text-green-800': test.status === 'passed',
                      'bg-red-50 text-red-800': test.status === 'failed',
                      'bg-gray-50 text-gray-800': test.status === 'skipped'
                    }"
                  >
                    <div class="font-medium">{{ test.fullName }}</div>
                    <div v-if="test.failureMessages && test.failureMessages.length > 0" class="mt-1 text-red-600">
                      {{ test.failureMessages[0] }}
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
          <div v-else class="text-gray-500 text-sm">
            No test results available. Run tests to see results.
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'

const loading = ref(false)
const runningBackend = ref(false)
const runningFrontend = ref(false)
const backendCoverage = ref<any>({ available: false })
const frontendCoverage = ref<any>({ available: false })
const backendTestResults = ref<any>(null)
const frontendTestResults = ref<any>(null)

const getCoverageColor = (percent: number) => {
  if (percent >= 80) return 'text-green-600'
  if (percent >= 60) return 'text-yellow-600'
  return 'text-red-600'
}

const getCoverageBarColor = (percent: number) => {
  if (percent >= 80) return 'bg-green-500'
  if (percent >= 60) return 'bg-yellow-500'
  return 'bg-red-500'
}

const refreshCoverage = async () => {
  loading.value = true
  try {
    const response = await fetch('/api/tests/summary', {
      credentials: 'include'
    })
    if (response.ok) {
      const data = await response.json()
      backendCoverage.value = data.backend.coverage
      frontendCoverage.value = data.frontend.coverage
    }
  } catch (e) {
    console.error('Failed to fetch coverage:', e)
  } finally {
    loading.value = false
  }
}

const runBackendTests = async () => {
  runningBackend.value = true
  try {
    const response = await fetch('/api/tests/backend/run', {
      method: 'POST',
      credentials: 'include'
    })
    if (response.ok) {
      backendTestResults.value = await response.json()
      // Refresh coverage after running tests
      await refreshCoverage()
    }
  } catch (e) {
    console.error('Failed to run backend tests:', e)
  } finally {
    runningBackend.value = false
  }
}

const runFrontendTests = async () => {
  runningFrontend.value = true
  try {
    const response = await fetch('/api/tests/frontend/run', {
      method: 'POST',
      credentials: 'include'
    })
    if (response.ok) {
      frontendTestResults.value = await response.json()
      // Refresh coverage after running tests
      await refreshCoverage()
    }
  } catch (e) {
    console.error('Failed to run frontend tests:', e)
  } finally {
    runningFrontend.value = false
  }
}

onMounted(() => {
  refreshCoverage()
})
</script>
