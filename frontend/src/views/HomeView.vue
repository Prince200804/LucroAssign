<template>
  <div class="home-page">
    <!-- Hero Section -->
    <section class="hero-section">
      <div class="hero-bg-animation"></div>
      <v-container class="hero-content">
        <v-row align="center" justify="center" style="min-height: 85vh;">
          <v-col cols="12" md="6" class="text-center text-md-start">
            <div class="hero-badge mb-4">
              <v-chip color="primary" variant="tonal" size="small" class="px-4">
                <v-icon size="small" class="mr-1">mdi-sparkles</v-icon>
                Premium Electronics Store
              </v-chip>
            </div>
            
            <h1 class="hero-title mb-6">
              <span class="gradient-text">Next-Gen</span>
              <br />
              Tech Shopping Experience
            </h1>
            
            <p class="hero-subtitle text-grey mb-8">
              Discover cutting-edge electronics and gadgets. Experience the future of 
              shopping with our curated collection of premium tech products.
            </p>
            
            <div class="hero-buttons d-flex flex-wrap ga-3 justify-center justify-md-start">
              <v-btn 
                size="x-large" 
                class="btn-gradient px-8"
                to="/products"
              >
                <v-icon class="mr-2">mdi-shopping</v-icon>
                Shop Now
              </v-btn>
              <v-btn 
                size="x-large" 
                variant="outlined"
                class="btn-outline-gradient px-8"
                to="/products"
              >
                <v-icon class="mr-2">mdi-compass</v-icon>
                Explore
              </v-btn>
            </div>
            
            <!-- Stats -->
            <div class="hero-stats d-flex ga-8 mt-12 justify-center justify-md-start">
              <div class="stat-item">
                <div class="stat-number gradient-text">500+</div>
                <div class="stat-label text-grey">Products</div>
              </div>
              <div class="stat-item">
                <div class="stat-number gradient-text">50K+</div>
                <div class="stat-label text-grey">Customers</div>
              </div>
              <div class="stat-item">
                <div class="stat-number gradient-text">4.9</div>
                <div class="stat-label text-grey">Rating</div>
              </div>
            </div>
          </v-col>
          
          <v-col cols="12" md="6" class="d-none d-md-flex justify-center">
            <div class="hero-image-container floating">
              <div class="hero-glow"></div>
              <v-img
                src="https://images.unsplash.com/photo-1616348436168-de43ad0db179?w=600&q=80"
                width="400"
                class="hero-product-image rounded-xl"
              ></v-img>
            </div>
          </v-col>
        </v-row>
      </v-container>
      
      <!-- Scroll Indicator -->
      <div class="scroll-indicator">
        <v-icon color="primary" class="bounce">mdi-chevron-double-down</v-icon>
      </div>
    </section>

    <!-- Categories Section -->
    <section class="categories-section py-16">
      <v-container>
        <div class="section-header text-center mb-12">
          <h2 class="text-h3 font-weight-bold mb-4">
            Shop by <span class="gradient-text">Category</span>
          </h2>
          <p class="text-body-1 text-grey mx-auto" style="max-width: 600px;">
            Browse our carefully curated collection of electronics across different categories
          </p>
        </div>
        
        <v-row v-if="categoriesLoading" justify="center">
          <v-col v-for="n in 6" :key="n" cols="6" sm="4" md="2">
            <v-skeleton-loader type="card" class="skeleton"></v-skeleton-loader>
          </v-col>
        </v-row>
        
        <v-row v-else justify="center">
          <v-col v-for="category in categories" :key="category.id" cols="6" sm="4" md="2">
            <v-card
              :to="`/category/${category.slug}`"
              class="category-card text-center pa-6"
            >
              <div class="category-icon-wrapper mb-4">
                <v-icon size="40" class="gradient-text">
                  {{ getCategoryIcon(category.slug) }}
                </v-icon>
              </div>
              <h3 class="text-body-1 font-weight-bold mb-1">{{ category.name }}</h3>
              <span class="text-caption text-grey">
                {{ category.product_count || 0 }} Products
              </span>
            </v-card>
          </v-col>
        </v-row>
      </v-container>
    </section>

    <!-- Featured Products Section -->
    <section class="products-section py-16">
      <v-container>
        <div class="d-flex flex-column flex-md-row justify-space-between align-center mb-12">
          <div class="text-center text-md-start mb-4 mb-md-0">
            <h2 class="text-h3 font-weight-bold mb-2">
              Featured <span class="gradient-text">Products</span>
            </h2>
            <p class="text-body-1 text-grey">Handpicked products just for you</p>
          </div>
          <v-btn variant="outlined" class="btn-outline-gradient" to="/products">
            View All Products
            <v-icon class="ml-2">mdi-arrow-right</v-icon>
          </v-btn>
        </div>

        <v-row v-if="productsLoading">
          <v-col v-for="n in 8" :key="n" cols="12" sm="6" md="3">
            <v-skeleton-loader type="card" class="skeleton"></v-skeleton-loader>
          </v-col>
        </v-row>

        <v-row v-else>
          <v-col
            v-for="product in featuredProducts"
            :key="product.id"
            cols="12"
            sm="6"
            md="3"
          >
            <ProductCard :product="product" />
          </v-col>
        </v-row>
      </v-container>
    </section>

    <!-- Features Section -->
    <section class="features-section py-16">
      <v-container>
        <div class="section-header text-center mb-12">
          <h2 class="text-h3 font-weight-bold mb-4">
            Why Choose <span class="gradient-text">Us</span>
          </h2>
          <p class="text-body-1 text-grey mx-auto" style="max-width: 600px;">
            Experience the best in online shopping with our premium features
          </p>
        </div>
        
        <v-row>
          <v-col cols="12" sm="6" md="3">
            <v-card class="feature-card pa-6 text-center h-100">
              <div class="feature-icon-wrapper mb-4">
                <v-icon size="36" class="gradient-text">mdi-truck-fast-outline</v-icon>
              </div>
              <h3 class="text-h6 font-weight-bold mb-2">Free Shipping</h3>
              <p class="text-body-2 text-grey">Free delivery on orders over ₹500. Fast & reliable shipping.</p>
            </v-card>
          </v-col>
          <v-col cols="12" sm="6" md="3">
            <v-card class="feature-card pa-6 text-center h-100">
              <div class="feature-icon-wrapper mb-4">
                <v-icon size="36" class="gradient-text">mdi-shield-check-outline</v-icon>
              </div>
              <h3 class="text-h6 font-weight-bold mb-2">Secure Payment</h3>
              <p class="text-body-2 text-grey">100% secure payment processing with multiple options.</p>
            </v-card>
          </v-col>
          <v-col cols="12" sm="6" md="3">
            <v-card class="feature-card pa-6 text-center h-100">
              <div class="feature-icon-wrapper mb-4">
                <v-icon size="36" class="gradient-text">mdi-refresh</v-icon>
              </div>
              <h3 class="text-h6 font-weight-bold mb-2">Easy Returns</h3>
              <p class="text-body-2 text-grey">30-day hassle-free return policy for all products.</p>
            </v-card>
          </v-col>
          <v-col cols="12" sm="6" md="3">
            <v-card class="feature-card pa-6 text-center h-100">
              <div class="feature-icon-wrapper mb-4">
                <v-icon size="36" class="gradient-text">mdi-headset</v-icon>
              </div>
              <h3 class="text-h6 font-weight-bold mb-2">24/7 Support</h3>
              <p class="text-body-2 text-grey">Round-the-clock customer support to help you.</p>
            </v-card>
          </v-col>
        </v-row>
      </v-container>
    </section>

    <!-- CTA Section -->
    <section class="cta-section py-16">
      <v-container>
        <v-card class="cta-card pa-12 text-center">
          <h2 class="text-h3 font-weight-bold mb-4">
            Ready to Get Started?
          </h2>
          <p class="text-body-1 text-grey mb-8 mx-auto" style="max-width: 500px;">
            Join thousands of happy customers and start shopping for the best electronics today.
          </p>
          <div class="d-flex ga-4 justify-center flex-wrap">
            <v-btn size="x-large" class="btn-gradient px-8" to="/register">
              <v-icon class="mr-2">mdi-account-plus</v-icon>
              Create Account
            </v-btn>
            <v-btn size="x-large" variant="outlined" class="btn-outline-gradient px-8" to="/products">
              Browse Products
            </v-btn>
          </div>
        </v-card>
      </v-container>
    </section>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useProductStore } from '@/stores/products'
