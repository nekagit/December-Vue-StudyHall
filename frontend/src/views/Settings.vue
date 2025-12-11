<template>
  <div class="px-4 py-4 sm:py-6 sm:px-0">
    <div class="mb-6 sm:mb-8">
      <h1 class="text-2xl sm:text-3xl font-bold text-msit-dark-50 mb-2 font-serif">Settings</h1>
      <p class="text-sm sm:text-base text-msit-dark-200 font-sans">Customize your StudyHall experience</p>
    </div>

    <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
      <!-- Left Column: Theme Selection -->
      <div class="lg:col-span-2">
        <!-- Theme Selection -->
        <div class="bg-msit-dark-800 border border-msit-dark-700 rounded-lg p-6 mb-6">
          <div class="flex items-center justify-between mb-4">
            <div>
              <h2 class="text-xl font-semibold text-msit-dark-50 mb-1 font-sans">Color Theme</h2>
              <p class="text-sm text-msit-dark-200 font-sans">
                Choose a color theme that matches your style. Changes are applied immediately.
              </p>
            </div>
            <div class="hidden sm:flex items-center gap-2 px-3 py-1.5 rounded-lg bg-msit-dark-900 border border-msit-dark-700">
              <div class="w-3 h-3 rounded-full" :style="{ backgroundColor: currentTheme?.colors.accent }"></div>
              <span class="text-sm text-msit-dark-200 font-sans">{{ currentTheme?.name }}</span>
            </div>
          </div>

          <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
            <button
              v-for="theme in themes"
              :key="theme.id"
              @click="selectTheme(theme.id)"
              :class="[
                'relative p-4 rounded-lg border-2 transition-all text-left group',
                currentThemeId === theme.id
                  ? 'border-msit-accent bg-msit-dark-700 shadow-lg shadow-msit-accent/20'
                  : 'border-msit-dark-600 bg-msit-dark-900 hover:border-msit-dark-500 hover:bg-msit-dark-800'
              ]"
            >
              <!-- Theme Preview -->
              <div class="mb-3 h-24 rounded-md overflow-hidden flex shadow-inner">
                <div
                  class="flex-1 transition-transform group-hover:scale-105"
                  :style="{ backgroundColor: theme.colors.dark }"
                ></div>
                <div
                  class="flex-1 transition-transform group-hover:scale-105"
                  :style="{ backgroundColor: theme.colors.dark800 }"
                ></div>
                <div
                  class="flex-1 transition-transform group-hover:scale-105"
                  :style="{ backgroundColor: theme.colors.accent }"
                ></div>
              </div>

              <!-- Theme Info -->
              <div class="flex items-start justify-between">
                <div class="flex-1">
                  <h3 class="text-base font-semibold text-msit-dark-50 mb-1 font-sans">
                    {{ theme.name }}
                  </h3>
                  <p class="text-xs text-msit-dark-300 mb-3 font-sans line-clamp-2">
                    {{ theme.description }}
                  </p>
                </div>
              </div>

              <!-- Selected Indicator -->
              <div
                v-if="currentThemeId === theme.id"
                class="absolute top-3 right-3 w-7 h-7 rounded-full bg-msit-accent flex items-center justify-center shadow-lg animate-pulse"
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
                    stroke-width="2.5"
                    d="M5 13l4 4L19 7"
                  />
                </svg>
              </div>

              <!-- Color Swatches -->
              <div class="flex gap-1.5 mt-3">
                <div
                  v-for="(color, index) in [
                    theme.colors.dark,
                    theme.colors.dark800,
                    theme.colors.accent
                  ]"
                  :key="index"
                  class="w-5 h-5 rounded-full border-2 border-msit-dark-600 shadow-sm"
                  :style="{ backgroundColor: color }"
                  :title="color"
                ></div>
              </div>
            </button>
          </div>
        </div>

        <!-- Design Preferences -->
        <div class="bg-msit-dark-800 border border-msit-dark-700 rounded-lg p-6">
          <h2 class="text-xl font-semibold text-msit-dark-50 mb-4 font-sans">Design Preferences</h2>
          
          <!-- Font Size -->
          <div class="mb-6">
            <label class="block text-sm font-medium text-msit-dark-200 mb-2 font-sans">
              Font Size
            </label>
            <div class="flex items-center gap-4">
              <input
                type="range"
                v-model="fontSize"
                min="14"
                max="18"
                step="1"
                class="flex-1 h-2 bg-msit-dark-700 rounded-lg appearance-none cursor-pointer accent-msit-accent"
                @input="updateFontSize"
              />
              <span class="text-sm text-msit-dark-300 font-sans min-w-[3rem] text-right">
                {{ fontSize }}px
              </span>
            </div>
          </div>

          <!-- Border Radius -->
          <div class="mb-6">
            <label class="block text-sm font-medium text-msit-dark-200 mb-2 font-sans">
              Border Radius
            </label>
            <div class="flex items-center gap-4">
              <input
                type="range"
                v-model="borderRadius"
                min="0"
                max="16"
                step="2"
                class="flex-1 h-2 bg-msit-dark-700 rounded-lg appearance-none cursor-pointer accent-msit-accent"
                @input="updateBorderRadius"
              />
              <span class="text-sm text-msit-dark-300 font-sans min-w-[3rem] text-right">
                {{ borderRadius }}px
              </span>
            </div>
          </div>

          <!-- Reset Button -->
          <button
            @click="resetPreferences"
            class="px-4 py-2 rounded-lg bg-msit-dark-700 border border-msit-dark-600 text-msit-dark-200 hover:bg-msit-dark-600 hover:text-msit-dark-50 transition-colors font-sans text-sm"
          >
            Reset to Defaults
          </button>
        </div>
      </div>

      <!-- Right Column: Live Preview -->
      <div class="lg:col-span-1">
        <div class="bg-msit-dark-800 border border-msit-dark-700 rounded-lg p-6 sticky top-6">
          <h2 class="text-xl font-semibold text-msit-dark-50 mb-4 font-sans">Live Preview</h2>
          
          <div class="space-y-4">
            <!-- Preview Card -->
            <div 
              class="p-4 rounded-lg border transition-all"
              :style="{
                backgroundColor: currentTheme?.colors.dark800,
                borderColor: currentTheme?.colors.dark700,
                borderRadius: `${borderRadius}px`
              }"
            >
              <div class="flex items-center gap-3 mb-3">
                <div 
                  class="w-10 h-10 rounded-full flex items-center justify-center font-bold"
                  :style="{
                    backgroundColor: currentTheme?.colors.accent,
                    color: currentTheme?.colors.dark,
                    fontSize: `${fontSize}px`
                  }"
                >
                  S
                </div>
                <div>
                  <div 
                    class="font-semibold mb-1"
                    :style="{
                      color: currentTheme?.colors.dark50,
                      fontSize: `${fontSize}px`
                    }"
                  >
                    StudyHall
                  </div>
                  <div 
                    class="text-xs"
                    :style="{
                      color: currentTheme?.colors.dark300,
                      fontSize: `${fontSize - 2}px`
                    }"
                  >
                    Learning Platform
                  </div>
                </div>
              </div>
              
              <div 
                class="text-sm mb-3"
                :style="{
                  color: currentTheme?.colors.dark200,
                  fontSize: `${fontSize - 1}px`
                }"
              >
                This is a preview of how your theme looks with the current settings.
              </div>
              
              <button
                class="w-full py-2 rounded-lg font-medium transition-colors"
                :style="{
                  backgroundColor: currentTheme?.colors.accent,
                  color: currentTheme?.colors.dark,
                  borderRadius: `${borderRadius}px`
                }"
              >
                Example Button
              </button>
            </div>

            <!-- Color Palette -->
            <div>
              <h3 class="text-sm font-medium text-msit-dark-200 mb-3 font-sans">Color Palette</h3>
              <div class="space-y-2">
                <div class="flex items-center gap-2">
                  <div 
                    class="w-8 h-8 rounded border border-msit-dark-600"
                    :style="{ backgroundColor: currentTheme?.colors.dark }"
                  ></div>
                  <div class="flex-1">
                    <div class="text-xs text-msit-dark-300 font-sans">Background</div>
                    <div class="text-xs text-msit-dark-400 font-mono">{{ currentTheme?.colors.dark }}</div>
                  </div>
                </div>
                <div class="flex items-center gap-2">
                  <div 
                    class="w-8 h-8 rounded border border-msit-dark-600"
                    :style="{ backgroundColor: currentTheme?.colors.dark800 }"
                  ></div>
                  <div class="flex-1">
                    <div class="text-xs text-msit-dark-300 font-sans">Card</div>
                    <div class="text-xs text-msit-dark-400 font-mono">{{ currentTheme?.colors.dark800 }}</div>
                  </div>
                </div>
                <div class="flex items-center gap-2">
                  <div 
                    class="w-8 h-8 rounded border border-msit-dark-600"
                    :style="{ backgroundColor: currentTheme?.colors.accent }"
                  ></div>
                  <div class="flex-1">
                    <div class="text-xs text-msit-dark-300 font-sans">Accent</div>
                    <div class="text-xs text-msit-dark-400 font-mono">{{ currentTheme?.colors.accent }}</div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'
