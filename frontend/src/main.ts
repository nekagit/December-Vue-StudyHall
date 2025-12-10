import { createApp } from 'vue'
import { createRouter, createWebHistory } from 'vue-router'
import './style.css'
import App from './App.vue'

// Override global fetch to include character headers
const originalFetch = window.fetch
window.fetch = function(url: RequestInfo | URL, init?: RequestInit): Promise<Response> {
  const character = localStorage.getItem('character')
  if (character && typeof url === 'string' && url.startsWith('/api/')) {
    try {
      const char = JSON.parse(character)
      const headers = new Headers(init?.headers)
      headers.set('X-Character-Id', char.id || '')
      headers.set('X-Character-Name', char.name || '')
      headers.set('X-Character-Role', char.role || 'student')
      return originalFetch(url, {
        ...init,
        headers,
        credentials: 'include'
      })
    } catch (e) {
      // If character parsing fails, use original fetch
    }
  }
  return originalFetch(url, init)
}

// Import components
import Configuration from './views/Configuration.vue'
import Home from './views/Home.vue'
import Materials from './views/Materials.vue'
import MaterialDetail from './views/MaterialDetail.vue'
import Compiler from './views/Compiler.vue'
import Dashboard from './views/Dashboard.vue'
import Bookmarks from './views/Bookmarks.vue'
import Profile from './views/Profile.vue'
import Goals from './views/Goals.vue'
import StudySessions from './views/StudySessions.vue'
import Notes from './views/Notes.vue'
import Ratings from './views/Ratings.vue'

const routes = [
  { path: '/configuration', component: Configuration },
  { path: '/', component: Home },
  { path: '/dashboard', component: Dashboard },
  { path: '/materials', component: Materials },
  { path: '/materials/:id', component: MaterialDetail },
  { path: '/bookmarks', component: Bookmarks },
  { path: '/compiler', component: Compiler },
  { path: '/profile', component: Profile },
  { path: '/goals', component: Goals },
  { path: '/study-sessions', component: StudySessions },
  { path: '/notes', component: Notes },
  { path: '/ratings', component: Ratings },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

// Configuration guard - redirect to configuration if character not set
router.beforeEach((to, from, next) => {
  const character = localStorage.getItem('character')
  
  // Configuration guard
  if (to.path !== '/configuration' && !character) {
    next('/configuration')
    return
  }
  
  if (to.path === '/configuration' && character) {
    next('/')
    return
  }
  
  next()
})

const app = createApp(App)
app.use(router)
app.mount('#app')
