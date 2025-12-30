import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const routes = [
  {
    path: '/',
    name: 'Home',
    component: () => import('@/views/HomeView.vue')
  },
  {
    path: '/products',
    name: 'Products',
    component: () => import('@/views/ProductsView.vue')
  },
  {
    path: '/products/:slug',
    name: 'ProductDetail',
    component: () => import('@/views/ProductDetailView.vue')
  },
  {
    path: '/category/:slug',
    name: 'Category',
    component: () => import('@/views/CategoryView.vue')
  },
  {
    path: '/cart',
    name: 'Cart',
    component: () => import('@/views/CartView.vue')
  },
  {
    path: '/checkout',
    name: 'Checkout',
    component: () => import('@/views/CheckoutView.vue')
  },
  {
    path: '/login',
    name: 'Login',
    component: () => import('@/views/LoginView.vue'),
    meta: { guest: true }
  },
  {
    path: '/register',
    name: 'Register',
    component: () => import('@/views/RegisterView.vue'),
    meta: { guest: true }
  },
  {
    path: '/profile',
    name: 'Profile',
    component: () => import('@/views/ProfileView.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/orders',
    name: 'Orders',
    component: () => import('@/views/OrdersView.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/order/:id',
    name: 'OrderDetail',
    component: () => import('@/views/OrderDetailView.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/track-order',
    name: 'TrackOrder',
    component: () => import('@/views/TrackOrderView.vue')
  },
  // Admin Routes
  {
    path: '/admin',
    name: 'AdminDashboard',
    component: () => import('@/views/admin/DashboardView.vue'),
    meta: { requiresAuth: true, requiresAdmin: true }
  },
  {
    path: '/admin/products',
    name: 'AdminProducts',
    component: () => import('@/views/admin/ProductsManageView.vue'),
    meta: { requiresAuth: true, requiresAdmin: true }
  },
  {
    path: '/admin/analytics',
    name: 'AdminAnalytics',
    component: () => import('@/views/admin/AnalyticsView.vue'),
    meta: { requiresAuth: true, requiresAdmin: true }
  },
  {
    path: '/admin/orders',
    name: 'AdminOrders',
    component: () => import('@/views/admin/OrdersManageView.vue'),
    meta: { requiresAuth: true, requiresAdmin: true }
  },
  // 404
  {
    path: '/:pathMatch(.*)*',
    name: 'NotFound',
    component: () => import('@/views/NotFoundView.vue')
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes,
  scrollBehavior(to, from, savedPosition) {
    if (savedPosition) {
      return savedPosition
    } else {
      return { top: 0 }
    }
  }
})

// Simple, fast navigation guard - don't block on auth initialization
router.beforeEach((to, from, next) => {
  const authStore = useAuthStore()
  
  // Quick check for token in localStorage
  const hasToken = !!localStorage.getItem('access_token')
  
  // For routes requiring auth, check if we have a token
  if (to.meta.requiresAuth && !hasToken) {
    return next({ name: 'Login', query: { redirect: to.fullPath } })
  }
  
  // For admin routes, check if user is admin (if already loaded)
  if (to.meta.requiresAdmin && authStore.initialized && !authStore.isAdmin) {
    return next({ name: 'Home' })
  }
  
  // For guest routes, redirect authenticated users
  if (to.meta.guest && hasToken) {
    return next({ name: 'Home' })
  }
  
  // Initialize auth in background if not done (don't block navigation)
  if (!authStore.initialized && hasToken) {
    authStore.initializeAuth() // Don't await - let it happen in background
  }
  
  next()
})

export default router
