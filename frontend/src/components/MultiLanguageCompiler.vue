<template>
  <div class="space-y-4">
    <!-- Language Selector -->
    <div class="flex flex-wrap items-center gap-2 pb-2 border-b border-msit-dark-700">
      <div class="flex items-center gap-2">
        <label class="text-sm font-medium text-msit-dark-50 font-sans">Language:</label>
        <select
          v-model="selectedLanguage"
          @change="onLanguageChange"
          class="px-3 py-1.5 bg-msit-dark-700 border border-msit-dark-600 rounded-md text-msit-dark-50 text-sm font-sans focus:outline-none focus:ring-2 focus:ring-msit-accent"
        >
          <option value="python">Python</option>
          <option value="javascript">JavaScript</option>
          <option value="html">HTML/CSS</option>
          <option value="php">PHP</option>
          <option value="dart">Flutter/Dart</option>
        </select>
      </div>
      
      <!-- Toolbar Buttons -->
      <button
        @click="showTemplates = !showTemplates"
        class="inline-flex items-center px-3 py-1.5 border border-msit-dark-600 shadow-sm text-sm font-medium rounded-md text-msit-dark-50 bg-msit-dark-700 hover:bg-msit-dark-600 transition-colors font-sans"
      >
        <svg class="h-4 w-4 mr-1" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16" />
        </svg>
        <span class="hidden sm:inline">Templates</span>
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

    <!-- Code Templates Panel -->
    <div v-if="showTemplates" class="bg-msit-dark-700 border border-msit-dark-600 rounded-md p-4">
      <h3 class="text-sm font-semibold text-msit-dark-50 mb-3 font-sans">Code Templates</h3>
      <div class="grid grid-cols-1 sm:grid-cols-2 gap-2">
        <button
          v-for="template in currentTemplates"
          :key="template.name"
          @click="loadTemplate(template.code)"
          class="text-left px-3 py-2 bg-msit-dark-800 border border-msit-dark-600 rounded hover:bg-msit-dark-600 hover:border-msit-accent transition-colors"
        >
          <div class="font-medium text-sm text-msit-dark-50 font-sans">{{ template.name }}</div>
          <div class="text-xs text-msit-dark-300 mt-1 font-sans">{{ template.description }}</div>
        </button>
      </div>
    </div>

    <!-- Code Editor -->
    <div>
      <div class="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-2 mb-2">
        <label class="block text-sm font-medium text-msit-dark-50 font-sans">
          {{ languageLabels[selectedLanguage] }} Code
        </label>
        <div class="flex items-center gap-3">
          <span class="text-xs text-msit-dark-300 font-sans">
            {{ code.length }} characters, {{ code.split('\n').length }} lines
          </span>
          <span v-if="executionTime > 0" class="text-xs text-msit-accent font-sans">{{ executionTime }}ms</span>
        </div>
      </div>
      <div class="relative border border-msit-dark-600 rounded-md overflow-hidden">
        <div ref="editorContainer" class="code-editor-container"></div>
      </div>
    </div>
    
    <!-- Action Buttons -->
    <div class="flex flex-col sm:flex-row items-stretch sm:items-center gap-2">
      <button
        @click="runCode"
        :disabled="isLoading"
        class="w-full sm:w-auto inline-flex items-center justify-center px-4 py-2 border border-transparent text-sm font-medium rounded-md shadow-sm text-msit-dark bg-msit-accent hover:bg-msit-accent-500 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-msit-accent disabled:opacity-50 transition-colors font-sans"
      >
        <svg v-if="!isLoading" class="h-4 w-4 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M14.752 11.168l-3.197-2.132A1 1 0 0010 9.87v4.263a1 1 0 001.555.832l3.197-2.132a1 1 0 000-1.664z" />
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
        </svg>
        {{ runButtonText }}
      </button>
      <button
        v-if="output"
        @click="clearOutput"
        class="w-full sm:w-auto inline-flex items-center justify-center px-3 py-2 border border-msit-dark-600 shadow-sm text-sm font-medium rounded-md text-msit-dark-50 bg-msit-dark-700 hover:bg-msit-dark-600 transition-colors font-sans"
      >
        Clear Output
      </button>
    </div>
    
    <!-- Output / Preview -->
    <div>
      <div class="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-2 mb-2">
        <label class="block text-sm font-medium text-msit-dark-50 font-sans">
          {{ selectedLanguage === 'html' ? 'Preview' : 'Output' }}
        </label>
        <div class="flex items-center gap-2">
          <span v-if="lastRunSuccess !== null" class="text-xs font-sans" :class="lastRunSuccess ? 'text-green-400' : 'text-red-400'">
            {{ lastRunSuccess ? '✓ Success' : '✗ Error' }}
          </span>
          <button
            v-if="output && selectedLanguage !== 'html'"
            @click="copyOutput"
            class="text-xs text-msit-dark-300 hover:text-msit-accent transition-colors font-sans"
          >
            Copy Output
          </button>
        </div>
      </div>
      
      <!-- HTML Preview -->
      <div v-if="selectedLanguage === 'html'" class="bg-white rounded-md border border-msit-dark-600 overflow-hidden" style="min-height: 300px;">
        <iframe
          ref="htmlPreview"
          class="w-full h-full"
          style="min-height: 300px;"
          sandbox="allow-scripts"
        ></iframe>
      </div>
      
      <!-- Text Output -->
      <div v-else class="bg-msit-dark-900 text-msit-accent p-3 sm:p-4 rounded-md font-mono text-xs sm:text-sm overflow-auto max-h-64 sm:max-h-96 border border-msit-dark-700">
        <pre class="whitespace-pre-wrap wrap-break-word">{{ output || 'Ready to run code...' }}</pre>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, onUnmounted, nextTick, computed } from 'vue'
