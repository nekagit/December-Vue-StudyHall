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
            <div class="hidden md:ml-6 md:flex md:space-x-4 lg:space-x-8">
              <router-link
                to="/"
                class="border-transparent inline-flex items-center px-1 pt-1 border-b-2 text-sm font-medium transition-colors"
                style="color: #E0EADD; font-family: 'Inter', sans-serif;"
                active-class="border-msit-accent"
                :style="$route.path === '/' ? 'border-color: #83E65B; color: #83E65B;' : ''"
                @mouseover="$event.target.style.color='#83E65B'"
                @mouseleave="$route.path === '/' ? $event.target.style.color='#83E65B' : $event.target.style.color='#E0EADD'"
              >
                Home
              </router-link>
              <router-link
                to="/dashboard"
                class="border-transparent inline-flex items-center px-1 pt-1 border-b-2 text-sm font-medium transition-colors"
                style="color: #E0EADD; font-family: 'Inter', sans-serif;"
                :style="$route.path === '/dashboard' ? 'border-color: #83E65B; color: #83E65B;' : ''"
                @mouseover="$event.target.style.color='#83E65B'"
                @mouseleave="$route.path === '/dashboard' ? $event.target.style.color='#83E65B' : $event.target.style.color='#E0EADD'"
              >
                Dashboard
              </router-link>
              <router-link
                to="/materials"
                class="border-transparent inline-flex items-center px-1 pt-1 border-b-2 text-sm font-medium transition-colors"
                style="color: #E0EADD; font-family: 'Inter', sans-serif;"
                :style="$route.path.startsWith('/materials') ? 'border-color: #83E65B; color: #83E65B;' : ''"
                @mouseover="$event.target.style.color='#83E65B'"
                @mouseleave="$route.path.startsWith('/materials') ? $event.target.style.color='#83E65B' : $event.target.style.color='#E0EADD'"
              >
                Materials
              </router-link>
              <router-link
                to="/compiler"
                class="border-transparent inline-flex items-center px-1 pt-1 border-b-2 text-sm font-medium transition-colors"
                style="color: #E0EADD; font-family: 'Inter', sans-serif;"
                :style="$route.path === '/compiler' ? 'border-color: #83E65B; color: #83E65B;' : ''"
                @mouseover="$event.target.style.color='#83E65B'"
                @mouseleave="$route.path === '/compiler' ? $event.target.style.color='#83E65B' : $event.target.style.color='#E0EADD'"
              >
                Compiler
              </router-link>
              <router-link
                to="/snippets"
                class="border-transparent inline-flex items-center px-1 pt-1 border-b-2 text-sm font-medium transition-colors"
                style="color: #E0EADD; font-family: 'Inter', sans-serif;"
                :style="$route.path === '/snippets' ? 'border-color: #83E65B; color: #83E65B;' : ''"
                @mouseover="$event.target.style.color='#83E65B'"
                @mouseleave="$route.path === '/snippets' ? $event.target.style.color='#83E65B' : $event.target.style.color='#E0EADD'"
              >
                Snippets
              </router-link>
              <router-link
                to="/export"
                class="border-transparent inline-flex items-center px-1 pt-1 border-b-2 text-sm font-medium transition-colors"
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
            to="/dashboard"
            @click="mobileMenuOpen = false"
            class="block px-3 py-2 rounded-md text-base font-medium transition-colors"
            style="color: #E0EADD; font-family: 'Inter', sans-serif;"
            :style="$route.path === '/dashboard' ? 'background-color: rgba(131, 230, 91, 0.1); color: #83E65B;' : ''"
            :class="$route.path === '/dashboard' ? 'text-msit-accent' : 'text-msit-dark-50 hover:bg-msit-dark-800 hover:text-msit-accent'"
          >
            Dashboard
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
            to="/export"
            @click="mobileMenuOpen = false"
            class="block px-3 py-2 rounded-md text-base font-medium transition-colors"
            style="color: #E0EADD; font-family: 'Inter', sans-serif;"
            :style="$route.path === '/export' ? 'background-color: rgba(131, 230, 91, 0.1); color: #83E65B;' : ''"
            :class="$route.path === '/export' ? 'text-msit-accent' : 'text-msit-dark-50 hover:bg-msit-dark-800 hover:text-msit-accent'"
          >
            Export
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
