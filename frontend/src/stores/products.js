import { defineStore } from 'pinia'
import api from '@/services/api'

export const useProductStore = defineStore('products', {
  state: () => ({
    products: [],
    featuredProducts: [],
    categories: [],
    currentProduct: null,
    loading: false,
    pagination: {
      count: 0,
      next: null,
      previous: null,
      currentPage: 1,
    },
    filters: {
      category: null,
      search: '',
      ordering: '-created_at',
    },
  }),

  actions: {
    async fetchProducts(params = {}) {
      try {
        this.loading = true
        const queryParams = {
          ...params,
        }
        
        // Only add store filters if not explicitly provided in params
        if (!params.category && this.filters.category) {
          queryParams.category = this.filters.category
        }
        if (!params.search && this.filters.search) {
          queryParams.search = this.filters.search
        }
        if (!params.ordering && this.filters.ordering) {
          queryParams.ordering = this.filters.ordering
        }
        
        // Remove null/undefined/empty values
        Object.keys(queryParams).forEach(key => {
          if (queryParams[key] === null || queryParams[key] === undefined || queryParams[key] === '') {
            delete queryParams[key]
          }
        })

        const response = await api.get('/products/', { params: queryParams })
        this.products = response.data.results || response.data
        this.pagination = {
          count: response.data.count,
          next: response.data.next,
          previous: response.data.previous,
          currentPage: params.page || 1,
        }
      } catch (error) {
        console.error('Error fetching products:', error)
      } finally {
        this.loading = false
      }
    },

    async fetchFeaturedProducts() {
      try {
        const response = await api.get('/products/featured/')
        this.featuredProducts = response.data
      } catch (error) {
        console.error('Error fetching featured products:', error)
      }
    },

    async fetchCategories() {
      try {
        const response = await api.get('/products/categories/')
        this.categories = response.data
      } catch (error) {
        console.error('Error fetching categories:', error)
      }
    },

    async fetchProductBySlug(slug) {
      try {
        this.loading = true
        const response = await api.get(`/products/${slug}/`)
        this.currentProduct = response.data
        
        // Track view interaction
        await this.trackInteraction(response.data.id, 'view')
        
        return response.data
      } catch (error) {
        console.error('Error fetching product:', error)
        throw error
      } finally {
        this.loading = false
      }
    },

    async fetchProductsByCategory(categorySlug, params = {}) {
      try {
        this.loading = true
        const response = await api.get(`/products/category/${categorySlug}/`, { params })
        this.products = response.data.results || response.data
        this.pagination = {
          count: response.data.count,
          next: response.data.next,
          previous: response.data.previous,
          currentPage: params.page || 1,
        }
      } catch (error) {
        console.error('Error fetching products by category:', error)
      } finally {
        this.loading = false
      }
    },

    async trackInteraction(productId, interactionType, metadata = {}) {
      try {
        await api.post('/analytics/track/', {
          product_id: productId,
          interaction_type: interactionType,
          metadata,
        })
      } catch (error) {
        console.error('Error tracking interaction:', error)
      }
    },

    setFilter(key, value) {
      this.filters[key] = value
    },

    clearFilters() {
      this.filters = {
        category: null,
        search: '',
        ordering: '-created_at',
      }
    },
  },
})
