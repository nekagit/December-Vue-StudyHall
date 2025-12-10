import { createApp } from 'vue'
import { createRouter, createWebHistory } from 'vue-router'
import './style.css'
import App from './App.vue'
import { hasCharacterConfig } from './utils/character'

// Import components
import Configuration from './views/Configuration.vue'
import Home from './views/Home.vue'
import Materials from './views/Materials.vue'
import MaterialDetail from './views/MaterialDetail.vue'
import Compiler from './views/Compiler.vue'
import Dashboard from './views/Dashboard.vue'
import Snippets from './views/Snippets.vue'

const routes = [
  { path: '/configuration', component: Configuration },
  { path: '/', component: Home },
  { path: '/dashboard', component: Dashboard },
  { path: '/materials', component: Materials },
  { path: '/materials/:id', component: MaterialDetail },
  { path: '/compiler', component: Compiler },
  { path: '/snippets', component: Snippets },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

// Configuration guard - redirect to configuration if character not set
router.beforeEach((to, from, next) => {
  // Allow access to root path and configuration page without character config
  if (to.path === '/' || to.path === '/configuration') {
    // If already configured and trying to access configuration, redirect to home
    if (to.path === '/configuration' && hasCharacterConfig()) {
      next('/')
      return
    }
    next()
    return
  }
  
  // For all other routes, require character config
  if (!hasCharacterConfig()) {
    next('/configuration')
    return
  }
  
  next()
})

const app = createApp(App)
app.use(router)
app.mount('#app')
