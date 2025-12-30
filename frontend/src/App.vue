<template>
  <v-app class="app-container">
    <!-- Modern Glassmorphism Navbar -->
    <v-app-bar class="navbar-glass" elevation="0" height="70">
      <v-container class="d-flex align-center">
        <v-app-bar-nav-icon 
          v-if="isMobile" 
          @click="drawer = !drawer"
          color="white"
        ></v-app-bar-nav-icon>
        
        <!-- Logo -->
        <router-link to="/" class="text-decoration-none d-flex align-center">
          <div class="logo-container mr-3">
            <v-icon size="32" class="gradient-text">mdi-shopping</v-icon>
          </div>
          <span class="text-h5 font-weight-bold gradient-text">TechStore</span>
        </router-link>

        <v-spacer></v-spacer>

        <!-- Desktop Navigation -->
        <template v-if="!isMobile">
          <div class="nav-links d-flex align-center ga-1">
            <v-btn variant="text" to="/" class="nav-link">
              <v-icon size="small" class="mr-1">mdi-home</v-icon>
              Home
            </v-btn>
            <v-btn variant="text" to="/products" class="nav-link">
              <v-icon size="small" class="mr-1">mdi-store</v-icon>
              Products
            </v-btn>
            
            <!-- Track Order Link -->
            <v-btn variant="text" to="/track-order" class="nav-link">
              <v-icon size="small" class="mr-1">mdi-truck-delivery</v-icon>
              Track Order
            </v-btn>
            
            <!-- Cart Button - Hidden for Admin -->
            <v-btn v-if="!isAdmin" variant="text" to="/cart" class="nav-link cart-btn">
              <v-badge 
                :content="cartItemCount" 
                color="error" 
                v-if="cartItemCount > 0"
                class="badge-glow"
              >
                <v-icon>mdi-cart-outline</v-icon>
              </v-badge>
              <v-icon v-else>mdi-cart-outline</v-icon>
            </v-btn>

            <v-divider vertical class="mx-3 opacity-20"></v-divider>

            <!-- Authenticated User Menu -->
            <template v-if="isAuthenticated">
              <v-btn 
                v-if="isAdmin" 
                variant="text" 
                to="/admin" 
                class="nav-link admin-btn"
              >
                <v-icon size="small" class="mr-1">mdi-chart-areaspline</v-icon>
                Dashboard
              </v-btn>
              
              <v-menu transition="slide-y-transition">
                <template v-slot:activator="{ props }">
                  <v-btn variant="text" v-bind="props" class="nav-link user-btn">
                    <v-avatar size="32" color="primary" class="mr-2">
                      <span class="text-body-2 font-weight-bold">
                        {{ user?.first_name?.charAt(0) || 'U' }}
                      </span>
                    </v-avatar>
                    {{ user?.first_name || 'Account' }}
                    <v-icon size="small" class="ml-1">mdi-chevron-down</v-icon>
                  </v-btn>
                </template>
                <v-list class="glass-card pa-2" density="compact">
                  <v-list-item to="/profile" rounded="lg" class="mb-1">
                    <template v-slot:prepend>
                      <v-icon color="primary">mdi-account-circle</v-icon>
                    </template>
                    <v-list-item-title>My Profile</v-list-item-title>
                  </v-list-item>
                  <v-list-item to="/orders" rounded="lg" class="mb-1">
                    <template v-slot:prepend>
                      <v-icon color="primary">mdi-package-variant-closed</v-icon>
                    </template>
                    <v-list-item-title>My Orders</v-list-item-title>
                  </v-list-item>
                  <v-divider class="my-2"></v-divider>
                  <v-list-item @click="handleLogout" rounded="lg" class="text-error">
                    <template v-slot:prepend>
                      <v-icon color="error">mdi-logout</v-icon>
                    </template>
                    <v-list-item-title>Logout</v-list-item-title>
                  </v-list-item>
                </v-list>
              </v-menu>
            </template>
            
            <!-- Guest Buttons -->
            <template v-else>
              <v-btn variant="text" to="/login" class="nav-link">
                Login
              </v-btn>
              <v-btn to="/register" class="btn-gradient ml-2 px-6">
                Sign Up
              </v-btn>
            </template>
          </div>
        </template>
      </v-container>
    </v-app-bar>

    <!-- Mobile Navigation Drawer -->
    <v-navigation-drawer v-model="drawer" temporary location="left">
      <div class="pa-4">
        <div class="d-flex align-center mb-6">
          <v-icon size="32" class="gradient-text mr-2">mdi-shopping</v-icon>
          <span class="text-h6 font-weight-bold gradient-text">TechStore</span>
        </div>
        
        <v-list density="compact" nav>
          <v-list-item to="/" prepend-icon="mdi-home" rounded="lg" class="mb-1">
            <v-list-item-title>Home</v-list-item-title>
          </v-list-item>
          <v-list-item to="/products" prepend-icon="mdi-store" rounded="lg" class="mb-1">
            <v-list-item-title>Products</v-list-item-title>
          </v-list-item>
          <v-list-item to="/track-order" prepend-icon="mdi-truck-delivery" rounded="lg" class="mb-1">
            <v-list-item-title>Track Order</v-list-item-title>
          </v-list-item>
          <v-list-item v-if="!isAdmin" to="/cart" prepend-icon="mdi-cart" rounded="lg" class="mb-1">
            <v-list-item-title>
              Cart
              <v-chip v-if="cartItemCount > 0" size="x-small" color="error" class="ml-2">
                {{ cartItemCount }}
              </v-chip>
            </v-list-item-title>
          </v-list-item>
          
          <v-divider class="my-4"></v-divider>
          
          <template v-if="isAuthenticated">
            <v-list-item v-if="isAdmin" to="/admin" prepend-icon="mdi-chart-areaspline" rounded="lg" class="mb-1">
              <v-list-item-title>Dashboard</v-list-item-title>
            </v-list-item>
            <v-list-item to="/profile" prepend-icon="mdi-account" rounded="lg" class="mb-1">
              <v-list-item-title>Profile</v-list-item-title>
            </v-list-item>
            <v-list-item to="/orders" prepend-icon="mdi-package-variant" rounded="lg" class="mb-1">
              <v-list-item-title>My Orders</v-list-item-title>
            </v-list-item>
            <v-list-item @click="handleLogout" prepend-icon="mdi-logout" rounded="lg" class="text-error">
              <v-list-item-title>Logout</v-list-item-title>
            </v-list-item>
          </template>
          
          <template v-else>
            <v-list-item to="/login" prepend-icon="mdi-login" rounded="lg" class="mb-1">
              <v-list-item-title>Login</v-list-item-title>
            </v-list-item>
            <v-list-item to="/register" prepend-icon="mdi-account-plus" rounded="lg">
              <v-list-item-title>Sign Up</v-list-item-title>
            </v-list-item>
          </template>
        </v-list>
      </div>
    </v-navigation-drawer>

    <!-- Main Content -->
    <v-main>
      <router-view v-slot="{ Component }">
        <transition name="fade" mode="out-in">
          <component :is="Component" />
        </transition>
      </router-view>
    </v-main>

    <!-- Modern Footer -->
    <v-footer class="footer-section pa-0">
      <v-container class="py-12">
        <v-row>
          <v-col cols="12" md="4" class="mb-6 mb-md-0">
            <div class="d-flex align-center mb-4">
              <v-icon size="36" class="gradient-text mr-2">mdi-shopping</v-icon>
              <span class="text-h5 font-weight-bold gradient-text">TechStore</span>
            </div>
            <p class="text-body-2 text-grey mb-4" style="max-width: 300px;">
              Your trusted destination for premium electronics and tech gadgets. Experience the future of shopping today.
            </p>
            <div class="d-flex ga-2">
              <v-btn icon variant="tonal" size="small" color="primary">
                <v-icon>mdi-facebook</v-icon>
              </v-btn>
              <v-btn icon variant="tonal" size="small" color="primary">
                <v-icon>mdi-twitter</v-icon>
              </v-btn>
              <v-btn icon variant="tonal" size="small" color="primary">
                <v-icon>mdi-instagram</v-icon>
              </v-btn>
              <v-btn icon variant="tonal" size="small" color="primary">
                <v-icon>mdi-linkedin</v-icon>
              </v-btn>
            </div>
          </v-col>
          
          <v-col cols="6" md="2">
            <h4 class="text-subtitle-1 font-weight-bold mb-4 gradient-text">Quick Links</h4>
            <div class="d-flex flex-column ga-2">
              <router-link to="/" class="footer-link">Home</router-link>
              <router-link to="/products" class="footer-link">Products</router-link>
              <router-link to="/cart" class="footer-link">Cart</router-link>
              <router-link to="/orders" class="footer-link">Orders</router-link>
            </div>
          </v-col>
          
          <v-col cols="6" md="2">
            <h4 class="text-subtitle-1 font-weight-bold mb-4 gradient-text">Categories</h4>
            <div class="d-flex flex-column ga-2">
              <router-link to="/category/smartphones" class="footer-link">Smartphones</router-link>
              <router-link to="/category/laptops" class="footer-link">Laptops</router-link>
              <router-link to="/category/headphones" class="footer-link">Headphones</router-link>
              <router-link to="/category/accessories" class="footer-link">Accessories</router-link>
            </div>
          </v-col>
          
          <v-col cols="12" md="4">
            <h4 class="text-subtitle-1 font-weight-bold mb-4 gradient-text">Contact Us</h4>
            <div class="d-flex flex-column ga-3">
              <div class="d-flex align-center">
                <v-icon size="20" color="primary" class="mr-3">mdi-email-outline</v-icon>
                <span class="text-body-2 text-grey">support@techstore.com</span>
              </div>
              <div class="d-flex align-center">
                <v-icon size="20" color="primary" class="mr-3">mdi-phone-outline</v-icon>
                <span class="text-body-2 text-grey">+91 1234567890</span>
              </div>
              <div class="d-flex align-center">
                <v-icon size="20" color="primary" class="mr-3">mdi-map-marker-outline</v-icon>
                <span class="text-body-2 text-grey">Bangalore, India</span>
              </div>
            </div>
          </v-col>
        </v-row>
        
        <v-divider class="my-8" style="opacity: 0.1;"></v-divider>
        
        <div class="d-flex flex-column flex-md-row justify-space-between align-center">
          <span class="text-body-2 text-grey">
            © {{ new Date().getFullYear() }} TechStore. All rights reserved.
          </span>
          <div class="d-flex ga-4 mt-4 mt-md-0">
            <a href="#" class="footer-link text-body-2">Privacy Policy</a>
            <a href="#" class="footer-link text-body-2">Terms of Service</a>
          </div>
        </div>
      </v-container>
    </v-footer>

    <!-- Global Snackbar -->
    <v-snackbar
      v-model="snackbar.show"
      :color="snackbar.color"
      :timeout="3000"
      location="top right"
      rounded="lg"
    >
      <div class="d-flex align-center">
        <v-icon class="mr-2">
          {{ snackbar.color === 'success' ? 'mdi-check-circle' : snackbar.color === 'error' ? 'mdi-alert-circle' : 'mdi-information' }}
        </v-icon>
        {{ snackbar.message }}
      </div>
      <template v-slot:actions>
        <v-btn variant="text" size="small" @click="snackbar.show = false">
          <v-icon>mdi-close</v-icon>
        </v-btn>
      </template>
    </v-snackbar>
  </v-app>
