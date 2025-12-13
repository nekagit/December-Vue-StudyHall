<template>
  <div class="px-4 py-4 sm:py-6 sm:px-0">
    <div class="max-w-5xl mx-auto">
      <!-- Header -->
      <div class="mb-6 sm:mb-8">
        <h1 class="text-2xl sm:text-3xl font-bold text-msit-dark-50 mb-2 font-serif">AI Tutor</h1>
        <p class="text-sm sm:text-base text-msit-dark-200 font-sans">
          Ask questions about any programming language and get personalized tutoring
        </p>
      </div>

      <!-- Language Selection and Question Input -->
      <div class="bg-msit-dark-800 border border-msit-dark-700 rounded-lg p-6 mb-6">
        <div class="space-y-4">
          <!-- Language Dropdown -->
          <div>
            <label class="block text-sm font-medium text-msit-dark-200 mb-2 font-sans">
              Select Programming Language
            </label>
            <select
              v-model="selectedLanguage"
              class="w-full px-4 py-2 bg-msit-dark-700 border border-msit-dark-600 rounded-lg text-msit-dark-50 focus:border-msit-accent focus:outline-none font-sans"
            >
              <option v-for="lang in languages" :key="lang" :value="lang">{{ lang }}</option>
            </select>
          </div>

          <!-- Question Input -->
          <div>
            <label class="block text-sm font-medium text-msit-dark-200 mb-2 font-sans">
              Ask Your Question
            </label>
            <textarea
              v-model="question"
              @keydown.enter.exact.prevent="askQuestion"
              @keydown.enter.shift.exact=""
              placeholder="e.g., How do I use async/await in JavaScript?"
              rows="4"
              class="w-full px-4 py-3 bg-msit-dark-700 border border-msit-dark-600 rounded-lg text-msit-dark-50 placeholder-msit-dark-400 focus:border-msit-accent focus:outline-none font-sans resize-none"
            ></textarea>
          </div>

          <!-- Ask Button -->
          <button
            @click="askQuestion"
            :disabled="loading || !question.trim() || !selectedLanguage"
            class="w-full px-6 py-3 bg-msit-accent text-msit-dark rounded-lg hover:bg-msit-accent-500 transition-colors font-semibold font-sans disabled:opacity-50 disabled:cursor-not-allowed"
          >
            <span v-if="loading" class="flex items-center justify-center">
              <svg class="animate-spin -ml-1 mr-3 h-5 w-5" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
              </svg>
              Generating response...
            </span>
            <span v-else>Ask Question</span>
          </button>
        </div>
      </div>

      <!-- Response Display -->
      <div v-if="response" class="bg-msit-dark-800 border border-msit-dark-700 rounded-lg p-6 mb-6">
        <!-- Response Header -->
        <div class="flex items-center justify-between mb-4 pb-4 border-b border-msit-dark-700">
          <h2 class="text-xl font-semibold text-msit-dark-50 font-sans">Tutor Response</h2>
          <div class="flex items-center gap-2">
            <span class="text-xs text-msit-dark-300 font-sans">{{ selectedLanguage }}</span>
          </div>
        </div>

        <!-- Markdown Content -->
        <div class="prose prose-invert max-w-none">
          <div 
            v-html="renderedMarkdown" 
            class="text-msit-dark-50 font-sans markdown-content"
          ></div>
        </div>

        <!-- Feedback Buttons -->
        <div v-if="!feedbackGiven" class="mt-6 pt-6 border-t border-msit-dark-700">
          <p class="text-sm text-msit-dark-300 mb-4 font-sans">Was this helpful?</p>
          <div class="flex gap-4">
            <button
              @click="submitFeedback('like')"
              class="flex items-center gap-2 px-6 py-2 bg-green-600 hover:bg-green-700 text-white rounded-lg transition-colors font-medium font-sans"
            >
              <svg class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M14 10h4.764a2 2 0 011.789 2.894l-3.5 7A2 2 0 0115.263 21h-4.017c-.163 0-.326-.02-.485-.06L7 20m7-10V5a2 2 0 00-2-2h-.095c-.5 0-.905.405-.905.905 0 .714-.211 1.412-.608 2.006L7 11v9m7-10h-2M7 20H5a2 2 0 01-2-2v-6a2 2 0 012-2h2.5" />
              </svg>
              Like
            </button>
            <button
              @click="submitFeedback('dislike')"
              class="flex items-center gap-2 px-6 py-2 bg-red-600 hover:bg-red-700 text-white rounded-lg transition-colors font-medium font-sans"
            >
              <svg class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 14H5.236a2 2 0 01-1.789-2.894l3.5-7A2 2 0 018.736 3h4.018a2 2 0 01.485.06l3.76.94m-7 10v5a2 2 0 002 2h.096c.5 0 .905-.405.905-.904 0-.715.211-1.413.608-2.008L17 13V4m-7 10h2m5-10h2a2 2 0 012 2v6a2 2 0 01-2 2h-2.5" />
              </svg>
              Dislike
            </button>
          </div>
        </div>

        <!-- Feedback Submitted -->
        <div v-else class="mt-6 pt-6 border-t border-msit-dark-700">
          <div class="flex items-center gap-2 text-msit-accent">
            <svg class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
            <span class="font-medium font-sans">Thank you for your feedback!</span>
          </div>
        </div>
      </div>

      <!-- Error Message -->
      <div v-if="error" class="bg-red-500/10 border border-red-500/30 rounded-lg p-4 mb-6">
        <div class="flex items-center gap-2 text-red-400">
          <svg class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
          </svg>
          <span class="font-medium font-sans">{{ error }}</span>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'

