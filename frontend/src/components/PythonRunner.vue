<template>
  <div class="space-y-4">
    <div>
      <label for="code" class="block text-sm font-medium text-gray-700 mb-2">Python Code</label>
      <textarea
        id="code"
        v-model="code"
        rows="12"
        class="shadow-sm focus:ring-indigo-500 focus:border-indigo-500 block w-full sm:text-sm border-gray-300 rounded-md font-mono"
        placeholder="print('Hello, StudyHall!')"
      ></textarea>
    </div>
    
    <div>
      <button
        @click="runPython"
        :disabled="isLoading"
        class="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md shadow-sm text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 disabled:opacity-50"
      >
        {{ isLoading ? 'Loading Pyodide...' : 'Run Code' }}
      </button>
    </div>
    
    <div>
      <label class="block text-sm font-medium text-gray-700 mb-2">Output</label>
      <div class="bg-gray-900 text-green-400 p-4 rounded-md font-mono text-sm overflow-auto max-h-96">
        <pre class="whitespace-pre-wrap">{{ output || 'Ready to run code...' }}</pre>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'

const code = ref('print("Hello, StudyHall!")')
const output = ref('Ready!')
const isLoading = ref(true)
let pyodide: any = null

const loadPyodide = async () => {
  output.value = 'Loading Pyodide environment...'
  try {
    // @ts-ignore
    pyodide = await window.loadPyodide()
    isLoading.value = false
    output.value = 'Ready!'
  } catch (e: any) {
    output.value = `Error loading Pyodide: ${e}`
  }
}

const runPython = async () => {
  if (!pyodide) return
  try {
    output.value = '' // Clear previous output
    pyodide.setStdout({ batched: (msg: string) => {
      output.value += msg + '\n'
    }})
    await pyodide.runPythonAsync(code.value)
  } catch (err: any) {
    output.value = `Error: ${err}`
  }
}

onMounted(() => {
  if ((window as any).loadPyodide) {
    loadPyodide()
  } else {
    const script = document.createElement('script')
    script.src = "https://cdn.jsdelivr.net/pyodide/v0.25.0/full/pyodide.js"
    script.onload = loadPyodide
    document.head.appendChild(script)
  }
})
</script>
