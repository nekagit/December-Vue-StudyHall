<template>
  <div class="px-4 py-6 sm:px-0">
    <div class="mb-8">
      <h1 class="text-3xl font-bold text-gray-900 mb-2">Dashboard</h1>
      <p class="text-gray-600">Overview of all platform features and your learning progress</p>
    </div>

    <div v-if="loading" class="text-center py-12">
      <div class="inline-block animate-spin rounded-full h-8 w-8 border-b-2 border-indigo-600"></div>
    </div>

    <div v-else-if="error" class="rounded-md bg-red-50 p-4 mb-4">
      <div class="text-sm text-red-800">{{ error }}</div>
    </div>

    <div v-else>
      <!-- Stats Grid -->
      <div class="grid grid-cols-1 gap-5 sm:grid-cols-2 lg:grid-cols-5 mb-8">
        <div class="bg-white overflow-hidden shadow rounded-lg">
          <div class="p-5">
            <div class="flex items-center">
              <div class="flex-shrink-0">
                <svg class="h-6 w-6 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5c1.747 0 3.332.477 4.5 1.253v13C19.832 18.477 18.247 18 16.5 18c-1.746 0-3.332.477-4.5 1.253" />
                </svg>
              </div>
              <div class="ml-5 w-0 flex-1">
                <dl>
                  <dt class="text-sm font-medium text-gray-500 truncate">Total Materials</dt>
                  <dd class="text-lg font-medium text-gray-900">{{ stats.total_materials }}</dd>
                </dl>
              </div>
            </div>
          </div>
        </div>

        <div class="bg-white overflow-hidden shadow rounded-lg">
          <div class="p-5">
            <div class="flex items-center">
              <div class="flex-shrink-0">
                <svg class="h-6 w-6 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 5a2 2 0 012-2h10a2 2 0 012 2v16l-7-3.5L5 21V5z" />
                </svg>
              </div>
              <div class="ml-5 w-0 flex-1">
                <dl>
                  <dt class="text-sm font-medium text-gray-500 truncate">Bookmarks</dt>
                  <dd class="text-lg font-medium text-gray-900">{{ stats.total_bookmarks }}</dd>
                </dl>
              </div>
            </div>
          </div>
        </div>

        <div class="bg-white overflow-hidden shadow rounded-lg">
          <div class="p-5">
            <div class="flex items-center">
              <div class="flex-shrink-0">
                <svg class="h-6 w-6 text-green-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
              </div>
              <div class="ml-5 w-0 flex-1">
                <dl>
                  <dt class="text-sm font-medium text-gray-500 truncate">Completed</dt>
                  <dd class="text-lg font-medium text-gray-900">{{ stats.completed_materials }}</dd>
                </dl>
              </div>
            </div>
          </div>
        </div>

        <div class="bg-white overflow-hidden shadow rounded-lg">
          <div class="p-5">
            <div class="flex items-center">
              <div class="flex-shrink-0">
                <svg class="h-6 w-6 text-blue-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
              </div>
              <div class="ml-5 w-0 flex-1">
                <dl>
                  <dt class="text-sm font-medium text-gray-500 truncate">In Progress</dt>
                  <dd class="text-lg font-medium text-gray-900">{{ stats.in_progress_materials }}</dd>
                </dl>
              </div>
            </div>
          </div>
        </div>

        <div class="bg-white overflow-hidden shadow rounded-lg">
          <div class="p-5">
            <div class="flex items-center">
              <div class="flex-shrink-0">
                <svg class="h-6 w-6 text-orange-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z" />
                </svg>
              </div>
              <div class="ml-5 w-0 flex-1">
                <dl>
                  <dt class="text-sm font-medium text-gray-500 truncate">Study Streak</dt>
                  <dd class="text-lg font-medium text-gray-900">{{ streak.current_streak }} days</dd>
                  <dd class="text-xs text-gray-400">Best: {{ streak.longest_streak }} days</dd>
                </dl>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- All Features Section -->
      <div class="mb-8">
        <h2 class="text-2xl font-bold text-gray-900 mb-4">All Features</h2>
        <div class="grid grid-cols-1 gap-6 sm:grid-cols-2 lg:grid-cols-3">
          <!-- Materials Feature -->
          <div class="bg-white shadow rounded-lg overflow-hidden hover:shadow-lg transition-shadow">
            <div class="p-6">
              <div class="flex items-center mb-3">
                <div class="flex-shrink-0">
                  <svg class="h-8 w-8 text-indigo-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5c1.747 0 3.332.477 4.5 1.253v13C19.832 18.477 18.247 18 16.5 18c-1.746 0-3.332.477-4.5 1.253" />
                  </svg>
                </div>
                <h3 class="ml-3 text-lg font-medium text-gray-900">Course Materials</h3>
              </div>
              <p class="text-sm text-gray-600 mb-4">
                Browse, search, and filter course materials. Sync content from Notion and track your learning progress.
              </p>
              <ul class="text-xs text-gray-500 space-y-1 mb-4">
                <li>• Search and filter by category</li>
                <li>• Sync from Notion database</li>
                <li>• View detailed material content</li>
                <li>• Track reading progress</li>
              </ul>
              <router-link
                to="/materials"
                class="inline-flex items-center text-sm font-medium text-indigo-600 hover:text-indigo-500"
              >
                Go to Materials →
              </router-link>
            </div>
          </div>

          <!-- Bookmarks Feature -->
          <div class="bg-white shadow rounded-lg overflow-hidden hover:shadow-lg transition-shadow">
            <div class="p-6">
              <div class="flex items-center mb-3">
                <div class="flex-shrink-0">
                  <svg class="h-8 w-8 text-indigo-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 5a2 2 0 012-2h10a2 2 0 012 2v16l-7-3.5L5 21V5z" />
                  </svg>
                </div>
                <h3 class="ml-3 text-lg font-medium text-gray-900">Bookmarks</h3>
              </div>
              <p class="text-sm text-gray-600 mb-4">
                Save materials for quick access later. Organize your favorite learning resources in one place.
              </p>
              <ul class="text-xs text-gray-500 space-y-1 mb-4">
                <li>• Bookmark any material</li>
                <li>• View all bookmarks</li>
                <li>• Quick access to saved content</li>
                <li>• Remove bookmarks easily</li>
              </ul>
              <router-link
                to="/bookmarks"
                class="inline-flex items-center text-sm font-medium text-indigo-600 hover:text-indigo-500"
              >
                Go to Bookmarks →
              </router-link>
            </div>
          </div>

          <!-- Progress Tracking Feature -->
          <div class="bg-white shadow rounded-lg overflow-hidden hover:shadow-lg transition-shadow">
            <div class="p-6">
              <div class="flex items-center mb-3">
                <div class="flex-shrink-0">
                  <svg class="h-8 w-8 text-indigo-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
                  </svg>
                </div>
                <h3 class="ml-3 text-lg font-medium text-gray-900">Progress Tracking</h3>
              </div>
              <p class="text-sm text-gray-600 mb-4">
                Track your learning progress on each material. Set completion status and percentage.
              </p>
              <ul class="text-xs text-gray-500 space-y-1 mb-4">
                <li>• Track progress per material</li>
                <li>• Set completion percentage</li>
                <li>• Status: Not Started, In Progress, Completed</li>
                <li>• Visual progress indicators</li>
              </ul>
              <router-link
                to="/materials"
                class="inline-flex items-center text-sm font-medium text-indigo-600 hover:text-indigo-500"
              >
                Track Progress →
              </router-link>
            </div>
          </div>

          <!-- Python Compiler Feature -->
          <div class="bg-white shadow rounded-lg overflow-hidden hover:shadow-lg transition-shadow">
            <div class="p-6">
              <div class="flex items-center mb-3">
                <div class="flex-shrink-0">
                  <svg class="h-8 w-8 text-indigo-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 20l4-16m4 4l4 4-4 4M6 16l-4-4 4-4" />
                  </svg>
                </div>
                <h3 class="ml-3 text-lg font-medium text-gray-900">Python Compiler</h3>
              </div>
              <p class="text-sm text-gray-600 mb-4">
                Write and execute Python code directly in your browser. Practice coding without leaving the platform.
              </p>
              <ul class="text-xs text-gray-500 space-y-1 mb-4">
                <li>• Interactive code editor</li>
                <li>• Execute Python code</li>
                <li>• View output instantly</li>
                <li>• Practice while learning</li>
              </ul>
              <router-link
                to="/compiler"
                class="inline-flex items-center text-sm font-medium text-indigo-600 hover:text-indigo-500"
              >
                Open Compiler →
              </router-link>
            </div>
          </div>

          <!-- Profile Feature -->
          <div class="bg-white shadow rounded-lg overflow-hidden hover:shadow-lg transition-shadow">
            <div class="p-6">
              <div class="flex items-center mb-3">
                <div class="flex-shrink-0">
                  <svg class="h-8 w-8 text-indigo-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
                  </svg>
                </div>
                <h3 class="ml-3 text-lg font-medium text-gray-900">Profile</h3>
              </div>
              <p class="text-sm text-gray-600 mb-4">
                View your account information and learning statistics. See your overall progress summary.
              </p>
              <ul class="text-xs text-gray-500 space-y-1 mb-4">
                <li>• View account details</li>
                <li>• Learning progress summary</li>
                <li>• Completed materials count</li>
                <li>• In-progress materials count</li>
              </ul>
              <router-link
                to="/profile"
                class="inline-flex items-center text-sm font-medium text-indigo-600 hover:text-indigo-500"
              >
                View Profile →
              </router-link>
            </div>
          </div>

          <!-- Notion Integration Feature -->
          <div class="bg-white shadow rounded-lg overflow-hidden hover:shadow-lg transition-shadow">
            <div class="p-6">
              <div class="flex items-center mb-3">
                <div class="flex-shrink-0">
                  <svg class="h-8 w-8 text-indigo-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
                  </svg>
                </div>
                <h3 class="ml-3 text-lg font-medium text-gray-900">Notion Sync</h3>
              </div>
              <p class="text-sm text-gray-600 mb-4">
                Sync course materials from your Notion database. Keep your content up-to-date automatically.
              </p>
              <ul class="text-xs text-gray-500 space-y-1 mb-4">
                <li>• Connect to Notion database</li>
                <li>• Sync materials automatically</li>
                <li>• Import new content</li>
                <li>• One-click sync button</li>
              </ul>
              <router-link
                to="/materials"
                class="inline-flex items-center text-sm font-medium text-indigo-600 hover:text-indigo-500"
              >
                Sync Materials →
              </router-link>
            </div>
          </div>

          <!-- Study Goals Feature -->
          <div class="bg-white shadow rounded-lg overflow-hidden hover:shadow-lg transition-shadow">
            <div class="p-6">
              <div class="flex items-center mb-3">
                <div class="flex-shrink-0">
                  <svg class="h-8 w-8 text-indigo-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
                  </svg>
                </div>
                <h3 class="ml-3 text-lg font-medium text-gray-900">Study Goals</h3>
              </div>
              <p class="text-sm text-gray-600 mb-4">
                Set and track your learning objectives. Create goals with target dates and mark them as complete.
              </p>
              <ul class="text-xs text-gray-500 space-y-1 mb-4">
                <li>• Create learning goals</li>
                <li>• Set target dates</li>
                <li>• Track completion</li>
                <li>• Organize your objectives</li>
              </ul>
              <router-link
                to="/goals"
                class="inline-flex items-center text-sm font-medium text-indigo-600 hover:text-indigo-500"
              >
                Manage Goals →
              </router-link>
            </div>
          </div>

          <!-- Study Sessions Feature -->
          <div class="bg-white shadow rounded-lg overflow-hidden hover:shadow-lg transition-shadow">
            <div class="p-6">
              <div class="flex items-center mb-3">
                <div class="flex-shrink-0">
                  <svg class="h-8 w-8 text-indigo-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
                  </svg>
                </div>
                <h3 class="ml-3 text-lg font-medium text-gray-900">Study Sessions</h3>
              </div>
              <p class="text-sm text-gray-600 mb-4">
                Track your study time with a built-in timer. Build consistency with study streaks and session history.
              </p>
              <ul class="text-xs text-gray-500 space-y-1 mb-4">
                <li>• Built-in study timer</li>
                <li>• Track study streaks</li>
                <li>• Session history</li>
                <li>• Link sessions to materials</li>
              </ul>
              <router-link
                to="/study-sessions"
                class="inline-flex items-center text-sm font-medium text-indigo-600 hover:text-indigo-500"
              >
                Start Session →
              </router-link>
            </div>
          </div>

          <!-- Notes & Ratings Feature -->
          <div class="bg-white shadow rounded-lg overflow-hidden hover:shadow-lg transition-shadow">
            <div class="p-6">
              <div class="flex items-center mb-3">
                <div class="flex-shrink-0">
                  <svg class="h-8 w-8 text-indigo-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z" />
                  </svg>
                </div>
                <h3 class="ml-3 text-lg font-medium text-gray-900">Notes & Ratings</h3>
              </div>
              <p class="text-sm text-gray-600 mb-4">
                Take notes on materials and rate them. Keep your thoughts organized and share feedback.
              </p>
              <ul class="text-xs text-gray-500 space-y-1 mb-4">
                <li>• Take notes on materials</li>
                <li>• Rate materials (1-5 stars)</li>
                <li>• Add comments</li>
                <li>• Edit and delete notes</li>
              </ul>
              <router-link
                to="/materials"
                class="inline-flex items-center text-sm font-medium text-indigo-600 hover:text-indigo-500"
              >
                View Materials →
              </router-link>
            </div>
          </div>
        </div>
      </div>

      <!-- Recent Activity -->
      <div class="grid grid-cols-1 gap-6 lg:grid-cols-2">
        <!-- Recent Bookmarks -->
        <div class="bg-white shadow rounded-lg">
          <div class="px-6 py-4 border-b border-gray-200 flex items-center justify-between">
            <h2 class="text-lg font-medium text-gray-900">Recent Bookmarks</h2>
            <router-link
              to="/bookmarks"
              class="text-sm text-indigo-600 hover:text-indigo-500"
            >
              View all →
            </router-link>
          </div>
          <div class="px-6 py-4">
            <div v-if="stats.recent_bookmarks.length === 0" class="text-center py-4 text-gray-500">
              No bookmarks yet
            </div>
            <ul v-else class="divide-y divide-gray-200">
              <li v-for="bookmark in stats.recent_bookmarks" :key="bookmark.id" class="py-3">
                <router-link
                  :to="`/materials/${bookmark.material.id}`"
                  class="block hover:bg-gray-50 -mx-3 px-3 py-2 rounded-md"
                >
                  <div class="flex items-center justify-between">
                    <div class="flex-1 min-w-0">
                      <p class="text-sm font-medium text-gray-900 truncate">
                        {{ bookmark.material.title }}
                      </p>
                      <p v-if="bookmark.material.category" class="text-sm text-gray-500">
                        {{ bookmark.material.category }}
                      </p>
                    </div>
                  </div>
                </router-link>
              </li>
            </ul>
          </div>
        </div>

        <!-- Recent Progress -->
        <div class="bg-white shadow rounded-lg">
          <div class="px-6 py-4 border-b border-gray-200">
            <h2 class="text-lg font-medium text-gray-900">Recent Progress</h2>
          </div>
          <div class="px-6 py-4">
            <div v-if="stats.recent_progress.length === 0" class="text-center py-4 text-gray-500">
              No progress yet
            </div>
            <ul v-else class="divide-y divide-gray-200">
              <li v-for="progress in stats.recent_progress" :key="progress.id" class="py-3">
                <router-link
                  :to="`/materials/${progress.material.id}`"
                  class="block hover:bg-gray-50 -mx-3 px-3 py-2 rounded-md"
                >
                  <div class="flex items-center justify-between">
                    <div class="flex-1 min-w-0">
                      <p class="text-sm font-medium text-gray-900 truncate">
                        {{ progress.material.title }}
                      </p>
                      <div class="mt-1 flex items-center">
                        <div class="flex-1 bg-gray-200 rounded-full h-2 mr-2">
                          <div
                            class="bg-indigo-600 h-2 rounded-full"
                            :style="{ width: `${progress.progress_percentage}%` }"
                          ></div>
                        </div>
                        <span class="text-xs text-gray-500">{{ Math.round(progress.progress_percentage) }}%</span>
                      </div>
                    </div>
                    <span
                      class="ml-2 inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium"
                      :class="{
                        'bg-green-100 text-green-800': progress.status === 'completed',
                        'bg-blue-100 text-blue-800': progress.status === 'in_progress',
                        'bg-gray-100 text-gray-800': progress.status === 'not_started'
                      }"
                    >
                      {{ progress.status.replace('_', ' ') }}
                    </span>
                  </div>
                </router-link>
              </li>
            </ul>
          </div>
        </div>
      </div>

      <!-- Recommendations Section -->
      <div class="mt-8 bg-white shadow rounded-lg">
        <div class="px-6 py-4 border-b border-gray-200 flex items-center justify-between">
          <h2 class="text-lg font-medium text-gray-900">Recommended Materials</h2>
          <router-link
            to="/materials"
            class="text-sm text-indigo-600 hover:text-indigo-500"
          >
            View all →
          </router-link>
        </div>
        <div class="px-6 py-4">
          <div v-if="recommendationsLoading" class="text-center py-4">
            <div class="inline-block animate-spin rounded-full h-6 w-6 border-b-2 border-indigo-600"></div>
          </div>
          <div v-else-if="recommendations.length === 0" class="text-center py-4 text-gray-500">
            No recommendations available
          </div>
          <div v-else class="grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-3">
            <router-link
              v-for="rec in recommendations"
              :key="rec.id"
              :to="`/materials/${rec.id}`"
              class="block p-4 border border-gray-200 rounded-lg hover:border-indigo-500 hover:shadow-md transition-all"
            >
              <h3 class="text-sm font-medium text-gray-900 mb-1">{{ rec.title }}</h3>
              <div class="flex items-center justify-between mt-2">
                <span v-if="rec.category" class="text-xs text-gray-500">{{ rec.category }}</span>
                <span class="text-xs px-2 py-1 rounded bg-indigo-100 text-indigo-800">
                  {{ rec.reason === 'bookmarked' ? 'Bookmarked' : rec.reason === 'in_progress' ? 'In Progress' : 'New' }}
                </span>
              </div>
            </router-link>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'

