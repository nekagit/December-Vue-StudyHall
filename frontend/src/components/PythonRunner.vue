<template>
  <div class="space-y-4">
    <!-- Toolbar -->
    <div class="flex flex-wrap items-center gap-2 pb-2 border-b border-msit-dark-700">
      <button
        @click="showSnippets = !showSnippets"
        class="inline-flex items-center px-3 py-1.5 border border-msit-dark-600 shadow-sm text-sm font-medium rounded-md text-msit-dark-50 bg-msit-dark-700 hover:bg-msit-dark-600 transition-colors font-sans"
      >
        <svg class="h-4 w-4 mr-1" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16" />
        </svg>
        <span class="hidden sm:inline">Templates</span>
      </button>
      <button
        @click="showHistory = !showHistory"
        class="inline-flex items-center px-3 py-1.5 border border-msit-dark-600 shadow-sm text-sm font-medium rounded-md text-msit-dark-50 bg-msit-dark-700 hover:bg-msit-dark-600 transition-colors font-sans"
      >
        <svg class="h-4 w-4 mr-1" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
        </svg>
        <span class="hidden sm:inline">History</span>
      </button>
      <button
        @click="formatCode"
        class="inline-flex items-center px-3 py-1.5 border border-msit-dark-600 shadow-sm text-sm font-medium rounded-md text-msit-dark-50 bg-msit-dark-700 hover:bg-msit-dark-600 transition-colors font-sans"
      >
        <svg class="h-4 w-4 mr-1" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
        </svg>
        <span class="hidden sm:inline">Format</span>
      </button>
      <button
        @click="clearCode"
        class="inline-flex items-center px-3 py-1.5 border border-msit-dark-600 shadow-sm text-sm font-medium rounded-md text-msit-dark-50 bg-msit-dark-700 hover:bg-msit-dark-600 transition-colors font-sans"
      >
        <svg class="h-4 w-4 mr-1" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
        </svg>
        <span class="hidden sm:inline">Clear</span>
      </button>
      <button
        @click="exportCode"
        class="inline-flex items-center px-3 py-1.5 border border-msit-dark-600 shadow-sm text-sm font-medium rounded-md text-msit-dark-50 bg-msit-dark-700 hover:bg-msit-dark-600 transition-colors font-sans"
      >
        <svg class="h-4 w-4 mr-1" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4" />
        </svg>
        <span class="hidden sm:inline">Export</span>
      </button>
    </div>

    <!-- Code Snippets Panel -->
    <div v-if="showSnippets" class="bg-msit-dark-700 border border-msit-dark-600 rounded-md p-4">
      <h3 class="text-sm font-semibold text-msit-dark-50 mb-3 font-sans">Code Templates</h3>
      <div class="grid grid-cols-1 sm:grid-cols-2 gap-2">
        <button
          v-for="snippet in codeSnippets"
          :key="snippet.name"
          @click="loadSnippet(snippet.code)"
          class="text-left px-3 py-2 bg-msit-dark-800 border border-msit-dark-600 rounded hover:bg-msit-dark-600 hover:border-msit-accent transition-colors"
        >
          <div class="font-medium text-sm text-msit-dark-50 font-sans">{{ snippet.name }}</div>
          <div class="text-xs text-msit-dark-300 mt-1 font-sans">{{ snippet.description }}</div>
        </button>
      </div>
    </div>

    <!-- History Panel -->
    <div v-if="showHistory" class="bg-msit-dark-700 border border-msit-dark-600 rounded-md p-4">
      <h3 class="text-sm font-semibold text-msit-dark-50 mb-3 font-sans">Code History</h3>
      <div v-if="codeHistory.length === 0" class="text-sm text-msit-dark-300 font-sans">No history yet</div>
      <div v-else class="space-y-2 max-h-48 overflow-y-auto">
        <div
          v-for="(item, index) in codeHistory"
          :key="index"
          class="bg-msit-dark-800 border border-msit-dark-600 rounded p-2 hover:bg-msit-dark-600 cursor-pointer transition-colors"
          @click="loadSnippet(item.code)"
        >
          <div class="text-xs text-msit-dark-300 mb-1 font-sans">{{ item.timestamp }}</div>
          <div class="text-sm font-mono text-msit-dark-100 line-clamp-2 break-words">{{ item.code.substring(0, 100) }}{{ item.code.length > 100 ? '...' : '' }}</div>
        </div>
      </div>
    </div>

    <!-- Code Editor -->
    <div>
      <div class="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-2 mb-2">
        <label for="code" class="block text-sm font-medium text-msit-dark-50 font-sans">Python Code</label>
        <span class="text-xs text-msit-dark-300 font-sans">{{ code.length }} characters</span>
      </div>
      <textarea
        id="code"
        v-model="code"
        rows="12"
        class="shadow-sm focus:ring-msit-accent focus:border-msit-accent block w-full text-sm sm:text-base border-msit-dark-600 bg-msit-dark-700 text-msit-dark-50 placeholder-msit-dark-300 rounded-md font-mono px-3 py-2 border resize-y"
        placeholder="print('Hello, StudyHall!')"
        @input="saveToHistory"
      ></textarea>
    </div>
    
    <!-- Action Buttons -->
    <div class="flex flex-col sm:flex-row items-stretch sm:items-center gap-2">
      <button
        @click="runPython"
        :disabled="isLoading"
        class="w-full sm:w-auto inline-flex items-center justify-center px-4 py-2 border border-transparent text-sm font-medium rounded-md shadow-sm text-msit-dark bg-msit-accent hover:bg-msit-accent-500 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-msit-accent disabled:opacity-50 transition-colors font-sans"
      >
        <svg v-if="!isLoading" class="h-4 w-4 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M14.752 11.168l-3.197-2.132A1 1 0 0010 9.87v4.263a1 1 0 001.555.832l3.197-2.132a1 1 0 000-1.664z" />
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
        </svg>
        {{ isLoading ? 'Loading Pyodide...' : 'Run Code' }}
      </button>
      <button
        v-if="output"
        @click="clearOutput"
        class="w-full sm:w-auto inline-flex items-center justify-center px-3 py-2 border border-msit-dark-600 shadow-sm text-sm font-medium rounded-md text-msit-dark-50 bg-msit-dark-700 hover:bg-msit-dark-600 transition-colors font-sans"
      >
        Clear Output
      </button>
    </div>
    
    <!-- Output -->
    <div>
      <div class="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-2 mb-2">
        <label class="block text-sm font-medium text-msit-dark-50 font-sans">Output</label>
        <button
          v-if="output"
          @click="copyOutput"
          class="text-xs text-msit-dark-300 hover:text-msit-accent transition-colors font-sans self-start sm:self-auto"
        >
          Copy
        </button>
      </div>
      <div class="bg-msit-dark-900 text-msit-accent p-3 sm:p-4 rounded-md font-mono text-xs sm:text-sm overflow-auto max-h-64 sm:max-h-96 border border-msit-dark-700">
        <pre class="whitespace-pre-wrap break-words">{{ output || 'Ready to run code...' }}</pre>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, onUnmounted } from 'vue'

