<template>
  <div class="min-h-screen bg-msit-dark text-msit-dark-50">
    <nav class="bg-msit-dark border-b border-msit-dark-700">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="flex justify-between h-16">
          <div class="flex items-center">
            <div class="flex-shrink-0">
              <router-link to="/" class="text-xl font-bold text-msit-accent">StudyHall</router-link>
            </div>
            <!-- Desktop Navigation -->
            <div class="hidden lg:ml-6 lg:flex lg:space-x-2 xl:space-x-4">
              <router-link
                to="/"
                class="border-transparent inline-flex items-center px-1 pt-1 border-b-2 text-xs xl:text-sm font-medium transition-colors"
                style="color: #E0EADD; font-family: 'Inter', sans-serif;"
                active-class="border-msit-accent"
                :style="$route.path === '/' ? 'border-color: #83E65B; color: #83E65B;' : ''"
                @mouseover="$event.target.style.color='#83E65B'"
                @mouseleave="$route.path === '/' ? $event.target.style.color='#83E65B' : $event.target.style.color='#E0EADD'"
              >
                Home
              </router-link>
              <router-link
                to="/search"
                class="border-transparent inline-flex items-center px-1 pt-1 border-b-2 text-xs xl:text-sm font-medium transition-colors"
                style="color: #E0EADD; font-family: 'Inter', sans-serif;"
                :style="$route.path === '/search' ? 'border-color: #83E65B; color: #83E65B;' : ''"
                @mouseover="$event.target.style.color='#83E65B'"
                @mouseleave="$route.path === '/search' ? $event.target.style.color='#83E65B' : $event.target.style.color='#E0EADD'"
              >
                Search
              </router-link>
              <router-link
                to="/materials"
                class="border-transparent inline-flex items-center px-1 pt-1 border-b-2 text-xs xl:text-sm font-medium transition-colors"
                style="color: #E0EADD; font-family: 'Inter', sans-serif;"
                :style="$route.path.startsWith('/materials') ? 'border-color: #83E65B; color: #83E65B;' : ''"
                @mouseover="$event.target.style.color='#83E65B'"
                @mouseleave="$route.path.startsWith('/materials') ? $event.target.style.color='#83E65B' : $event.target.style.color='#E0EADD'"
              >
                Materials
              </router-link>
              <router-link
                to="/practice-problems"
                class="border-transparent inline-flex items-center px-1 pt-1 border-b-2 text-xs xl:text-sm font-medium transition-colors"
                style="color: #E0EADD; font-family: 'Inter', sans-serif;"
                :style="$route.path === '/practice-problems' ? 'border-color: #83E65B; color: #83E65B;' : ''"
                @mouseover="$event.target.style.color='#83E65B'"
                @mouseleave="$route.path === '/practice-problems' ? $event.target.style.color='#83E65B' : $event.target.style.color='#E0EADD'"
              >
                Practice
              </router-link>
              <router-link
                to="/compiler"
                class="border-transparent inline-flex items-center px-1 pt-1 border-b-2 text-xs xl:text-sm font-medium transition-colors"
                style="color: #E0EADD; font-family: 'Inter', sans-serif;"
                :style="$route.path === '/compiler' ? 'border-color: #83E65B; color: #83E65B;' : ''"
                @mouseover="$event.target.style.color='#83E65B'"
                @mouseleave="$route.path === '/compiler' ? $event.target.style.color='#83E65B' : $event.target.style.color='#E0EADD'"
              >
                Compiler
              </router-link>
              <router-link
                to="/snippets"
                class="border-transparent inline-flex items-center px-1 pt-1 border-b-2 text-xs xl:text-sm font-medium transition-colors"
                style="color: #E0EADD; font-family: 'Inter', sans-serif;"
                :style="$route.path === '/snippets' ? 'border-color: #83E65B; color: #83E65B;' : ''"
                @mouseover="$event.target.style.color='#83E65B'"
                @mouseleave="$route.path === '/snippets' ? $event.target.style.color='#83E65B' : $event.target.style.color='#E0EADD'"
              >
                Snippets
              </router-link>
              <router-link
                to="/learning-path"
                class="border-transparent inline-flex items-center px-1 pt-1 border-b-2 text-xs xl:text-sm font-medium transition-colors"
                style="color: #E0EADD; font-family: 'Inter', sans-serif;"
                :style="$route.path === '/learning-path' ? 'border-color: #83E65B; color: #83E65B;' : ''"
                @mouseover="$event.target.style.color='#83E65B'"
                @mouseleave="$route.path === '/learning-path' ? $event.target.style.color='#83E65B' : $event.target.style.color='#E0EADD'"
              >
                Learning Path
              </router-link>
              <router-link
                to="/challenges"
                class="border-transparent inline-flex items-center px-1 pt-1 border-b-2 text-xs xl:text-sm font-medium transition-colors"
                style="color: #E0EADD; font-family: 'Inter', sans-serif;"
                :style="$route.path === '/challenges' ? 'border-color: #83E65B; color: #83E65B;' : ''"
                @mouseover="$event.target.style.color='#83E65B'"
                @mouseleave="$route.path === '/challenges' ? $event.target.style.color='#83E65B' : $event.target.style.color='#E0EADD'"
              >
                Challenges
              </router-link>
              <router-link
                to="/library"
                class="border-transparent inline-flex items-center px-1 pt-1 border-b-2 text-xs xl:text-sm font-medium transition-colors"
                style="color: #E0EADD; font-family: 'Inter', sans-serif;"
                :style="$route.path === '/library' ? 'border-color: #83E65B; color: #83E65B;' : ''"
                @mouseover="$event.target.style.color='#83E65B'"
                @mouseleave="$route.path === '/library' ? $event.target.style.color='#83E65B' : $event.target.style.color='#E0EADD'"
              >
                Library
              </router-link>
              <router-link
                to="/resources"
                class="border-transparent inline-flex items-center px-1 pt-1 border-b-2 text-xs xl:text-sm font-medium transition-colors"
                style="color: #E0EADD; font-family: 'Inter', sans-serif;"
                :style="$route.path === '/resources' ? 'border-color: #83E65B; color: #83E65B;' : ''"
                @mouseover="$event.target.style.color='#83E65B'"
                @mouseleave="$route.path === '/resources' ? $event.target.style.color='#83E65B' : $event.target.style.color='#E0EADD'"
              >
                Resources
              </router-link>
              <router-link
                to="/tools"
                class="border-transparent inline-flex items-center px-1 pt-1 border-b-2 text-xs xl:text-sm font-medium transition-colors"
                style="color: #E0EADD; font-family: 'Inter', sans-serif;"
                :style="$route.path === '/tools' ? 'border-color: #83E65B; color: #83E65B;' : ''"
                @mouseover="$event.target.style.color='#83E65B'"
                @mouseleave="$route.path === '/tools' ? $event.target.style.color='#83E65B' : $event.target.style.color='#E0EADD'"
              >
                Tools
              </router-link>
              <router-link
                to="/export"
                class="border-transparent inline-flex items-center px-1 pt-1 border-b-2 text-xs xl:text-sm font-medium transition-colors"
                style="color: #E0EADD; font-family: 'Inter', sans-serif;"
                :style="$route.path === '/export' ? 'border-color: #83E65B; color: #83E65B;' : ''"
                @mouseover="$event.target.style.color='#83E65B'"
                @mouseleave="$route.path === '/export' ? $event.target.style.color='#83E65B' : $event.target.style.color='#E0EADD'"
              >
                Export
              </router-link>
            </div>
          </div>
          <!-- Mobile menu button -->
          <div class="md:hidden flex items-center">
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
      <div v-if="mobileMenuOpen" class="md:hidden border-t border-msit-dark-700">
        <div class="px-2 pt-2 pb-3 space-y-1">
          <router-link
            to="/"
            @click="mobileMenuOpen = false"
            class="block px-3 py-2 rounded-md text-base font-medium transition-colors"
            style="color: #E0EADD; font-family: 'Inter', sans-serif;"
            :style="$route.path === '/' ? 'background-color: rgba(131, 230, 91, 0.1); color: #83E65B;' : ''"
            :class="$route.path === '/' ? 'text-msit-accent' : 'text-msit-dark-50 hover:bg-msit-dark-800 hover:text-msit-accent'"
          >
            Home
          </router-link>
          <router-link
            to="/materials"
            @click="mobileMenuOpen = false"
            class="block px-3 py-2 rounded-md text-base font-medium transition-colors"
            style="color: #E0EADD; font-family: 'Inter', sans-serif;"
            :style="$route.path.startsWith('/materials') ? 'background-color: rgba(131, 230, 91, 0.1); color: #83E65B;' : ''"
            :class="$route.path.startsWith('/materials') ? 'text-msit-accent' : 'text-msit-dark-50 hover:bg-msit-dark-800 hover:text-msit-accent'"
          >
            Materials
          </router-link>
          <router-link
            to="/compiler"
            @click="mobileMenuOpen = false"
            class="block px-3 py-2 rounded-md text-base font-medium transition-colors"
            style="color: #E0EADD; font-family: 'Inter', sans-serif;"
            :style="$route.path === '/compiler' ? 'background-color: rgba(131, 230, 91, 0.1); color: #83E65B;' : ''"
            :class="$route.path === '/compiler' ? 'text-msit-accent' : 'text-msit-dark-50 hover:bg-msit-dark-800 hover:text-msit-accent'"
          >
            Compiler
          </router-link>
          <router-link
            to="/snippets"
            @click="mobileMenuOpen = false"
            class="block px-3 py-2 rounded-md text-base font-medium transition-colors"
            style="color: #E0EADD; font-family: 'Inter', sans-serif;"
            :style="$route.path === '/snippets' ? 'background-color: rgba(131, 230, 91, 0.1); color: #83E65B;' : ''"
            :class="$route.path === '/snippets' ? 'text-msit-accent' : 'text-msit-dark-50 hover:bg-msit-dark-800 hover:text-msit-accent'"
          >
            Snippets
          </router-link>
          <router-link
            to="/search"
            @click="mobileMenuOpen = false"
            class="block px-3 py-2 rounded-md text-base font-medium transition-colors"
            style="color: #E0EADD; font-family: 'Inter', sans-serif;"
            :style="$route.path === '/search' ? 'background-color: rgba(131, 230, 91, 0.1); color: #83E65B;' : ''"
            :class="$route.path === '/search' ? 'text-msit-accent' : 'text-msit-dark-50 hover:bg-msit-dark-800 hover:text-msit-accent'"
          >
            Search
          </router-link>
          <router-link
            to="/practice"
            @click="mobileMenuOpen = false"
            class="block px-3 py-2 rounded-md text-base font-medium transition-colors"
            style="color: #E0EADD; font-family: 'Inter', sans-serif;"
            :style="$route.path === '/practice' ? 'background-color: rgba(131, 230, 91, 0.1); color: #83E65B;' : ''"
            :class="$route.path === '/practice' ? 'text-msit-accent' : 'text-msit-dark-50 hover:bg-msit-dark-800 hover:text-msit-accent'"
          >
            Practice
          </router-link>
          <router-link
            to="/templates"
            @click="mobileMenuOpen = false"
            class="block px-3 py-2 rounded-md text-base font-medium transition-colors"
            style="color: #E0EADD; font-family: 'Inter', sans-serif;"
            :style="$route.path === '/templates' ? 'background-color: rgba(131, 230, 91, 0.1); color: #83E65B;' : ''"
            :class="$route.path === '/templates' ? 'text-msit-accent' : 'text-msit-dark-50 hover:bg-msit-dark-800 hover:text-msit-accent'"
          >
            Templates
          </router-link>
          <router-link
            to="/cheat-sheets"
            @click="mobileMenuOpen = false"
            class="block px-3 py-2 rounded-md text-base font-medium transition-colors"
            style="color: #E0EADD; font-family: 'Inter', sans-serif;"
            :style="$route.path === '/cheat-sheets' ? 'background-color: rgba(131, 230, 91, 0.1); color: #83E65B;' : ''"
            :class="$route.path === '/cheat-sheets' ? 'text-msit-accent' : 'text-msit-dark-50 hover:bg-msit-dark-800 hover:text-msit-accent'"
          >
            Cheat Sheets
          </router-link>
          <router-link
            to="/resources"
            @click="mobileMenuOpen = false"
            class="block px-3 py-2 rounded-md text-base font-medium transition-colors"
            style="color: #E0EADD; font-family: 'Inter', sans-serif;"
            :style="$route.path === '/resources' ? 'background-color: rgba(131, 230, 91, 0.1); color: #83E65B;' : ''"
            :class="$route.path === '/resources' ? 'text-msit-accent' : 'text-msit-dark-50 hover:bg-msit-dark-800 hover:text-msit-accent'"
          >
            Resources
          </router-link>
          <router-link
            to="/practice"
            @click="mobileMenuOpen = false"
            class="block px-3 py-2 rounded-md text-base font-medium transition-colors"
            style="color: #E0EADD; font-family: 'Inter', sans-serif;"
            :style="$route.path === '/practice' ? 'background-color: rgba(131, 230, 91, 0.1); color: #83E65B;' : ''"
            :class="$route.path === '/practice' ? 'text-msit-accent' : 'text-msit-dark-50 hover:bg-msit-dark-800 hover:text-msit-accent'"
          >
            Practice
          </router-link>
          <router-link
            to="/challenges"
            @click="mobileMenuOpen = false"
            class="block px-3 py-2 rounded-md text-base font-medium transition-colors"
            style="color: #E0EADD; font-family: 'Inter', sans-serif;"
            :style="$route.path === '/challenges' ? 'background-color: rgba(131, 230, 91, 0.1); color: #83E65B;' : ''"
            :class="$route.path === '/challenges' ? 'text-msit-accent' : 'text-msit-dark-50 hover:bg-msit-dark-800 hover:text-msit-accent'"
          >
            Challenges
          </router-link>
          <router-link
            to="/library"
            @click="mobileMenuOpen = false"
            class="block px-3 py-2 rounded-md text-base font-medium transition-colors"
            style="color: #E0EADD; font-family: 'Inter', sans-serif;"
            :style="$route.path === '/library' ? 'background-color: rgba(131, 230, 91, 0.1); color: #83E65B;' : ''"
            :class="$route.path === '/library' ? 'text-msit-accent' : 'text-msit-dark-50 hover:bg-msit-dark-800 hover:text-msit-accent'"
          >
            Library
          </router-link>
          <router-link
            to="/resources"
            @click="mobileMenuOpen = false"
            class="block px-3 py-2 rounded-md text-base font-medium transition-colors"
            style="color: #E0EADD; font-family: 'Inter', sans-serif;"
            :style="$route.path === '/resources' ? 'background-color: rgba(131, 230, 91, 0.1); color: #83E65B;' : ''"
            :class="$route.path === '/resources' ? 'text-msit-accent' : 'text-msit-dark-50 hover:bg-msit-dark-800 hover:text-msit-accent'"
          >
            Resources
          </router-link>
          <router-link
            to="/tools"
            @click="mobileMenuOpen = false"
            class="block px-3 py-2 rounded-md text-base font-medium transition-colors"
            style="color: #E0EADD; font-family: 'Inter', sans-serif;"
            :style="$route.path === '/tools' ? 'background-color: rgba(131, 230, 91, 0.1); color: #83E65B;' : ''"
            :class="$route.path === '/tools' ? 'text-msit-accent' : 'text-msit-dark-50 hover:bg-msit-dark-800 hover:text-msit-accent'"
          >
            Tools
          </router-link>
          <router-link
            to="/search"
            @click="mobileMenuOpen = false"
            class="block px-3 py-2 rounded-md text-base font-medium transition-colors"
            style="color: #E0EADD; font-family: 'Inter', sans-serif;"
            :style="$route.path === '/search' ? 'background-color: rgba(131, 230, 91, 0.1); color: #83E65B;' : ''"
            :class="$route.path === '/search' ? 'text-msit-accent' : 'text-msit-dark-50 hover:bg-msit-dark-800 hover:text-msit-accent'"
          >
            Search
          </router-link>
          <router-link
            to="/export"
            @click="mobileMenuOpen = false"
            class="block px-3 py-2 rounded-md text-base font-medium transition-colors"
            style="color: #E0EADD; font-family: 'Inter', sans-serif;"
            :style="$route.path === '/export' ? 'background-color: rgba(131, 230, 91, 0.1); color: #83E65B;' : ''"
            :class="$route.path === '/export' ? 'text-msit-accent' : 'text-msit-dark-50 hover:bg-msit-dark-800 hover:text-msit-accent'"
          >
            Export
          </router-link>
          <router-link
            to="/help"
            @click="mobileMenuOpen = false"
            class="block px-3 py-2 rounded-md text-base font-medium transition-colors"
            style="color: #E0EADD; font-family: 'Inter', sans-serif;"
            :style="$route.path === '/help' ? 'background-color: rgba(131, 230, 91, 0.1); color: #83E65B;' : ''"
            :class="$route.path === '/help' ? 'text-msit-accent' : 'text-msit-dark-50 hover:bg-msit-dark-800 hover:text-msit-accent'"
          >
            Help
          </router-link>
        </div>
      </div>
    </nav>

    <main class="max-w-7xl mx-auto py-4 sm:py-6 px-4 sm:px-6 lg:px-8">
      <router-view />
    </main>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'

const mobileMenuOpen = ref(false)
</script>
