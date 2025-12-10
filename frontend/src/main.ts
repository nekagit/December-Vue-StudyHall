import { createApp } from 'vue'
import { createRouter, createWebHistory } from 'vue-router'
import './style.scss'
import App from './App.vue'

// Import components
import Login from './views/Login.vue'
import Register from './views/Register.vue'
import Home from './views/Home.vue'
import Materials from './views/Materials.vue'
import MaterialDetail from './views/MaterialDetail.vue'
import Compiler from './views/Compiler.vue'

const routes = [
  { path: '/', component: Home },
  { path: '/login', component: Login },
  { path: '/register', component: Register },
  { path: '/materials', component: Materials, meta: { requiresAuth: true } },
  { path: '/materials/:id', component: MaterialDetail, meta: { requiresAuth: true } },
  { path: '/compiler', component: Compiler, meta: { requiresAuth: true } },
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
