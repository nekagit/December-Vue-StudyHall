<template>
  <div class="px-4 py-4 sm:py-6 sm:px-0">
    <div class="mb-6 sm:mb-8">
      <h1 class="text-2xl sm:text-3xl font-bold text-msit-dark-50 mb-2 font-serif">Help & Guide</h1>
      <p class="text-sm sm:text-base text-msit-dark-200 font-sans">Learn how to use StudyHall platform</p>
    </div>

    <!-- Quick Links -->
    <div class="mb-8 grid grid-cols-1 md:grid-cols-3 gap-4">
      <router-link
        to="/materials"
        class="bg-msit-dark-800 border border-msit-dark-700 rounded-lg p-4 hover:border-msit-accent transition-all"
      >
        <h3 class="text-lg font-semibold text-msit-dark-50 mb-2 font-sans">Materials</h3>
        <p class="text-sm text-msit-dark-200 font-sans">Browse course materials</p>
      </router-link>
      <router-link
        to="/compiler"
        class="bg-msit-dark-800 border border-msit-dark-700 rounded-lg p-4 hover:border-msit-accent transition-all"
      >
        <h3 class="text-lg font-semibold text-msit-dark-50 mb-2 font-sans">Compiler</h3>
        <p class="text-sm text-msit-dark-200 font-sans">Run Python code</p>
      </router-link>
      <router-link
        to="/export"
        class="bg-msit-dark-800 border border-msit-dark-700 rounded-lg p-4 hover:border-msit-accent transition-all"
      >
        <h3 class="text-lg font-semibold text-msit-dark-50 mb-2 font-sans">Export</h3>
        <p class="text-sm text-msit-dark-200 font-sans">Export your work</p>
      </router-link>
    </div>

    <!-- FAQ Sections -->
    <div class="space-y-6">
      <div
        v-for="section in sections"
        :key="section.title"
        class="bg-msit-dark-800 border border-msit-dark-700 rounded-lg overflow-hidden"
      >
        <button
          @click="toggleSection(section.title)"
          class="w-full px-6 py-4 flex items-center justify-between hover:bg-msit-dark-700 transition-colors"
        >
          <h2 class="text-xl font-semibold text-msit-dark-50 font-sans">{{ section.title }}</h2>
          <svg
            :class="['h-5 w-5 text-msit-dark-400 transition-transform', openSections[section.title] ? 'rotate-180' : '']"
            fill="none"
            viewBox="0 0 24 24"
            stroke="currentColor"
          >
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7" />
          </svg>
        </button>
        <div v-if="openSections[section.title]" class="px-6 py-4 border-t border-msit-dark-700">
          <div class="space-y-4">
            <div
              v-for="item in section.items"
              :key="item.question"
              class="border-l-2 border-msit-accent pl-4"
            >
              <h3 class="text-lg font-semibold text-msit-dark-50 mb-2 font-sans">{{ item.question }}</h3>
              <p class="text-sm text-msit-dark-200 whitespace-pre-line font-sans">{{ item.answer }}</p>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Keyboard Shortcuts -->
    <div class="mt-8 bg-msit-dark-800 border border-msit-dark-700 rounded-lg p-6">
      <h2 class="text-xl font-semibold text-msit-dark-50 mb-4 font-sans">Keyboard Shortcuts</h2>
      <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
        <div
          v-for="shortcut in shortcuts"
          :key="shortcut.action"
          class="flex items-center justify-between p-3 bg-msit-dark-900 rounded-lg"
        >
          <span class="text-sm text-msit-dark-200 font-sans">{{ shortcut.action }}</span>
          <kbd class="px-2 py-1 bg-msit-dark-700 border border-msit-dark-600 rounded text-xs text-msit-dark-200 font-mono font-sans">
            {{ shortcut.key }}
          </kbd>
        </div>
      </div>
    </div>

    <!-- Contact/Support -->
    <div class="mt-8 bg-msit-dark-800 border border-msit-dark-700 rounded-lg p-6 text-center">
      <h2 class="text-xl font-semibold text-msit-dark-50 mb-2 font-sans">Need More Help?</h2>
      <p class="text-sm text-msit-dark-200 mb-4 font-sans">
        Check out the Resources page for additional learning materials and community support.
      </p>
      <router-link
        to="/resources"
        class="inline-flex items-center px-4 py-2 bg-msit-accent text-msit-dark rounded-lg hover:bg-msit-accent-500 transition-colors text-sm font-medium font-sans"
      >
        Browse Resources
      </router-link>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'

