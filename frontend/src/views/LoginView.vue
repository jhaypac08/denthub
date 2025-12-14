<template>
  <div class="login-page" style="background: linear-gradient(135deg, #A9E1E9 0%, #E6FFFF 100%);">
    <div class="login-box">
      <div class="login-logo">
        <b style="color: #00B2A9;">Dent</b><span style="color: #007B7F;">Hub</span>
      </div>
      <div class="card" style="border-top: 3px solid #00B2A9; box-shadow: 0 4px 12px rgba(0, 178, 169, 0.2);">
        <div class="card-body login-card-body">
          <p class="login-box-msg">Sign in to start your session</p>

          <form @submit.prevent="handleLogin">
            <div v-if="errorMessage" class="alert alert-danger">
              {{ errorMessage }}
            </div>
            
            <div class="input-group mb-3">
              <input 
                v-model="username" 
                type="text" 
                class="form-control" 
                placeholder="Username"
                required
                style="border-color: #00B2A9;"
              >
              <div class="input-group-append">
                <div class="input-group-text" style="background-color: #00B2A9; border-color: #00B2A9; color: white;">
                  <span class="fas fa-user"></span>
                </div>
              </div>
            </div>
            
            <div class="input-group mb-3">
              <input 
                v-model="password" 
                type="password" 
                class="form-control" 
                placeholder="Password"
                required
                style="border-color: #00B2A9;"
              >
              <div class="input-group-append">
                <div class="input-group-text" style="background-color: #00B2A9; border-color: #00B2A9; color: white;">
                  <span class="fas fa-lock"></span>
                </div>
              </div>
            </div>
            
            <div class="row mb-3">
              <div class="col-12">
                <div class="icheck-primary">
                  <input type="checkbox" id="remember" v-model="rememberMe" style="accent-color: #00B2A9;">
                  <label for="remember" style="color: #2F404A;">
                    Remember Me
                  </label>
                </div>
              </div>
            </div>
            
            <div class="row">
              <div class="col-12">
                <button type="submit" class="btn btn-block" :disabled="loading" style="background-color: #00B2A9; border-color: #00B2A9; color: white; font-weight: 500; transition: all 0.3s ease;" @mouseover="$event.target.style.backgroundColor='#007B7F'" @mouseout="$event.target.style.backgroundColor='#00B2A9'">
                  <span v-if="loading">
                    <i class="fas fa-spinner fa-spin"></i> Logging in...
                  </span>
                  <span v-else>Sign In</span>
                </button>
              </div>
            </div>
          </form>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../stores/auth'
import api from '../services/api'

const router = useRouter()
const authStore = useAuthStore()

const username = ref('')
const password = ref('')
const rememberMe = ref(false)
const errorMessage = ref('')
const loading = ref(false)

// Fetch CSRF token on mount
onMounted(async () => {
  // Fetch CSRF token
  try {
    await api.get('/csrf/')
  } catch (error) {
    console.error('Error fetching CSRF token:', error)
  }
  
  // Load saved credentials if remember me was checked
  const savedUsername = localStorage.getItem('rememberedUsername')
  const savedPassword = localStorage.getItem('rememberedPassword')
  
  if (savedUsername && savedPassword) {
    username.value = savedUsername
    password.value = savedPassword
    rememberMe.value = true
  }
})

const handleLogin = async () => {
  errorMessage.value = ''
  loading.value = true
  
  const result = await authStore.login(username.value, password.value, rememberMe.value)
  
  loading.value = false
  
  if (result.success) {
    // Save credentials for auto-fill if remember me is checked
    if (rememberMe.value) {
      localStorage.setItem('rememberedUsername', username.value)
      localStorage.setItem('rememberedPassword', password.value)
    } else {
      localStorage.removeItem('rememberedUsername')
      localStorage.removeItem('rememberedPassword')
    }
    
    // Redirect based on user role
    const isPatient = authStore.user?.group_names?.includes('patient')
    if (isPatient) {
      router.push('/patient-profile')
    } else {
      router.push('/')
    }
  } else {
    errorMessage.value = result.error
  }
}
</script>

<style scoped>
.login-page {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}
</style>
