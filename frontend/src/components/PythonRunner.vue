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
        @click="showStudyHelp = !showStudyHelp"
        class="inline-flex items-center px-3 py-1.5 border border-msit-dark-600 shadow-sm text-sm font-medium rounded-md text-msit-dark-50 bg-msit-dark-700 hover:bg-msit-dark-600 transition-colors font-sans"
      >
        <svg class="h-4 w-4 mr-1" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z" />
        </svg>
        <span class="hidden sm:inline">Study Help</span>
      </button>
      <button
        @click="showVariables = !showVariables"
        class="inline-flex items-center px-3 py-1.5 border border-msit-dark-600 shadow-sm text-sm font-medium rounded-md text-msit-dark-50 bg-msit-dark-700 hover:bg-msit-dark-600 transition-colors font-sans"
      >
        <svg class="h-4 w-4 mr-1" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
        </svg>
        <span class="hidden sm:inline">Variables</span>
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
          <div class="text-sm font-mono text-msit-dark-100 line-clamp-2 wrap-break-word">{{ item.code.substring(0, 100) }}{{ item.code.length > 100 ? '...' : '' }}</div>
        </div>
      </div>
    </div>

    <!-- Study Help Panel -->
    <div v-if="showStudyHelp" class="bg-msit-dark-700 border border-msit-dark-600 rounded-md p-4">
      <h3 class="text-sm font-semibold text-msit-dark-50 mb-3 font-sans flex items-center">
        <svg class="h-4 w-4 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
        </svg>
        Study Tips & Help
      </h3>
      <div class="space-y-3">
        <div v-for="tip in studyTips" :key="tip.title" class="bg-msit-dark-800 border border-msit-dark-600 rounded p-3">
          <div class="font-medium text-sm text-msit-dark-50 mb-1 font-sans">{{ tip.title }}</div>
          <div class="text-xs text-msit-dark-300 font-sans">{{ tip.description }}</div>
        </div>
        <div v-if="currentError" class="bg-red-900/20 border border-red-700 rounded p-3">
          <div class="font-medium text-sm text-red-300 mb-1 font-sans">Error Explanation</div>
          <div class="text-xs text-red-200 font-sans">{{ currentError }}</div>
        </div>
      </div>
    </div>

    <!-- Variables Inspector Panel -->
    <div v-if="showVariables && variables.length > 0" class="bg-msit-dark-700 border border-msit-dark-600 rounded-md p-4">
      <h3 class="text-sm font-semibold text-msit-dark-50 mb-3 font-sans">Variable Inspector</h3>
      <div class="space-y-2 max-h-48 overflow-y-auto">
        <div v-for="(variable, index) in variables" :key="index" class="bg-msit-dark-800 border border-msit-dark-600 rounded p-2">
          <div class="font-mono text-sm text-msit-dark-50">
            <span class="text-msit-accent">{{ variable.name }}</span>
            <span class="text-msit-dark-300 mx-2">=</span>
            <span class="text-msit-dark-100">{{ variable.value }}</span>
            <span class="text-msit-dark-400 ml-2 text-xs">({{ variable.type }})</span>
          </div>
        </div>
      </div>
    </div>

    <!-- Code Editor with Line Numbers -->
    <div>
      <div class="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-2 mb-2">
        <label for="code" class="block text-sm font-medium text-msit-dark-50 font-sans">Python Code</label>
        <div class="flex items-center gap-3">
          <span class="text-xs text-msit-dark-300 font-sans">{{ code.length }} characters, {{ code.split('\n').length }} lines</span>
          <span v-if="executionTime > 0" class="text-xs text-msit-accent font-sans">{{ executionTime }}ms</span>
        </div>
      </div>
      <div class="relative">
        <!-- Line Numbers -->
        <div class="absolute left-0 top-0 bottom-0 w-12 bg-msit-dark-800 border-r border-msit-dark-600 text-right py-2 font-mono text-xs text-msit-dark-400 select-none z-10">
          <div v-for="n in code.split('\n').length" :key="n" class="px-2">{{ n }}</div>
        </div>
        <!-- Code Editor -->
        <textarea
          id="code"
          ref="codeEditor"
          v-model="code"
          rows="12"
          class="shadow-sm focus:ring-msit-accent focus:border-msit-accent block w-full text-sm sm:text-base border-msit-dark-600 bg-msit-dark-700 text-msit-dark-50 placeholder-msit-dark-300 rounded-md font-mono px-3 py-2 pl-16 border resize-y"
          placeholder="print('Hello, StudyHall!')"
          @input="saveToHistory"
          @paste.prevent="handlePaste"
          @copy.prevent="handleCopy"
          @cut.prevent="handleCut"
          @keydown="handleEditorKeyDown"
          @contextmenu.prevent="handleContextMenu"
        ></textarea>
        <!-- Copy/Paste Warning Overlay -->
        <div v-if="showCopyWarning" class="absolute inset-0 bg-red-900/80 flex items-center justify-center rounded-md z-20">
          <div class="bg-msit-dark-800 border-2 border-red-500 rounded-lg p-4 max-w-sm text-center">
            <div class="text-red-300 font-semibold mb-2 font-sans">Copy/Paste Disabled</div>
            <div class="text-sm text-msit-dark-200 font-sans">Type your code manually to improve your learning!</div>
          </div>
        </div>
      </div>
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
        <div class="flex items-center gap-2">
          <span v-if="lastRunSuccess !== null" class="text-xs font-sans" :class="lastRunSuccess ? 'text-green-400' : 'text-red-400'">
            {{ lastRunSuccess ? '✓ Success' : '✗ Error' }}
          </span>
          <button
            v-if="output"
            @click="copyOutput"
            class="text-xs text-msit-dark-300 hover:text-msit-accent transition-colors font-sans self-start sm:self-auto"
          >
            Copy Output
          </button>
        </div>
      </div>
      <div class="bg-msit-dark-900 text-msit-accent p-3 sm:p-4 rounded-md font-mono text-xs sm:text-sm overflow-auto max-h-64 sm:max-h-96 border border-msit-dark-700">
        <pre class="whitespace-pre-wrap wrap-break-word">{{ output || 'Ready to run code...' }}</pre>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, onUnmounted, nextTick } from 'vue'

