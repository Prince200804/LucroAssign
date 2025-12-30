<template>
  <div class="product-detail-page">
    <v-container class="py-8">
      <!-- Loading State -->
      <div v-if="loading" class="loading-state">
        <v-row>
          <v-col cols="12" md="6">
            <div class="skeleton-image"></div>
          </v-col>
          <v-col cols="12" md="6">
            <div class="skeleton-content">
              <div class="skeleton-line short"></div>
              <div class="skeleton-line"></div>
              <div class="skeleton-line medium"></div>
              <div class="skeleton-line short"></div>
            </div>
          </v-col>
        </v-row>
      </div>

      <!-- Product Not Found -->
      <div v-else-if="!product" class="not-found">
        <div class="not-found-icon">
          <v-icon size="80">mdi-alert-circle-outline</v-icon>
        </div>
        <h2>Product Not Found</h2>
        <p>The product you're looking for doesn't exist or has been removed.</p>
        <router-link to="/products" class="back-btn">
          <v-icon size="20" class="mr-2">mdi-arrow-left</v-icon>
          Browse Products
        </router-link>
      </div>

      <!-- Product Details -->
      <template v-else>
        <!-- Breadcrumbs -->
        <div class="breadcrumbs">
          <router-link to="/">Home</router-link>
          <v-icon size="16">mdi-chevron-right</v-icon>
          <router-link to="/products">Products</router-link>
          <v-icon size="16">mdi-chevron-right</v-icon>
          <router-link v-if="product.category" :to="`/category/${product.category.slug}`">
            {{ product.category.name }}
          </router-link>
          <v-icon v-if="product.category" size="16">mdi-chevron-right</v-icon>
          <span class="current">{{ product.name }}</span>
        </div>

        <v-row>
          <!-- Product Images -->
          <v-col cols="12" md="6">
            <div class="image-section">
              <div class="main-image">
                <img 
                  :src="product.image || 'https://via.placeholder.com/600x600?text=No+Image'" 
                  :alt="product.name"
                />
                <!-- Badges -->
                <div class="image-badges">
                  <span v-if="product.discount_percentage > 0" class="badge discount">
                    -{{ product.discount_percentage }}%
                  </span>
                  <span v-if="product.is_featured" class="badge featured">
                    <v-icon size="14">mdi-star</v-icon> Featured
                  </span>
                </div>
              </div>

              <!-- Thumbnail Gallery -->
              <div v-if="product.images && product.images.length > 0" class="thumbnails">
                <button 
                  v-for="img in product.images" 
                  :key="img.id" 
                  class="thumb"
                  @click="selectImage(img.image)"
                >
                  <img :src="img.image" :alt="product.name" />
                </button>
              </div>
            </div>
          </v-col>

          <!-- Product Info -->
          <v-col cols="12" md="6">
            <div class="product-info">
              <!-- Category & Tags -->
              <div class="tags-row">
                <span class="category-tag">{{ product.category?.name }}</span>
                <span v-if="product.brand" class="brand-tag">{{ product.brand }}</span>
              </div>

              <!-- Title -->
              <h1 class="product-title">{{ product.name }}</h1>
              
              <!-- SKU -->
              <div class="sku">SKU: {{ product.sku }}</div>

              <!-- Price Section -->
              <div class="price-section">
                <div v-if="product.discount_price" class="price-with-discount">
                  <span class="current-price">₹{{ formatPrice(product.discount_price) }}</span>
                  <span class="original-price">₹{{ formatPrice(product.price) }}</span>
                  <span class="discount-badge">Save {{ product.discount_percentage }}%</span>
                </div>
                <span v-else class="current-price">₹{{ formatPrice(product.price) }}</span>
              </div>

              <!-- Stock Status -->
              <div class="stock-status" :class="product.in_stock ? 'in-stock' : 'out-of-stock'">
                <v-icon size="20">{{ product.in_stock ? 'mdi-check-circle' : 'mdi-close-circle' }}</v-icon>
                {{ product.in_stock ? `In Stock (${product.stock} available)` : 'Out of Stock' }}
              </div>

              <!-- Short Description -->
              <p class="short-description">{{ product.short_description || product.description }}</p>

              <!-- Quantity Selector - Hidden for Admin -->
              <div v-if="!isAdmin" class="quantity-section">
                <label>Quantity</label>
                <div class="quantity-controls">
                  <button 
                    class="qty-btn" 
                    :disabled="quantity <= 1"
                    @click="quantity--"
                  >
                    <v-icon size="20">mdi-minus</v-icon>
                  </button>
                  <span class="qty-value">{{ quantity }}</span>
                  <button 
                    class="qty-btn"
                    :disabled="quantity >= product.stock"
                    @click="quantity++"
                  >
                    <v-icon size="20">mdi-plus</v-icon>
                  </button>
                </div>
              </div>

              <!-- Action Buttons - Hidden for Admin -->
              <div v-if="!isAdmin" class="action-buttons">
                <button
                  class="add-to-cart-btn"
                  :class="{ disabled: !product.in_stock || addingToCart }"
                  :disabled="!product.in_stock || addingToCart"
                  @click="addToCart"
                >
                  <span v-if="addingToCart" class="loading-spinner"></span>
                  <template v-else>
                    <v-icon size="20" class="mr-2">mdi-cart-plus</v-icon>
                    Add to Cart
                  </template>
                </button>
                <button
                  class="buy-now-btn"
                  :class="{ disabled: !product.in_stock }"
                  :disabled="!product.in_stock"
                  @click="buyNow"
                >
                  <v-icon size="20" class="mr-2">mdi-flash</v-icon>
                  Buy Now
                </button>
              </div>

              <!-- Admin Edit Button -->
              <div v-else class="action-buttons">
                <button class="add-to-cart-btn" @click="editProduct">
                  <v-icon size="20" class="mr-2">mdi-pencil</v-icon>
                  Edit Product
                </button>
              </div>

              <!-- Trust Features -->
              <div class="trust-features">
                <div class="feature">
                  <v-icon size="24">mdi-truck-fast</v-icon>
                  <div>
                    <strong>Free Shipping</strong>
                    <span>On orders over ₹500</span>
                  </div>
                </div>
                <div class="feature">
                  <v-icon size="24">mdi-shield-check</v-icon>
                  <div>
                    <strong>Secure Payment</strong>
                    <span>100% protected</span>
                  </div>
                </div>
                <div class="feature">
                  <v-icon size="24">mdi-refresh</v-icon>
                  <div>
                    <strong>Easy Returns</strong>
                    <span>30 day policy</span>
                  </div>
                </div>
              </div>

              <!-- Specifications -->
              <div v-if="product.specifications && Object.keys(product.specifications).length > 0" class="specifications">
                <button class="spec-toggle" @click="showSpecs = !showSpecs">
                  <v-icon size="20" class="mr-2">mdi-clipboard-list</v-icon>
                  Specifications
                  <v-icon size="20" class="ml-auto">{{ showSpecs ? 'mdi-chevron-up' : 'mdi-chevron-down' }}</v-icon>
                </button>
                <div v-show="showSpecs" class="spec-content">
                  <div v-for="(value, key) in product.specifications" :key="key" class="spec-row">
                    <span class="spec-label">{{ key }}</span>
                    <span class="spec-value">{{ value }}</span>
                  </div>
                </div>
              </div>
            </div>
          </v-col>
        </v-row>

        <!-- Full Description -->
        <div class="description-section">
          <h2>Product Description</h2>
          <div class="description-content">
            {{ product.description }}
          </div>
        </div>
      </template>
    </v-container>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, inject } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useProductStore } from '@/stores/products'
