import { createApp } from 'vue'
import { createRouter, createWebHistory } from 'vue-router'
import './style.css'
import App from './App.vue'
import { hasCharacterConfig } from './utils/character'
import { initializeTheme } from './utils/theme'

// Import components
import Configuration from './views/Configuration.vue'
import Home from './views/Home.vue'
import Materials from './views/Materials.vue'
import MaterialDetail from './views/MaterialDetail.vue'
import Compiler from './views/Compiler.vue'
import Dashboard from './views/Dashboard.vue'
import Snippets from './views/Snippets.vue'
import Practice from './views/Practice.vue'
import PracticeProblems from './views/PracticeProblems.vue'
import Search from './views/Search.vue'
import Resources from './views/Resources.vue'
import Challenges from './views/Challenges.vue'
import Tools from './views/Tools.vue'
import Library from './views/Library.vue'
import Export from './views/Export.vue'
import LearningPath from './views/LearningPath.vue'
import TypingTest from './views/TypingTest.vue'
import Gym from './views/Gym.vue'
import MockInterview from './views/MockInterview.vue'
import TestCoverage from './views/TestCoverage.vue'
import CheatSheets from './views/CheatSheets.vue'
import Templates from './views/Templates.vue'
import Help from './views/Help.vue'
import Editor from './views/Editor.vue'
import Settings from './views/Settings.vue'
import Tutor from './views/Tutor.vue'

const routes = [
  { path: '/configuration', component: Configuration },
  { path: '/', component: Home },
  { path: '/dashboard', component: Dashboard },
  { path: '/search', component: Search },
  { path: '/materials', component: Materials },
  { path: '/materials/:id', component: MaterialDetail },
  { path: '/compiler', component: Compiler },
  { path: '/snippets', component: Snippets },
  { path: '/practice', component: Practice },
  { path: '/practice-problems', component: PracticeProblems },
  { path: '/challenges', component: Challenges },
  { path: '/library', component: Library },
  { path: '/resources', component: Resources },
  { path: '/tools', component: Tools },
  { path: '/export', component: Export },
  { path: '/learning-path', component: LearningPath },
  { path: '/typing-test', component: TypingTest },
  { path: '/gym', component: Gym },
  { path: '/mock-interview', component: MockInterview },
  { path: '/test-coverage', component: TestCoverage },
  { path: '/cheat-sheets', component: CheatSheets },
  { path: '/templates', component: Templates },
  { path: '/editor', component: Editor },
  { path: '/help', component: Help },
  { path: '/settings', component: Settings },
  { path: '/tutor', component: Tutor },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

// Configuration guard - redirect to configuration if character not set
router.beforeEach((to, _from, next) => {
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

// Initialize theme before mounting app
initializeTheme()

const app = createApp(App)
app.use(router)
app.mount('#app')
