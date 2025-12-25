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
        <div class="flex flex-wrap gap-2 mb-4">
          <button
            @click="exportEverything('json')"
            class="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md text-msit-dark bg-msit-accent hover:bg-msit-accent-500 transition-colors font-sans"
          >
            <svg class="h-4 w-4 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-8l-4-4m0 0L8 8m4-4v12" />
            </svg>
            Export as JSON
          </button>
          <button
            @click="exportEverything('markdown')"
            class="inline-flex items-center px-4 py-2 border border-msit-dark-600 text-sm font-medium rounded-md text-msit-dark-200 bg-msit-dark-700 hover:bg-msit-dark-600 transition-colors font-sans"
          >
            <svg class="h-4 w-4 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
            </svg>
            Export as Markdown
          </button>
        </div>
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
    alert('No code history found. Start coding in the Compiler to build your history!')
    return
  }
  
  try {
    const codeHistory = JSON.parse(history)
    if (!Array.isArray(codeHistory) || codeHistory.length === 0) {
      alert('No code history found')
      return
    }
    
    const content = `# Code Export - ${new Date().toLocaleDateString()}\n\n` +
      `**Total Snippets:** ${codeHistory.length}\n\n` +
      `---\n\n` +
      codeHistory.map((item: any, index: number) => 
        `## Code Snippet ${index + 1}\n\n` +
        `*Timestamp: ${item.timestamp || 'Unknown time'}*\n\n` +
        `\`\`\`python\n${item.code || ''}\n\`\`\`\n\n` +
        `---\n\n`
      ).join('')
    
    const filename = `code-export-${new Date().toISOString().split('T')[0]}.md`
    downloadFile(content, filename, 'text/markdown')
    saveExportHistory(filename, { type: 'code', data: codeHistory })
  } catch (e) {
    console.error('Export error:', e)
    alert('Error exporting code. Please try again.')
  }
}

const exportMaterials = async () => {
  try {
    const response = await fetch('/api/materials', {
      credentials: 'include'
    })
    if (!response.ok) {
      alert('Failed to fetch materials. Please check your connection and try again.')
      return
    }
    
    const materials = await response.json()
    if (!Array.isArray(materials) || materials.length === 0) {
      alert('No materials found.')
      return
    }
    
    const content = `# Materials Export - ${new Date().toLocaleDateString()}\n\n` +
      `**Total Materials:** ${materials.length}\n\n` +
      `---\n\n` +
      materials.map((m: any) => 
        `## ${m.title || 'Untitled'}\n\n` +
        `**Category:** ${m.category || 'N/A'}\n` +
        (m.created_at ? `**Created:** ${m.created_at}\n` : '') +
        (m.notion_url ? `**Notion URL:** [View](${m.notion_url})\n` : '') +
        `\n${m.content || 'No content'}\n\n` +
        `---\n\n`
      ).join('')
    
    const filename = `materials-export-${new Date().toISOString().split('T')[0]}.md`
    downloadFile(content, filename, 'text/markdown')
    saveExportHistory(filename, { type: 'materials', data: materials })
  } catch (e) {
    console.error('Export error:', e)
    alert('Error exporting materials. Please try again.')
  }
}

const exportEverything = async (format: 'json' | 'markdown' = 'json') => {
  try {
    const codeHistory = localStorage.getItem('python_code_history')
    const codeData = codeHistory ? JSON.parse(codeHistory) : []
    
    // Get editor files if available
    const editorFiles = localStorage.getItem('editor_files')
    const editorData = editorFiles ? JSON.parse(editorFiles) : []
    
    const materialsResponse = await fetch('/api/materials', {
      credentials: 'include'
    })
    const materials = materialsResponse.ok ? await materialsResponse.json() : []
    
    const exportData = {
      date: new Date().toISOString().split('T')[0],
      timestamp: new Date().toISOString(),
      code: codeData,
      editorFiles: editorData,
      materials: materials,
      summary: {
        codeSnippets: codeData.length,
        editorFiles: Array.isArray(editorData) ? editorData.length : 0,
        materials: materials.length
      }
    }
    
    if (format === 'markdown') {
      // Generate markdown format
      const markdown = generateMarkdownExport(exportData)
      const filename = `studyhall-export-${new Date().toISOString().split('T')[0]}.md`
      downloadFile(markdown, filename, 'text/markdown')
      saveExportHistory(filename, exportData)
    } else {
      // Use the export API endpoint for JSON
      const exportResponse = await fetch('/api/export', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        credentials: 'include',
        body: JSON.stringify(exportData)
      })
      
      if (!exportResponse.ok) {
        throw new Error('Failed to export via API')
      }
      
      const result = await exportResponse.json()
      const filename = result.filename || `studyhall-export-${new Date().toISOString().split('T')[0]}.json`
      
      // Download the file
      downloadFile(JSON.stringify(exportData, null, 2), filename, 'application/json')
      saveExportHistory(filename, exportData)
    }
  } catch (e: any) {
    console.error('Export error:', e)
    alert(`Error exporting everything: ${e.message || 'Unknown error'}`)
  }
}

const generateMarkdownExport = (data: any): string => {
  const lines: string[] = []
  
  lines.push('# StudyHall Export')
  lines.push(`\n**Date:** ${data.date}`)
  lines.push(`**Timestamp:** ${data.timestamp}`)
  lines.push(`\n## Summary\n`)
  lines.push(`- Code Snippets: ${data.summary.codeSnippets}`)
  lines.push(`- Editor Files: ${data.summary.editorFiles}`)
  lines.push(`- Materials: ${data.summary.materials}`)
  
  // Code Section
  if (data.code && data.code.length > 0) {
    lines.push(`\n## Code Snippets\n`)
    data.code.forEach((item: any, index: number) => {
      lines.push(`\n### Code Snippet ${index + 1}`)
      if (item.timestamp) {
        lines.push(`*Created: ${item.timestamp}*`)
      }
      lines.push(`\n\`\`\`python`)
      lines.push(item.code || '')
      lines.push(`\`\`\``)
    })
  }
  
  // Editor Files Section
  if (data.editorFiles && Array.isArray(data.editorFiles) && data.editorFiles.length > 0) {
    lines.push(`\n## Editor Files\n`)
    data.editorFiles.forEach((file: any) => {
      if (file.type === 'file') {
        lines.push(`\n### ${file.name || file.path || 'Untitled'}`)
        lines.push(`\n\`\`\`${file.language || 'text'}`)
        lines.push(file.content || '')
        lines.push(`\`\`\``)
      }
    })
  }
  
  // Materials Section
  if (data.materials && data.materials.length > 0) {
    lines.push(`\n## Materials\n`)
    data.materials.forEach((material: any) => {
      lines.push(`\n### ${material.title || 'Untitled'}`)
      if (material.category) {
        lines.push(`*Category: ${material.category}*`)
      }
      if (material.created_at) {
        lines.push(`*Created: ${material.created_at}*`)
      }
      lines.push(`\n${material.content || 'No content'}`)
      if (material.notion_url) {
        lines.push(`\n[View in Notion](${material.notion_url})`)
      }
      lines.push(`\n---`)
    })
  }
  
  lines.push(`\n\n---\n*Exported from StudyHall Platform*`)
  
  return lines.join('\n')
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
