<template>
  <div class="px-4 py-4 sm:py-6 sm:px-0">
    <div class="mb-6 sm:mb-8">
      <h1 class="text-2xl sm:text-3xl font-bold text-msit-dark-50 mb-2 font-serif">Settings</h1>
      <p class="text-sm sm:text-base text-msit-dark-200 font-sans">Customize your StudyHall experience</p>
    </div>

    <!-- Theme Selection -->
    <div class="mb-8">
      <div class="bg-msit-dark-800 border border-msit-dark-700 rounded-lg p-6">
        <h2 class="text-xl font-semibold text-msit-dark-50 mb-4 font-sans">Color Theme</h2>
        <p class="text-sm text-msit-dark-200 mb-6 font-sans">
          Choose a color theme that matches your style. Changes are applied immediately.
        </p>

        <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
          <button
            v-for="theme in themes"
            :key="theme.id"
            @click="selectTheme(theme.id)"
            :class="[
              'relative p-4 rounded-lg border-2 transition-all text-left',
              currentThemeId === theme.id
                ? 'border-msit-accent bg-msit-dark-700'
                : 'border-msit-dark-600 bg-msit-dark-900 hover:border-msit-dark-500'
            ]"
          >
            <!-- Theme Preview -->
            <div class="mb-3 h-20 rounded-md overflow-hidden flex">
              <div
                class="flex-1"
                :style="{ backgroundColor: theme.colors.dark }"
              ></div>
              <div
                class="flex-1"
                :style="{ backgroundColor: theme.colors.dark800 }"
              ></div>
              <div
                class="flex-1"
                :style="{ backgroundColor: theme.colors.accent }"
              ></div>
            </div>

            <!-- Theme Info -->
            <h3 class="text-base font-semibold text-msit-dark-50 mb-1 font-sans">
              {{ theme.name }}
            </h3>
            <p class="text-xs text-msit-dark-300 mb-3 font-sans">
              {{ theme.description }}
            </p>

            <!-- Selected Indicator -->
            <div
              v-if="currentThemeId === theme.id"
              class="absolute top-2 right-2 w-6 h-6 rounded-full bg-msit-accent flex items-center justify-center"
            >
              <svg
                class="w-4 h-4 text-msit-dark"
                fill="none"
                stroke="currentColor"
                viewBox="0 0 24 24"
              >
                <path
                  stroke-linecap="round"
                  stroke-linejoin="round"
                  stroke-width="2"
                  d="M5 13l4 4L19 7"
                />
              </svg>
            </div>

            <!-- Color Swatches -->
            <div class="flex gap-1 mt-2">
              <div
                v-for="(color, index) in [
                  theme.colors.dark,
                  theme.colors.dark800,
                  theme.colors.accent
                ]"
                :key="index"
                class="w-4 h-4 rounded-full border border-msit-dark-600"
                :style="{ backgroundColor: color }"
              ></div>
            </div>
          </button>
        </div>
      </div>
    </div>

    <!-- Additional Settings Section -->
    <div class="bg-msit-dark-800 border border-msit-dark-700 rounded-lg p-6">
      <h2 class="text-xl font-semibold text-msit-dark-50 mb-4 font-sans">Preferences</h2>
      <p class="text-sm text-msit-dark-200 font-sans">
        More customization options coming soon!
      </p>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { themes, getCurrentTheme, saveTheme, getThemeById, applyTheme } from '../utils/theme'

const currentThemeId = ref<string>('msit-green')

onMounted(() => {
  currentThemeId.value = getCurrentTheme()
})

const selectTheme = (themeId: string) => {
  const theme = getThemeById(themeId)
  if (!theme) return

  currentThemeId.value = themeId
  saveTheme(themeId)
  applyTheme(theme)
}
</script>
