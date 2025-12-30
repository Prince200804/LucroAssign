<template>
  <div class="cart-page">
    <!-- Page Header -->
    <div class="page-hero">
      <div class="hero-bg"></div>
      <v-container>
        <div class="hero-content">
          <h1 class="page-title">
            <v-icon size="40" class="mr-3">mdi-cart</v-icon>
            Shopping <span class="gradient-text">Cart</span>
          </h1>
          <p class="page-subtitle" v-if="items.length > 0">
            You have {{ totalItems }} item{{ totalItems > 1 ? 's' : '' }} in your cart
          </p>
        </div>
      </v-container>
    </div>

    <v-container class="py-8">
      <!-- Empty Cart -->
      <div v-if="!loading && items.length === 0" class="empty-cart">
        <div class="empty-icon">
          <v-icon size="80">mdi-cart-outline</v-icon>
        </div>
        <h2>Your Cart is Empty</h2>
        <p>Looks like you haven't added any items to your cart yet.</p>
        <router-link to="/products" class="shop-btn">
          <v-icon size="20" class="mr-2">mdi-shopping</v-icon>
          Start Shopping
        </router-link>
      </div>

      <v-row v-else>
        <!-- Cart Items -->
        <v-col cols="12" lg="8">
          <div class="cart-section">
            <div class="section-header">
              <h2>Cart Items</h2>
              <button class="clear-btn" @click="handleClearCart">
                <v-icon size="18" class="mr-1">mdi-delete-outline</v-icon>
                Clear All
              </button>
            </div>

            <!-- Loading State -->
            <div v-if="loading" class="cart-items">
              <div v-for="n in 3" :key="n" class="cart-item skeleton">
                <div class="skeleton-img"></div>
                <div class="skeleton-content">
                  <div class="skeleton-line"></div>
                  <div class="skeleton-line short"></div>
                </div>
              </div>
            </div>

            <!-- Cart Items List -->
            <div v-else class="cart-items">
              <div v-for="item in items" :key="item.id" class="cart-item">
                <router-link :to="`/products/${item.product.slug}`" class="item-image">
                  <img :src="item.product.image || 'https://via.placeholder.com/120x120'" :alt="item.product.name" />
                </router-link>

                <div class="item-details">
                  <router-link :to="`/products/${item.product.slug}`" class="item-name">
                    {{ item.product.name }}
                  </router-link>
                  <span class="item-category">{{ item.product.category_name }}</span>
                  <div class="item-price">₹{{ formatPrice(item.unit_price) }}</div>
                </div>

                <div class="item-quantity">
                  <button 
                    class="qty-btn" 
                    :disabled="item.quantity <= 1"
                    @click="updateQuantity(item, item.quantity - 1)"
                  >
                    <v-icon size="18">mdi-minus</v-icon>
                  </button>
                  <span class="qty-value">{{ item.quantity }}</span>
                  <button 
                    class="qty-btn"
                    @click="updateQuantity(item, item.quantity + 1)"
                  >
                    <v-icon size="18">mdi-plus</v-icon>
                  </button>
                </div>

                <div class="item-total">
                  ₹{{ formatPrice(item.total_price) }}
                </div>

                <button class="remove-btn" @click="removeItem(item)">
                  <v-icon size="20">mdi-close</v-icon>
                </button>
              </div>
            </div>
          </div>
        </v-col>

        <!-- Order Summary -->
        <v-col cols="12" lg="4">
          <div class="summary-card">
            <h3 class="summary-title">Order Summary</h3>
            
            <div class="summary-rows">
              <div class="summary-row">
                <span>Subtotal ({{ totalItems }} items)</span>
                <span>₹{{ formatPrice(subtotal) }}</span>
              </div>
              <div class="summary-row">
                <span>Shipping</span>
                <span class="free-shipping">FREE</span>
              </div>
              <div class="summary-row">
                <span>Tax</span>
                <span>₹0</span>
              </div>
            </div>

            <div class="summary-total">
              <span>Total</span>
              <span class="total-amount">₹{{ formatPrice(total) }}</span>
            </div>

            <router-link 
              to="/checkout" 
              class="checkout-btn"
              :class="{ disabled: items.length === 0 }"
            >
              Proceed to Checkout
              <v-icon size="20" class="ml-2">mdi-arrow-right</v-icon>
            </router-link>

            <router-link to="/products" class="continue-link">
              <v-icon size="18" class="mr-2">mdi-arrow-left</v-icon>
              Continue Shopping
            </router-link>

            <!-- Promo Code -->
            <div class="promo-section">
              <label>Have a promo code?</label>
              <div class="promo-input">
                <input type="text" placeholder="Enter code" />
                <button>Apply</button>
              </div>
            </div>

            <!-- Trust Badges -->
            <div class="trust-badges">
              <div class="badge">
                <v-icon size="24">mdi-shield-check</v-icon>
                <span>Secure Checkout</span>
              </div>
              <div class="badge">
                <v-icon size="24">mdi-truck-fast</v-icon>
                <span>Free Shipping</span>
              </div>
              <div class="badge">
                <v-icon size="24">mdi-refresh</v-icon>
                <span>Easy Returns</span>
              </div>
            </div>
          </div>
        </v-col>
      </v-row>
    </v-container>
  </div>
