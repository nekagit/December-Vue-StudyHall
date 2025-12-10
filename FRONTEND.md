# Frontend Development Guide

Complete guide for frontend development in the StudyHall Platform.

## Overview

The frontend is built with Vue.js 3, TypeScript, and TailwindCSS. It's a Single Page Application (SPA) that communicates with the Flask backend via REST API.

## Technology Stack

- **Framework**: Vue.js 3 (Composition API)
- **Language**: TypeScript
- **Styling**: TailwindCSS 4
- **Build Tool**: Vite 7
- **Routing**: Vue Router 4
- **Python Execution**: Pyodide (browser-based)

## Project Structure

```
frontend/
├── src/
│   ├── main.ts              # Application entry point
│   ├── App.vue              # Root component
│   ├── style.scss           # TailwindCSS imports
│   ├── style.css            # Global styles
│   ├── views/               # Page components
│   │   ├── Home.vue
│   │   ├── Login.vue
│   │   ├── Register.vue
│   │   ├── Materials.vue
│   │   ├── MaterialDetail.vue
│   │   └── Compiler.vue
│   ├── components/          # Reusable components
│   │   ├── PythonRunner.vue
│   │   └── HelloWorld.vue
│   └── utils/               # Utility functions
│       └── mount.ts
├── public/                  # Static assets
├── index.html              # HTML entry point
├── vite.config.ts          # Vite configuration
├── package.json            # Dependencies
└── tsconfig.json           # TypeScript configuration
```

## Getting Started

### Installation

```bash
cd frontend
npm install
```

### Development Server

```bash
npm run dev
```

Access at: http://localhost:5173

### Production Build

```bash
npm run build
```

Output: `frontend/dist/`

### Preview Production Build

```bash
npm run preview
```

## Vue.js Patterns

### Composition API

All components use `<script setup>` syntax:

```vue
<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'

const count = ref(0)
const doubled = computed(() => count.value * 2)

onMounted(() => {
  console.log('Component mounted')
})
</script>
```

### Component Structure

```vue
<template>
  <!-- HTML template -->
  <div class="container mx-auto p-4">
    <h1>{{ title }}</h1>
  </div>
</template>

<script setup lang="ts">
// TypeScript logic
interface Props {
  title: string
}

const props = defineProps<Props>()
</script>

<style scoped>
/* Component-specific styles (if needed) */
</style>
```

## Routing

### Route Configuration

Routes are defined in `src/main.ts`:

```typescript
const routes = [
  { path: '/', component: Home },
  { path: '/login', component: Login },
  { path: '/materials', component: Materials, meta: { requiresAuth: true } },
]
```

### Navigation

```vue
<script setup lang="ts">
import { useRouter } from 'vue-router'

const router = useRouter()

function goToMaterials() {
  router.push('/materials')
}
</script>
```

### Route Guards

Authentication guard is in `src/main.ts`:

```typescript
router.beforeEach((to, from, next) => {
  const token = document.cookie.split('; ').find(row => row.startsWith('session_token='))
  if (to.meta.requiresAuth && !token) {
    next('/login')
  } else {
    next()
  }
})
```

## API Communication

### Making API Calls

```typescript
// GET request
async function fetchMaterials() {
  const response = await fetch('/api/materials', {
    credentials: 'include' // Important for cookies
  })
  
  if (!response.ok) {
    throw new Error('Failed to fetch materials')
  }
  
  return await response.json()
}

// POST request
async function createBookmark(materialId: number) {
  const response = await fetch('/api/bookmarks', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ material_id: materialId }),
    credentials: 'include'
  })
  
  return await response.json()
}
```

### Error Handling

```typescript
async function fetchData() {
  try {
    const response = await fetch('/api/materials', {
      credentials: 'include'
    })
    
    if (!response.ok) {
      if (response.status === 401) {
        // Redirect to login
        router.push('/login')
        return
      }
      throw new Error(`HTTP error! status: ${response.status}`)
    }
    
    const data = await response.json()
    return data
  } catch (error) {
    console.error('Error fetching data:', error)
    // Show error message to user
  }
}
```

## State Management

### Component State

Use `ref` for reactive values:

```typescript
import { ref } from 'vue'

const materials = ref<Material[]>([])
const loading = ref(false)
const error = ref<string | null>(null)
```

### Computed Properties

```typescript
import { computed } from 'vue'

const filteredMaterials = computed(() => {
  return materials.value.filter(m => m.category === selectedCategory.value)
})
```

### Watchers

```typescript
import { watch } from 'vue'

watch(searchTerm, (newValue) => {
  if (newValue.length > 2) {
    performSearch(newValue)
  }
})
```

## Styling with TailwindCSS

### Utility Classes

```vue
<template>
  <div class="container mx-auto p-4">
    <h1 class="text-2xl font-bold text-indigo-600 mb-4">
      Title
    </h1>
    <button class="px-4 py-2 bg-indigo-600 text-white rounded hover:bg-indigo-700">
      Click Me
    </button>
  </div>
</template>
```

### Responsive Design

```vue
<div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
  <!-- Responsive grid -->
</div>
```

### Common Patterns

**Card:**
```vue
<div class="bg-white rounded-lg shadow-md p-6">
  <!-- Card content -->
</div>
```

**Button:**
```vue
<button class="px-4 py-2 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700 transition-colors">
  Button
</button>
```

**Input:**
```vue
<input 
  type="text" 
  class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-transparent"
/>
```

## TypeScript

### Type Definitions

```typescript
interface Material {
  id: number
  title: string
  content: string
  category: string
  created_at: string
  is_bookmarked: boolean
}

interface Bookmark {
  id: number
  material_id: number
  material: Material
  created_at: string
}
```

### Component Props

