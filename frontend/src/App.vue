<template>
  <div class="min-h-screen bg-msit-dark text-msit-dark-50">
    <nav class="bg-msit-dark border-b border-msit-dark-700 relative z-50">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="flex justify-between h-16">
          <div class="flex items-center">
            <div class="shrink-0">
              <router-link to="/" class="text-xl font-bold text-msit-accent">StudyHall</router-link>
            </div>
            <!-- Desktop Navigation -->
            <div class="hidden lg:ml-8 lg:flex lg:items-center lg:space-x-1">
              <!-- Home -->
              <router-link
                to="/"
                class="nav-item"
                :class="{ 'nav-item-active': $route.path === '/' }"
              >
                Home
              </router-link>

              <!-- Learn Dropdown -->
              <div
                class="nav-dropdown-container"
                @mouseenter="openDropdown('learn')"
                @mouseleave="closeDropdown('learn')"
              >
                <button
                  class="nav-item"
                  :class="{ 'nav-item-active': isLearnActive }"
                >
                  Learn
                  <svg class="nav-arrow" :class="{ 'nav-arrow-open': openDropdowns.learn }" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7" />
                  </svg>
                </button>
                <transition name="dropdown">
                  <div v-if="openDropdowns.learn" class="nav-dropdown">
                    <router-link to="/materials" class="nav-dropdown-item" @click="closeDropdown('learn')">
                      <span class="font-medium">Materials</span>
                      <span class="text-xs text-msit-dark-300">Study materials and content</span>
                    </router-link>
                    <router-link to="/learning-path" class="nav-dropdown-item" @click="closeDropdown('learn')">
                      <span class="font-medium">Learning Path</span>
                      <span class="text-xs text-msit-dark-300">Structured learning journey</span>
                    </router-link>
                    <router-link to="/library" class="nav-dropdown-item" @click="closeDropdown('learn')">
                      <span class="font-medium">Library</span>
                      <span class="text-xs text-msit-dark-300">Resource collection</span>
                    </router-link>
                    <router-link to="/resources" class="nav-dropdown-item" @click="closeDropdown('learn')">
                      <span class="font-medium">Resources</span>
                      <span class="text-xs text-msit-dark-300">Additional learning resources</span>
                    </router-link>
                    <router-link to="/tutor" class="nav-dropdown-item" @click="closeDropdown('learn')">
                      <span class="font-medium">AI Tutor</span>
                      <span class="text-xs text-msit-dark-300">Get personalized tutoring</span>
                    </router-link>
                  </div>
                </transition>
              </div>

              <!-- Practice Dropdown -->
              <div
                class="nav-dropdown-container"
                @mouseenter="openDropdown('practice')"
                @mouseleave="closeDropdown('practice')"
              >
                <button
                  class="nav-item"
                  :class="{ 'nav-item-active': isPracticeActive }"
                >
                  Practice
                  <svg class="nav-arrow" :class="{ 'nav-arrow-open': openDropdowns.practice }" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7" />
                  </svg>
                </button>
                <transition name="dropdown">
                  <div v-if="openDropdowns.practice" class="nav-dropdown">
                    <router-link to="/practice-problems" class="nav-dropdown-item" @click="closeDropdown('practice')">
                      <span class="font-medium">Practice Problems</span>
                      <span class="text-xs text-msit-dark-300">Solve coding challenges</span>
                    </router-link>
                    <router-link to="/challenges" class="nav-dropdown-item" @click="closeDropdown('practice')">
                      <span class="font-medium">Challenges</span>
                      <span class="text-xs text-msit-dark-300">Test your skills</span>
                    </router-link>
                    <router-link to="/gym" class="nav-dropdown-item" @click="closeDropdown('practice')">
                      <span class="font-medium">Gym</span>
                      <span class="text-xs text-msit-dark-300">Practice exercises</span>
                    </router-link>
                    <router-link to="/typing-test" class="nav-dropdown-item" @click="closeDropdown('practice')">
                      <span class="font-medium">Typing Test</span>
                      <span class="text-xs text-msit-dark-300">Improve typing speed</span>
                    </router-link>
                    <router-link to="/mock-interview" class="nav-dropdown-item" @click="closeDropdown('practice')">
                      <span class="font-medium">Mock Interview</span>
                      <span class="text-xs text-msit-dark-300">Interview preparation</span>
                    </router-link>
                  </div>
                </transition>
              </div>

              <!-- Tools Dropdown -->
              <div
                class="nav-dropdown-container"
                @mouseenter="openDropdown('tools')"
                @mouseleave="closeDropdown('tools')"
              >
                <button
                  class="nav-item"
                  :class="{ 'nav-item-active': isToolsActive }"
                >
                  Tools
                  <svg class="nav-arrow" :class="{ 'nav-arrow-open': openDropdowns.tools }" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7" />
                  </svg>
                </button>
                <transition name="dropdown">
                  <div v-if="openDropdowns.tools" class="nav-dropdown">
                    <router-link to="/compiler" class="nav-dropdown-item" @click="closeDropdown('tools')">
                      <span class="font-medium">Compiler</span>
                      <span class="text-xs text-msit-dark-300">Run code online</span>
                    </router-link>
                    <router-link to="/snippets" class="nav-dropdown-item" @click="closeDropdown('tools')">
                      <span class="font-medium">Snippets</span>
                      <span class="text-xs text-msit-dark-300">Code snippets library</span>
                    </router-link>
                    <router-link to="/templates" class="nav-dropdown-item" @click="closeDropdown('tools')">
                      <span class="font-medium">Templates</span>
                      <span class="text-xs text-msit-dark-300">Code templates</span>
                    </router-link>
                    <router-link to="/editor" class="nav-dropdown-item" @click="closeDropdown('tools')">
                      <span class="font-medium">Code Editor</span>
                      <span class="text-xs text-msit-dark-300">VS Code-like editor</span>
                    </router-link>
                    <router-link to="/cheat-sheets" class="nav-dropdown-item" @click="closeDropdown('tools')">
                      <span class="font-medium">Cheat Sheets</span>
                      <span class="text-xs text-msit-dark-300">Quick reference guides</span>
                    </router-link>
                    <router-link to="/tools" class="nav-dropdown-item" @click="closeDropdown('tools')">
                      <span class="font-medium">All Tools</span>
                      <span class="text-xs text-msit-dark-300">Browse all tools</span>
                    </router-link>
                  </div>
                </transition>
              </div>

              <!-- Discover Dropdown -->
              <div
                class="nav-dropdown-container"
                @mouseenter="openDropdown('discover')"
                @mouseleave="closeDropdown('discover')"
              >
                <button
                  class="nav-item"
                  :class="{ 'nav-item-active': isDiscoverActive }"
                >
                  Discover
                  <svg class="nav-arrow" :class="{ 'nav-arrow-open': openDropdowns.discover }" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7" />
                  </svg>
                </button>
                <transition name="dropdown">
                  <div v-if="openDropdowns.discover" class="nav-dropdown">
                    <router-link to="/search" class="nav-dropdown-item" @click="closeDropdown('discover')">
                      <span class="font-medium">Search</span>
                      <span class="text-xs text-msit-dark-300">Find content quickly</span>
                    </router-link>
                    <router-link to="/export" class="nav-dropdown-item" @click="closeDropdown('discover')">
                      <span class="font-medium">Export</span>
                      <span class="text-xs text-msit-dark-300">Export your work</span>
                    </router-link>
                    <router-link to="/settings" class="nav-dropdown-item" @click="closeDropdown('discover')">
                      <span class="font-medium">Settings</span>
                      <span class="text-xs text-msit-dark-300">Customize your experience</span>
                    </router-link>
                  </div>
                </transition>
              </div>
            </div>
          </div>
          <!-- Mobile menu button -->
          <div class="lg:hidden flex items-center">
            <button
              @click="mobileMenuOpen = !mobileMenuOpen"
              class="inline-flex items-center justify-center p-2 rounded-md text-msit-dark-50 hover:text-msit-accent hover:bg-msit-dark-800 focus:outline-none focus:ring-2 focus:ring-inset focus:ring-msit-accent transition-colors"
              aria-expanded="false"
            >
              <span class="sr-only">Open main menu</span>
              <svg
                v-if="!mobileMenuOpen"
                class="block h-6 w-6"
                xmlns="http://www.w3.org/2000/svg"
                fill="none"
                viewBox="0 0 24 24"
                stroke="currentColor"
              >
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16" />
              </svg>
              <svg
                v-else
                class="block h-6 w-6"
                xmlns="http://www.w3.org/2000/svg"
                fill="none"
                viewBox="0 0 24 24"
                stroke="currentColor"
              >
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
              </svg>
            </button>
          </div>
        </div>
      </div>

      <!-- Mobile menu -->
      <transition name="mobile-menu">
        <div v-if="mobileMenuOpen" class="lg:hidden border-t border-msit-dark-700">
          <div class="px-2 pt-2 pb-3 space-y-1">
            <router-link
              to="/"
              @click="closeMobileMenu"
              class="mobile-nav-item"
              :class="{ 'mobile-nav-item-active': $route.path === '/' }"
            >
              Home
            </router-link>

            <!-- Mobile Learn Section -->
            <div class="mobile-nav-section">
              <button
                @click="toggleMobileSection('learn')"
                class="mobile-nav-section-header"
              >
                Learn
                <svg class="mobile-nav-arrow" :class="{ 'mobile-nav-arrow-open': mobileSections.learn }" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7" />
                </svg>
              </button>
              <transition name="mobile-section">
                <div v-if="mobileSections.learn" class="mobile-nav-section-content">
                  <router-link to="/materials" @click="closeMobileMenu" class="mobile-nav-subitem">Materials</router-link>
                  <router-link to="/learning-path" @click="closeMobileMenu" class="mobile-nav-subitem">Learning Path</router-link>
                  <router-link to="/library" @click="closeMobileMenu" class="mobile-nav-subitem">Library</router-link>
                  <router-link to="/resources" @click="closeMobileMenu" class="mobile-nav-subitem">Resources</router-link>
                  <router-link to="/tutor" @click="closeMobileMenu" class="mobile-nav-subitem">AI Tutor</router-link>
                </div>
              </transition>
            </div>

            <!-- Mobile Practice Section -->
            <div class="mobile-nav-section">
              <button
                @click="toggleMobileSection('practice')"
                class="mobile-nav-section-header"
              >
                Practice
                <svg class="mobile-nav-arrow" :class="{ 'mobile-nav-arrow-open': mobileSections.practice }" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7" />
                </svg>
              </button>
              <transition name="mobile-section">
                <div v-if="mobileSections.practice" class="mobile-nav-section-content">
                  <router-link to="/practice-problems" @click="closeMobileMenu" class="mobile-nav-subitem">Practice Problems</router-link>
                  <router-link to="/challenges" @click="closeMobileMenu" class="mobile-nav-subitem">Challenges</router-link>
                  <router-link to="/gym" @click="closeMobileMenu" class="mobile-nav-subitem">Gym</router-link>
                  <router-link to="/typing-test" @click="closeMobileMenu" class="mobile-nav-subitem">Typing Test</router-link>
                  <router-link to="/mock-interview" @click="closeMobileMenu" class="mobile-nav-subitem">Mock Interview</router-link>
                </div>
              </transition>
            </div>

            <!-- Mobile Tools Section -->
            <div class="mobile-nav-section">
              <button
                @click="toggleMobileSection('tools')"
                class="mobile-nav-section-header"
              >
                Tools
                <svg class="mobile-nav-arrow" :class="{ 'mobile-nav-arrow-open': mobileSections.tools }" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7" />
                </svg>
              </button>
              <transition name="mobile-section">
                <div v-if="mobileSections.tools" class="mobile-nav-section-content">
                  <router-link to="/compiler" @click="closeMobileMenu" class="mobile-nav-subitem">Compiler</router-link>
                  <router-link to="/snippets" @click="closeMobileMenu" class="mobile-nav-subitem">Snippets</router-link>
                  <router-link to="/templates" @click="closeMobileMenu" class="mobile-nav-subitem">Templates</router-link>
                  <router-link to="/editor" @click="closeMobileMenu" class="mobile-nav-subitem">Code Editor</router-link>
                  <router-link to="/cheat-sheets" @click="closeMobileMenu" class="mobile-nav-subitem">Cheat Sheets</router-link>
                  <router-link to="/tools" @click="closeMobileMenu" class="mobile-nav-subitem">All Tools</router-link>
                </div>
              </transition>
            </div>

            <!-- Mobile Discover Section -->
            <div class="mobile-nav-section">
              <button
                @click="toggleMobileSection('discover')"
                class="mobile-nav-section-header"
              >
                Discover
                <svg class="mobile-nav-arrow" :class="{ 'mobile-nav-arrow-open': mobileSections.discover }" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7" />
                </svg>
              </button>
              <transition name="mobile-section">
                <div v-if="mobileSections.discover" class="mobile-nav-section-content">
                  <router-link to="/search" @click="closeMobileMenu" class="mobile-nav-subitem">Search</router-link>
                  <router-link to="/export" @click="closeMobileMenu" class="mobile-nav-subitem">Export</router-link>
                  <router-link to="/settings" @click="closeMobileMenu" class="mobile-nav-subitem">Settings</router-link>
                </div>
              </transition>
            </div>

            <router-link
              to="/help"
              @click="closeMobileMenu"
              class="mobile-nav-item"
              :class="{ 'mobile-nav-item-active': $route.path === '/help' }"
            >
              Help
            </router-link>
          </div>
        </div>
      </transition>
    </nav>

    <main :class="route.path === '/editor' ? '' : 'max-w-7xl mx-auto py-4 sm:py-6 px-4 sm:px-6 lg:px-8'">
      <router-view />
    </main>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import { useRoute } from 'vue-router'