const code = ref('print("Hello, StudyHall!")')
const output = ref('Ready!')
const isLoading = ref(true)
const showSnippets = ref(false)
const showHistory = ref(false)
const showStudyHelp = ref(false)
const showVariables = ref(false)
const showCopyWarning = ref(false)
const codeHistory = ref<Array<{ code: string; timestamp: string }>>([])
const executionTime = ref(0)
const lastRunSuccess = ref<boolean | null>(null)
const currentError = ref('')
const variables = ref<Array<{ name: string; value: string; type: string }>>([])
const codeEditor = ref<HTMLTextAreaElement | null>(null)
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
    currentError.value = ''
    variables.value = []
    lastRunSuccess.value = null
    const startTime = performance.now()
    
    pyodide.setStdout({ batched: (msg: string) => {
      output.value += msg + '\n'
    }})
    pyodide.setStderr({ batched: (msg: string) => {
      output.value += `ERROR: ${msg}\n`
      analyzeError(msg)
    }})
    
    await pyodide.runPythonAsync(code.value)
    
    // Extract variables
    try {
      const globals = pyodide.globals.toJs({ dict_converter: Object.fromEntries })
      const variableList: Array<{ name: string; value: string; type: string }> = []
      
      for (const [key, value] of Object.entries(globals)) {
        if (!key.startsWith('_') && typeof value !== 'function' && key !== 'pyodide') {
          const typeName = typeof value === 'object' && value !== null 
            ? Array.isArray(value) ? 'list' : value.constructor?.name || 'object'
            : typeof value
          variableList.push({
            name: key,
            value: String(value),
            type: typeName
          })
        }
      }
      variables.value = variableList
    } catch (e) {
      // Ignore variable extraction errors
    }
    
    const endTime = performance.now()
    executionTime.value = Math.round(endTime - startTime)
    lastRunSuccess.value = true
    saveToHistory()
  } catch (err: any) {
    const endTime = performance.now()
    executionTime.value = Math.round(endTime - startTime)
    output.value = `Error: ${err}`
    analyzeError(String(err))
    lastRunSuccess.value = false
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

const handlePaste = (e: ClipboardEvent) => {
  e.preventDefault()
  showCopyWarningMessage()
}

const handleCopy = (e: ClipboardEvent) => {
  e.preventDefault()
  showCopyWarningMessage()
}

const handleCut = (e: ClipboardEvent) => {
  e.preventDefault()
  showCopyWarningMessage()
}

const showCopyWarningMessage = () => {
  showCopyWarning.value = true
  setTimeout(() => {
    showCopyWarning.value = false
  }, 2000)
}

const handleEditorKeyDown = (e: KeyboardEvent) => {
  // Prevent Ctrl+V, Ctrl+C, Ctrl+X in code editor
  if ((e.ctrlKey || e.metaKey) && (e.key === 'v' || e.key === 'c' || e.key === 'x')) {
    e.preventDefault()
    showCopyWarningMessage()
    return
  }
  
  // Ctrl/Cmd + Enter to run code
  if ((e.ctrlKey || e.metaKey) && e.key === 'Enter') {
    e.preventDefault()
    runPython()
  }
}

const handleContextMenu = (e: MouseEvent) => {
  e.preventDefault()
  showCopyWarningMessage()
}

const handleKeyDown = (e: KeyboardEvent) => {
  // Global shortcuts (only when not in code editor)
  const target = e.target as HTMLElement
  if (target.tagName === 'TEXTAREA' && target.id === 'code') {
    return // Let handleEditorKeyDown handle it
  }
  
  // Ctrl/Cmd + Enter to run code (global)
  if ((e.ctrlKey || e.metaKey) && e.key === 'Enter') {
    e.preventDefault()
    runPython()
  }
  // Ctrl/Cmd + S to save/export (global)
  if ((e.ctrlKey || e.metaKey) && e.key === 's') {
    e.preventDefault()
    exportCode()
  }
}

const analyzeError = (errorMsg: string) => {
  const errorLower = errorMsg.toLowerCase()
  
  if (errorLower.includes('syntaxerror') || errorLower.includes('invalid syntax')) {
    currentError.value = 'Syntax Error: Check for missing colons (:), unmatched parentheses, brackets, or quotes. Make sure your indentation is correct.'
  } else if (errorLower.includes('nameerror') || errorLower.includes('is not defined')) {
    currentError.value = 'Name Error: You\'re using a variable or function that hasn\'t been defined. Check spelling and make sure you\'ve assigned a value before using it.'
  } else if (errorLower.includes('typeerror')) {
    currentError.value = 'Type Error: You\'re trying to perform an operation on incompatible types. Check if you\'re mixing strings with numbers or calling methods on wrong types.'
  } else if (errorLower.includes('indentationerror') || errorLower.includes('unexpected indent')) {
    currentError.value = 'Indentation Error: Python uses indentation to define code blocks. Make sure you use consistent spaces (usually 4) for each level of indentation.'
  } else if (errorLower.includes('indexerror') || errorLower.includes('list index out of range')) {
    currentError.value = 'Index Error: You\'re trying to access an index that doesn\'t exist. Remember: lists start at index 0, so the last item is at index length-1.'
  } else if (errorLower.includes('keyerror')) {
    currentError.value = 'Key Error: The dictionary key you\'re trying to access doesn\'t exist. Use .get() method or check if the key exists first.'
  } else if (errorLower.includes('attributeerror')) {
    currentError.value = 'Attribute Error: The object doesn\'t have the attribute or method you\'re trying to use. Check the object type and available methods.'
  } else if (errorLower.includes('valueerror')) {
    currentError.value = 'Value Error: The function received the right type but an inappropriate value. Check function arguments and their expected ranges.'
  } else {
    currentError.value = 'Error detected. Read the error message carefully and check your code logic. Common issues: typos, wrong variable names, or incorrect function calls.'
  }
}

const studyTips = ref([
  {
    title: '💡 Start Simple',
    description: 'Begin with basic print statements and gradually add complexity. Master fundamentals before moving to advanced topics.'
  },
  {
    title: '📝 Read Error Messages',
    description: 'Python error messages tell you exactly what went wrong and where. Read them carefully - they\'re your best debugging tool!'
  },
  {
    title: '🔍 Use Print Statements',
    description: 'Add print() statements to see what values your variables have at different points in your code. This helps you understand what\'s happening.'
  },
  {
    title: '🎯 One Problem at a Time',
    description: 'Break complex problems into smaller pieces. Solve each piece separately, then combine them together.'
  },
  {
    title: '📚 Practice Regularly',
    description: 'Coding is a skill that improves with practice. Try writing code daily, even if it\'s just a few lines.'
  },
  {
    title: '🐍 Pythonic Style',
    description: 'Python values readability. Use meaningful variable names, add comments for complex logic, and follow PEP 8 style guidelines.'
  }
])

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
