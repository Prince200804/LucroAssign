<template>
  <v-container class="py-8">
    <h1 class="text-h4 font-weight-bold mb-6">Checkout</h1>

    <!-- Empty Cart Warning -->
    <v-card v-if="items.length === 0" class="pa-8 text-center">
      <v-icon size="64" color="warning">mdi-cart-off</v-icon>
      <h2 class="text-h5 mt-4 mb-2">Your cart is empty</h2>
      <p class="text-body-2 text-grey mb-4">
        Add some items to your cart before checkout.
      </p>
      <v-btn color="primary" to="/products">Continue Shopping</v-btn>
    </v-card>

    <v-row v-else>
      <!-- Checkout Form -->
      <v-col cols="12" md="8">
        <v-form ref="formRef" v-model="formValid" @submit.prevent="handleCheckout">
          <!-- Contact Information -->
          <v-card class="mb-4">
            <v-card-title>
              <v-icon class="mr-2">mdi-account</v-icon>
              Contact Information
            </v-card-title>
            <v-card-text>
              <v-row>
                <v-col cols="12" sm="6">
                  <v-text-field
                    v-model="form.first_name"
                    label="First Name"
                    :rules="[rules.required]"
                    prepend-inner-icon="mdi-account"
                  ></v-text-field>
                </v-col>
                <v-col cols="12" sm="6">
                  <v-text-field
                    v-model="form.last_name"
                    label="Last Name"
                    :rules="[rules.required]"
                    prepend-inner-icon="mdi-account"
                  ></v-text-field>
                </v-col>
                <v-col cols="12" sm="6">
                  <v-text-field
                    v-model="form.email"
                    label="Email"
                    type="email"
                    :rules="[rules.required, rules.email]"
                    prepend-inner-icon="mdi-email"
                  ></v-text-field>
                </v-col>
                <v-col cols="12" sm="6">
                  <v-text-field
                    v-model="form.phone"
                    label="Phone"
                    :rules="[rules.required]"
                    prepend-inner-icon="mdi-phone"
                  ></v-text-field>
                </v-col>
              </v-row>
            </v-card-text>
          </v-card>

          <!-- Shipping Address -->
          <v-card class="mb-4">
            <v-card-title>
              <v-icon class="mr-2">mdi-truck</v-icon>
              Shipping Address
            </v-card-title>
            <v-card-text>
              <v-row>
                <v-col cols="12">
                  <v-textarea
                    v-model="form.shipping_address"
                    label="Street Address"
                    :rules="[rules.required]"
                    rows="2"
                    prepend-inner-icon="mdi-map-marker"
                  ></v-textarea>
                </v-col>
                <v-col cols="12" sm="6">
                  <v-text-field
                    v-model="form.shipping_city"
                    label="City"
                    :rules="[rules.required]"
                    prepend-inner-icon="mdi-city"
                  ></v-text-field>
                </v-col>
                <v-col cols="12" sm="6">
                  <v-text-field
                    v-model="form.shipping_state"
                    label="State"
                    :rules="[rules.required]"
                    prepend-inner-icon="mdi-map"
                  ></v-text-field>
                </v-col>
                <v-col cols="12" sm="6">
                  <v-text-field
                    v-model="form.shipping_zip"
                    label="ZIP Code"
                    :rules="[rules.required]"
                    prepend-inner-icon="mdi-mailbox"
                  ></v-text-field>
                </v-col>
                <v-col cols="12" sm="6">
                  <v-text-field
                    v-model="form.shipping_country"
                    label="Country"
                    :rules="[rules.required]"
                    prepend-inner-icon="mdi-earth"
                  ></v-text-field>
                </v-col>
              </v-row>
            </v-card-text>
          </v-card>

          <!-- Order Notes -->
          <v-card class="mb-4">
            <v-card-title>
              <v-icon class="mr-2">mdi-note</v-icon>
              Order Notes (Optional)
            </v-card-title>
            <v-card-text>
              <v-textarea
                v-model="form.notes"
                label="Special instructions or notes"
                rows="3"
                hide-details
              ></v-textarea>
            </v-card-text>
          </v-card>

          <!-- Payment Method -->
          <v-card>
            <v-card-title>
              <v-icon class="mr-2">mdi-credit-card</v-icon>
              Payment Method
            </v-card-title>
            <v-card-text>
              <v-radio-group v-model="paymentMethod">
                <v-radio value="stripe">
                  <template v-slot:label>
                    <div class="d-flex align-center">
                      <v-icon class="mr-2" color="primary">mdi-credit-card-outline</v-icon>
                      <div>
                        <span class="font-weight-medium">Pay with Stripe</span>
                        <p class="text-caption text-grey ma-0">Credit/Debit Card (Secure Payment)</p>
                      </div>
                    </div>
                  </template>
                </v-radio>
                <v-radio value="cod">
                  <template v-slot:label>
                    <div class="d-flex align-center">
                      <v-icon class="mr-2" color="success">mdi-cash</v-icon>
                      <div>
                        <span class="font-weight-medium">Cash on Delivery</span>
                        <p class="text-caption text-grey ma-0">Pay when you receive your order</p>
                      </div>
                    </div>
                  </template>
                </v-radio>
              </v-radio-group>

              <!-- Stripe Card Element -->
              <div v-if="paymentMethod === 'stripe'" class="mt-4">
                <v-alert type="info" variant="tonal" class="mb-4">
                  <v-icon>mdi-shield-check</v-icon>
                  Secure payment powered by Stripe. Test card: 4242 4242 4242 4242 (any future expiry, any CVC)
                </v-alert>
                
                <div id="stripe-card-element" class="stripe-card-element pa-4 rounded border"></div>
                <p v-if="stripeError" class="text-error text-caption mt-2">{{ stripeError }}</p>
              </div>
            </v-card-text>
          </v-card>
        </v-form>
      </v-col>

      <!-- Order Summary -->
      <v-col cols="12" md="4">
        <v-card class="sticky-summary">
          <v-card-title>Order Summary</v-card-title>
          <v-divider></v-divider>
          
          <!-- Items Preview -->
          <v-list density="compact">
            <v-list-item v-for="item in items" :key="item.id">
              <template v-slot:prepend>
                <v-img
                  :src="item.product.image || 'https://via.placeholder.com/50'"
                  width="50"
                  height="50"
                  cover
                  class="rounded mr-2"
                ></v-img>
              </template>
              <v-list-item-title class="text-body-2">
                {{ item.product.name }}
              </v-list-item-title>
              <v-list-item-subtitle>
                {{ item.quantity }} × ₹{{ formatPrice(item.unit_price) }}
              </v-list-item-subtitle>
              <template v-slot:append>
                <span class="font-weight-medium">₹{{ formatPrice(item.total_price) }}</span>
              </template>
            </v-list-item>
          </v-list>

          <v-divider></v-divider>

          <v-card-text>
            <div class="d-flex justify-space-between mb-2">
              <span>Subtotal</span>
              <span>₹{{ formatPrice(subtotal) }}</span>
            </div>
            <div class="d-flex justify-space-between mb-2">
              <span>Shipping</span>
              <span class="text-success">Free</span>
            </div>
            <div class="d-flex justify-space-between mb-2">
              <span>Tax</span>
              <span>₹0</span>
            </div>
            
            <v-divider class="my-4"></v-divider>
            
            <div class="d-flex justify-space-between">
              <span class="text-h6 font-weight-bold">Total</span>
              <span class="text-h6 font-weight-bold text-primary">
                ₹{{ formatPrice(total) }}
              </span>
            </div>
          </v-card-text>

          <v-card-actions class="pa-4">
            <v-btn
              color="primary"
              size="large"
              block
              :loading="submitting"
              :disabled="!formValid || items.length === 0"
              @click="handleCheckout"
            >
              <v-icon left>{{ paymentMethod === 'stripe' ? 'mdi-credit-card' : 'mdi-check' }}</v-icon>
              {{ paymentMethod === 'stripe' ? 'Pay Now' : 'Place Order' }}
            </v-btn>
          </v-card-actions>
        </v-card>
      </v-col>
    </v-row>

    <!-- Success Dialog -->
    <v-dialog v-model="showSuccessDialog" max-width="500" persistent>
      <v-card class="text-center pa-6">
        <v-icon size="80" color="success" class="mb-4">mdi-check-circle</v-icon>
        <h2 class="text-h5 font-weight-bold mb-2">Order Placed Successfully!</h2>
        <p class="text-body-1 text-grey mb-2">
          Your order number is:
        </p>
        <p class="text-h6 font-weight-bold text-primary mb-4">
          {{ orderNumber }}
        </p>
        <p class="text-body-2 text-grey mb-6">
          {{ paymentMethod === 'stripe' ? 'Payment successful! ' : '' }}We've sent a confirmation to your email. Thank you for shopping with us!
        </p>
        <div class="d-flex gap-2 justify-center">
          <v-btn variant="outlined" @click="trackOrder">
            <v-icon left>mdi-truck-delivery</v-icon>
            Track Order
          </v-btn>
          <v-btn color="primary" @click="goToOrders">
            View My Orders
          </v-btn>
        </div>
      </v-card>
    </v-dialog>

    <!-- Payment Processing Dialog -->
    <v-dialog v-model="showProcessingDialog" max-width="400" persistent>
      <v-card class="text-center pa-6">
        <v-progress-circular indeterminate color="primary" size="64" class="mb-4"></v-progress-circular>
        <h3 class="text-h6 font-weight-bold">Processing Payment...</h3>
        <p class="text-body-2 text-grey">Please don't close this window</p>
      </v-card>
    </v-dialog>
  </v-container>