const route = useRoute()
const mobileMenuOpen = ref(false)
const openDropdowns = ref({
  learn: false,
  practice: false,
  tools: false,
  discover: false
})

const mobileSections = ref({
  learn: false,
  practice: false,
  tools: false,
  discover: false
})

const isLearnActive = computed(() => {
  return route.path.startsWith('/materials') ||
         route.path === '/learning-path' ||
         route.path === '/library' ||
         route.path === '/resources' ||
         route.path === '/tutor'
})

const isPracticeActive = computed(() => {
  return route.path === '/practice-problems' ||
         route.path === '/challenges' ||
         route.path === '/gym' ||
         route.path === '/typing-test' ||
         route.path === '/mock-interview'
})

const isToolsActive = computed(() => {
  return route.path === '/compiler' ||
         route.path === '/snippets' ||
         route.path === '/templates' ||
         route.path === '/editor' ||
         route.path === '/cheat-sheets' ||
         route.path === '/tools'
})

const isDiscoverActive = computed(() => {
  return route.path === '/search' ||
         route.path === '/export' ||
         route.path === '/settings'
})

function openDropdown(name: keyof typeof openDropdowns.value) {
  openDropdowns.value[name] = true
}

function closeDropdown(name: keyof typeof openDropdowns.value) {
  openDropdowns.value[name] = false
}