import { EditorView, basicSetup } from 'codemirror'
import { keymap } from '@codemirror/view'
import { python } from '@codemirror/lang-python'
import { javascript } from '@codemirror/lang-javascript'
import { html } from '@codemirror/lang-html'
import { php } from '@codemirror/lang-php'
import { EditorState } from '@codemirror/state'

type Language = 'python' | 'javascript' | 'html' | 'php' | 'dart'

const selectedLanguage = ref<Language>('python')
const code = ref('print("Hello, StudyHall!")')
const output = ref('Ready!')
const isLoading = ref(false)
const showTemplates = ref(false)
const executionTime = ref(0)
const lastRunSuccess = ref<boolean | null>(null)
const editorContainer = ref<HTMLElement | null>(null)
const htmlPreview = ref<HTMLIFrameElement | null>(null)

let editorView: EditorView | null = null
let pyodide: any = null

const languageLabels: Record<Language, string> = {
  python: 'Python',
  javascript: 'JavaScript',
  html: 'HTML/CSS',
  php: 'PHP',
  dart: 'Flutter/Dart'
}

const runButtonText = computed(() => {
  if (isLoading.value) {
    return selectedLanguage.value === 'python' ? 'Loading Pyodide...' : 'Running...'
  }
  return selectedLanguage.value === 'html' ? 'Preview' : 'Run Code'
})