</template>

<script setup>
import { ref, computed, inject, onMounted, watch, nextTick } from 'vue'
import { useRouter } from 'vue-router'
import { useCartStore } from '@/stores/cart'
import { useAuthStore } from '@/stores/auth'
import api from '@/services/api'

const router = useRouter()
const cartStore = useCartStore()
const authStore = useAuthStore()
const showSnackbar = inject('showSnackbar')

const formRef = ref(null)
const formValid = ref(false)
const submitting = ref(false)
const showSuccessDialog = ref(false)
const showProcessingDialog = ref(false)
const orderNumber = ref('')
const paymentMethod = ref('stripe')
const stripeError = ref('')

// Stripe elements
let stripe = null
let cardElement = null
let stripeClientSecret = ref('')
let stripePaymentIntentId = ref('')

const form = ref({
  first_name: '',
  last_name: '',
  email: '',
  phone: '',
  shipping_address: '',
  shipping_city: '',
  shipping_state: '',
  shipping_zip: '',
  shipping_country: 'India',
  notes: '',
})

const rules = {
  required: v => !!v || 'This field is required',
  email: v => /.+@.+\..+/.test(v) || 'Please enter a valid email',
}

const items = computed(() => cartStore.items)
const subtotal = computed(() => cartStore.subtotal)
const total = computed(() => cartStore.total)

