<template>
  <div class="px-4 py-4 sm:py-6 sm:px-0">
    <div v-if="loading" class="text-center py-12">
      <div class="inline-block animate-spin rounded-full h-8 w-8 border-b-2 border-msit-accent"></div>
    </div>

    <div v-else-if="error" class="rounded-md bg-red-900/30 border border-red-700 p-4">
      <div class="text-sm text-red-300 font-sans">{{ error }}</div>
    </div>

    <div v-else-if="material" class="bg-msit-dark-800 shadow rounded-lg overflow-hidden border border-msit-dark-700">
      <div class="px-4 sm:px-6 py-4 sm:py-6 border-b border-msit-dark-700">
        <div class="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-3 mb-4">
          <h1 class="text-2xl sm:text-3xl font-bold text-msit-dark-50 font-serif break-words">{{ material.title }}</h1>
          <span v-if="material.category" class="inline-flex items-center px-3 py-1 rounded-full text-sm font-medium bg-msit-accent/20 text-msit-accent font-sans self-start sm:self-auto">
            {{ material.category }}
          </span>
        </div>
        
        <!-- Action Buttons -->
        <div class="flex flex-col sm:flex-row items-stretch sm:items-center gap-2 sm:gap-3">
          <a
            v-if="material.notion_url"
            :href="material.notion_url"
            target="_blank"
            class="w-full sm:w-auto inline-flex items-center justify-center px-4 py-2 border border-msit-dark-600 shadow-sm text-sm font-medium rounded-md text-msit-dark-50 bg-msit-dark-700 hover:bg-msit-dark-600 transition-colors font-sans"
          >
            <svg class="h-4 w-4 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 6H6a2 2 0 00-2 2v10a2 2 0 002 2h10a2 2 0 002-2v-4M14 4h6m0 0v6m0-6L10 14" />
            </svg>
            View in Notion
          </a>
          <button
            @click="exportMaterial"
            class="w-full sm:w-auto inline-flex items-center justify-center px-4 py-2 border border-msit-dark-600 shadow-sm text-sm font-medium rounded-md text-msit-dark-50 bg-msit-dark-700 hover:bg-msit-dark-600 transition-colors font-sans"
          >
            <svg class="h-4 w-4 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4" />
            </svg>
            Export
          </button>
          <button
            @click="printMaterial"
            class="w-full sm:w-auto inline-flex items-center justify-center px-4 py-2 border border-msit-dark-600 shadow-sm text-sm font-medium rounded-md text-msit-dark-50 bg-msit-dark-700 hover:bg-msit-dark-600 transition-colors font-sans"
          >
            <svg class="h-4 w-4 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 17h2a2 2 0 002-2v-4a2 2 0 00-2-2H5a2 2 0 00-2 2v4a2 2 0 002 2h2m2 4h6a2 2 0 002-2v-4a2 2 0 00-2-2H9a2 2 0 00-2 2v4a2 2 0 002 2zm8-12V5a2 2 0 00-2-2H9a2 2 0 00-2 2v4h10z" />
            </svg>
            Print
          </button>
          <button
            @click="copyMaterialLink"
            class="w-full sm:w-auto inline-flex items-center justify-center px-4 py-2 border border-msit-dark-600 shadow-sm text-sm font-medium rounded-md text-msit-dark-50 bg-msit-dark-700 hover:bg-msit-dark-600 transition-colors font-sans"
          >
            <svg class="h-4 w-4 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 16H6a2 2 0 01-2-2V6a2 2 0 012-2h8a2 2 0 012 2v2m-6 12h8a2 2 0 002-2v-8a2 2 0 00-2-2h-8a2 2 0 00-2 2v8a2 2 0 002 2z" />
            </svg>
            Copy Link
          </button>
        </div>
      </div>
      <div class="px-4 sm:px-6 py-4 sm:py-6">
        <div class="prose prose-invert max-w-none text-msit-dark-100" style="color: #E0EADD;" v-html="formatContent(material.content)"></div>
      </div>

      <div class="px-4 sm:px-6 py-4 border-t border-msit-dark-700">
        <router-link
          to="/materials"
          class="text-msit-accent hover:text-msit-accent-300 font-medium transition-colors font-sans inline-flex items-center"
        >
          ← Back to Materials
        </router-link>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'

