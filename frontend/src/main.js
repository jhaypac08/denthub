import { createApp } from 'vue'
import { createPinia } from 'pinia'
import App from './App.vue'
import router from './router'
import { useAuthStore } from './stores/auth'
import api from './services/api'

// AdminLTE CSS
import 'admin-lte/dist/css/adminlte.min.css'
import 'admin-lte/plugins/fontawesome-free/css/all.min.css'

// Custom Theme CSS
import './assets/custom-theme.css'

// AdminLTE JS
import 'admin-lte/dist/js/adminlte.min.js'

const app = createApp(App)
const pinia = createPinia()

app.use(pinia)
app.use(router)

// Initialize CSRF token and check for persisted session on app startup
const authStore = useAuthStore()

async function initApp() {
  // Get CSRF token first
  try {
    await api.get('/csrf/')
  } catch (error) {
    console.error('Failed to get CSRF token:', error)
  }
  
  // Only check auth if we have a remembered session
  const rememberSession = localStorage.getItem('rememberSession')
  if (rememberSession === 'true') {
    await authStore.checkAuth()
  }
  
  app.mount('#app')
}

initApp()
