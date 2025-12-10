<template>
  <div class="px-4 py-4 sm:py-6 sm:px-0">
    <div class="mb-6 sm:mb-8">
      <h1 class="text-2xl sm:text-3xl font-bold text-msit-dark-50 mb-2 font-serif">Dashboard</h1>
      <p class="text-sm sm:text-base text-msit-dark-200 font-sans">Welcome to StudyHall - A simple learning platform</p>
    </div>

    <!-- All Features Section -->
    <div class="mb-8">
      <h2 class="text-xl sm:text-2xl font-bold text-msit-dark-50 mb-4 font-serif">Features</h2>
      <div class="grid grid-cols-1 gap-4 sm:gap-6 sm:grid-cols-2 lg:grid-cols-3">
        <!-- Materials Feature -->
        <div class="bg-msit-dark-800 shadow rounded-lg overflow-hidden hover:shadow-lg transition-shadow border border-msit-dark-700 hover:border-msit-accent">
          <div class="p-4 sm:p-6">
            <div class="flex items-center mb-3">
              <div class="flex-shrink-0">
                <svg class="h-8 w-8 text-msit-accent" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5c1.747 0 3.332.477 4.5 1.253v13C19.832 18.477 18.247 18 16.5 18c-1.746 0-3.332.477-4.5 1.253" />
                </svg>
              </div>
              <h3 class="ml-3 text-base sm:text-lg font-medium text-msit-dark-50 font-sans">Course Materials</h3>
            </div>
            <p class="text-sm text-msit-dark-200 mb-4 font-sans">
              Browse, search, and filter course materials. Sync content from Notion.
            </p>
            <ul class="text-xs text-msit-dark-300 space-y-1 mb-4 font-sans">
              <li>• Search and filter by category</li>
              <li>• Sync from Notion database</li>
              <li>• View detailed material content</li>
            </ul>
            <router-link
              to="/materials"
              class="inline-flex items-center text-sm font-medium text-msit-accent hover:text-msit-accent-300 transition-colors font-sans"
            >
              Go to Materials →
            </router-link>
          </div>
        </div>

        <!-- Python Compiler Feature -->
        <div class="bg-msit-dark-800 shadow rounded-lg overflow-hidden hover:shadow-lg transition-shadow border border-msit-dark-700 hover:border-msit-accent">
          <div class="p-4 sm:p-6">
            <div class="flex items-center mb-3">
              <div class="flex-shrink-0">
                <svg class="h-8 w-8 text-msit-accent" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 20l4-16m4 4l4 4-4 4M6 16l-4-4 4-4" />
                </svg>
              </div>
              <h3 class="ml-3 text-base sm:text-lg font-medium text-msit-dark-50 font-sans">Python Compiler</h3>
            </div>
            <p class="text-sm text-msit-dark-200 mb-4 font-sans">
              Write and execute Python code directly in your browser. Practice coding without leaving the platform.
            </p>
            <ul class="text-xs text-msit-dark-300 space-y-1 mb-4 font-sans">
              <li>• Interactive code editor</li>
              <li>• Execute Python code</li>
              <li>• View output instantly</li>
              <li>• Practice while learning</li>
            </ul>
            <router-link
              to="/compiler"
              class="inline-flex items-center text-sm font-medium text-msit-accent hover:text-msit-accent-300 transition-colors font-sans"
            >
              Open Compiler →
            </router-link>
          </div>
        </div>

        <!-- Export Feature -->
        <div class="bg-msit-dark-800 shadow rounded-lg overflow-hidden hover:shadow-lg transition-shadow border border-msit-dark-700 hover:border-msit-accent">
          <div class="p-4 sm:p-6">
            <div class="flex items-center mb-3">
              <div class="flex-shrink-0">
                <svg class="h-8 w-8 text-msit-accent" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 10v6m0 0l-3-3m3 3l3-3m2 8H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                </svg>
              </div>
              <h3 class="ml-3 text-base sm:text-lg font-medium text-msit-dark-50 font-sans">Export Your Work</h3>
            </div>
            <p class="text-sm text-msit-dark-200 mb-4 font-sans">
              Export what you've done today. Save your notes, code, and learning progress.
            </p>
            <ul class="text-xs text-msit-dark-300 space-y-1 mb-4 font-sans">
              <li>• Export daily work</li>
              <li>• Save as JSON</li>
              <li>• Keep your learning records</li>
            </ul>
            <button
              @click="exportWork"
              class="inline-flex items-center text-sm font-medium text-msit-accent hover:text-msit-accent-300 transition-colors font-sans"
            >
              Export Now →
            </button>
          </div>
        </div>

        <!-- Notion Integration Feature -->
        <div class="bg-msit-dark-800 shadow rounded-lg overflow-hidden hover:shadow-lg transition-shadow border border-msit-dark-700 hover:border-msit-accent">
          <div class="p-4 sm:p-6">
            <div class="flex items-center mb-3">
              <div class="flex-shrink-0">
                <svg class="h-8 w-8 text-msit-accent" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
                </svg>
              </div>
              <h3 class="ml-3 text-base sm:text-lg font-medium text-msit-dark-50 font-sans">Notion Sync</h3>
            </div>
            <p class="text-sm text-msit-dark-200 mb-4 font-sans">
              Sync course materials from your Notion database. Keep your content up-to-date automatically.
            </p>
            <ul class="text-xs text-msit-dark-300 space-y-1 mb-4 font-sans">
              <li>• Connect to Notion database</li>
              <li>• Sync materials automatically</li>
              <li>• Import new content</li>
              <li>• One-click sync button</li>
            </ul>
            <router-link
              to="/materials"
              class="inline-flex items-center text-sm font-medium text-msit-accent hover:text-msit-accent-300 transition-colors font-sans"
            >
              Sync Materials →
            </router-link>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'

const exportWork = async () => {
  try {
    const today = new Date().toISOString().split('T')[0]
    const exportData = {
      date: today,
      timestamp: new Date().toISOString(),
      materials_viewed: [], // Could be populated from localStorage or session
      code_executed: [], // Could be populated from compiler history
      notes: [] // Could be populated from any notes taken
    }

    // Try to get any stored data from localStorage
    try {
      const storedData = localStorage.getItem('studyhall_data')
      if (storedData) {
        const parsed = JSON.parse(storedData)
        exportData.materials_viewed = parsed.materials_viewed || []
        exportData.code_executed = parsed.code_executed || []
        exportData.notes = parsed.notes || []
      }
    } catch (e) {
      // Ignore errors
    }

    const response = await fetch('/api/export', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(exportData)
    })

    if (response.ok) {
      const data = await response.json()
      // Create download link
      const blob = new Blob([JSON.stringify(exportData, null, 2)], { type: 'application/json' })
      const url = URL.createObjectURL(blob)
      const a = document.createElement('a')
      a.href = url
      a.download = data.filename || `studyhall-export-${today}.json`
      document.body.appendChild(a)
      a.click()
      document.body.removeChild(a)
      URL.revokeObjectURL(url)
    } else {
      alert('Failed to export work')
    }
  } catch (e) {
    alert('An error occurred while exporting')
  }
}
</script>
