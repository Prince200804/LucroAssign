import { defineStore } from 'pinia'
import api from '@/services/api'

export const useCartStore = defineStore('cart', {
  state: () => ({
    cart: null,
    loading: false,
  }),

  getters: {
    items: (state) => state.cart?.items || [],
    totalItems: (state) => state.cart?.total_items || 0,
    subtotal: (state) => state.cart?.subtotal || 0,
    total: (state) => state.cart?.total || 0,
  },

  actions: {
    async fetchCart() {
      try {
        this.loading = true
        const response = await api.get('/cart/')
        this.cart = response.data
      } catch (error) {
        console.error('Error fetching cart:', error)
      } finally {
        this.loading = false
      }
    },

    async addToCart(productId, quantity = 1) {
      try {
        this.loading = true
        const response = await api.post('/cart/add/', {
          product_id: productId,
          quantity,
        })
        this.cart = response.data
        return { success: true }
      } catch (error) {
        return { 
          success: false, 
          error: error.response?.data?.error || 'Failed to add to cart' 
        }
      } finally {
        this.loading = false
      }
    },

    async updateCartItem(itemId, quantity) {
      try {
        this.loading = true
        const response = await api.patch(`/cart/update/${itemId}/`, { quantity })
        this.cart = response.data
        return { success: true }
      } catch (error) {
        return { 
          success: false, 
          error: error.response?.data?.error || 'Failed to update item' 
        }
      } finally {
        this.loading = false
      }
    },

    async removeFromCart(itemId) {
      try {
        this.loading = true
        const response = await api.delete(`/cart/remove/${itemId}/`)
        this.cart = response.data
        return { success: true }
      } catch (error) {
        return { 
          success: false, 
          error: error.response?.data?.error || 'Failed to remove item' 
        }
      } finally {
        this.loading = false
      }
    },

    async clearCart() {
      try {
        this.loading = true
        const response = await api.delete('/cart/clear/')
        this.cart = response.data
        return { success: true }
      } catch (error) {
        return { 
          success: false, 
          error: error.response?.data?.error || 'Failed to clear cart' 
        }
      } finally {
        this.loading = false
      }
    },

    async mergeCart(sessionKey) {
      try {
        const response = await api.post('/cart/merge/', { session_key: sessionKey })
        this.cart = response.data
      } catch (error) {
        console.error('Error merging cart:', error)
      }
    },
  },
})