const stats = ref<any>({
  total_materials: 0,
  total_bookmarks: 0,
  completed_materials: 0,
  in_progress_materials: 0,
  recent_bookmarks: [],
  recent_progress: []
})
const streak = ref<any>({
  current_streak: 0,
  longest_streak: 0,
  last_study_date: null
})
const recommendations = ref<any[]>([])
const recommendationsLoading = ref(false)
const loading = ref(true)
const error = ref('')

const loadStats = async () => {
  loading.value = true
  try {
    const [statsResponse, streakResponse] = await Promise.all([
      fetch('/api/dashboard/stats', { credentials: 'include' }),
      fetch('/api/streak', { credentials: 'include' })
    ])
    
    if (statsResponse.ok) {
      stats.value = await statsResponse.json()
    } else {
      error.value = 'Failed to load dashboard stats'
    }
    
    if (streakResponse.ok) {
      streak.value = await streakResponse.json()
    }
  } catch (e) {
    error.value = 'An error occurred'
  } finally {
    loading.value = false
  }
}

const loadRecommendations = async () => {
  recommendationsLoading.value = true
  try {
    const response = await fetch('/api/materials/recommendations', {
      credentials: 'include'
    })
    if (response.ok) {
      recommendations.value = await response.json()
    }
  } catch (e) {
    // Ignore errors
  } finally {
    recommendationsLoading.value = false
  }
}

onMounted(() => {
  loadStats()
  loadRecommendations()
})
</script>
