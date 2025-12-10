<template>
  <div class="px-4 py-4 sm:py-6 sm:px-0">
    <div class="mb-6 sm:mb-8">
      <h1 class="text-2xl sm:text-3xl font-bold text-msit-dark-50 mb-2 font-serif">Export Your Work</h1>
      <p class="text-sm sm:text-base text-msit-dark-200 font-sans">Export your code, materials, and notes from today</p>
    </div>
    
    <div class="space-y-6">
      <!-- Code Export -->
      <div class="bg-msit-dark-800 border border-msit-dark-700 rounded-lg p-4 sm:p-6">
        <h3 class="text-lg font-semibold text-msit-dark-50 mb-3 font-sans">Code Snippets</h3>
        <p class="text-sm text-msit-dark-200 mb-4 font-sans">Export all code you've written today</p>
        <button
          @click="exportCode"
          class="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md text-msit-dark bg-msit-accent hover:bg-msit-accent-500 transition-colors font-sans"
        >
          <svg class="h-4 w-4 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4" />
          </svg>
          Export Code History
        </button>
      </div>

      <!-- Materials Export -->
      <div class="bg-msit-dark-800 border border-msit-dark-700 rounded-lg p-4 sm:p-6">
        <h3 class="text-lg font-semibold text-msit-dark-50 mb-3 font-sans">Materials</h3>
        <p class="text-sm text-msit-dark-200 mb-4 font-sans">Export materials you've viewed today</p>
        <button
          @click="exportMaterials"
          class="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md text-msit-dark bg-msit-accent hover:bg-msit-accent-500 transition-colors font-sans"
        >
          <svg class="h-4 w-4 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4" />
          </svg>
          Export Materials
        </button>
      </div>

      <!-- Complete Export -->
      <div class="bg-msit-dark-800 border-2 border-msit-accent rounded-lg p-4 sm:p-6">
        <h3 class="text-lg font-semibold text-msit-dark-50 mb-3 font-sans">Complete Export</h3>
        <p class="text-sm text-msit-dark-200 mb-4 font-sans">Export everything: code, materials, and notes in one file</p>
        <button
          @click="exportEverything"
          class="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md text-msit-dark bg-msit-accent hover:bg-msit-accent-500 transition-colors font-sans"
        >
          <svg class="h-4 w-4 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-8l-4-4m0 0L8 8m4-4v12" />
          </svg>
          Export Everything
        </button>
      </div>

      <!-- Export History -->
      <div class="bg-msit-dark-800 border border-msit-dark-700 rounded-lg p-4 sm:p-6">
        <h3 class="text-lg font-semibold text-msit-dark-50 mb-3 font-sans">Recent Exports</h3>
        <div v-if="exportHistory.length === 0" class="text-sm text-msit-dark-300 font-sans">
          No exports yet
        </div>
        <div v-else class="space-y-2">
          <div
            v-for="(exportItem, index) in exportHistory"
            :key="index"
            class="flex items-center justify-between p-2 bg-msit-dark-900 rounded border border-msit-dark-700"
          >
            <div>
              <div class="text-sm font-medium text-msit-dark-50 font-sans">{{ exportItem.filename }}</div>
              <div class="text-xs text-msit-dark-300 font-sans">{{ exportItem.timestamp }}</div>
            </div>
            <button
              @click="downloadExport(exportItem)"
              class="text-sm text-msit-accent hover:text-msit-accent-300 transition-colors font-sans"
            >
              Download
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'

const exportHistory = ref<Array<{ filename: string; timestamp: string; data: any }>>([])

const loadExportHistory = () => {
  const stored = localStorage.getItem('export_history')
  if (stored) {
    try {
      exportHistory.value = JSON.parse(stored)
    } catch (e) {
      exportHistory.value = []
    }
  }
}

const saveExportHistory = (filename: string, data: any) => {
  const item = {
    filename,
    timestamp: new Date().toLocaleString(),
    data
  }
  exportHistory.value.unshift(item)
  if (exportHistory.value.length > 10) {
    exportHistory.value = exportHistory.value.slice(0, 10)
  }
  localStorage.setItem('export_history', JSON.stringify(exportHistory.value))
}

const downloadFile = (content: string, filename: string, type: string = 'text/plain') => {
  const blob = new Blob([content], { type })
  const url = URL.createObjectURL(blob)
  const a = document.createElement('a')
  a.href = url
  a.download = filename
  document.body.appendChild(a)
  a.click()
  document.body.removeChild(a)
  URL.revokeObjectURL(url)
}

const exportCode = () => {
  const history = localStorage.getItem('python_code_history')
  if (!history) {
    alert('No code history found')
    return
  }
  
  try {
    const codeHistory = JSON.parse(history)
    const content = `# Code Export - ${new Date().toLocaleDateString()}\n\n` +
      codeHistory.map((item: any, index: number) => 
        `## Code Snippet ${index + 1} - ${item.timestamp}\n\`\`\`python\n${item.code}\n\`\`\`\n`
      ).join('\n')
    
    const filename = `code-export-${new Date().toISOString().split('T')[0]}.md`
    downloadFile(content, filename, 'text/markdown')
    saveExportHistory(filename, { type: 'code', data: codeHistory })
  } catch (e) {
    alert('Error exporting code')
  }
}

const exportMaterials = async () => {
  try {
    const response = await fetch('/api/materials', {
      credentials: 'include'
    })
    if (!response.ok) {
      alert('Failed to fetch materials')
      return
    }
    
    const materials = await response.json()
    const content = `# Materials Export - ${new Date().toLocaleDateString()}\n\n` +
      materials.map((m: any) => 
        `## ${m.title}\n\n` +
        `**Category:** ${m.category || 'N/A'}\n\n` +
        `${m.content}\n\n` +
        `---\n\n`
      ).join('')
    
    const filename = `materials-export-${new Date().toISOString().split('T')[0]}.md`
    downloadFile(content, filename, 'text/markdown')
    saveExportHistory(filename, { type: 'materials', data: materials })
  } catch (e) {
    alert('Error exporting materials')
  }
}

const exportEverything = async () => {
  try {
    const codeHistory = localStorage.getItem('python_code_history')
    const codeData = codeHistory ? JSON.parse(codeHistory) : []
    
    const response = await fetch('/api/materials', {
      credentials: 'include'
    })
    const materials = response.ok ? await response.json() : []
    
    const content = {
      exportDate: new Date().toISOString(),
      code: codeData,
      materials: materials,
      summary: {
        codeSnippets: codeData.length,
        materials: materials.length
      }
    }
    
    const filename = `studyhall-export-${new Date().toISOString().split('T')[0]}.json`
    downloadFile(JSON.stringify(content, null, 2), filename, 'application/json')
    saveExportHistory(filename, content)
  } catch (e) {
    alert('Error exporting everything')
  }
}

const downloadExport = (item: any) => {
  const content = typeof item.data === 'string' 
    ? item.data 
    : JSON.stringify(item.data, null, 2)
  const type = item.filename.endsWith('.json') ? 'application/json' : 'text/markdown'
  downloadFile(content, item.filename, type)
}

onMounted(() => {
  loadExportHistory()
})
</script>