// Templates for each language
const templates: Record<Language, Array<{ name: string; description: string; code: string }>> = {
  python: [
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
      name: 'Functions',
      description: 'Define and call functions',
      code: `def greet(name):
    return f"Hello, {name}!"

def add(a, b):
    return a + b

print(greet("StudyHall"))
print(f"5 + 3 = {add(5, 3)}")`
    }
  ],
  javascript: [
    {
      name: 'Hello World',
      description: 'Basic console.log',
      code: 'console.log("Hello, World!");'
    },
    {
      name: 'Variables',
      description: 'Variable declarations',
      code: `const name = "StudyHall";
let age = 25;
const height = 5.9;
const isStudent = true;

console.log(\`Name: \${name}, Age: \${age}, Height: \${height}, Student: \${isStudent}\`);`
    },
    {
      name: 'Arrays',
      description: 'Working with arrays',
      code: `const numbers = [1, 2, 3, 4, 5];
console.log("First:", numbers[0]);
console.log("Last:", numbers[numbers.length - 1]);
console.log("Sum:", numbers.reduce((a, b) => a + b, 0));
console.log("Length:", numbers.length);`
    },
    {
      name: 'Functions',
      description: 'Function declarations',
      code: `function greet(name) {
  return \`Hello, \${name}!\`;
}

const add = (a, b) => a + b;

console.log(greet("StudyHall"));
console.log(\`5 + 3 = \${add(5, 3)}\`);`
    },
    {
      name: 'Async/Await',
      description: 'Asynchronous programming',
      code: `async function fetchData() {
  console.log("Fetching data...");
  await new Promise(resolve => setTimeout(resolve, 1000));
  console.log("Data fetched!");
  return { message: "Success" };
}

fetchData().then(data => console.log(data));`
    }
  ],
  html: [
    {
      name: 'Basic HTML',
      description: 'Simple HTML page',
      code: `<!DOCTYPE html>
<html>
<head>
  <title>StudyHall</title>
  <style>
    body {
      font-family: Arial, sans-serif;
      padding: 20px;
      background: #f0f0f0;
    }
    h1 { color: #333; }
  <\/style>
<\/head>
<body>
  <h1>Hello, StudyHall!</h1>
  <p>This is a simple HTML page.</p>
<\/body>
<\/html>`
    },
    {
      name: 'Styled Card',
      description: 'Card component with CSS',
      code: `<!DOCTYPE html>
<html>
<head>
  <style>
    body {
      display: flex;
      justify-content: center;
      align-items: center;
      min-height: 100vh;
      margin: 0;
      background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
      font-family: Arial, sans-serif;
    }
    .card {
      background: white;
      padding: 30px;
      border-radius: 10px;
      box-shadow: 0 10px 30px rgba(0,0,0,0.2);
      max-width: 400px;
    }
    h1 {
      color: #667eea;
      margin-top: 0;
    }
  <\/style>
<\/head>
<body>
  <div class="card">
    <h1>Welcome to StudyHall</h1>
    <p>Learn to code with interactive examples!</p>
    <button onclick="alert('Hello!')">Click Me</button>
  </div>
<\/body>
<\/html>`
    },
    {
      name: 'Interactive Form',
      description: 'Form with JavaScript',
      code: `<!DOCTYPE html>
<html>
<head>
  <style>
    body { font-family: Arial; padding: 20px; }
    input { padding: 8px; margin: 5px 0; width: 200px; }
    button { padding: 10px 20px; background: #667eea; color: white; border: none; cursor: pointer; }
  <\/style>
<\/head>
<body>
  <h2>Greeting Form</h2>
  <input type="text" id="nameInput" placeholder="Enter your name">
  <button onclick="greet()">Greet</button>
  <p id="output"></p>
  
  <script>
    function greet() {
      const name = document.getElementById('nameInput').value;
      document.getElementById('output').textContent = 'Hello, ' + name + '!';
    }
  <\/script>
<\/body>
<\/html>`
    }
  ],
  php: [
    {
      name: 'Hello World',
      description: 'Basic PHP echo',
      code: `<?php
echo "Hello, World!";
?>`
    },
    {
      name: 'Variables',
      description: 'PHP variables and types',
      code: `<?php
$name = "StudyHall";
$age = 25;
$height = 5.9;
$isStudent = true;

echo "Name: $name, Age: $age, Height: $height, Student: " . ($isStudent ? "Yes" : "No");
?>`
    },
    {
      name: 'Arrays',
      description: 'Working with arrays',
      code: `<?php
$numbers = [1, 2, 3, 4, 5];
echo "First: " . $numbers[0] . "\\n";
echo "Last: " . end($numbers) . "\\n";
echo "Sum: " . array_sum($numbers) . "\\n";
echo "Count: " . count($numbers);
?>`
    },
    {
      name: 'Functions',
      description: 'PHP functions',
      code: `<?php
function greet($name) {
    return "Hello, $name!";
}

function add($a, $b) {
    return $a + $b;
}

echo greet("StudyHall") . "\\n";
echo "5 + 3 = " . add(5, 3);
?>`
    }
  ],
  dart: [
    {
      name: 'Hello World',
      description: 'Basic Dart print',
      code: `void main() {
  print('Hello, World!');
}`
    },
    {
      name: 'Variables',
      description: 'Dart variables and types',
      code: `void main() {
  String name = 'StudyHall';
  int age = 25;
  double height = 5.9;
  bool isStudent = true;
  
  print('Name: $name, Age: $age, Height: $height, Student: $isStudent');
}`
    },
    {
      name: 'Lists',
      description: 'Working with lists',
      code: `void main() {
  List<int> numbers = [1, 2, 3, 4, 5];
  print('First: \${numbers.first}');
  print('Last: \${numbers.last}');
  print('Sum: \${numbers.reduce((a, b) => a + b)}');
  print('Length: \${numbers.length}');
}`
    },
    {
      name: 'Functions',
      description: 'Dart functions',
      code: `String greet(String name) {
  return 'Hello, $name!';
}

int add(int a, int b) => a + b;

void main() {
  print(greet('StudyHall'));
  print('5 + 3 = \${add(5, 3)}');
}`
    },
    {
      name: 'Flutter Widget',
      description: 'Basic Flutter widget structure',
      code: `import 'package:flutter/material.dart';

void main() => runApp(MyApp());

class MyApp extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      home: Scaffold(
        appBar: AppBar(title: Text('StudyHall')),
        body: Center(
          child: Text('Hello, Flutter!'),
        ),
      ),
    );
  }
}`
    }
  ]
}

