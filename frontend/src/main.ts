import { createApp } from 'vue'
import { createRouter, createWebHistory } from 'vue-router'
import './style.css'
import App from './App.vue'

// Import components
import Login from './views/Login.vue'
import Register from './views/Register.vue'
import Home from './views/Home.vue'
import Materials from './views/Materials.vue'
import MaterialDetail from './views/MaterialDetail.vue'
import Compiler from './views/Compiler.vue'
import Dashboard from './views/Dashboard.vue'
import Bookmarks from './views/Bookmarks.vue'
import Profile from './views/Profile.vue'
import StudySessions from './views/StudySessions.vue'
import Goals from './views/Goals.vue'
import Goals from './views/Goals.vue'
import StudySessions from './views/StudySessions.vue'

const routes = [
  { path: '/', component: Home },
  { path: '/login', component: Login },
  { path: '/register', component: Register },
  { path: '/dashboard', component: Dashboard, meta: { requiresAuth: true } },
  { path: '/materials', component: Materials, meta: { requiresAuth: true } },
  { path: '/materials/:id', component: MaterialDetail, meta: { requiresAuth: true } },
  { path: '/bookmarks', component: Bookmarks, meta: { requiresAuth: true } },
  { path: '/compiler', component: Compiler, meta: { requiresAuth: true } },
  { path: '/profile', component: Profile, meta: { requiresAuth: true } },
  { path: '/study-sessions', component: StudySessions, meta: { requiresAuth: true } },
  { path: '/goals', component: Goals, meta: { requiresAuth: true } },
  { path: '/goals', component: Goals, meta: { requiresAuth: true } },
  { path: '/study-sessions', component: StudySessions, meta: { requiresAuth: true } },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

// Auth guard
router.beforeEach((to, from, next) => {
  const token = document.cookie.split('; ').find(row => row.startsWith('session_token='))
  if (to.meta.requiresAuth && !token) {
    next('/login')
  } else {
    next()
  }
})

const app = createApp(App)
app.use(router)
app.mount('#app')