```vue
<script setup lang="ts">
interface Props {
  title: string
  count?: number
  items: Material[]
}

const props = withDefaults(defineProps<Props>(), {
  count: 0
})
</script>
```

### Component Emits

```vue
<script setup lang="ts">
interface Emits {
  (e: 'update', value: string): void
  (e: 'delete', id: number): void
}

const emit = defineEmits<Emits>()

function handleClick() {
  emit('update', 'new value')
}
</script>
```

## Components

### Creating a New Component

**File**: `src/components/YourComponent.vue`

```vue
<template>
  <div class="your-component">
    <h2>{{ title }}</h2>
    <slot />
  </div>
</template>

<script setup lang="ts">
interface Props {
  title: string
}

defineProps<Props>()
</script>

<style scoped>
.your-component {
  /* Component styles */
}
</style>
```

**Usage:**
```vue
<YourComponent title="Hello">
  <p>Content</p>
</YourComponent>
```

### Creating a New View

**File**: `src/views/YourView.vue`

```vue
<template>
  <div class="container mx-auto p-4">
    <h1 class="text-2xl font-bold mb-4">Your View</h1>
    <!-- View content -->
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'

const data = ref(null)

onMounted(async () => {
  // Fetch data
})
</script>
```

Then add route in `src/main.ts`:
```typescript
import YourView from './views/YourView.vue'

const routes = [
  // ...
  { path: '/your-view', component: YourView },
]
```

## Forms

### Form Handling

```vue
<template>
  <form @submit.prevent="handleSubmit">
    <input 
      v-model="form.email" 
      type="email" 
      placeholder="Email"
      class="w-full px-4 py-2 border rounded"
    />
    <input 
      v-model="form.password" 
      type="password" 
      placeholder="Password"
      class="w-full px-4 py-2 border rounded"
    />
    <button 
      type="submit"
      :disabled="loading"
      class="px-4 py-2 bg-indigo-600 text-white rounded"
    >
      Submit
    </button>
  </form>
</template>

<script setup lang="ts">
import { ref } from 'vue'

const form = ref({
  email: '',
  password: ''
})

const loading = ref(false)

async function handleSubmit() {
  loading.value = true
  try {
    const response = await fetch('/api/auth/login', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(form.value),
      credentials: 'include'
    })
    
    if (response.ok) {
      // Success
    }
  } finally {
    loading.value = false
  }
}
</script>
```

## Loading States

```vue
<template>
  <div v-if="loading" class="flex justify-center items-center h-64">
    <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-indigo-600"></div>
  </div>
  
  <div v-else-if="error" class="text-red-600">
    {{ error }}
  </div>
  
  <div v-else>
    <!-- Content -->
  </div>
</template>
```

## Error Handling

```vue
<script setup lang="ts">
import { ref } from 'vue'

const error = ref<string | null>(null)

async function fetchData() {
  try {
    error.value = null
    const response = await fetch('/api/materials', {
      credentials: 'include'
    })
    
    if (!response.ok) {
      throw new Error('Failed to fetch')
    }
    
    return await response.json()
  } catch (err) {
    error.value = err instanceof Error ? err.message : 'Unknown error'
    throw err
  }
}
</script>
```

## Performance Optimization

### Lazy Loading Routes

```typescript
const routes = [
  {
    path: '/materials',
    component: () => import('./views/Materials.vue')
  }
]
```

### Computed Caching

```typescript
const expensiveComputation = computed(() => {
  // Only recomputes when dependencies change
  return heavyCalculation(data.value)
})
```

### v-memo for Lists

```vue
<div v-for="item in items" :key="item.id" v-memo="[item.id, item.title]">
  <!-- Expensive rendering -->
</div>
```

## Testing

### Component Testing (Future)

```typescript
import { mount } from '@vue/test-utils'
import YourComponent from './YourComponent.vue'

test('renders correctly', () => {
  const wrapper = mount(YourComponent, {
    props: { title: 'Test' }
  })
  expect(wrapper.text()).toContain('Test')
})
```

## Build Configuration

### Vite Config

See `vite.config.ts` for:
- Vue plugin configuration
- Proxy settings for API
- Build optimizations

### TypeScript Config

See `tsconfig.json` for:
- Compiler options
- Type checking rules
- Path aliases

## Common Patterns

### Modal/Dialog

```vue
<template>
  <div v-if="isOpen" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center">
    <div class="bg-white rounded-lg p-6 max-w-md w-full">
      <slot />
      <button @click="close" class="mt-4 px-4 py-2 bg-gray-200 rounded">
        Close
      </button>
    </div>
  </div>
</template>
```

### Search/Filter

```vue
<script setup lang="ts">
import { ref, computed } from 'vue'

const searchTerm = ref('')
const materials = ref<Material[]>([])

const filteredMaterials = computed(() => {
  if (!searchTerm.value) return materials.value
  
  return materials.value.filter(m => 
    m.title.toLowerCase().includes(searchTerm.value.toLowerCase())
  )
})
</script>
```

## Best Practices

1. **Use TypeScript**: Define types for all data
2. **Component Composition**: Break down complex components
3. **Reusability**: Create reusable components
4. **Error Handling**: Always handle errors gracefully
5. **Loading States**: Show loading indicators
6. **Accessibility**: Use semantic HTML and ARIA labels
7. **Performance**: Lazy load routes, optimize images
8. **Code Organization**: Keep components focused

## Resources

- [Vue.js Documentation](https://vuejs.org/)
- [Vue Router](https://router.vuejs.org/)
- [TailwindCSS Documentation](https://tailwindcss.com/)
- [TypeScript Handbook](https://www.typescriptlang.org/docs/)
- [Vite Guide](https://vitejs.dev/)
