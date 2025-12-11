<template>
  <div class="px-4 py-4 sm:py-6 sm:px-0">
    <div class="mb-6 sm:mb-8">
      <h1 class="text-2xl sm:text-3xl font-bold text-msit-dark-50 mb-2 font-serif">Dashboard</h1>
      <p class="text-sm sm:text-base text-msit-dark-200 font-sans">Welcome to StudyHall - A simple learning platform</p>
    </div>

    <!-- Python Compiler Section -->
    <div class="mb-8">
      <div class="bg-msit-dark-800 shadow rounded-lg overflow-hidden border border-msit-dark-700">
        <div class="px-4 sm:px-6 py-4 border-b border-msit-dark-700">
          <div class="flex items-center">
            <svg class="h-6 w-6 text-msit-accent mr-3" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 20l4-16m4 4l4 4-4 4M6 16l-4-4 4-4" />
            </svg>
            <h2 class="text-xl sm:text-2xl font-bold text-msit-dark-50 font-serif">Python Compiler</h2>
          </div>
          <p class="mt-2 text-sm text-msit-dark-200 font-sans">Write and execute Python code directly in your browser</p>
        </div>
        <div class="px-4 sm:px-6 py-4 sm:py-6">
          <PythonRunner />
        </div>
      </div>
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
              Browse, search, and filter course materials.
            </p>
            <ul class="text-xs text-msit-dark-300 space-y-1 mb-4 font-sans">
              <li>• Search and filter by category</li>
              <li>• View detailed material content</li>
              <li>• Access all course materials</li>
            </ul>
            <router-link
              to="/materials"
              class="inline-flex items-center text-sm font-medium text-msit-accent hover:text-msit-accent-300 transition-colors font-sans"
            >
              Go to Materials →
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

        <!-- Practice Problems Feature -->
        <div class="bg-msit-dark-800 shadow rounded-lg overflow-hidden hover:shadow-lg transition-shadow border border-msit-dark-700 hover:border-msit-accent">
          <div class="p-4 sm:p-6">
            <div class="flex items-center mb-3">
              <div class="flex-shrink-0">
                <svg class="h-8 w-8 text-msit-accent" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                </svg>
              </div>
              <h3 class="ml-3 text-base sm:text-lg font-medium text-msit-dark-50 font-sans">Practice Problems</h3>
            </div>
            <p class="text-sm text-msit-dark-200 mb-4 font-sans">
              Solve coding challenges to improve your Python skills. Filter by difficulty and topic.
            </p>
            <ul class="text-xs text-msit-dark-300 space-y-1 mb-4 font-sans">
              <li>• Beginner to advanced problems</li>
              <li>• Filter by difficulty and topic</li>
              <li>• Detailed problem descriptions</li>
              <li>• Solve directly in compiler</li>
            </ul>
            <router-link
              to="/practice-problems"
              class="inline-flex items-center text-sm font-medium text-msit-accent hover:text-msit-accent-300 transition-colors font-sans"
            >
              View Problems →
            </router-link>
          </div>
        </div>

        <!-- Learning Path Feature -->
        <div class="bg-msit-dark-800 shadow rounded-lg overflow-hidden hover:shadow-lg transition-shadow border border-msit-dark-700 hover:border-msit-accent">
          <div class="p-4 sm:p-6">
            <div class="flex items-center mb-3">
              <div class="flex-shrink-0">
                <svg class="h-8 w-8 text-msit-accent" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 20l-5.447-2.724A1 1 0 013 16.382V5.618a1 1 0 011.447-.894L9 7m0 13l6-3m-6 3V7m6 10l4.553 2.276A1 1 0 0021 18.382V7.618a1 1 0 00-.553-.894L15 4m0 13V4m0 0L9 7" />
                </svg>
              </div>
              <h3 class="ml-3 text-base sm:text-lg font-medium text-msit-dark-50 font-sans">Learning Paths</h3>
            </div>
            <p class="text-sm text-msit-dark-200 mb-4 font-sans">
              Follow structured learning paths to master Python step by step. Track your progress.
            </p>
            <ul class="text-xs text-msit-dark-300 space-y-1 mb-4 font-sans">
              <li>• Structured curriculum</li>
              <li>• Progress tracking</li>
              <li>• Multiple skill levels</li>
              <li>• Comprehensive lessons</li>
            </ul>
            <router-link
              to="/learning-path"
              class="inline-flex items-center text-sm font-medium text-msit-accent hover:text-msit-accent-300 transition-colors font-sans"
            >
              Explore Paths →
            </router-link>
          </div>
        </div>

        <!-- Challenges Feature -->
        <div class="bg-msit-dark-800 shadow rounded-lg overflow-hidden hover:shadow-lg transition-shadow border border-msit-dark-700 hover:border-msit-accent">
          <div class="p-4 sm:p-6">
            <div class="flex items-center mb-3">
              <div class="flex-shrink-0">
                <svg class="h-8 w-8 text-msit-accent" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4M7.835 4.697a3.42 3.42 0 001.946-.806 3.42 3.42 0 014.438 0 3.42 3.42 0 001.946.806 3.42 3.42 0 013.138 3.138 3.42 3.42 0 00.806 1.946 3.42 3.42 0 010 4.438 3.42 3.42 0 00-.806 1.946 3.42 3.42 0 01-3.138 3.138 3.42 3.42 0 00-1.946.806 3.42 3.42 0 01-4.438 0 3.42 3.42 0 00-1.946-.806 3.42 3.42 0 01-3.138-3.138 3.42 3.42 0 00-.806-1.946 3.42 3.42 0 010-4.438 3.42 3.42 0 00.806-1.946 3.42 3.42 0 013.138-3.138z" />
                </svg>
              </div>
              <h3 class="ml-3 text-base sm:text-lg font-medium text-msit-dark-50 font-sans">Daily Challenges</h3>
            </div>
            <p class="text-sm text-msit-dark-200 mb-4 font-sans">
              Daily and weekly coding challenges to keep your skills sharp. Earn points and track your progress.
            </p>
            <ul class="text-xs text-msit-dark-300 space-y-1 mb-4 font-sans">
              <li>• Daily coding challenges</li>
              <li>• Weekly advanced problems</li>
              <li>• Points and achievements</li>
              <li>• Challenge history</li>
            </ul>
            <router-link
              to="/challenges"
              class="inline-flex items-center text-sm font-medium text-msit-accent hover:text-msit-accent-300 transition-colors font-sans"
            >
              View Challenges →
            </router-link>
          </div>
        </div>

        <!-- Resources Feature -->
        <div class="bg-msit-dark-800 shadow rounded-lg overflow-hidden hover:shadow-lg transition-shadow border border-msit-dark-700 hover:border-msit-accent">
          <div class="p-4 sm:p-6">
            <div class="flex items-center mb-3">
              <div class="flex-shrink-0">
                <svg class="h-8 w-8 text-msit-accent" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5c1.747 0 3.332.477 4.5 1.253v13C19.832 18.477 18.247 18 16.5 18c-1.746 0-3.332.477-4.5 1.253" />
                </svg>
              </div>
              <h3 class="ml-3 text-base sm:text-lg font-medium text-msit-dark-50 font-sans">Resources</h3>
            </div>
            <p class="text-sm text-msit-dark-200 mb-4 font-sans">
              Curated resources, documentation, and tools to enhance your Python learning journey.
            </p>
            <ul class="text-xs text-msit-dark-300 space-y-1 mb-4 font-sans">
              <li>• Official documentation</li>
              <li>• Tutorials and courses</li>
              <li>• Practice platforms</li>
              <li>• Community resources</li>
            </ul>
            <router-link
              to="/resources"
              class="inline-flex items-center text-sm font-medium text-msit-accent hover:text-msit-accent-300 transition-colors font-sans"
            >
              Browse Resources →
            </router-link>
          </div>
        </div>

        <!-- Library Feature -->
        <div class="bg-msit-dark-800 shadow rounded-lg overflow-hidden hover:shadow-lg transition-shadow border border-msit-dark-700 hover:border-msit-accent">
          <div class="p-4 sm:p-6">
            <div class="flex items-center mb-3">
              <div class="flex-shrink-0">
                <svg class="h-8 w-8 text-msit-accent" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 012-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10" />
                </svg>
              </div>
              <h3 class="ml-3 text-base sm:text-lg font-medium text-msit-dark-50 font-sans">Library</h3>
            </div>
            <p class="text-sm text-msit-dark-200 mb-4 font-sans">
              Access a comprehensive collection of learning resources, books, and reference materials.
            </p>
            <ul class="text-xs text-msit-dark-300 space-y-1 mb-4 font-sans">
              <li>• Curated book collection</li>
              <li>• Reference materials</li>
              <li>• Learning resources</li>
              <li>• Organized by topic</li>
            </ul>
            <router-link
              to="/library"
              class="inline-flex items-center text-sm font-medium text-msit-accent hover:text-msit-accent-300 transition-colors font-sans"
            >
              Visit Library →
            </router-link>
          </div>
        </div>

        <!-- Gym Feature -->
        <div class="bg-msit-dark-800 shadow rounded-lg overflow-hidden hover:shadow-lg transition-shadow border border-msit-dark-700 hover:border-msit-accent">
          <div class="p-4 sm:p-6">
            <div class="flex items-center mb-3">
              <div class="flex-shrink-0">
                <svg class="h-8 w-8 text-msit-accent" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z" />
                </svg>
              </div>
              <h3 class="ml-3 text-base sm:text-lg font-medium text-msit-dark-50 font-sans">Gym</h3>
            </div>
            <p class="text-sm text-msit-dark-200 mb-4 font-sans">
              Practice exercises and workouts to strengthen your Python programming skills.
            </p>
            <ul class="text-xs text-msit-dark-300 space-y-1 mb-4 font-sans">
              <li>• Interactive exercises</li>
              <li>• Skill-building workouts</li>
              <li>• Progressive difficulty</li>
              <li>• Hands-on practice</li>
            </ul>
            <router-link
              to="/gym"
              class="inline-flex items-center text-sm font-medium text-msit-accent hover:text-msit-accent-300 transition-colors font-sans"
            >
              Start Training →
            </router-link>
          </div>
        </div>

        <!-- Typing Test Feature -->
        <div class="bg-msit-dark-800 shadow rounded-lg overflow-hidden hover:shadow-lg transition-shadow border border-msit-dark-700 hover:border-msit-accent">
          <div class="p-4 sm:p-6">
            <div class="flex items-center mb-3">
              <div class="flex-shrink-0">
                <svg class="h-8 w-8 text-msit-accent" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                </svg>
              </div>
              <h3 class="ml-3 text-base sm:text-lg font-medium text-msit-dark-50 font-sans">Typing Test</h3>
            </div>
            <p class="text-sm text-msit-dark-200 mb-4 font-sans">
              Improve your typing speed and accuracy with code-focused typing tests.
            </p>
            <ul class="text-xs text-msit-dark-300 space-y-1 mb-4 font-sans">
              <li>• Code typing practice</li>
              <li>• Speed and accuracy tracking</li>
              <li>• Python syntax focused</li>
              <li>• Real-time feedback</li>
            </ul>
            <router-link
              to="/typing-test"
              class="inline-flex items-center text-sm font-medium text-msit-accent hover:text-msit-accent-300 transition-colors font-sans"
            >
              Take Test →
            </router-link>
          </div>
        </div>

        <!-- Mock Interview Feature -->
        <div class="bg-msit-dark-800 shadow rounded-lg overflow-hidden hover:shadow-lg transition-shadow border border-msit-dark-700 hover:border-msit-accent">
          <div class="p-4 sm:p-6">
            <div class="flex items-center mb-3">
              <div class="flex-shrink-0">
                <svg class="h-8 w-8 text-msit-accent" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z" />
                </svg>
              </div>
              <h3 class="ml-3 text-base sm:text-lg font-medium text-msit-dark-50 font-sans">Mock Interview</h3>
            </div>
            <p class="text-sm text-msit-dark-200 mb-4 font-sans">
              Practice technical interviews with realistic coding questions and scenarios.
            </p>
            <ul class="text-xs text-msit-dark-300 space-y-1 mb-4 font-sans">
              <li>• Interview-style questions</li>
              <li>• Real-world scenarios</li>
              <li>• Time-limited practice</li>
              <li>• Interview preparation</li>
            </ul>
            <router-link
              to="/mock-interview"
              class="inline-flex items-center text-sm font-medium text-msit-accent hover:text-msit-accent-300 transition-colors font-sans"
            >
              Start Interview →
            </router-link>
          </div>
        </div>

        <!-- Snippets Feature -->
        <div class="bg-msit-dark-800 shadow rounded-lg overflow-hidden hover:shadow-lg transition-shadow border border-msit-dark-700 hover:border-msit-accent">
          <div class="p-4 sm:p-6">
            <div class="flex items-center mb-3">
              <div class="flex-shrink-0">
                <svg class="h-8 w-8 text-msit-accent" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 9l3 3-3 3m5 0h3M5 20h14a2 2 0 002-2V6a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
                </svg>
              </div>
              <h3 class="ml-3 text-base sm:text-lg font-medium text-msit-dark-50 font-sans">Code Snippets</h3>
            </div>
            <p class="text-sm text-msit-dark-200 mb-4 font-sans">
              Browse and use reusable code snippets for common Python tasks and patterns.
            </p>
            <ul class="text-xs text-msit-dark-300 space-y-1 mb-4 font-sans">
              <li>• Reusable code snippets</li>
              <li>• Common patterns</li>
              <li>• Quick copy-paste</li>
              <li>• Organized by category</li>
            </ul>
            <router-link
              to="/snippets"
              class="inline-flex items-center text-sm font-medium text-msit-accent hover:text-msit-accent-300 transition-colors font-sans"
            >
              Browse Snippets →
            </router-link>
          </div>
        </div>

        <!-- Templates Feature -->
        <div class="bg-msit-dark-800 shadow rounded-lg overflow-hidden hover:shadow-lg transition-shadow border border-msit-dark-700 hover:border-msit-accent">
          <div class="p-4 sm:p-6">
            <div class="flex items-center mb-3">
              <div class="flex-shrink-0">
                <svg class="h-8 w-8 text-msit-accent" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 5a1 1 0 011-1h14a1 1 0 011 1v2a1 1 0 01-1 1H5a1 1 0 01-1-1V5zM4 13a1 1 0 011-1h6a1 1 0 011 1v6a1 1 0 01-1 1H5a1 1 0 01-1-1v-6zM16 13a1 1 0 011-1h2a1 1 0 011 1v6a1 1 0 01-1 1h-2a1 1 0 01-1-1v-6z" />
                </svg>
              </div>
              <h3 class="ml-3 text-base sm:text-lg font-medium text-msit-dark-50 font-sans">Templates</h3>
            </div>
            <p class="text-sm text-msit-dark-200 mb-4 font-sans">
              Start your projects faster with pre-built code templates and project structures.
            </p>
            <ul class="text-xs text-msit-dark-300 space-y-1 mb-4 font-sans">
              <li>• Project templates</li>
              <li>• Code structure templates</li>
              <li>• Quick project setup</li>
              <li>• Best practices included</li>
            </ul>
            <router-link
              to="/templates"
              class="inline-flex items-center text-sm font-medium text-msit-accent hover:text-msit-accent-300 transition-colors font-sans"
            >
              View Templates →
            </router-link>
          </div>
        </div>

        <!-- Cheat Sheets Feature -->
        <div class="bg-msit-dark-800 shadow rounded-lg overflow-hidden hover:shadow-lg transition-shadow border border-msit-dark-700 hover:border-msit-accent">
          <div class="p-4 sm:p-6">
            <div class="flex items-center mb-3">
              <div class="flex-shrink-0">
                <svg class="h-8 w-8 text-msit-accent" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                </svg>
              </div>
              <h3 class="ml-3 text-base sm:text-lg font-medium text-msit-dark-50 font-sans">Cheat Sheets</h3>
            </div>
            <p class="text-sm text-msit-dark-200 mb-4 font-sans">
              Quick reference guides for Python syntax, libraries, and common operations.
            </p>
            <ul class="text-xs text-msit-dark-300 space-y-1 mb-4 font-sans">
              <li>• Python syntax reference</li>
              <li>• Library quick guides</li>
              <li>• Common operations</li>
              <li>• Print-friendly format</li>
            </ul>
            <router-link
              to="/cheat-sheets"
              class="inline-flex items-center text-sm font-medium text-msit-accent hover:text-msit-accent-300 transition-colors font-sans"
            >
              View Cheat Sheets →
            </router-link>
          </div>
        </div>

        <!-- Tools Feature -->
        <div class="bg-msit-dark-800 shadow rounded-lg overflow-hidden hover:shadow-lg transition-shadow border border-msit-dark-700 hover:border-msit-accent">
          <div class="p-4 sm:p-6">
            <div class="flex items-center mb-3">
              <div class="flex-shrink-0">
                <svg class="h-8 w-8 text-msit-accent" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.065 2.572c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.572 1.065c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.065-2.572c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z" />
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
                </svg>
              </div>
              <h3 class="ml-3 text-base sm:text-lg font-medium text-msit-dark-50 font-sans">All Tools</h3>
            </div>
            <p class="text-sm text-msit-dark-200 mb-4 font-sans">
              Access all development tools, utilities, and helpers in one place.
            </p>
            <ul class="text-xs text-msit-dark-300 space-y-1 mb-4 font-sans">
              <li>• Complete tool collection</li>
              <li>• Development utilities</li>
              <li>• Productivity helpers</li>
              <li>• One-stop tool hub</li>
            </ul>
            <router-link
              to="/tools"
              class="inline-flex items-center text-sm font-medium text-msit-accent hover:text-msit-accent-300 transition-colors font-sans"
            >
              Browse Tools →
            </router-link>
          </div>
        </div>

        <!-- Search Feature -->
        <div class="bg-msit-dark-800 shadow rounded-lg overflow-hidden hover:shadow-lg transition-shadow border border-msit-dark-700 hover:border-msit-accent">
          <div class="p-4 sm:p-6">
            <div class="flex items-center mb-3">
              <div class="flex-shrink-0">
                <svg class="h-8 w-8 text-msit-accent" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
                </svg>
              </div>
              <h3 class="ml-3 text-base sm:text-lg font-medium text-msit-dark-50 font-sans">Search</h3>
            </div>
            <p class="text-sm text-msit-dark-200 mb-4 font-sans">
              Quickly find materials, code examples, and resources across the platform.
            </p>
            <ul class="text-xs text-msit-dark-300 space-y-1 mb-4 font-sans">
              <li>• Search all content</li>
              <li>• Filter by type</li>
              <li>• Quick access</li>
              <li>• Advanced filters</li>
            </ul>
            <router-link
              to="/search"
              class="inline-flex items-center text-sm font-medium text-msit-accent hover:text-msit-accent-300 transition-colors font-sans"
            >
              Start Searching →
            </router-link>
          </div>
        </div>

        <!-- Test Coverage Feature -->
        <div class="bg-msit-dark-800 shadow rounded-lg overflow-hidden hover:shadow-lg transition-shadow border border-msit-dark-700 hover:border-msit-accent">
          <div class="p-4 sm:p-6">
            <div class="flex items-center mb-3">
              <div class="flex-shrink-0">
                <svg class="h-8 w-8 text-msit-accent" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
              </div>
              <h3 class="ml-3 text-base sm:text-lg font-medium text-msit-dark-50 font-sans">Test Coverage</h3>
            </div>
            <p class="text-sm text-msit-dark-200 mb-4 font-sans">
              Analyze and improve your code's test coverage with comprehensive testing tools.
            </p>
            <ul class="text-xs text-msit-dark-300 space-y-1 mb-4 font-sans">
              <li>• Coverage analysis</li>
              <li>• Testing tools</li>
              <li>• Quality metrics</li>
              <li>• Code quality insights</li>
            </ul>
            <router-link
              to="/test-coverage"
              class="inline-flex items-center text-sm font-medium text-msit-accent hover:text-msit-accent-300 transition-colors font-sans"
            >
              View Coverage →
            </router-link>
          </div>
        </div>

        <!-- Help Feature -->
        <div class="bg-msit-dark-800 shadow rounded-lg overflow-hidden hover:shadow-lg transition-shadow border border-msit-dark-700 hover:border-msit-accent">
          <div class="p-4 sm:p-6">
            <div class="flex items-center mb-3">
              <div class="flex-shrink-0">
                <svg class="h-8 w-8 text-msit-accent" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8.228 9c.549-1.165 2.03-2 3.772-2 2.21 0 4 1.343 4 3 0 1.4-1.278 2.575-3.006 2.907-.542.104-.994.54-.994 1.093m0 3h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
              </div>
              <h3 class="ml-3 text-base sm:text-lg font-medium text-msit-dark-50 font-sans">Help & Support</h3>
            </div>
            <p class="text-sm text-msit-dark-200 mb-4 font-sans">
              Get help, find answers to common questions, and learn how to use the platform.
            </p>
            <ul class="text-xs text-msit-dark-300 space-y-1 mb-4 font-sans">
              <li>• FAQ and guides</li>
              <li>• Platform documentation</li>
              <li>• Troubleshooting tips</li>
              <li>• User support</li>
            </ul>
            <router-link
              to="/help"
              class="inline-flex items-center text-sm font-medium text-msit-accent hover:text-msit-accent-300 transition-colors font-sans"
            >
              Get Help →
            </router-link>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import PythonRunner from '../components/PythonRunner.vue'

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
