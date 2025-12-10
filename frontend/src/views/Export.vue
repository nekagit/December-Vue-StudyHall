<template>
  <div class="px-4 py-6 sm:px-0">
    <div class="bg-white shadow rounded-lg overflow-hidden">
      <div class="px-6 py-4 border-b border-gray-200">
        <h1 class="text-3xl font-bold text-gray-900">Export Your Work</h1>
        <p class="mt-2 text-sm text-gray-600">Export your code, materials, and notes from today</p>
      </div>
      
      <div class="px-6 py-4">
        <div class="space-y-6">
          <!-- Code Export -->
          <div class="border border-gray-200 rounded-lg p-4">
            <h3 class="text-lg font-semibold text-gray-900 mb-3">Code Snippets</h3>
            <p class="text-sm text-gray-600 mb-4">Export all code you've written today</p>
            <button
              @click="exportCode"
              class="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md text-white bg-indigo-600 hover:bg-indigo-700"
            >
              <svg class="h-4 w-4 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4" />
              </svg>
              Export Code History
            </button>
          </div>

          <!-- Materials Export -->
          <div class="border border-gray-200 rounded-lg p-4">
            <h3 class="text-lg font-semibold text-gray-900 mb-3">Materials</h3>
            <p class="text-sm text-gray-600 mb-4">Export materials you've viewed today</p>
            <button
              @click="exportMaterials"
              class="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md text-white bg-indigo-600 hover:bg-indigo-700"
            >
              <svg class="h-4 w-4 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4" />
              </svg>
              Export Materials
            </button>
          </div>

          <!-- Complete Export -->
          <div class="border-2 border-indigo-500 rounded-lg p-4 bg-indigo-50">
            <h3 class="text-lg font-semibold text-gray-900 mb-3">Complete Export</h3>
            <p class="text-sm text-gray-600 mb-4">Export everything: code, materials, and notes in one file</p>
            <button
              @click="exportEverything"
              class="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md text-white bg-indigo-600 hover:bg-indigo-700"
            >
              <svg class="h-4 w-4 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-8l-4-4m0 0L8 8m4-4v12" />
              </svg>
              Export Everything
            </button>
          </div>

          <!-- Export History -->
          <div class="border border-gray-200 rounded-lg p-4">
            <h3 class="text-lg font-semibold text-gray-900 mb-3">Recent Exports</h3>
            <div v-if="exportHistory.length === 0" class="text-sm text-gray-500">
              No exports yet
            </div>
            <div v-else class="space-y-2">
              <div
                v-for="(exportItem, index) in exportHistory"
                :key="index"
                class="flex items-center justify-between p-2 bg-gray-50 rounded"
              >
                <div>
                  <div class="text-sm font-medium text-gray-900">{{ exportItem.filename }}</div>
                  <div class="text-xs text-gray-500">{{ exportItem.timestamp }}</div>
                </div>
                <button
                  @click="downloadExport(exportItem)"
                  class="text-sm text-indigo-600 hover:text-indigo-700"
                >
                  Download
                </button>
              </div>
            </div>
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