import { useCartStore } from '@/stores/cart'
import { useAuthStore } from '@/stores/auth'

const route = useRoute()
const router = useRouter()
const productStore = useProductStore()
const cartStore = useCartStore()
const authStore = useAuthStore()
const showSnackbar = inject('showSnackbar')

const quantity = ref(1)
const addingToCart = ref(false)
const showSpecs = ref(false)

const loading = computed(() => productStore.loading)
const product = computed(() => productStore.currentProduct)
const isAdmin = computed(() => authStore.isAdmin)

const formatPrice = (price) => {
  return parseFloat(price).toLocaleString('en-IN')
}

const addToCart = async () => {
  addingToCart.value = true
  
  // Backend automatically tracks 'add_to_cart' interaction
  const result = await cartStore.addToCart(product.value.id, quantity.value)
  
  if (result.success) {
    showSnackbar(`Added ${quantity.value} item(s) to cart!`, 'success')
  } else {
    showSnackbar(result.error, 'error')
  }
  
  addingToCart.value = false
}

const buyNow = async () => {
  await addToCart()
  router.push('/checkout')
}

const editProduct = () => {
  router.push('/admin/products')
}

const selectImage = (imageUrl) => {
  // Could implement image gallery here
  console.log('Selected image:', imageUrl)
}