const openSections = ref<Record<string, boolean>>({
  'Getting Started': true,
  'Using the Compiler': false,
  'Materials': false,
  'Export & Backup': false
})

const toggleSection = (title: string) => {
  openSections.value[title] = !openSections.value[title]
}

const sections = [
  {
    title: 'Getting Started',
    items: [
      {
        question: 'What is StudyHall?',
        answer: 'StudyHall is a simple learning platform for Python. It provides course materials, an in-browser Python compiler, code snippets, and export functionality - all without requiring any setup or installation.'
      },
      {
        question: 'Do I need to create an account?',
        answer: 'No! StudyHall is designed to be simple and accessible. You can start using all features immediately without any registration.'
      },
      {
        question: 'How do I get started?',
        answer: 'Simply navigate to any section from the menu:\n• Materials: Browse course content\n• Compiler: Write and run Python code\n• Snippets: Find code examples\n• Practice: Try coding exercises\n• Export: Save your work'
      }
    ]
  },
  {
    title: 'Using the Compiler',
    items: [
      {
        question: 'How do I run Python code?',
        answer: 'Go to the Compiler page, type or paste your Python code in the editor, and click the "Run" button. Your code will execute and display the output below.'
      },
      {
        question: 'What Python version is supported?',
        answer: 'The compiler runs Python 3.x. Most standard library features are available. Note that some system-specific features may have limitations.'
      },
      {
        question: 'Can I save my code?',
        answer: 'Yes! Your code is automatically saved in your browser\'s local storage. You can also export your code using the Export feature.'
      },
      {
        question: 'How do I use code from Snippets?',
        answer: 'Browse the Snippets page, find a code example you like, and click "Use" to load it into the Compiler automatically.'
      }
    ]
  },
  {
    title: 'Materials',
    items: [
      {
        question: 'What are Materials?',
        answer: 'Materials are course content pages that contain lessons, tutorials, and learning resources. They are available for browsing and learning.'
      },
      {
        question: 'How do I search for materials?',
        answer: 'Use the search bar on the Materials page or use the global Search feature to find materials by title, content, or category.'
      },
      {
        question: 'Can I filter materials by category?',
        answer: 'Yes! On the Materials page, you can filter by category using the category buttons. You can also use the search functionality.'
      }
    ]
  },
  {
    title: 'Export & Backup',
    items: [
      {
        question: 'How do I export my work?',
        answer: 'Go to the Export page and choose what you want to export:\n• Code snippets you\'ve written\n• Materials you\'ve viewed\n• Everything in one complete export'
      },
      {
        question: 'What format are exports in?',
        answer: 'Exports are available in JSON format for complete exports, or Markdown format for code and materials. You can download them directly to your computer.'
      },
      {
        question: 'Is my data stored?',
        answer: 'Your code and activity are stored locally in your browser. They are not sent to any server unless you explicitly export them.'
      }
    ]
  }
]

const shortcuts = [
  { action: 'Search', key: 'Ctrl/Cmd + K' },
  { action: 'Run Code', key: 'Ctrl/Cmd + Enter' },
  { action: 'Copy Code', key: 'Ctrl/Cmd + C' },
  { action: 'Clear Editor', key: 'Ctrl/Cmd + L' }
]
</script>