const languages = [
  'Python',
  'JavaScript',
  'TypeScript',
  'Java',
  'C++',
  'C',
  'Go',
  'Rust',
  'PHP',
  'Ruby',
  'Swift',
  'Kotlin',
  'Dart',
  'HTML/CSS',
  'SQL',
  'R',
  'MATLAB',
  'Scala',
  'Perl',
  'Lua'
]

const selectedLanguage = ref('Python')
const question = ref('')
const response = ref('')
const sessionId = ref('')
const loading = ref(false)
const error = ref('')
const feedbackGiven = ref(false)

// Simple markdown to HTML converter
const renderedMarkdown = computed(() => {
  if (!response.value) return ''
  
  let html = response.value
  
  // Headers
  html = html.replace(/^### (.*$)/gim, '<h3 class="text-lg font-semibold mt-4 mb-2 text-msit-dark-50">$1</h3>')
  html = html.replace(/^## (.*$)/gim, '<h2 class="text-xl font-semibold mt-6 mb-3 text-msit-dark-50">$1</h2>')
  html = html.replace(/^# (.*$)/gim, '<h1 class="text-2xl font-bold mt-6 mb-4 text-msit-dark-50">$1</h1>')
  
  // Bold
  html = html.replace(/\*\*(.*?)\*\*/gim, '<strong class="font-semibold text-msit-accent">$1</strong>')
  
  // Italic
  html = html.replace(/\*(.*?)\*/gim, '<em class="italic">$1</em>')
  
  // Code blocks
  html = html.replace(/```(\w+)?\n([\s\S]*?)```/gim, (match, lang, code) => {
    return `<pre class="bg-msit-dark-900 border border-msit-dark-600 rounded-lg p-4 overflow-x-auto my-4"><code class="text-sm text-msit-dark-50 font-mono">${escapeHtml(code.trim())}</code></pre>`
  })
  
  // Inline code
  html = html.replace(/`([^`]+)`/gim, '<code class="bg-msit-dark-900 px-1.5 py-0.5 rounded text-sm text-msit-accent font-mono">$1</code>')
  
  // Lists
  html = html.replace(/^\* (.*$)/gim, '<li class="ml-4 mb-1 text-msit-dark-200">$1</li>')
  html = html.replace(/^- (.*$)/gim, '<li class="ml-4 mb-1 text-msit-dark-200">$1</li>')
  html = html.replace(/^(\d+)\. (.*$)/gim, '<li class="ml-4 mb-1 text-msit-dark-200">$1. $2</li>')
  
  // Wrap consecutive list items in ul
  html = html.replace(/(<li[^>]*>.*<\/li>\n?)+/gim, (match) => {
    return `<ul class="list-disc my-3 space-y-1">${match}</ul>`
  })
  
  // Paragraphs
  html = html.split('\n\n').map(para => {
    if (!para.trim() || para.trim().startsWith('<')) return para
    return `<p class="mb-4 text-msit-dark-200 leading-relaxed">${para.trim()}</p>`
  }).join('\n')
  
  // Line breaks
  html = html.replace(/\n/g, '<br>')
  
  return html
})

function escapeHtml(text: string): string {
  const div = document.createElement('div')
  div.textContent = text
  return div.innerHTML
}

async function askQuestion() {
  if (!question.value.trim() || !selectedLanguage.value || loading.value) {
    return
  }

  loading.value = true
  error.value = ''
  response.value = ''
  feedbackGiven.value = false
  sessionId.value = ''

  try {
    const res = await fetch('/api/tutor/ask', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        question: question.value.trim(),
        language: selectedLanguage.value,
      }),
    })

    if (!res.ok) {
      const data = await res.json()
      throw new Error(data.error || 'Failed to get tutor response')
    }

    const data = await res.json()
    if (data.success) {
      response.value = data.markdown
      sessionId.value = data.session_id
    } else {
      throw new Error(data.error || 'Failed to generate response')
    }
  } catch (err) {
    error.value = err instanceof Error ? err.message : 'An error occurred'
  } finally {
    loading.value = false
  }
}

async function submitFeedback(feedback: 'like' | 'dislike') {
  if (!sessionId.value || feedbackGiven.value) {
    return
  }

  try {
    const res = await fetch('/api/tutor/feedback', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        session_id: sessionId.value,
        feedback: feedback,
      }),
    })

    if (!res.ok) {
      throw new Error('Failed to submit feedback')
    }

    feedbackGiven.value = true
    
    // Clear response after a short delay
    setTimeout(() => {
      response.value = ''
      sessionId.value = ''
      feedbackGiven.value = false
      question.value = ''
    }, 2000)
  } catch (err) {
    error.value = err instanceof Error ? err.message : 'Failed to submit feedback'
  }
}
</script>

<style scoped>
@reference "../style.css";

.markdown-content :deep(h1) {
  @apply text-2xl font-bold mt-6 mb-4 text-msit-dark-50;
}

.markdown-content :deep(h2) {
  @apply text-xl font-semibold mt-6 mb-3 text-msit-dark-50;
}

.markdown-content :deep(h3) {
  @apply text-lg font-semibold mt-4 mb-2 text-msit-dark-50;
}

.markdown-content :deep(p) {
  @apply mb-4 text-msit-dark-200 leading-relaxed;
}

.markdown-content :deep(ul),
.markdown-content :deep(ol) {
  @apply my-3 ml-6 space-y-1;
}

.markdown-content :deep(ul) {
  @apply list-disc;
}

.markdown-content :deep(ol) {
  @apply list-decimal;
}

.markdown-content :deep(li) {
  @apply text-msit-dark-200;
}

.markdown-content :deep(code) {
  @apply bg-msit-dark-900 px-1.5 py-0.5 rounded text-sm text-msit-accent font-mono;
}

.markdown-content :deep(pre) {
  @apply bg-msit-dark-900 border border-msit-dark-600 rounded-lg p-4 overflow-x-auto my-4;
}

.markdown-content :deep(pre code) {
  @apply bg-transparent p-0 text-msit-dark-50;
}

.markdown-content :deep(strong) {
  @apply font-semibold text-msit-accent;
}

.markdown-content :deep(em) {
  @apply italic;
}
</style>