import { themes, getCurrentTheme, saveTheme, getThemeById, applyTheme } from '../utils/theme'

const currentThemeId = ref<string>('msit-green')
const fontSize = ref<number>(16)
const borderRadius = ref<number>(8)

const currentTheme = computed(() => {
  return getThemeById(currentThemeId.value)
})

onMounted(() => {
  currentThemeId.value = getCurrentTheme()
  
  // Load saved preferences
  const savedFontSize = localStorage.getItem('fontSize')
  const savedBorderRadius = localStorage.getItem('borderRadius')
  
  if (savedFontSize) {
    fontSize.value = parseInt(savedFontSize)
    updateFontSize()
  }
  
  if (savedBorderRadius) {
    borderRadius.value = parseInt(savedBorderRadius)
    updateBorderRadius()
  }
})

const selectTheme = (themeId: string) => {
  const theme = getThemeById(themeId)
  if (!theme) return

  currentThemeId.value = themeId
  saveTheme(themeId)
  applyTheme(theme)
}

const updateFontSize = () => {
  document.documentElement.style.setProperty('--base-font-size', `${fontSize.value}px`)
  localStorage.setItem('fontSize', fontSize.value.toString())
}

const updateBorderRadius = () => {
  document.documentElement.style.setProperty('--base-border-radius', `${borderRadius.value}px`)
  localStorage.setItem('borderRadius', borderRadius.value.toString())
}

const resetPreferences = () => {
  fontSize.value = 16
  borderRadius.value = 8
  updateFontSize()
  updateBorderRadius()
}
</script>

<<<<<<< HEAD
<style scoped>
input[type="range"] {
  -webkit-appearance: none;
  appearance: none;
}

input[type="range"]::-webkit-slider-thumb {
  -webkit-appearance: none;
  appearance: none;
  width: 18px;
  height: 18px;
  border-radius: 50%;
  background: var(--msit-accent);
  cursor: pointer;
  border: 2px solid var(--msit-dark);
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
}

input[type="range"]::-moz-range-thumb {
  width: 18px;
  height: 18px;
  border-radius: 50%;
  background: var(--msit-accent);
  cursor: pointer;
  border: 2px solid var(--msit-dark);
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
}

.line-clamp-2 {
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}
</style>
=======
>>>>>>> df4caa5f5de63697a7bd9f2f6108875a189ed0fc