import ProductCard from '@/components/ProductCard.vue'

const productStore = useProductStore()

const categoriesLoading = ref(true)
const productsLoading = ref(true)
const categories = ref([])
const featuredProducts = ref([])

const getCategoryIcon = (slug) => {
  const icons = {
    'smartphones': 'mdi-cellphone',
    'laptops': 'mdi-laptop',
    'headphones': 'mdi-headphones',
    'tablets': 'mdi-tablet',
    'smartwatches': 'mdi-watch',
    'accessories': 'mdi-cable-data',
    'electronics': 'mdi-chip',
    'cameras': 'mdi-camera',
    'gaming': 'mdi-gamepad-variant',
  }
  return icons[slug] || 'mdi-tag'
}

onMounted(() => {
  // Load data without blocking - use Promise.all for parallel loading
  Promise.all([
    productStore.fetchCategories(),
    productStore.fetchFeaturedProducts()
  ]).then(() => {
    categories.value = productStore.categories
    featuredProducts.value = productStore.featuredProducts.slice(0, 8)
    categoriesLoading.value = false
    productsLoading.value = false
  }).catch(error => {
    console.error('Error loading home data:', error)
    categoriesLoading.value = false
    productsLoading.value = false
  })
})
</script>

<style scoped>
.home-page {
  background: #0a0a0a;
}