function toggleMobileSection(name: keyof typeof mobileSections.value) {
  mobileSections.value[name] = !mobileSections.value[name]
}

function closeMobileMenu() {
  mobileMenuOpen.value = false
  // Reset all mobile sections
  Object.keys(mobileSections.value).forEach(key => {
    mobileSections.value[key as keyof typeof mobileSections.value] = false
  })
}
</script>

<style scoped>
/* Navigation Item Styles */
.nav-item {
  position: relative;
  display: inline-flex;
  align-items: center;
  padding-left: 0.75rem;
  padding-right: 0.75rem;
  padding-top: 0.5rem;
  padding-bottom: 0.5rem;
  font-size: 0.875rem;
  font-weight: 500;
  transition-property: all;
  transition-duration: 200ms;
  color: #E0EADD;
  font-family: 'Inter', sans-serif;
}

.nav-item:hover {
  color: #83E65B;
}

.nav-item-active {
  color: #83E65B;
}

.nav-arrow {
  margin-left: 0.25rem;
  height: 0.75rem;
  width: 0.75rem;
  transition-property: transform;
  transition-duration: 200ms;
  transform: rotate(0deg);
}

.nav-arrow-open {
  transform: rotate(180deg);
}

/* Dropdown Container */
.nav-dropdown-container {
  position: relative;
}