const code = ref('print("Hello, StudyHall!")')
const output = ref('Ready!')
const isLoading = ref(true)
const showSnippets = ref(false)
const showHistory = ref(false)
const codeHistory = ref<Array<{ code: string; timestamp: string }>>([])
let pyodide: any = null
let historyTimeout: ReturnType<typeof setTimeout> | null = null

const codeSnippets = [
  {
    name: 'Hello World',
    description: 'Basic print statement',
    code: 'print("Hello, World!")'
  },
  {
    name: 'Variables',
    description: 'Variable assignment and types',
    code: `name = "StudyHall"
age = 25
height = 5.9
is_student = True

print(f"Name: {name}, Age: {age}, Height: {height}, Student: {is_student}")`
  },
  {
    name: 'Lists',
    description: 'Working with lists',
    code: `numbers = [1, 2, 3, 4, 5]
print(f"First: {numbers[0]}")
print(f"Last: {numbers[-1]}")
print(f"Sum: {sum(numbers)}")
print(f"Length: {len(numbers)}")`
  },
  {
    name: 'Loops',
    description: 'For and while loops',
    code: `# For loop
for i in range(5):
    print(f"Number: {i}")

# While loop
count = 0
while count < 3:
    print(f"Count: {count}")
    count += 1`
  },
  {
    name: 'Functions',
    description: 'Define and call functions',
    code: `def greet(name):
    return f"Hello, {name}!"

def add(a, b):
    return a + b

print(greet("StudyHall"))
print(f"5 + 3 = {add(5, 3)}")`
  },
  {
    name: 'Dictionaries',
    description: 'Working with dictionaries',
    code: `student = {
    "name": "Alice",
    "age": 20,
    "courses": ["Python", "Web Dev"]
}

print(f"Name: {student['name']}")
print(f"Age: {student.get('age')}")
print(f"Courses: {', '.join(student['courses'])}")`
  },
  {
    name: 'List Comprehension',
    description: 'Pythonic list operations',
    code: `# Square numbers
squares = [x**2 for x in range(10)]
print(f"Squares: {squares}")

# Filter even numbers
evens = [x for x in range(20) if x % 2 == 0]
print(f"Evens: {evens}")`
  },
  {
    name: 'File Operations',
    description: 'Read and write files',
    code: `# Write to file
with open("example.txt", "w") as f:
    f.write("Hello from StudyHall!")

# Read from file
with open("example.txt", "r") as f:
    content = f.read()
    print(content)`
  }
]

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
    pyodide.setStderr({ batched: (msg: string) => {
      output.value += `ERROR: ${msg}\n`
    }})
    await pyodide.runPythonAsync(code.value)
    saveToHistory()
  } catch (err: any) {
    output.value = `Error: ${err}`
  }
}

