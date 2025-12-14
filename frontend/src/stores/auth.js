import { defineStore } from 'pinia'
import api from '../services/api'

export const useAuthStore = defineStore('auth', {
  state: () => ({
    user: null,
    isAuthenticated: false
  }),
  
  getters: {
    isPatient: (state) => {
      return state.user?.group_names?.includes('patient') || false
    },
    isStaff: (state) => {
      return state.user?.is_staff || false
    },
    isAdmin: (state) => {
      return state.user?.group_names?.includes('admin') || false
    }
  },
  
  actions: {
    async login(username, password, rememberMe = false) {
      try {
        const response = await api.post('/login/', { username, password })
        this.user = response.data.user
        this.isAuthenticated = true
        
        // Persist session if remember me is checked
        if (rememberMe) {
          localStorage.setItem('rememberSession', 'true')
          localStorage.setItem('sessionUser', JSON.stringify(response.data.user))
        } else {
          localStorage.removeItem('rememberSession')
          localStorage.removeItem('sessionUser')
        }
        
        return { success: true }
      } catch (error) {
        return { 
          success: false, 
          error: error.response?.data?.error || 'Login failed' 
        }
      }
    },
    
    async logout() {
      try {
        await api.post('/logout/')
      } catch (error) {
        console.error('Logout error:', error)
      } finally {
        // Always clear state and localStorage, even if API call fails
        this.user = null
        this.isAuthenticated = false
        
        // Clear session persistence
        localStorage.removeItem('rememberSession')
        localStorage.removeItem('sessionUser')
        localStorage.removeItem('rememberedUsername')
        localStorage.removeItem('rememberedPassword')
      }
    },
    
    async checkAuth() {
      // Check if session should be remembered
      const rememberSession = localStorage.getItem('rememberSession')
      const savedUser = localStorage.getItem('sessionUser')
      
      if (rememberSession === 'true' && savedUser) {
        try {
          // Verify session is still valid with backend
          const response = await api.get('/current-user/', { _silentAuth: true })
          this.user = response.data
          this.isAuthenticated = true
          // Update saved user data
          localStorage.setItem('sessionUser', JSON.stringify(response.data))
        } catch (error) {
          // Session expired - try to re-authenticate using saved credentials
          const savedUsername = localStorage.getItem('rememberedUsername')
          const savedPassword = localStorage.getItem('rememberedPassword')
          
          if (savedUsername && savedPassword) {
            // Attempt automatic re-login
            const loginResult = await this.login(savedUsername, savedPassword, true)
            if (!loginResult.success) {
              // Auto-login failed, clear everything
              this.user = null
              this.isAuthenticated = false
              localStorage.removeItem('rememberSession')
              localStorage.removeItem('sessionUser')
            }
          } else {
            // No credentials to re-login, clear session
            this.user = null
            this.isAuthenticated = false
            localStorage.removeItem('rememberSession')
            localStorage.removeItem('sessionUser')
          }
        }
      } else {
        try {
          const response = await api.get('/current-user/', { _silentAuth: true })
          this.user = response.data
          this.isAuthenticated = true
        } catch (error) {
          // Silently fail - user is not authenticated
          this.user = null
          this.isAuthenticated = false
        }
      }
    }
  }
})
