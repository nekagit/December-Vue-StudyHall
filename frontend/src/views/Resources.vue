<template>
  <div class="px-4 py-4 sm:py-6 sm:px-0">
    <div class="mb-6 sm:mb-8">
      <h1 class="text-2xl sm:text-3xl font-bold text-msit-dark-50 mb-2 font-serif">Resources</h1>
      <p class="text-sm sm:text-base text-msit-dark-200 font-sans">Curated resources, documentation, and tools to enhance your Python learning</p>
    </div>

    <!-- Category Tabs -->
    <div class="mb-6 flex flex-wrap gap-2 border-b border-msit-dark-700 pb-4">
      <button
        v-for="category in categories"
        :key="category"
        @click="selectedCategory = category"
        :class="[
          'px-4 py-2 rounded-lg text-sm font-semibold transition-colors font-sans',
          selectedCategory === category
            ? 'bg-msit-accent text-msit-dark'
            : 'bg-msit-dark-800 text-msit-dark-200 hover:bg-msit-dark-700'
        ]"
      >
        {{ category }}
      </button>
    </div>

    <!-- Loading State -->
    <div v-if="loading" class="text-center py-12">
      <div class="inline-block animate-spin rounded-full h-8 w-8 border-b-2 border-msit-accent"></div>
      <p class="mt-2 text-msit-dark-200 font-sans">Loading resources...</p>
    </div>

    <!-- Resources Grid -->
    <div v-else class="space-y-6">
      <div
        v-for="category in filteredCategories"
        :key="category"
        class="bg-msit-dark-800 rounded-lg shadow border border-msit-dark-700 p-6"
      >
        <h2 class="text-xl font-semibold text-msit-dark-50 mb-4 font-serif">{{ category }}</h2>
        <div class="grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-3">
          <a
            v-for="resource in getResourcesByCategory(category)"
            :key="resource.id"
            :href="resource.url"
            target="_blank"
            rel="noopener noreferrer"
            class="group bg-msit-dark-900 p-4 rounded-lg border border-msit-dark-700 hover:border-msit-accent transition-all hover:shadow-lg"
          >
            <div class="flex items-start justify-between mb-2">
              <div class="flex-1">
                <h3 class="text-base font-semibold text-msit-dark-50 group-hover:text-msit-accent transition-colors mb-1 font-sans">
                  {{ resource.title }}
                </h3>
                <p class="text-xs text-msit-dark-300 mb-2 font-sans">{{ resource.description }}</p>
              </div>
              <svg class="h-5 w-5 text-msit-dark-400 group-hover:text-msit-accent transition-colors shrink-0 ml-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 6H6a2 2 0 00-2 2v10a2 2 0 002 2h10a2 2 0 002-2v-4M14 4h6m0 0v6m0-6L10 14" />
              </svg>
            </div>
            <div class="flex items-center gap-2 mt-3">
              <span
                v-if="resource.type"
                class="inline-flex items-center px-2 py-0.5 rounded text-xs font-medium bg-msit-accent/20 text-msit-accent font-sans"
              >
                {{ resource.type }}
              </span>
              <span
                v-if="resource.free"
                class="inline-flex items-center px-2 py-0.5 rounded text-xs font-medium bg-green-500/20 text-green-400 font-sans"
              >
                Free
              </span>
            </div>
          </a>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'

const selectedCategory = ref('All')
const resources = ref<any[]>([])
const loading = ref(false)

const loadResources = async () => {
  loading.value = true
  try {
    const params = new URLSearchParams()
    if (selectedCategory.value && selectedCategory.value !== 'All') {
      params.append('category', selectedCategory.value)
    }
    
    const response = await fetch(`/api/resources?${params.toString()}`, {
      credentials: 'include'
    })
    if (response.ok) {
      resources.value = await response.json()
    }
  } catch (e) {
    console.error('Error loading resources:', e)
  } finally {
    loading.value = false
  }
}