const currentTemplates = computed(() => templates[selectedLanguage.value])

// Language mode getter
const getLanguageMode = () => {
  switch (selectedLanguage.value) {
    case 'python':
      return python()
    case 'javascript':
      return javascript()
    case 'html':
      return html()
    case 'php':
      return php()
    case 'dart':
      return javascript() // Use JavaScript mode for Dart (similar syntax)
    default:
      return python()
  }
}

// Initialize editor
const initEditor = async () => {
  if (!editorContainer.value) return
  
  await nextTick()
  
  const customTheme = EditorView.theme({
    '&': {
      backgroundColor: '#1e293b',
      color: '#f1f5f9',
      fontSize: '14px'
    },
    '.cm-content': {
      padding: '12px',
      minHeight: '300px'
    },
    '.cm-focused': {
      outline: 'none'
    },
    '.cm-gutters': {
      backgroundColor: '#0f172a',
      borderRight: '1px solid #334155',
      color: '#64748b'
    }
  }, { dark: true })
  
  const state = EditorState.create({
    doc: code.value,
    extensions: [
      basicSetup,
      getLanguageMode(),
      customTheme,
      EditorView.updateListener.of((update) => {
        if (update.docChanged) {
          code.value = update.state.doc.toString()
        }
      }),
      keymap.of([
        {
          key: 'Mod-Enter',
          run: () => {
            runCode()
            return true
          }
        }
      ])
    ]
  })
  
  editorView = new EditorView({
    state,
    parent: editorContainer.value
  })
}

// Update editor when language changes
const onLanguageChange = async () => {
  // Load default code for the language
  const defaultCodes: Record<Language, string> = {
    python: 'print("Hello, StudyHall!")',
    javascript: 'console.log("Hello, StudyHall!");',
    html: '<!DOCTYPE html>\n<html>\n<head>\n  <title>StudyHall<\/title>\n<\/head>\n<body>\n  <h1>Hello, StudyHall!</h1>\n<\/body>\n<\/html>',
    php: '<?php\necho "Hello, StudyHall!";\n?>',
    dart: 'void main() {\n  print(\'Hello, StudyHall!\');\n}'
  }
  
  code.value = defaultCodes[selectedLanguage.value]
  output.value = 'Ready!'
  lastRunSuccess.value = null
  
  // Recreate editor with new language mode
  if (editorView) {
    editorView.destroy()
  }
  await initEditor()
}

// Run code based on language
const runCode = async () => {
  const startTime = performance.now()
  
  try {
    output.value = ''
    lastRunSuccess.value = null
    
    switch (selectedLanguage.value) {
      case 'python':
        await runPython()
        break
      case 'javascript':
        await runJavaScript()
        break
      case 'html':
        await previewHTML()
        break
      case 'php':
        output.value = 'PHP execution requires a server environment.\nThis is a client-side editor for learning PHP syntax.'
        lastRunSuccess.value = null
        break
      case 'dart':
        output.value = 'Dart/Flutter execution requires the Dart SDK.\nThis editor is for learning Dart syntax and Flutter widget structure.'
        lastRunSuccess.value = null
        break
    }
    
    const endTime = performance.now()
    executionTime.value = Math.round(endTime - startTime)
  } catch (err: any) {
    output.value = `Error: ${err}`
    lastRunSuccess.value = false
    const endTime = performance.now()
    executionTime.value = Math.round(endTime - startTime)
  }
}

// Python execution
const loadPyodide = async () => {
  if (pyodide) return
  
  isLoading.value = true
  output.value = 'Loading Pyodide environment...'
  
  try {
    if (!(window as any).loadPyodide) {
      const script = document.createElement('script')
      script.src = "https://cdn.jsdelivr.net/pyodide/v0.25.0/full/pyodide.js"
      await new Promise((resolve, reject) => {
        script.onload = resolve
        script.onerror = reject
        document.head.appendChild(script)
      })
    }
    
    pyodide = await (window as any).loadPyodide()
    output.value = 'Ready!'
  } catch (e: any) {
    output.value = `Error loading Pyodide: ${e}`
  } finally {
    isLoading.value = false
  }
}

const runPython = async () => {
  if (!pyodide) {
    await loadPyodide()
  }
  
  if (!pyodide) return
  
  try {
    output.value = ''
    
    pyodide.setStdout({ batched: (msg: string) => {
      output.value += msg + '\n'
    }})
    pyodide.setStderr({ batched: (msg: string) => {
      output.value += `ERROR: ${msg}\n`
    }})
    
    await pyodide.runPythonAsync(code.value)
    lastRunSuccess.value = true
  } catch (err: any) {
    output.value = `Error: ${err}`
    lastRunSuccess.value = false
  }
}

