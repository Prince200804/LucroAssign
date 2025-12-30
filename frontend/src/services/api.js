import axios from 'axios'

// Get API URL from environment or use localhost as fallback
const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api'

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
  // Only use credentials for same-origin requests
  withCredentials: API_BASE_URL.includes('localhost'),
  timeout: 15000, // 15 second timeout for slower connections
})

// Request interceptor to add auth token
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('access_token')
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }
    return config
  },
  (error) => Promise.reject(error)
)

// Response interceptor to handle token refresh
api.interceptors.response.use(
  (response) => response,
  async (error) => {
    // Handle network errors gracefully
    if (!error.response) {
      console.error('Network error:', error.message)
      return Promise.reject({ 
        response: { 
          data: { error: 'Network error. Please check your connection.' } 
        } 
      })
    }
    
    const originalRequest = error.config

    if (error.response?.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true

      try {
        const refreshToken = localStorage.getItem('refresh_token')
        if (refreshToken) {
          const response = await axios.post('http://localhost:8000/api/users/token/refresh/', {
            refresh: refreshToken,
          }, { timeout: 5000 })

          const { access } = response.data
          localStorage.setItem('access_token', access)

          originalRequest.headers.Authorization = `Bearer ${access}`
          return api(originalRequest)
        }
      } catch (refreshError) {
        // Refresh failed, clear tokens
        localStorage.removeItem('access_token')
        localStorage.removeItem('refresh_token')
        // Don't redirect automatically - let the app handle it
      }
    }

    return Promise.reject(error)
  }
)

export default api