/* Hero Section */
.hero-section {
  position: relative;
  min-height: 100vh;
  overflow: hidden;
  background: linear-gradient(180deg, #0a0a0a 0%, #0f0f1a 50%, #0a0a0a 100%);
}

.hero-bg-animation {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: 
    radial-gradient(ellipse at 30% 20%, rgba(99, 102, 241, 0.15) 0%, transparent 50%),
    radial-gradient(ellipse at 70% 80%, rgba(139, 92, 246, 0.1) 0%, transparent 50%);
  animation: heroGlow 8s ease-in-out infinite alternate;
}

@keyframes heroGlow {
  0% { opacity: 0.5; transform: scale(1); }
  100% { opacity: 0.8; transform: scale(1.1); }
}

.hero-content {
  position: relative;
  z-index: 1;
}

.hero-title {
  font-size: clamp(2.5rem, 5vw, 4rem);
  font-weight: 800;
  line-height: 1.1;
  letter-spacing: -0.02em;
}

.hero-subtitle {
  font-size: 1.1rem;
  line-height: 1.7;
  max-width: 500px;
}

.hero-image-container {
  position: relative;
}

.hero-glow {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  width: 300px;
  height: 300px;
  background: radial-gradient(circle, rgba(99, 102, 241, 0.3) 0%, transparent 70%);
  filter: blur(40px);
}

.hero-product-image {
  position: relative;
  z-index: 1;
  box-shadow: 0 25px 50px rgba(99, 102, 241, 0.2);
}

.hero-stats {
  flex-wrap: wrap;
}

.stat-item {
  text-align: center;
}

.stat-number {
  font-size: 2rem;
  font-weight: 800;
  font-family: 'Space Grotesk', sans-serif;
}

.stat-label {
  font-size: 0.875rem;
}

.scroll-indicator {
  position: absolute;
  bottom: 30px;
  left: 50%;
  transform: translateX(-50%);
}

.bounce {
  animation: bounce 2s infinite;
}

@keyframes bounce {
  0%, 20%, 50%, 80%, 100% { transform: translateY(0); }
  40% { transform: translateY(-10px); }
  60% { transform: translateY(-5px); }
}

/* Categories Section */
.categories-section {
  background: linear-gradient(180deg, #0a0a0a 0%, #0d0d15 100%);
}

.category-card {
  background: rgba(20, 20, 20, 0.6) !important;
  border: 1px solid rgba(255, 255, 255, 0.05) !important;
  transition: all 0.3s ease;
  cursor: pointer;
}

.category-card:hover {
  transform: translateY(-8px);
  border-color: rgba(99, 102, 241, 0.3) !important;
  box-shadow: 0 20px 40px rgba(99, 102, 241, 0.15);
}

.category-icon-wrapper {
  width: 70px;
  height: 70px;
  border-radius: 16px;
  background: rgba(99, 102, 241, 0.1);
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 0 auto;
}

/* Products Section */
.products-section {
  background: #0a0a0a;
}

/* Features Section */
.features-section {
  background: linear-gradient(180deg, #0a0a0a 0%, #0d0d15 100%);
}

.feature-card {
  background: rgba(20, 20, 20, 0.4) !important;
  border: 1px solid rgba(255, 255, 255, 0.05) !important;
  transition: all 0.3s ease;
}

.feature-card:hover {
  transform: translateY(-4px);
  border-color: rgba(99, 102, 241, 0.2) !important;
}

.feature-icon-wrapper {
  width: 64px;
  height: 64px;
  border-radius: 16px;
  background: rgba(99, 102, 241, 0.1);
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 0 auto;
}

/* CTA Section */
.cta-section {
  background: #0a0a0a;
}

.cta-card {
  background: linear-gradient(145deg, rgba(99, 102, 241, 0.1) 0%, rgba(139, 92, 246, 0.05) 100%) !important;
  border: 1px solid rgba(99, 102, 241, 0.2) !important;
}

/* Responsive */
@media (max-width: 960px) {
  .hero-section {
    min-height: auto;
    padding: 100px 0 60px;
  }
  
  .hero-title {
    font-size: 2.5rem;
  }
  
  .hero-subtitle {
    margin-left: auto;
    margin-right: auto;
  }
}
</style>