onMounted(async () => {
  const slug = route.params.slug
  try {
    await productStore.fetchProductBySlug(slug)
  } catch (error) {
    console.error('Error loading product:', error)
  }
})
</script>

<style scoped>
.product-detail-page {
  min-height: 100vh;
  padding-top: 20px;
}

/* Breadcrumbs */
.breadcrumbs {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 32px;
  font-size: 14px;
}

.breadcrumbs a {
  color: rgba(255, 255, 255, 0.6);
  text-decoration: none;
  transition: color 0.3s ease;
}

.breadcrumbs a:hover {
  color: #8B5CF6;
}

.breadcrumbs .current {
  color: #ffffff;
  font-weight: 500;
}

.breadcrumbs .v-icon {
  color: rgba(255, 255, 255, 0.3);
}

/* Loading State */
.loading-state {
  padding: 40px 0;
}

.skeleton-image {
  width: 100%;
  aspect-ratio: 1;
  background: linear-gradient(90deg, rgba(255, 255, 255, 0.05), rgba(255, 255, 255, 0.1), rgba(255, 255, 255, 0.05));
  background-size: 200% 100%;
  animation: shimmer 1.5s infinite;
  border-radius: 20px;
}

.skeleton-content {
  display: flex;
  flex-direction: column;
  gap: 20px;
  padding: 20px 0;
}

.skeleton-line {
  height: 24px;
  background: linear-gradient(90deg, rgba(255, 255, 255, 0.05), rgba(255, 255, 255, 0.1), rgba(255, 255, 255, 0.05));
  background-size: 200% 100%;
  animation: shimmer 1.5s infinite;
  border-radius: 8px;
}

.skeleton-line.short { width: 40%; }
.skeleton-line.medium { width: 70%; }

@keyframes shimmer {
  0% { background-position: 200% 0; }
  100% { background-position: -200% 0; }
}

/* Not Found */
.not-found {
  text-align: center;
  padding: 80px 40px;
  background: rgba(30, 30, 46, 0.6);
  border-radius: 24px;
}

.not-found-icon {
  width: 120px;
  height: 120px;
  margin: 0 auto 24px;
  background: rgba(239, 68, 68, 0.1);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #EF4444;
}

.not-found h2 {
  font-size: 1.8rem;
  color: #ffffff;
  margin-bottom: 12px;
}

.not-found p {
  color: rgba(255, 255, 255, 0.6);
  margin-bottom: 24px;
}

.back-btn {
  display: inline-flex;
  align-items: center;
  padding: 14px 28px;
  background: linear-gradient(135deg, #6366F1, #8B5CF6);
  border-radius: 12px;
  color: white;
  text-decoration: none;
  font-weight: 600;
  transition: all 0.3s ease;
}

.back-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 10px 30px rgba(99, 102, 241, 0.4);
}

/* Image Section */
.image-section {
  position: sticky;
  top: 100px;
}