// JavaScript execution
const runJavaScript = async () => {
  try {
    const logs: string[] = []
    
    // Override console methods
    const originalLog = console.log
    const originalError = console.error
    const originalWarn = console.warn
    
    console.log = (...args: any[]) => {
      logs.push(args.map(arg => 
        typeof arg === 'object' ? JSON.stringify(arg, null, 2) : String(arg)
      ).join(' '))
      originalLog(...args)
    }
    
    console.error = (...args: any[]) => {
      logs.push('ERROR: ' + args.map(arg => String(arg)).join(' '))
      originalError(...args)
    }
    
    console.warn = (...args: any[]) => {
      logs.push('WARNING: ' + args.map(arg => String(arg)).join(' '))
      originalWarn(...args)
    }
    
    // Execute code
    const AsyncFunction = Object.getPrototypeOf(async function(){}).constructor
    const fn = new AsyncFunction(code.value)
    await fn()
    
    // Restore console
    console.log = originalLog
    console.error = originalError
    console.warn = originalWarn
    
    output.value = logs.length > 0 ? logs.join('\n') : 'Code executed successfully (no output)'
    lastRunSuccess.value = true
  } catch (err: any) {
    output.value = `Error: ${err.message}`
    lastRunSuccess.value = false
  }
}

// HTML preview
const previewHTML = async () => {
  if (!htmlPreview.value) return
  
  try {
    const iframe = htmlPreview.value
    const doc = iframe.contentDocument || iframe.contentWindow?.document
    
    if (doc) {
      doc.open()
      doc.write(code.value)
      doc.close()
      lastRunSuccess.value = true
    }
  } catch (err: any) {
    output.value = `Error: ${err.message}`
    lastRunSuccess.value = false
  }
}

// Utility functions
const loadTemplate = (templateCode: string) => {
  code.value = templateCode
  showTemplates.value = false
  if (editorView) {
    editorView.dispatch({
      changes: {
        from: 0,
        to: editorView.state.doc.length,
        insert: templateCode
      }
    })
  }
}

const clearCode = () => {
  if (confirm('Clear all code?')) {
    code.value = ''
    if (editorView) {
      editorView.dispatch({
        changes: {
          from: 0,
          to: editorView.state.doc.length,
          insert: ''
        }
      })
    }
  }
}

const clearOutput = () => {
  output.value = ''
}

const formatCode = () => {
  // Simple formatting based on language
  if (selectedLanguage.value === 'python') {
    const lines = code.value.split('\n')
    let indent = 0
    const formatted: string[] = []
    
    for (const line of lines) {
      const trimmed = line.trim()
      if (!trimmed) {
        formatted.push('')
        continue
      }
      
      if (trimmed.startsWith('except') || trimmed.startsWith('elif') || 
          trimmed.startsWith('else') || trimmed.startsWith('finally')) {
        indent = Math.max(0, indent - 1)
      }
      
      formatted.push('  '.repeat(indent) + trimmed)
      
      if (trimmed.endsWith(':') && !trimmed.startsWith('#')) {
        indent += 1
      }
    }
    
    code.value = formatted.join('\n')
  }
  // Add formatting for other languages as needed
}

const exportCode = () => {
  const extensions: Record<Language, string> = {
    python: 'py',
    javascript: 'js',
    html: 'html',
    php: 'php',
    dart: 'dart'
  }
  
  const blob = new Blob([code.value], { type: 'text/plain' })
  const url = URL.createObjectURL(blob)
  const a = document.createElement('a')
  a.href = url
  a.download = `code-${new Date().toISOString().split('T')[0]}.${extensions[selectedLanguage.value]}`
  document.body.appendChild(a)
  a.click()
  document.body.removeChild(a)
  URL.revokeObjectURL(url)
}

const copyOutput = () => {
  navigator.clipboard.writeText(output.value)
}

onMounted(async () => {
  await initEditor()
  
  // Load Pyodide if Python is selected
  if (selectedLanguage.value === 'python') {
    loadPyodide()
  }
})

onUnmounted(() => {
  if (editorView) {
    editorView.destroy()
  }
})
</script>

<style scoped>
.code-editor-container {
  min-height: 300px;
}

.code-editor-container :deep(.cm-editor) {
  border-radius: 6px;
}

.code-editor-container :deep(.cm-scroller) {
  font-family: 'Monaco', 'Menlo', 'Ubuntu Mono', 'Consolas', 'source-code-pro', monospace;
}
</style>





