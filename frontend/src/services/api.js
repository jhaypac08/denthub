import axios from 'axios'

// Use environment variable or default to localhost
const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://127.0.0.1:8000/api'

const api = axios.create({
  baseURL: API_BASE_URL,
  withCredentials: true,
  headers: {
    'Content-Type': 'application/json',
  }
})

// Add CSRF token to requests
api.interceptors.request.use(config => {
  const csrfToken = getCookie('csrftoken')
  if (csrfToken) {
    config.headers['X-CSRFToken'] = csrfToken
  }
  return config
})

// Handle authentication errors
api.interceptors.response.use(
  response => response,
  error => {
    // Don't log errors for silent auth checks
    const isSilentAuth = error.config?._silentAuth
    
    if (error.response?.status === 403 && error.response?.data?.detail?.includes('CSRF')) {
      console.error('CSRF token error - try refreshing the page')
    }
    if (error.response?.status === 401 && !isSilentAuth) {
      console.error('Authentication error - user may need to login again')
    }
    return Promise.reject(error)
  }
)

function getCookie(name) {
  let cookieValue = null
  if (document.cookie && document.cookie !== '') {
    const cookies = document.cookie.split(';')
    for (let i = 0; i < cookies.length; i++) {
      const cookie = cookies[i].trim()
      if (cookie.substring(0, name.length + 1) === (name + '=')) {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1))
        break
      }
    }
  }
  return cookieValue
}

export default api