</template>

<script setup>
import { computed, inject, onMounted } from 'vue'
import { useCartStore } from '@/stores/cart'

const cartStore = useCartStore()
const showSnackbar = inject('showSnackbar')

const loading = computed(() => cartStore.loading)
const items = computed(() => cartStore.items)
const totalItems = computed(() => cartStore.totalItems)
const subtotal = computed(() => cartStore.subtotal)
const total = computed(() => cartStore.total)

const formatPrice = (price) => {
  return parseFloat(price).toLocaleString('en-IN')
}

const updateQuantity = async (item, newQuantity) => {
  const result = await cartStore.updateCartItem(item.id, newQuantity)
  if (!result.success) {
    showSnackbar(result.error, 'error')
  }
}

const removeItem = async (item) => {
  const result = await cartStore.removeFromCart(item.id)
  if (result.success) {
    showSnackbar('Item removed from cart', 'success')
  } else {
    showSnackbar(result.error, 'error')
  }
}

const handleClearCart = async () => {
  const result = await cartStore.clearCart()
  if (result.success) {
    showSnackbar('Cart cleared', 'success')
  } else {
    showSnackbar(result.error, 'error')
  }
}

onMounted(() => {
  cartStore.fetchCart()
})
</script>

<style scoped>
.cart-page {
  min-height: 100vh;
}

/* Page Hero */
.page-hero {
  position: relative;
  padding: 60px 0 40px;
  overflow: hidden;
}

.hero-bg {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: linear-gradient(135deg, rgba(99, 102, 241, 0.1), rgba(139, 92, 246, 0.1));
}

.hero-content {
  position: relative;
  z-index: 1;
}

.page-title {
  font-size: 2.5rem;
  font-weight: 700;
  color: #ffffff;
  display: flex;
  align-items: center;
  margin-bottom: 8px;
}

.gradient-text {
  background: linear-gradient(135deg, #6366F1, #8B5CF6, #EC4899);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.page-subtitle {
  color: rgba(255, 255, 255, 0.7);
  font-size: 1.1rem;
}

/* Empty Cart */
.empty-cart {
  text-align: center;
  padding: 80px 40px;
  background: rgba(30, 30, 46, 0.6);
  backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.05);
  border-radius: 24px;
}

.empty-icon {
  width: 140px;
  height: 140px;
  margin: 0 auto 32px;
  background: rgba(99, 102, 241, 0.1);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #6366F1;
}

.empty-cart h2 {
  font-size: 1.8rem;
  font-weight: 700;
  color: #ffffff;
  margin-bottom: 12px;
}

.empty-cart p {
  color: rgba(255, 255, 255, 0.6);
  margin-bottom: 32px;
}