// Legacy resources for fallback
const legacyResources = [
  // Documentation
  {
    id: 1,
    title: 'Python Official Documentation',
    description: 'Comprehensive official Python documentation',
    url: 'https://docs.python.org/3/',
    category: 'Documentation',
    type: 'Official',
    free: true
  },
  {
    id: 2,
    title: 'Real Python',
    description: 'Python tutorials and articles for all skill levels',
    url: 'https://realpython.com/',
    category: 'Documentation',
    type: 'Tutorial',
    free: true
  },
  {
    id: 3,
    title: 'Python.org Tutorial',
    description: 'Official Python tutorial for beginners',
    url: 'https://docs.python.org/3/tutorial/',
    category: 'Documentation',
    type: 'Tutorial',
    free: true
  },
  
  // Courses
  {
    id: 4,
    title: 'Python for Everybody',
    description: 'Free Python course by University of Michigan',
    url: 'https://www.py4e.com/',
    category: 'Courses',
    type: 'Course',
    free: true
  },
  {
    id: 5,
    title: 'Automate the Boring Stuff',
    description: 'Practical Python programming for beginners',
    url: 'https://automatetheboringstuff.com/',
    category: 'Courses',
    type: 'Book/Course',
    free: true
  },
  {
    id: 6,
    title: 'Python Crash Course',
    description: 'A hands-on, project-based introduction to programming',
    url: 'https://ehmatthes.github.io/pcc/',
    category: 'Courses',
    type: 'Book',
    free: false
  },
  
  // Practice Platforms
  {
    id: 7,
    title: 'LeetCode',
    description: 'Practice coding problems and prepare for interviews',
    url: 'https://leetcode.com/',
    category: 'Practice',
    type: 'Platform',
    free: true
  },
  {
    id: 8,
    title: 'HackerRank',
    description: 'Solve coding challenges and improve your skills',
    url: 'https://www.hackerrank.com/',
    category: 'Practice',
    type: 'Platform',
    free: true
  },
  {
    id: 9,
    title: 'Codewars',
    description: 'Achieve mastery through challenge',
    url: 'https://www.codewars.com/',
    category: 'Practice',
    type: 'Platform',
    free: true
  },
  {
    id: 10,
    title: 'Project Euler',
    description: 'Mathematical programming challenges',
    url: 'https://projecteuler.net/',
    category: 'Practice',
    type: 'Platform',
    free: true
  },
  
  // Libraries & Frameworks
  {
    id: 11,
    title: 'Flask Documentation',
    description: 'Official Flask web framework documentation',
    url: 'https://flask.palletsprojects.com/',
    category: 'Libraries',
    type: 'Framework',
    free: true
  },
  {
    id: 12,
    title: 'Django Documentation',
    description: 'Official Django web framework documentation',
    url: 'https://docs.djangoproject.com/',
    category: 'Libraries',
    type: 'Framework',
    free: true
  },
  {
    id: 13,
    title: 'NumPy Documentation',
    description: 'Scientific computing with Python',
    url: 'https://numpy.org/doc/',
    category: 'Libraries',
    type: 'Library',
    free: true
  },
  {
    id: 14,
    title: 'Pandas Documentation',
    description: 'Data manipulation and analysis',
    url: 'https://pandas.pydata.org/docs/',
    category: 'Libraries',
    type: 'Library',
    free: true
  },
  {
    id: 15,
    title: 'Requests Library',
    description: 'HTTP library for Python',
    url: 'https://requests.readthedocs.io/',
    category: 'Libraries',
    type: 'Library',
    free: true
  },
  
  // Tools
  {
    id: 16,
    title: 'PyCharm',
    description: 'Professional Python IDE',
    url: 'https://www.jetbrains.com/pycharm/',
    category: 'Tools',
    type: 'IDE',
    free: false
  },
  {
    id: 17,
    title: 'VS Code',
    description: 'Free code editor with Python support',
    url: 'https://code.visualstudio.com/',
    category: 'Tools',
    type: 'Editor',
    free: true
  },
  {
    id: 18,
    title: 'Jupyter Notebook',
    description: 'Interactive computing environment',
    url: 'https://jupyter.org/',
    category: 'Tools',
    type: 'Tool',
    free: true
  },
  {
    id: 19,
    title: 'GitHub',
    description: 'Version control and code hosting',
    url: 'https://github.com/',
    category: 'Tools',
    type: 'Platform',
    free: true
  },
  
  // Communities
  {
    id: 20,
    title: 'Python Reddit',
    description: 'r/Python community discussions',
    url: 'https://www.reddit.com/r/Python/',
    category: 'Communities',
    type: 'Forum',
    free: true
  },
  {
    id: 21,
    title: 'Stack Overflow',
    description: 'Q&A platform for programmers',
    url: 'https://stackoverflow.com/questions/tagged/python',
    category: 'Communities',
    type: 'Q&A',
    free: true
  },
  {
    id: 22,
    title: 'Python Discord',
    description: 'Python community Discord server',
    url: 'https://discord.gg/python',
    category: 'Communities',
    type: 'Chat',
    free: true
  },
  
  // Books
  {
    id: 23,
    title: 'Fluent Python',
    description: 'Clear, concise, and effective Python',
    url: 'https://www.oreilly.com/library/view/fluent-python/9781491946237/',
    category: 'Books',
    type: 'Book',
    free: false
  },
  {
    id: 24,
    title: 'Effective Python',
    description: '90 specific ways to write better Python',
    url: 'https://effectivepython.com/',
    category: 'Books',
    type: 'Book',
    free: false
  }
]

const categories = ['All', 'Documentation', 'Courses', 'Practice', 'Libraries', 'Tools', 'Communities', 'Books']

const filteredCategories = computed(() => {
  if (selectedCategory.value === 'All') {
    return categories.filter(c => c !== 'All')
  }
  return [selectedCategory.value]
})

const getResourcesByCategory = (category: string) => {
  return resources.value.filter(r => r.category === category)
}

onMounted(() => {
  loadResources()
})
</script>