</template>

<script setup>
import { ref, computed, onMounted, provide } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { useCartStore } from '@/stores/cart'
import { useDisplay } from 'vuetify'

const router = useRouter()
const authStore = useAuthStore()
const cartStore = useCartStore()
const { mobile } = useDisplay()

const drawer = ref(false)
const snackbar = ref({
  show: false,
  message: '',
  color: 'success'
})

const isMobile = computed(() => mobile.value)
const isAuthenticated = computed(() => authStore.isAuthenticated)
const isAdmin = computed(() => authStore.isAdmin)
const user = computed(() => authStore.user)
const cartItemCount = computed(() => cartStore.totalItems)

// Provide snackbar function globally
const showSnackbar = (message, color = 'success') => {
  snackbar.value = { show: true, message, color }
}
provide('showSnackbar', showSnackbar)

const handleLogout = async () => {
  await authStore.logout()
  showSnackbar('Logged out successfully')
  router.push('/')
}

onMounted(() => {
  // Initialize auth state - don't await to prevent blocking UI
  authStore.initializeAuth()
  // Fetch cart - don't await to prevent blocking UI
  cartStore.fetchCart()
})
</script>

<style scoped>
.app-container {
  background: #0a0a0a;
  min-height: 100vh;
}

.navbar-glass {
  background: rgba(10, 10, 10, 0.8) !important;
  backdrop-filter: blur(20px);
  -webkit-backdrop-filter: blur(20px);
  border-bottom: 1px solid rgba(255, 255, 255, 0.05);
}

.logo-container {
  width: 40px;
  height: 40px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 10px;
  background: rgba(99, 102, 241, 0.1);
}

.nav-link {
  color: rgba(255, 255, 255, 0.7) !important;
  font-weight: 500;
  font-size: 14px;
  transition: all 0.3s ease;
}

.nav-link:hover {
  color: #a5b4fc !important;
  background: rgba(99, 102, 241, 0.1) !important;
}

.admin-btn {
  color: #a5b4fc !important;
}

.footer-section {
  background: linear-gradient(180deg, #0a0a0a 0%, #050510 100%);
  border-top: 1px solid rgba(255, 255, 255, 0.05);
}

.footer-link {
  color: rgba(255, 255, 255, 0.5);
  text-decoration: none;
  font-size: 14px;
  transition: color 0.3s ease;
}

.footer-link:hover {
  color: #a5b4fc;
}

.glass-card {
  background: rgba(20, 20, 20, 0.95) !important;
  backdrop-filter: blur(20px);
  border: 1px solid rgba(255, 255, 255, 0.08) !important;
}
</style>