.shop-btn {
  display: inline-flex;
  align-items: center;
  padding: 16px 32px;
  background: linear-gradient(135deg, #6366F1, #8B5CF6);
  border-radius: 12px;
  color: white;
  font-weight: 600;
  text-decoration: none;
  transition: all 0.3s ease;
}

.shop-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 10px 30px rgba(99, 102, 241, 0.4);
}

/* Cart Section */
.cart-section {
  background: rgba(30, 30, 46, 0.6);
  backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.05);
  border-radius: 20px;
  padding: 24px;
}

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 24px;
  padding-bottom: 16px;
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
}

.section-header h2 {
  font-size: 1.3rem;
  font-weight: 600;
  color: #ffffff;
}

.clear-btn {
  display: flex;
  align-items: center;
  padding: 8px 16px;
  background: rgba(239, 68, 68, 0.1);
  border: 1px solid rgba(239, 68, 68, 0.3);
  border-radius: 8px;
  color: #EF4444;
  font-size: 14px;
  cursor: pointer;
  transition: all 0.3s ease;
}

.clear-btn:hover {
  background: rgba(239, 68, 68, 0.2);
}

/* Cart Items */
.cart-items {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.cart-item {
  display: grid;
  grid-template-columns: 100px 1fr auto auto auto;
  gap: 20px;
  align-items: center;
  padding: 20px;
  background: rgba(255, 255, 255, 0.02);
  border: 1px solid rgba(255, 255, 255, 0.05);
  border-radius: 16px;
  transition: all 0.3s ease;
}

.cart-item:hover {
  background: rgba(255, 255, 255, 0.05);
  border-color: rgba(99, 102, 241, 0.2);
}

@media (max-width: 768px) {
  .cart-item {
    grid-template-columns: 80px 1fr;
    gap: 16px;
  }
  .item-quantity, .item-total {
    grid-column: span 2;
  }
  .remove-btn {
    position: absolute;
    top: 10px;
    right: 10px;
  }
  .cart-item {
    position: relative;
  }
}

.item-image {
  width: 100px;
  height: 100px;
  border-radius: 12px;
  overflow: hidden;
  background: rgba(255, 255, 255, 0.05);
}

.item-image img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: transform 0.3s ease;
}

.item-image:hover img {
  transform: scale(1.1);
}

.item-details {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.item-name {
  font-size: 16px;
  font-weight: 600;
  color: #ffffff;
  text-decoration: none;
  transition: color 0.3s ease;
}

.item-name:hover {
  color: #8B5CF6;
}

.item-category {
  font-size: 13px;
  color: rgba(255, 255, 255, 0.5);
}

.item-price {
  font-size: 15px;
  font-weight: 600;
  color: #8B5CF6;
}

/* Quantity Controls */
.item-quantity {
  display: flex;
  align-items: center;
  gap: 12px;
}

.qty-btn {
  width: 36px;
  height: 36px;
  border-radius: 10px;
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid rgba(255, 255, 255, 0.1);
  color: #ffffff;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.3s ease;
}

.qty-btn:hover:not(:disabled) {
  background: rgba(99, 102, 241, 0.2);
  border-color: #6366F1;
}

.qty-btn:disabled {
  opacity: 0.4;
  cursor: not-allowed;
}

.qty-value {
  font-size: 16px;
  font-weight: 600;
  color: #ffffff;
  min-width: 30px;
  text-align: center;
}

.item-total {
  font-size: 18px;
  font-weight: 700;
  color: #ffffff;
  min-width: 100px;
  text-align: right;
}

.remove-btn {
  width: 40px;
  height: 40px;
  border-radius: 10px;
  background: rgba(239, 68, 68, 0.1);
  border: none;
  color: #EF4444;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.3s ease;
}

.remove-btn:hover {
  background: rgba(239, 68, 68, 0.2);
}

/* Summary Card */
.summary-card {
  background: rgba(30, 30, 46, 0.6);
  backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.05);
  border-radius: 20px;
  padding: 28px;
  position: sticky;
  top: 100px;
}