const loadSnippet = (snippetCode: string) => {
  code.value = snippetCode
  showSnippets.value = false
}

const clearCode = () => {
  if (confirm('Clear all code?')) {
    code.value = ''
  }
}

const clearOutput = () => {
  output.value = ''
}

const formatCode = () => {
  // Simple formatting - indent properly
  const lines = code.value.split('\n')
  let indent = 0
  const formatted: string[] = []
  
  for (const line of lines) {
    const trimmed = line.trim()
    if (!trimmed) {
      formatted.push('')
      continue
    }
    
    // Decrease indent for dedent keywords
    if (trimmed.startsWith('except') || trimmed.startsWith('elif') || 
        trimmed.startsWith('else') || trimmed.startsWith('finally')) {
      indent = Math.max(0, indent - 1)
    }
    
    formatted.push('  '.repeat(indent) + trimmed)
    
    // Increase indent for block starters
    if (trimmed.endsWith(':') && !trimmed.startsWith('#')) {
      indent += 1
    }
  }
  
  code.value = formatted.join('\n')
}

const exportCode = () => {
  const blob = new Blob([code.value], { type: 'text/x-python' })
  const url = URL.createObjectURL(blob)
  const a = document.createElement('a')
  a.href = url
  a.download = `code-${new Date().toISOString().split('T')[0]}.py`
  document.body.appendChild(a)
  a.click()
  document.body.removeChild(a)
  URL.revokeObjectURL(url)
}

const copyOutput = () => {
  navigator.clipboard.writeText(output.value)
}

const saveToHistory = () => {
  if (historyTimeout) {
    clearTimeout(historyTimeout)
  }
  
  historyTimeout = setTimeout(() => {
    if (code.value.trim() && code.value.length > 10) {
      const historyItem = {
        code: code.value,
        timestamp: new Date().toLocaleString()
      }
      
      // Load existing history
      const existing = localStorage.getItem('python_code_history')
      let history: Array<{ code: string; timestamp: string }> = []
      
      if (existing) {
        try {
          history = JSON.parse(existing)
        } catch (e) {
          history = []
        }
      }
      
      // Add new item (avoid duplicates)
      if (history.length === 0 || history[history.length - 1].code !== code.value) {
        history.push(historyItem)
        // Keep only last 20 items
        if (history.length > 20) {
          history = history.slice(-20)
        }
        localStorage.setItem('python_code_history', JSON.stringify(history))
        codeHistory.value = history.reverse()
      }
    }
  }, 2000) // Save after 2 seconds of inactivity
}

const loadHistory = () => {
  const existing = localStorage.getItem('python_code_history')
  if (existing) {
    try {
      codeHistory.value = JSON.parse(existing).reverse()
    } catch (e) {
      codeHistory.value = []
    }
  }
}

const handleKeyDown = (e: KeyboardEvent) => {
  // Ctrl/Cmd + Enter to run code
  if ((e.ctrlKey || e.metaKey) && e.key === 'Enter') {
    e.preventDefault()
    runPython()
  }
  // Ctrl/Cmd + S to save/export
  if ((e.ctrlKey || e.metaKey) && e.key === 's') {
    e.preventDefault()
    exportCode()
  }
}

onMounted(() => {
  loadHistory()
  
  // Check if code was passed from snippets page
  const savedCode = localStorage.getItem('compiler_code')
  if (savedCode) {
    code.value = savedCode
    localStorage.removeItem('compiler_code')
  }
  
  // Add keyboard shortcuts
  window.addEventListener('keydown', handleKeyDown)
  
  if ((window as any).loadPyodide) {
    loadPyodide()
  } else {
    const script = document.createElement('script')
    script.src = "https://cdn.jsdelivr.net/pyodide/v0.25.0/full/pyodide.js"
    script.onload = loadPyodide
    document.head.appendChild(script)
  }
})

onUnmounted(() => {
  window.removeEventListener('keydown', handleKeyDown)
})
</script>