const formatPrice = (price) => {
  return parseFloat(price).toLocaleString('en-IN')
}

// Load Stripe script
const loadStripeScript = () => {
  return new Promise((resolve) => {
    if (window.Stripe) {
      resolve(true)
      return
    }
    const script = document.createElement('script')
    script.src = 'https://js.stripe.com/v3/'
    script.onload = () => resolve(true)
    script.onerror = () => resolve(false)
    document.body.appendChild(script)
  })
}

// Initialize Stripe Elements
const initStripeElements = async (publishableKey) => {
  if (!window.Stripe) return
  
  stripe = window.Stripe(publishableKey)
  const elements = stripe.elements()
  
  cardElement = elements.create('card', {
    style: {
      base: {
        fontSize: '16px',
        color: '#424770',
        '::placeholder': {
          color: '#aab7c4',
        },
      },
      invalid: {
        color: '#9e2146',
      },
    },
  })
  
  // Wait for DOM element to exist
  await nextTick()
  const cardContainer = document.getElementById('stripe-card-element')
  if (cardContainer) {
    cardElement.mount('#stripe-card-element')
    cardElement.on('change', (event) => {
      stripeError.value = event.error ? event.error.message : ''
    })
  }
}

// Watch payment method changes to mount/unmount card element
watch(paymentMethod, async (newMethod) => {
  if (newMethod === 'stripe' && stripe) {
    await nextTick()
    const cardContainer = document.getElementById('stripe-card-element')
    if (cardContainer && cardElement) {
      cardElement.mount('#stripe-card-element')
    }
  }
})