.summary-title {
  font-size: 1.3rem;
  font-weight: 600;
  color: #ffffff;
  margin-bottom: 24px;
  padding-bottom: 16px;
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
}

.summary-rows {
  display: flex;
  flex-direction: column;
  gap: 14px;
  margin-bottom: 20px;
}

.summary-row {
  display: flex;
  justify-content: space-between;
  font-size: 15px;
  color: rgba(255, 255, 255, 0.7);
}

.free-shipping {
  color: #10B981;
  font-weight: 600;
}

.summary-total {
  display: flex;
  justify-content: space-between;
  padding: 20px 0;
  border-top: 1px solid rgba(255, 255, 255, 0.1);
  margin-bottom: 24px;
}

.summary-total span:first-child {
  font-size: 18px;
  font-weight: 600;
  color: #ffffff;
}

.total-amount {
  font-size: 24px;
  font-weight: 700;
  background: linear-gradient(135deg, #6366F1, #8B5CF6);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.checkout-btn {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 100%;
  padding: 16px;
  background: linear-gradient(135deg, #6366F1, #8B5CF6);
  border-radius: 12px;
  color: white;
  font-size: 16px;
  font-weight: 600;
  text-decoration: none;
  transition: all 0.3s ease;
  margin-bottom: 16px;
}

.checkout-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 10px 30px rgba(99, 102, 241, 0.4);
}

.checkout-btn.disabled {
  opacity: 0.5;
  pointer-events: none;
}

.continue-link {
  display: flex;
  align-items: center;
  justify-content: center;
  color: rgba(255, 255, 255, 0.7);
  font-size: 14px;
  text-decoration: none;
  margin-bottom: 28px;
  transition: color 0.3s ease;
}

.continue-link:hover {
  color: #8B5CF6;
}

/* Promo Section */
.promo-section {
  padding-top: 20px;
  border-top: 1px solid rgba(255, 255, 255, 0.1);
  margin-bottom: 24px;
}

.promo-section label {
  display: block;
  font-size: 13px;
  font-weight: 500;
  color: rgba(255, 255, 255, 0.6);
  margin-bottom: 10px;
}

.promo-input {
  display: flex;
  gap: 10px;
}

.promo-input input {
  flex: 1;
  padding: 12px 16px;
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 10px;
  color: #ffffff;
  font-size: 14px;
}

.promo-input input:focus {
  outline: none;
  border-color: #6366F1;
}

.promo-input button {
  padding: 12px 20px;
  background: rgba(99, 102, 241, 0.2);
  border: 1px solid rgba(99, 102, 241, 0.3);
  border-radius: 10px;
  color: #8B5CF6;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
}

.promo-input button:hover {
  background: rgba(99, 102, 241, 0.3);
}

/* Trust Badges */
.trust-badges {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 12px;
  padding-top: 20px;
  border-top: 1px solid rgba(255, 255, 255, 0.1);
}

.badge {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 6px;
  text-align: center;
  color: rgba(255, 255, 255, 0.6);
}

.badge .v-icon {
  color: #10B981;
}

.badge span {
  font-size: 11px;
}

/* Skeleton Loading */
.skeleton {
  pointer-events: none;
}

.skeleton-img {
  width: 100px;
  height: 100px;
  border-radius: 12px;
  background: linear-gradient(90deg, rgba(255, 255, 255, 0.05), rgba(255, 255, 255, 0.1), rgba(255, 255, 255, 0.05));
  background-size: 200% 100%;
  animation: shimmer 1.5s infinite;
}

.skeleton-content {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.skeleton-line {
  height: 16px;
  background: linear-gradient(90deg, rgba(255, 255, 255, 0.05), rgba(255, 255, 255, 0.1), rgba(255, 255, 255, 0.05));
  background-size: 200% 100%;
  animation: shimmer 1.5s infinite;
  border-radius: 8px;
}

.skeleton-line.short {
  width: 60%;
}

@keyframes shimmer {
  0% { background-position: 200% 0; }
  100% { background-position: -200% 0; }
}
</style>