/* Dropdown Menu */
.nav-dropdown {
  position: absolute;
  top: 100%;
  left: 0;
  margin-top: 0.5rem;
  width: 16rem;
  border-radius: 0.5rem;
  box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04);
  background-color: rgba(26, 49, 43, 0.98);
  backdrop-filter: blur(20px);
  border: 1px solid rgba(131, 230, 91, 0.1);
  padding: 0.5rem 0;
}

.nav-dropdown-item {
  display: block;
  padding-left: 1rem;
  padding-right: 1rem;
  padding-top: 0.75rem;
  padding-bottom: 0.75rem;
  transition-property: color, background-color;
  transition-duration: 150ms;
  color: #E0EADD;
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
}

.nav-dropdown-item:hover {
  background-color: rgba(131, 230, 91, 0.1);
  color: #83E65B;
}

.nav-dropdown-item.router-link-active {
  background-color: rgba(131, 230, 91, 0.15);
  color: #83E65B;
}

/* Dropdown Transitions */
.dropdown-enter-active,
.dropdown-leave-active {
  transition: all 0.2s ease-out;
}

.dropdown-enter-from {
  opacity: 0;
  transform: translateY(-10px);
}

.dropdown-leave-to {
  opacity: 0;
  transform: translateY(-10px);
}

