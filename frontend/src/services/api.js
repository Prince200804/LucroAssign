import axios from 'axios'

const api = axios.create({
  baseURL: 'http://localhost:8000/api',
  headers: {
    'Content-Type': 'application/json',
  },
  withCredentials: true,
  timeout: 10000, // 10 second timeout
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