const handleCheckout = async () => {
  const { valid } = await formRef.value.validate()
  if (!valid) return

  if (paymentMethod.value === 'stripe') {
    await processStripePayment()
  } else {
    await processCODOrder()
  }
}

const processStripePayment = async () => {
  submitting.value = true
  stripeError.value = ''

  try {
    // Create Payment Intent
    const intentResponse = await api.post('/orders/stripe/create-payment-intent/')
    const { client_secret, payment_intent_id, publishable_key } = intentResponse.data
    
    stripeClientSecret.value = client_secret
    stripePaymentIntentId.value = payment_intent_id
    
    // Initialize Stripe if not already done
    if (!stripe) {
      await loadStripeScript()
      await initStripeElements(publishable_key)
      await nextTick()
    }
    
    // Confirm payment
    showProcessingDialog.value = true
    
    const { error, paymentIntent } = await stripe.confirmCardPayment(client_secret, {
      payment_method: {
        card: cardElement,
        billing_details: {
          name: `${form.value.first_name} ${form.value.last_name}`,
          email: form.value.email,
          phone: form.value.phone,
          address: {
            line1: form.value.shipping_address,
            city: form.value.shipping_city,
            state: form.value.shipping_state,
            postal_code: form.value.shipping_zip,
            country: 'IN'
          }
        }
      }
    })
    
    if (error) {
      showProcessingDialog.value = false
      stripeError.value = error.message
      showSnackbar(error.message, 'error')
      submitting.value = false
      return
    }
    
    if (paymentIntent.status === 'succeeded') {
      // Create order with successful payment
      const orderResponse = await api.post('/orders/create/', {
        ...form.value,
        payment_method: 'stripe',
        stripe_payment_intent_id: payment_intent_id
      })
      
      orderNumber.value = orderResponse.data.order_number
      showProcessingDialog.value = false
      showSuccessDialog.value = true
      
      // Refresh cart
      await cartStore.fetchCart()
    }
  } catch (error) {
    showProcessingDialog.value = false
    showSnackbar(error.response?.data?.error || 'Payment failed', 'error')
  } finally {
    submitting.value = false
  }
}

const processCODOrder = async () => {
  submitting.value = true

  try {
    const response = await api.post('/orders/create/', {
      ...form.value,
      payment_method: 'cod'
    })
    orderNumber.value = response.data.order_number
    showSuccessDialog.value = true
    
    // Refresh cart
    await cartStore.fetchCart()
  } catch (error) {
    showSnackbar(error.response?.data?.error || 'Failed to place order', 'error')
  } finally {
    submitting.value = false
  }
}

const trackOrder = () => {
  showSuccessDialog.value = false
  router.push(`/track-order?order=${orderNumber.value}`)
}

const goToOrders = () => {
  showSuccessDialog.value = false
  if (authStore.isAuthenticated) {
    router.push('/orders')
  } else {
    router.push('/')
  }
}

onMounted(async () => {
  // Pre-fill form if user is authenticated
  if (authStore.user) {
    form.value = {
      ...form.value,
      first_name: authStore.user.first_name || '',
      last_name: authStore.user.last_name || '',
      email: authStore.user.email || '',
      phone: authStore.user.phone || '',
      shipping_address: authStore.user.address || '',
      shipping_city: authStore.user.city || '',
      shipping_state: authStore.user.state || '',
      shipping_zip: authStore.user.zip_code || '',
      shipping_country: authStore.user.country || 'India',
    }
  }

  // Preload Stripe script and get publishable key
  await loadStripeScript()
  
  // Create a payment intent to get the publishable key and initialize Stripe
  if (cartStore.items.length > 0) {
    try {
      const intentResponse = await api.post('/orders/stripe/create-payment-intent/')
      const { publishable_key } = intentResponse.data
      if (publishable_key) {
        await initStripeElements(publishable_key)
      }
    } catch (error) {
      console.log('Cart empty or error initializing Stripe:', error)
    }
  }
})
</script>

<style scoped>
.sticky-summary {
  position: sticky;
  top: 80px;
}

.stripe-card-element {
  background: #f5f5f5;
  min-height: 50px;
}
</style>
