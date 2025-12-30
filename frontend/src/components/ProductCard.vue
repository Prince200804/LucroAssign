<template>
  <div class="product-card-wrapper">
    <v-card class="product-card h-100 d-flex flex-column">
      <!-- Image Container -->
      <div class="image-container">
        <router-link :to="`/products/${product.slug}`" class="text-decoration-none">
          <v-img
            :src="product.image || 'https://via.placeholder.com/300x300?text=No+Image'"
            height="220"
            cover
            class="product-image"
          >
            <template v-slot:placeholder>
              <div class="d-flex align-center justify-center fill-height">
                <v-progress-circular indeterminate color="primary" size="40"></v-progress-circular>
              </div>
            </template>
          </v-img>
        </router-link>
        
        <!-- Floating Badges -->
        <div class="badge-container">
          <div class="badge-left">
            <span v-if="product.discount_percentage > 0" class="discount-badge">
              -{{ product.discount_percentage }}%
            </span>
          </div>
          <div class="badge-right">
            <span v-if="product.is_featured" class="featured-badge">
              <v-icon size="14">mdi-star</v-icon>
            </span>
          </div>
        </div>
        
        <!-- Quick Actions Overlay -->
        <div class="quick-actions">
          <button class="action-btn" @click.prevent="handleQuickView" title="Quick View">
            <v-icon size="20">mdi-eye</v-icon>
          </button>
          <button class="action-btn" @click.prevent="handleWishlist" title="Add to Wishlist">
            <v-icon size="20">mdi-heart-outline</v-icon>
          </button>
        </div>
      </div>

      <!-- Card Content -->
      <v-card-text class="card-content flex-grow-1 pa-4">
        <!-- Category -->
        <div class="category-tag mb-2">
          {{ product.category_name || 'General' }}
        </div>
        
        <!-- Product Name -->
        <router-link 
          :to="`/products/${product.slug}`" 
          class="text-decoration-none"
        >
          <h3 class="product-title mb-3">
            {{ product.name }}
          </h3>
        </router-link>

        <!-- Price Section -->
        <div class="price-section mb-3">
          <span v-if="product.discount_price" class="original-price">
            ₹{{ formatPrice(product.price) }}
          </span>
          <span class="current-price" :class="{ 'discounted': product.discount_price }">
            ₹{{ formatPrice(product.final_price) }}
          </span>
        </div>

        <!-- Stock & Brand Info -->
        <div class="meta-info d-flex align-center justify-space-between">
          <span class="stock-status" :class="product.in_stock ? 'in-stock' : 'out-of-stock'">
            <v-icon size="12" class="mr-1">{{ product.in_stock ? 'mdi-check-circle' : 'mdi-close-circle' }}</v-icon>
            {{ product.in_stock ? 'In Stock' : 'Out of Stock' }}
          </span>
          <span v-if="product.brand" class="brand-name">
            {{ product.brand }}
          </span>
        </div>
      </v-card-text>

      <!-- Add to Cart Button -->
      <div class="card-actions pa-4 pt-0">
        <button
          class="add-to-cart-btn"
          :class="{ 'disabled': !product.in_stock || loading }"
          :disabled="!product.in_stock || loading"
          @click.prevent="handleAddToCart"
        >
          <span v-if="loading" class="loading-spinner"></span>
          <template v-else>
            <v-icon size="18" class="mr-2">mdi-shopping</v-icon>
            Add to Cart
          </template>
        </button>
      </div>
    </v-card>
  </div>
</template>

<script setup>
import { ref, inject } from 'vue'
import { useCartStore } from '@/stores/cart'
import { useProductStore } from '@/stores/products'
import { useRouter } from 'vue-router'

const props = defineProps({
  product: {
    type: Object,
    required: true
  }
})

const router = useRouter()
const cartStore = useCartStore()
const productStore = useProductStore()
const showSnackbar = inject('showSnackbar')
const loading = ref(false)

const formatPrice = (price) => {
  return parseFloat(price).toLocaleString('en-IN')
}

const handleAddToCart = async () => {
  if (!props.product.in_stock) return
  
  loading.value = true
  
  // Backend automatically tracks 'add_to_cart' interaction
  const result = await cartStore.addToCart(props.product.id, 1)
  
  if (result.success) {
    showSnackbar('Added to cart successfully!', 'success')
  } else {
    showSnackbar(result.error, 'error')
  }
  
  loading.value = false
}

const handleQuickView = () => {
  router.push(`/products/${props.product.slug}`)
}

const handleWishlist = () => {
  showSnackbar('Added to wishlist!', 'success')
}
</script>

<style scoped>
.product-card-wrapper {
  height: 100%;
}

.product-card {
  background: rgba(30, 30, 46, 0.6);
  backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.05);
  border-radius: 20px;
  overflow: hidden;
  transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
  position: relative;
}