const route = useRoute()
const material = ref<any>(null)
const loading = ref(true)
const error = ref('')

const formatContent = (content: string) => {
  if (!content) return ''
  // Simple markdown-like formatting
  return content
    .replace(/\n/g, '<br>')
    .replace(/#{3}\s(.+)/g, '<h3>$1</h3>')
    .replace(/#{2}\s(.+)/g, '<h2>$1</h2>')
    .replace(/#{1}\s(.+)/g, '<h1>$1</h1>')
    .replace(/```python\n([\s\S]*?)```/g, '<pre class="bg-msit-dark-700 p-4 rounded my-2 overflow-x-auto"><code class="text-msit-dark-50">$1</code></pre>')
    .replace(/```([\s\S]*?)```/g, '<pre class="bg-msit-dark-700 p-4 rounded my-2 overflow-x-auto"><code class="text-msit-dark-50">$1</code></pre>')
    .replace(/`([^`]+)`/g, '<code class="bg-msit-dark-700 px-1 rounded text-msit-accent">$1</code>')
    .replace(/\*\*(.+?)\*\*/g, '<strong>$1</strong>')
    .replace(/\*(.+?)\*/g, '<em>$1</em>')
}

const exportMaterial = () => {
  if (!material.value) return
  
  const content = `
# ${material.value.title}

${material.value.category ? `**Category:** ${material.value.category}\n` : ''}
${material.value.notion_url ? `**Source:** ${material.value.notion_url}\n` : ''}

---

${material.value.content}

---

*Exported from StudyHall on ${new Date().toLocaleString()}*
  `.trim()
  
  const blob = new Blob([content], { type: 'text/markdown' })
  const url = URL.createObjectURL(blob)
  const a = document.createElement('a')
  a.href = url
  a.download = `${material.value.title.replace(/[^a-z0-9]/gi, '_').toLowerCase()}.md`
  document.body.appendChild(a)
  a.click()
  document.body.removeChild(a)
  URL.revokeObjectURL(url)
}

const printMaterial = () => {
  const printWindow = window.open('', '_blank')
  if (!printWindow || !material.value) return
  
  printWindow.document.write(`
    <!DOCTYPE html>
    <html>
      <head>
        <title>${material.value.title}</title>
        <style>
          body { font-family: Arial, sans-serif; max-width: 800px; margin: 40px auto; padding: 20px; }
          h1 { color: #333; border-bottom: 2px solid #333; padding-bottom: 10px; }
          h2 { color: #555; margin-top: 30px; }
          h3 { color: #777; }
          pre { background: #f5f5f5; padding: 15px; border-radius: 5px; overflow-x: auto; }
          code { background: #f5f5f5; padding: 2px 6px; border-radius: 3px; }
          .meta { color: #666; font-size: 14px; margin-bottom: 20px; }
          @media print { body { margin: 0; } }
        </style>
      </head>
      <body>
        <h1>${material.value.title}</h1>
        <div class="meta">
          ${material.value.category ? `<strong>Category:</strong> ${material.value.category}<br>` : ''}
          ${material.value.notion_url ? `<strong>Source:</strong> <a href="${material.value.notion_url}">${material.value.notion_url}</a><br>` : ''}
          <strong>Date:</strong> ${new Date().toLocaleString()}
        </div>
        <div>${formatContent(material.value.content)}</div>
      </body>
    </html>
  `)
  printWindow.document.close()
  printWindow.focus()
  setTimeout(() => {
    printWindow.print()
  }, 250)
}

const copyMaterialLink = () => {
  const url = window.location.href
  navigator.clipboard.writeText(url)
  alert('Link copied to clipboard!')
}

const loadMaterial = async () => {
  loading.value = true
  try {
    const response = await fetch(`/api/materials/${route.params.id}`)
    if (response.ok) {
      material.value = await response.json()
    } else {
      error.value = 'Material not found'
    }
  } catch (e) {
    error.value = 'An error occurred'
  } finally {
    loading.value = false
  }
}

onMounted(loadMaterial)
</script>