.main-image {
  position: relative;
  background: rgba(30, 30, 46, 0.6);
  border: 1px solid rgba(255, 255, 255, 0.05);
  border-radius: 20px;
  overflow: hidden;
}

.main-image img {
  width: 100%;
  aspect-ratio: 1;
  object-fit: cover;
}

.image-badges {
  position: absolute;
  top: 16px;
  left: 16px;
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.badge {
  padding: 8px 14px;
  border-radius: 20px;
  font-size: 12px;
  font-weight: 700;
  display: flex;
  align-items: center;
  gap: 4px;
}

.badge.discount {
  background: linear-gradient(135deg, #EF4444, #DC2626);
  color: white;
}

.badge.featured {
  background: linear-gradient(135deg, #F59E0B, #D97706);
  color: white;
}

.thumbnails {
  display: flex;
  gap: 12px;
  margin-top: 16px;
}

.thumb {
  width: 80px;
  height: 80px;
  border-radius: 12px;
  overflow: hidden;
  border: 2px solid transparent;
  cursor: pointer;
  transition: all 0.3s ease;
  background: rgba(30, 30, 46, 0.6);
}

.thumb:hover {
  border-color: #8B5CF6;
}

.thumb img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

/* Product Info */
.product-info {
  padding: 0 20px;
}

.tags-row {
  display: flex;
  gap: 10px;
  margin-bottom: 16px;
}

.category-tag {
  padding: 6px 14px;
  background: rgba(99, 102, 241, 0.2);
  border: 1px solid rgba(99, 102, 241, 0.3);
  border-radius: 20px;
  color: #8B5CF6;
  font-size: 13px;
  font-weight: 600;
}

.brand-tag {
  padding: 6px 14px;
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 20px;
  color: rgba(255, 255, 255, 0.7);
  font-size: 13px;
}

.product-title {
  font-size: 2rem;
  font-weight: 700;
  color: #ffffff;
  line-height: 1.3;
  margin-bottom: 8px;
}

.sku {
  font-size: 13px;
  color: rgba(255, 255, 255, 0.4);
  margin-bottom: 24px;
}

/* Price Section */
.price-section {
  margin-bottom: 20px;
}

.price-with-discount {
  display: flex;
  align-items: center;
  gap: 16px;
  flex-wrap: wrap;
}

.current-price {
  font-size: 2.2rem;
  font-weight: 800;
  background: linear-gradient(135deg, #6366F1, #8B5CF6);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.price-with-discount .current-price {
  background: linear-gradient(135deg, #10B981, #059669);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.original-price {
  font-size: 1.2rem;
  color: rgba(255, 255, 255, 0.4);
  text-decoration: line-through;
}

.discount-badge {
  padding: 6px 12px;
  background: rgba(16, 185, 129, 0.2);
  border-radius: 8px;
  color: #10B981;
  font-size: 13px;
  font-weight: 600;
}

/* Stock Status */
.stock-status {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  padding: 10px 18px;
  border-radius: 12px;
  font-size: 14px;
  font-weight: 600;
  margin-bottom: 24px;
}

.stock-status.in-stock {
  background: rgba(16, 185, 129, 0.1);
  color: #10B981;
}

.stock-status.out-of-stock {
  background: rgba(239, 68, 68, 0.1);
  color: #EF4444;
}

.short-description {
  font-size: 15px;
  line-height: 1.7;
  color: rgba(255, 255, 255, 0.7);
  margin-bottom: 28px;
}

/* Quantity Section */
.quantity-section {
  margin-bottom: 28px;
}

.quantity-section label {
  display: block;
  font-size: 14px;
  font-weight: 600;
  color: rgba(255, 255, 255, 0.8);
  margin-bottom: 12px;
}

.quantity-controls {
  display: inline-flex;
  align-items: center;
  gap: 16px;
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 14px;
  padding: 8px;
}

.qty-btn {
  width: 44px;
  height: 44px;
  border-radius: 10px;
  background: rgba(255, 255, 255, 0.1);
  border: none;
  color: #ffffff;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.3s ease;
}

.qty-btn:hover:not(:disabled) {
  background: linear-gradient(135deg, #6366F1, #8B5CF6);
}

.qty-btn:disabled {
  opacity: 0.4;
  cursor: not-allowed;
}

.qty-value {
  font-size: 20px;
  font-weight: 700;
  color: #ffffff;
  min-width: 40px;
  text-align: center;
}

/* Action Buttons */
.action-buttons {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 16px;
  margin-bottom: 32px;
}

.add-to-cart-btn,
.buy-now-btn {
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 18px 24px;
  border-radius: 14px;
  font-size: 16px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  border: none;
}

.add-to-cart-btn {
  background: linear-gradient(135deg, #6366F1, #8B5CF6);
  color: white;
}

.add-to-cart-btn:hover:not(.disabled) {
  transform: translateY(-2px);
  box-shadow: 0 10px 30px rgba(99, 102, 241, 0.4);
}

.buy-now-btn {
  background: transparent;
  border: 2px solid rgba(255, 255, 255, 0.2);
  color: #ffffff;
}

.buy-now-btn:hover:not(.disabled) {
  border-color: #EC4899;
  color: #EC4899;
  background: rgba(236, 72, 153, 0.1);
}

.add-to-cart-btn.disabled,
.buy-now-btn.disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.loading-spinner {
  width: 24px;
  height: 24px;
  border: 3px solid rgba(255, 255, 255, 0.3);
  border-top-color: white;
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

/* Trust Features */
.trust-features {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 16px;
  margin-bottom: 28px;
  padding: 20px;
  background: rgba(255, 255, 255, 0.03);
  border-radius: 16px;
}

.feature {
  display: flex;
  align-items: flex-start;
  gap: 12px;
}

.feature .v-icon {
  color: #10B981;
}

.feature div {
  display: flex;
  flex-direction: column;
}

.feature strong {
  font-size: 13px;
  color: #ffffff;
}

.feature span {
  font-size: 11px;
  color: rgba(255, 255, 255, 0.5);
}

/* Specifications */
.specifications {
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 16px;
  overflow: hidden;
}

.spec-toggle {
  width: 100%;
  display: flex;
  align-items: center;
  padding: 18px 20px;
  background: rgba(255, 255, 255, 0.03);
  border: none;
  color: #ffffff;
  font-size: 15px;
  font-weight: 600;
  cursor: pointer;
  transition: background 0.3s ease;
}

.spec-toggle:hover {
  background: rgba(255, 255, 255, 0.05);
}

.spec-content {
  padding: 16px 20px;
}

.spec-row {
  display: flex;
  justify-content: space-between;
  padding: 12px 0;
  border-bottom: 1px solid rgba(255, 255, 255, 0.05);
}

.spec-row:last-child {
  border-bottom: none;
}

.spec-label {
  color: rgba(255, 255, 255, 0.6);
  text-transform: capitalize;
}

.spec-value {
  color: #ffffff;
  font-weight: 500;
}

/* Description Section */
.description-section {
  margin-top: 48px;
  padding: 32px;
  background: rgba(30, 30, 46, 0.6);
  backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.05);
  border-radius: 20px;
}

.description-section h2 {
  font-size: 1.4rem;
  font-weight: 700;
  color: #ffffff;
  margin-bottom: 20px;
  padding-bottom: 16px;
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
}

.description-content {
  font-size: 15px;
  line-height: 1.8;
  color: rgba(255, 255, 255, 0.7);
  white-space: pre-line;
}

/* Responsive */
@media (max-width: 960px) {
  .image-section {
    position: relative;
    top: 0;
  }
  
  .product-info {
    padding: 24px 0 0;
  }
  
  .trust-features {
    grid-template-columns: 1fr;
  }
  
  .action-buttons {
    grid-template-columns: 1fr;
  }
}
</style>