.product-card::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 3px;
  background: linear-gradient(90deg, #6366F1, #8B5CF6, #EC4899);
  opacity: 0;
  transition: opacity 0.3s ease;
}

.product-card:hover {
  transform: translateY(-8px);
  box-shadow: 0 20px 40px rgba(99, 102, 241, 0.2);
  border-color: rgba(99, 102, 241, 0.3);
}

.product-card:hover::before {
  opacity: 1;
}

/* Image Container */
.image-container {
  position: relative;
  overflow: hidden;
  background: rgba(20, 20, 35, 0.5);
}

.product-image {
  transition: transform 0.5s ease;
}

.product-card:hover .product-image {
  transform: scale(1.08);
}

/* Badges */
.badge-container {
  position: absolute;
  top: 12px;
  left: 12px;
  right: 12px;
  display: flex;
  justify-content: space-between;
  z-index: 2;
}

.discount-badge {
  background: linear-gradient(135deg, #EF4444, #DC2626);
  color: white;
  padding: 6px 12px;
  border-radius: 20px;
  font-size: 12px;
  font-weight: 700;
  box-shadow: 0 4px 15px rgba(239, 68, 68, 0.4);
}

.featured-badge {
  background: linear-gradient(135deg, #F59E0B, #D97706);
  color: white;
  width: 32px;
  height: 32px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 4px 15px rgba(245, 158, 11, 0.4);
}

/* Quick Actions */
.quick-actions {
  position: absolute;
  bottom: -50px;
  left: 50%;
  transform: translateX(-50%);
  display: flex;
  gap: 10px;
  transition: all 0.3s ease;
  opacity: 0;
}

.product-card:hover .quick-actions {
  bottom: 15px;
  opacity: 1;
}

.action-btn {
  width: 42px;
  height: 42px;
  border-radius: 50%;
  background: rgba(255, 255, 255, 0.95);
  border: none;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.3s ease;
  color: #1e1e2e;
}

.action-btn:hover {
  background: linear-gradient(135deg, #6366F1, #8B5CF6);
  color: white;
  transform: scale(1.1);
}

/* Card Content */
.card-content {
  background: transparent;
}

.category-tag {
  display: inline-block;
  font-size: 11px;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 1px;
  color: #8B5CF6;
  background: rgba(139, 92, 246, 0.1);
  padding: 4px 10px;
  border-radius: 20px;
}

.product-title {
  font-size: 16px;
  font-weight: 600;
  color: #ffffff;
  line-height: 1.4;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
  min-height: 44px;
  transition: color 0.3s ease;
}

.product-title:hover {
  color: #8B5CF6;
}

/* Price Section */
.price-section {
  display: flex;
  align-items: center;
  gap: 10px;
}

.original-price {
  font-size: 14px;
  color: rgba(255, 255, 255, 0.4);
  text-decoration: line-through;
}

.current-price {
  font-size: 22px;
  font-weight: 700;
  background: linear-gradient(135deg, #6366F1, #8B5CF6);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.current-price.discounted {
  background: linear-gradient(135deg, #EF4444, #EC4899);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

/* Meta Info */
.meta-info {
  font-size: 12px;
}

.stock-status {
  display: flex;
  align-items: center;
  font-weight: 500;
}

.stock-status.in-stock {
  color: #10B981;
}

.stock-status.out-of-stock {
  color: #EF4444;
}

.brand-name {
  color: rgba(255, 255, 255, 0.5);
  font-weight: 500;
}

/* Add to Cart Button */
.add-to-cart-btn {
  width: 100%;
  padding: 14px 24px;
  border: none;
  border-radius: 12px;
  background: linear-gradient(135deg, #6366F1, #8B5CF6);
  color: white;
  font-size: 14px;
  font-weight: 600;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.3s ease;
  position: relative;
  overflow: hidden;
}

.add-to-cart-btn::before {
  content: '';
  position: absolute;
  top: 0;
  left: -100%;
  width: 100%;
  height: 100%;
  background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.2), transparent);
  transition: left 0.5s ease;
}

.add-to-cart-btn:hover:not(.disabled)::before {
  left: 100%;
}

.add-to-cart-btn:hover:not(.disabled) {
  transform: translateY(-2px);
  box-shadow: 0 10px 30px rgba(99, 102, 241, 0.4);
}

.add-to-cart-btn.disabled {
  background: rgba(100, 100, 120, 0.3);
  cursor: not-allowed;
  color: rgba(255, 255, 255, 0.4);
}

.loading-spinner {
  width: 20px;
  height: 20px;
  border: 2px solid rgba(255, 255, 255, 0.3);
  border-top-color: white;
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
}

@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}
</style>
