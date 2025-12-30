import { defineStore } from 'pinia'
import api from '@/services/api'

export const useAuthStore = defineStore('auth', {
  state: () => ({
    user: null,
    isAdmin: false,
    initialized: false,
  }),

  getters: {
    isAuthenticated: (state) => !!state.user,
  },

  actions: {
    async initializeAuth() {
      const token = localStorage.getItem('access_token')
      if (token) {
        try {
          await this.fetchUser()
        } catch (error) {
          this.clearAuth()
        }
      }
      this.initialized = true
    },

    async login(email, password) {
      try {
        const response = await api.post('/users/login/', { email, password })
        const { user, tokens } = response.data

        localStorage.setItem('access_token', tokens.access)
        localStorage.setItem('refresh_token', tokens.refresh)

        this.user = user
        await this.checkAdmin()

        return { success: true }
      } catch (error) {
        return { 
          success: false, 
          error: error.response?.data?.error || 'Login failed' 
        }
      }
    },

    async register(userData) {
      try {
        const response = await api.post('/users/register/', userData)
        const { user, tokens } = response.data

        localStorage.setItem('access_token', tokens.access)
        localStorage.setItem('refresh_token', tokens.refresh)

        this.user = user
        await this.checkAdmin()

        return { success: true }
      } catch (error) {
        return { 
          success: false, 
          errors: error.response?.data || { general: 'Registration failed' } 
        }
      }
    },

    async logout() {
      try {
        const refreshToken = localStorage.getItem('refresh_token')
        await api.post('/users/logout/', { refresh: refreshToken })
      } catch (error) {
        console.error('Logout error:', error)
      } finally {
        this.clearAuth()
      }
    },

    async fetchUser() {
      const response = await api.get('/users/profile/')
      this.user = response.data
      await this.checkAdmin()
    },

    async checkAdmin() {
      try {
        const response = await api.get('/users/admin-check/')
        this.isAdmin = response.data.is_admin
      } catch (error) {
        this.isAdmin = false
      }
    },

    async updateProfile(userData) {
      try {
        const response = await api.patch('/users/profile/', userData)
        this.user = response.data
        return { success: true }
      } catch (error) {
        return { 
          success: false, 
          errors: error.response?.data || { general: 'Update failed' } 
        }
      }
    },

    async changePassword(passwordData) {
      try {
        await api.post('/users/change-password/', passwordData)
        return { success: true }
      } catch (error) {
        return { 
          success: false, 
          error: error.response?.data?.error || 'Password change failed' 
        }
      }
    },

    clearAuth() {
      this.user = null
      this.isAdmin = false
      localStorage.removeItem('access_token')
      localStorage.removeItem('refresh_token')
    },
  },
})
