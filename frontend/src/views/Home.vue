<template>
  <!-- Landing page for users without character configured -->
  <div v-if="!character" class="min-h-screen">
    <!-- Hero Section -->
    <div class="relative overflow-hidden bg-msit-dark">
      <!-- Background decoration -->
      <div class="absolute inset-0 overflow-hidden">
        <div class="absolute -top-40 -right-40 w-80 h-80 bg-msit-accent opacity-10 rounded-full blur-3xl"></div>
        <div class="absolute -bottom-40 -left-40 w-80 h-80 bg-msit-accent opacity-10 rounded-full blur-3xl"></div>
      </div>
      
      <div class="relative max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 pt-20 pb-16 sm:pt-24 sm:pb-20 lg:pt-32 lg:pb-28">
        <div class="text-center">
          <!-- Badge -->
          <div class="inline-flex items-center px-4 py-2 rounded-full bg-msit-dark-800 border border-msit-dark-700 mb-8">
            <span class="text-sm font-medium text-msit-accent font-sans">✨ No setup required</span>
          </div>
          
          <!-- Main Heading -->
          <h1 class="text-5xl sm:text-6xl md:text-7xl lg:text-8xl font-serif font-bold text-msit-dark-50 leading-tight tracking-tight">
            <span class="block">Master Python</span>
            <span class="block text-msit-accent mt-2">with StudyHall</span>
          </h1>
          
          <!-- Subheading -->
          <p class="mt-6 max-w-3xl mx-auto text-lg sm:text-xl md:text-2xl text-msit-dark-100 font-sans leading-relaxed">
            Your simple, powerful learning platform. Access course materials, run code in your browser, and export your work—all in one place.
          </p>
          
          <!-- CTA Buttons -->
          <div class="mt-10 flex flex-col sm:flex-row gap-4 justify-center items-center">
            <router-link
              to="/configuration"
              class="group w-full sm:w-auto inline-flex items-center justify-center px-8 py-4 border border-transparent text-base font-semibold rounded-lg text-msit-dark bg-msit-accent hover:bg-msit-accent-500 shadow-lg shadow-msit-accent/20 hover:shadow-xl hover:shadow-msit-accent/30 transition-all duration-200 font-sans"
            >
              Get Started Free
              <svg class="ml-2 h-5 w-5 group-hover:translate-x-1 transition-transform" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 7l5 5m0 0l-5 5m5-5H6" />
              </svg>
            </router-link>
            <router-link
              to="/compiler"
              class="w-full sm:w-auto inline-flex items-center justify-center px-8 py-4 border-2 border-msit-dark-700 text-base font-semibold rounded-lg text-msit-dark-50 bg-msit-dark-800 hover:border-msit-accent hover:bg-msit-dark-700 transition-all duration-200 font-sans"
            >
              Try Compiler
            </router-link>
          </div>
          
          <!-- Trust indicators -->
          <div class="mt-12 flex flex-wrap justify-center items-center gap-8 text-sm text-msit-dark-300 font-sans">
            <div class="flex items-center gap-2">
              <svg class="h-5 w-5 text-msit-accent" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
              </svg>
              <span>No installation</span>
            </div>
            <div class="flex items-center gap-2">
              <svg class="h-5 w-5 text-msit-accent" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
              </svg>
              <span>Free to use</span>
            </div>
            <div class="flex items-center gap-2">
              <svg class="h-5 w-5 text-msit-accent" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
              </svg>
              <span>Instant access</span>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Code Preview Section -->
    <div class="bg-msit-dark-900 py-16 sm:py-20">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="text-center mb-12">
          <h2 class="text-3xl sm:text-4xl font-serif font-bold text-msit-dark-50">
            Code directly in your browser
          </h2>
          <p class="mt-4 text-lg text-msit-dark-100 font-sans max-w-2xl mx-auto">
            No setup, no configuration. Just write Python code and see results instantly.
          </p>
        </div>
        
        <div class="max-w-4xl mx-auto">
          <div class="bg-msit-dark-800 rounded-xl border border-msit-dark-700 overflow-hidden shadow-2xl">
            <div class="bg-msit-dark-700 px-4 py-3 flex items-center gap-2 border-b border-msit-dark-600">
              <div class="flex gap-2">
                <div class="w-3 h-3 rounded-full bg-red-500"></div>
                <div class="w-3 h-3 rounded-full bg-yellow-500"></div>
                <div class="w-3 h-3 rounded-full bg-green-500"></div>
              </div>
              <span class="ml-4 text-sm text-msit-dark-300 font-mono font-sans">python_runner.py</span>
            </div>
            <div class="p-6 font-mono text-sm">
              <div class="space-y-2">
                <div><span class="text-msit-dark-300"># Welcome to StudyHall</span></div>
                <div><span class="text-msit-accent">def</span> <span class="text-msit-dark-50">greet</span><span class="text-msit-dark-300">(</span><span class="text-msit-dark-50">name</span><span class="text-msit-dark-300">):</span></div>
                <div class="ml-4"><span class="text-msit-accent">return</span> <span class="text-msit-dark-300">f</span><span class="text-msit-dark-50">"Hello, {name}! Welcome to Python."</span></div>
                <div class="pt-2"><span class="text-msit-dark-50">result</span> <span class="text-msit-dark-300">=</span> <span class="text-msit-dark-50">greet</span><span class="text-msit-dark-300">(</span><span class="text-msit-dark-50">"StudyHall"</span><span class="text-msit-dark-300">)</span></div>
                <div><span class="text-msit-dark-50">print</span><span class="text-msit-dark-300">(</span><span class="text-msit-dark-50">result</span><span class="text-msit-dark-300">)</span></div>
                <div class="pt-4 border-t border-msit-dark-700">
                  <span class="text-msit-dark-300">$ </span><span class="text-msit-accent">Output:</span>
                  <div class="mt-2 text-msit-dark-50">Hello, StudyHall! Welcome to Python.</div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Features Section -->
    <div class="py-20 bg-msit-dark">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="text-center mb-16">
          <h2 class="text-base text-msit-accent font-semibold tracking-wide uppercase font-sans mb-3">Features</h2>
          <p class="text-3xl sm:text-4xl lg:text-5xl font-serif font-bold text-msit-dark-50">
            Everything you need to learn Python
          </p>
          <p class="mt-4 text-lg text-msit-dark-100 font-sans max-w-2xl mx-auto">
            A complete learning environment designed for simplicity and effectiveness
          </p>
        </div>

        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8">
          <div class="group relative bg-msit-dark-800 p-8 rounded-xl border border-msit-dark-700 hover:border-msit-accent transition-all duration-200 hover:shadow-lg hover:shadow-msit-accent/10">
            <div class="flex items-center justify-center w-14 h-14 rounded-lg bg-msit-accent/20 text-msit-accent mb-6 group-hover:bg-msit-accent group-hover:text-msit-dark transition-colors">
              <svg class="h-7 w-7" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5c1.747 0 3.332.477 4.5 1.253v13C19.832 18.477 18.247 18 16.5 18c-1.746 0-3.332.477-4.5 1.253" />
              </svg>
            </div>
            <h3 class="text-xl font-semibold text-msit-dark-50 mb-3 font-sans">Course Materials</h3>
            <p class="text-msit-dark-100 font-sans leading-relaxed">
              Access comprehensive Python course materials and tutorials organized for easy learning and reference.
            </p>
          </div>

          <div class="group relative bg-msit-dark-800 p-8 rounded-xl border border-msit-dark-700 hover:border-msit-accent transition-all duration-200 hover:shadow-lg hover:shadow-msit-accent/10">
            <div class="flex items-center justify-center w-14 h-14 rounded-lg bg-msit-accent/20 text-msit-accent mb-6 group-hover:bg-msit-accent group-hover:text-msit-dark transition-colors">
              <svg class="h-7 w-7" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 20l4-16m4 4l4 4-4 4M6 16l-4-4 4-4" />
              </svg>
            </div>
            <h3 class="text-xl font-semibold text-msit-dark-50 mb-3 font-sans">Python Compiler</h3>
            <p class="text-msit-dark-100 font-sans leading-relaxed">
              Run Python code directly in your browser. No setup required, just code and execute instantly.
            </p>
          </div>

          <div class="group relative bg-msit-dark-800 p-8 rounded-xl border border-msit-dark-700 hover:border-msit-accent transition-all duration-200 hover:shadow-lg hover:shadow-msit-accent/10">
            <div class="flex items-center justify-center w-14 h-14 rounded-lg bg-msit-accent/20 text-msit-accent mb-6 group-hover:bg-msit-accent group-hover:text-msit-dark transition-colors">
              <svg class="h-7 w-7" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 10v6m0 0l-3-3m3 3l3-3m2 8H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
              </svg>
            </div>
            <h3 class="text-xl font-semibold text-msit-dark-50 mb-3 font-sans">Export Your Work</h3>
            <p class="text-msit-dark-100 font-sans leading-relaxed">
              Export your code and work at any time. Keep your learning organized and accessible whenever you need it.
            </p>
          </div>

          <div class="group relative bg-msit-dark-800 p-8 rounded-xl border border-msit-dark-700 hover:border-msit-accent transition-all duration-200 hover:shadow-lg hover:shadow-msit-accent/10">
            <div class="flex items-center justify-center w-14 h-14 rounded-lg bg-msit-accent/20 text-msit-accent mb-6 group-hover:bg-msit-accent group-hover:text-msit-dark transition-colors">
              <svg class="h-7 w-7" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
              </svg>
            </div>
            <h3 class="text-xl font-semibold text-msit-dark-50 mb-3 font-sans">Notion Integration</h3>
            <p class="text-msit-dark-100 font-sans leading-relaxed">
              Sync course materials from your Notion database automatically. Keep everything in sync effortlessly.
            </p>
          </div>
        </div>
      </div>
    </div>

    <!-- How It Works Section -->
    <div class="py-20 bg-msit-dark-900">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="text-center mb-16">
          <h2 class="text-3xl sm:text-4xl font-serif font-bold text-msit-dark-50 mb-4">
            How it works
          </h2>
          <p class="text-lg text-msit-dark-100 font-sans max-w-2xl mx-auto">
            Get started in three simple steps
          </p>
        </div>
        
        <div class="grid grid-cols-1 md:grid-cols-3 gap-8 lg:gap-12">
          <div class="text-center">
            <div class="inline-flex items-center justify-center w-16 h-16 rounded-full bg-msit-accent text-msit-dark text-2xl font-bold mb-6 font-sans">
              1
            </div>
            <h3 class="text-xl font-semibold text-msit-dark-50 mb-3 font-sans">Set up your character</h3>
            <p class="text-msit-dark-100 font-sans">
              Create your profile with a simple name and role. Takes less than a minute.
            </p>
          </div>
          
          <div class="text-center">
            <div class="inline-flex items-center justify-center w-16 h-16 rounded-full bg-msit-accent text-msit-dark text-2xl font-bold mb-6 font-sans">
              2
            </div>
            <h3 class="text-xl font-semibold text-msit-dark-50 mb-3 font-sans">Explore materials</h3>
            <p class="text-msit-dark-100 font-sans">
              Browse through comprehensive Python course materials and tutorials.
            </p>
          </div>
          
          <div class="text-center">
            <div class="inline-flex items-center justify-center w-16 h-16 rounded-full bg-msit-accent text-msit-dark text-2xl font-bold mb-6 font-sans">
              3
            </div>
            <h3 class="text-xl font-semibold text-msit-dark-50 mb-3 font-sans">Start coding</h3>
            <p class="text-msit-dark-100 font-sans">
              Write and run Python code in your browser. No installation needed.
            </p>
          </div>
        </div>
      </div>
    </div>

    <!-- CTA Section -->
    <div class="bg-msit-dark-800">
      <div class="max-w-2xl mx-auto text-center py-12 sm:py-16 md:py-20 px-4 sm:px-6 lg:px-8">
        <h2 class="text-2xl sm:text-3xl md:text-4xl font-serif font-bold text-msit-dark-50">
          <span class="block">Ready to start learning?</span>
          <span class="block mt-2">Join StudyHall today.</span>
        </h2>
        <p class="mt-4 text-base sm:text-lg leading-6 text-msit-dark-100 font-sans">
          Start learning Python today. No setup required, just code and practice.
        </p>
        <router-link
          to="/configuration"
          class="mt-6 sm:mt-8 w-full sm:w-auto inline-flex items-center justify-center px-6 sm:px-5 py-2.5 sm:py-3 border border-transparent text-sm sm:text-base font-semibold rounded-md text-msit-dark bg-msit-accent hover:bg-msit-accent-500 transition-colors font-sans"
        >
          Get Started
          <svg class="ml-2 h-4 w-4 sm:h-5 sm:w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7" />
          </svg>
        </router-link>
      </div>
    </div>
  </div>

  <!-- Dashboard view for users with character configured -->
  <div v-else class="px-4 py-4 sm:py-6 sm:px-0">
    <div class="text-center">
      <h1 class="text-2xl sm:text-4xl md:text-5xl lg:text-6xl font-serif font-bold text-msit-dark-50">
        Welcome back, {{ character.name }}!
      </h1>
      <p class="mt-3 max-w-md mx-auto text-sm sm:text-base md:text-lg lg:text-xl text-msit-dark-100 md:mt-5 md:max-w-3xl font-sans px-2 sm:px-0">
        Continue your learning journey
      </p>
    </div>

    <div class="mt-8 sm:mt-12">
      <div class="grid grid-cols-1 gap-4 sm:gap-6 md:gap-8 sm:grid-cols-2 lg:grid-cols-3">
        <router-link
          to="/materials"
          class="relative group bg-msit-dark-800 p-6 focus-within:ring-2 focus-within:ring-inset focus-within:ring-msit-accent rounded-lg border border-msit-dark-700 hover:border-msit-accent transition-all"
        >
          <div>
            <span class="rounded-lg inline-flex p-3 bg-msit-accent text-msit-dark ring-4 ring-msit-dark-800">
              <svg class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5c1.747 0 3.332.477 4.5 1.253v13C19.832 18.477 18.247 18 16.5 18c-1.746 0-3.332.477-4.5 1.253" />
              </svg>
            </span>
          </div>
          <div class="mt-4">
            <h3 class="text-lg font-semibold text-msit-dark-50 font-sans">
              <span class="absolute inset-0" aria-hidden="true"></span>
              Course Materials
            </h3>
            <p class="mt-2 text-sm text-msit-dark-100 font-sans">Access Python and other course materials</p>
          </div>
        </router-link>

        <router-link
          to="/compiler"
          class="relative group bg-msit-dark-800 p-6 focus-within:ring-2 focus-within:ring-inset focus-within:ring-msit-accent rounded-lg border border-msit-dark-700 hover:border-msit-accent transition-all"
        >
          <div>
            <span class="rounded-lg inline-flex p-3 bg-msit-accent text-msit-dark ring-4 ring-msit-dark-800">
              <svg class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 20l4-16m4 4l4 4-4 4M6 16l-4-4 4-4" />
              </svg>
            </span>
          </div>
          <div class="mt-4">
            <h3 class="text-lg font-semibold text-msit-dark-50 font-sans">
              <span class="absolute inset-0" aria-hidden="true"></span>
              Python Compiler
            </h3>
            <p class="mt-2 text-sm text-msit-dark-100 font-sans">Run Python code directly in your browser</p>
          </div>
        </router-link>

        <router-link
          to="/dashboard"
          class="relative group bg-msit-dark-800 p-6 focus-within:ring-2 focus-within:ring-inset focus-within:ring-msit-accent rounded-lg border border-msit-dark-700 hover:border-msit-accent transition-all"
        >
          <div>
            <span class="rounded-lg inline-flex p-3 bg-msit-accent text-msit-dark ring-4 ring-msit-dark-800">
              <svg class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
              </svg>
            </span>
          </div>
          <div class="mt-4">
            <h3 class="text-lg font-semibold text-msit-dark-50 font-sans">
              <span class="absolute inset-0" aria-hidden="true"></span>
              Dashboard
            </h3>
            <p class="mt-2 text-sm text-msit-dark-100 font-sans">View platform features and export your work</p>
          </div>
        </router-link>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { getCharacterConfig } from '../utils/character'

const character = ref<any>(null)

const loadCharacter = () => {
  character.value = getCharacterConfig()
}

onMounted(() => {
  loadCharacter()
})
</script>