/* Mobile Navigation */
.mobile-nav-item {
  display: block;
  padding-left: 0.75rem;
  padding-right: 0.75rem;
  padding-top: 0.5rem;
  padding-bottom: 0.5rem;
  border-radius: 0.375rem;
  font-size: 1rem;
  font-weight: 500;
  transition-property: color, background-color;
  color: #E0EADD;
  font-family: 'Inter', sans-serif;
}

.mobile-nav-item:hover {
  background-color: rgba(42, 63, 53, 0.5);
  color: #83E65B;
}

.mobile-nav-item-active {
  background-color: rgba(131, 230, 91, 0.1);
  color: #83E65B;
}

.mobile-nav-section {
  border-top-width: 1px;
  border-top-color: var(--msit-dark-700);
}

.mobile-nav-section-header {
  width: 100%;
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding-left: 0.75rem;
  padding-right: 0.75rem;
  padding-top: 0.5rem;
  padding-bottom: 0.5rem;
  font-size: 1rem;
  font-weight: 500;
  transition-property: color, background-color;
  color: #E0EADD;
  font-family: 'Inter', sans-serif;
}

.mobile-nav-section-header:hover {
  color: #83E65B;
}

.mobile-nav-section-content {
  padding-left: 1.5rem;
  padding-bottom: 0.5rem;
}

.mobile-nav-section-content > * + * {
  margin-top: 0.25rem;
}

.mobile-nav-subitem {
  display: block;
  padding-left: 0.75rem;
  padding-right: 0.75rem;
  padding-top: 0.5rem;
  padding-bottom: 0.5rem;
  border-radius: 0.375rem;
  font-size: 0.875rem;
  transition-property: color, background-color;
  color: #C2D5BC;
  font-family: 'Inter', sans-serif;
}

.mobile-nav-subitem:hover {
  background-color: rgba(42, 63, 53, 0.5);
  color: #83E65B;
}

.mobile-nav-subitem.router-link-active {
  color: #83E65B;
}

.mobile-nav-arrow {
  height: 1rem;
  width: 1rem;
  transition-property: transform;
  transition-duration: 200ms;
  transform: rotate(0deg);
}

.mobile-nav-arrow-open {
  transform: rotate(180deg);
}

.mobile-menu-enter-active,
.mobile-menu-leave-active {
  transition: all 0.3s ease;
}

.mobile-menu-enter-from,
.mobile-menu-leave-to {
  opacity: 0;
  max-height: 0;
}

.mobile-section-enter-active,
.mobile-section-leave-active {
  transition: all 0.2s ease;
}

.mobile-section-enter-from,
.mobile-section-leave-to {
  opacity: 0;
  max-height: 0;
  overflow: hidden;
}
</style>
