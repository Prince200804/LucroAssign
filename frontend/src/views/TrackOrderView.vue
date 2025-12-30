<template>
  <v-container class="py-8">
    <h1 class="text-h4 font-weight-bold mb-6">Track Your Order</h1>

    <!-- Search Form -->
    <v-card class="mb-6">
      <v-card-text>
        <v-row align="center">
          <v-col cols="12" md="8">
            <v-text-field
              v-model="searchOrderNumber"
              label="Enter Order Number"
              placeholder="e.g., ORD-ABC12345"
              prepend-inner-icon="mdi-magnify"
              variant="outlined"
              hide-details
              @keyup.enter="searchOrder"
            ></v-text-field>
          </v-col>
          <v-col cols="12" md="4">
            <v-btn
              color="primary"
              size="large"
              block
              :loading="loading"
              @click="searchOrder"
            >
              <v-icon left>mdi-truck-delivery</v-icon>
              Track Order
            </v-btn>
          </v-col>
        </v-row>
      </v-card-text>
    </v-card>

    <!-- Loading State -->
    <v-skeleton-loader v-if="loading" type="card, list-item-avatar-three-line"></v-skeleton-loader>

    <!-- Error State -->
    <v-alert v-else-if="error" type="error" class="mb-6">
      {{ error }}
    </v-alert>

    <!-- Order Not Found -->
    <v-card v-else-if="searched && !order" class="pa-8 text-center">
      <v-icon size="64" color="warning">mdi-package-variant-remove</v-icon>
      <h2 class="text-h5 mt-4 mb-2">Order Not Found</h2>
      <p class="text-body-2 text-grey mb-4">
        Please check the order number and try again.
      </p>
    </v-card>

    <!-- Order Details -->
    <template v-else-if="order">
      <!-- Order Status Timeline -->
      <v-card class="mb-6">
        <v-card-title class="d-flex justify-space-between align-center">
          <span>
            <v-icon class="mr-2">mdi-package-variant</v-icon>
            Order #{{ order.order_number }}
          </span>
          <v-chip :color="getStatusColor(order.status)" size="large">
            {{ formatStatus(order.status) }}
          </v-chip>
        </v-card-title>
        <v-card-text>
          <!-- Status Timeline -->
          <v-timeline density="compact" side="end" class="my-4">
            <v-timeline-item
              v-for="step in statusSteps"
              :key="step.status"
              :dot-color="getTimelineColor(step.status)"
              :icon="step.icon"
              size="small"
            >
              <div class="d-flex align-center">
                <div>
                  <div class="font-weight-medium">{{ step.title }}</div>
                  <div class="text-caption text-grey">{{ step.description }}</div>
                  <div v-if="getStatusTime(step.status)" class="text-caption text-primary">
                    {{ getStatusTime(step.status) }}
                  </div>
                </div>
                <v-icon
                  v-if="isStepCompleted(step.status)"
                  color="success"
                  class="ml-auto"
                >
                  mdi-check-circle
                </v-icon>
              </div>
            </v-timeline-item>
          </v-timeline>

          <!-- Estimated Delivery -->
          <v-alert
            v-if="order.estimated_delivery && !['delivered', 'cancelled', 'returned'].includes(order.status)"
            type="info"
            variant="tonal"
            class="mt-4"
          >
            <v-icon>mdi-calendar-clock</v-icon>
            <strong>Estimated Delivery:</strong> {{ formatDate(order.estimated_delivery) }}
          </v-alert>

          <!-- Tracking Number -->
          <v-alert
            v-if="order.tracking_number"
            type="info"
            variant="tonal"
            class="mt-4"
          >
            <v-icon>mdi-barcode</v-icon>
            <strong>Tracking Number:</strong> {{ order.tracking_number }}
          </v-alert>
        </v-card-text>
      </v-card>

      <!-- Order Details -->
      <v-row>
        <v-col cols="12" md="8">
          <v-card>
            <v-card-title>
              <v-icon class="mr-2">mdi-shopping</v-icon>
              Order Items
            </v-card-title>
            <v-list>
              <v-list-item
                v-for="item in order.items"
                :key="item.id"
                class="py-3"
              >
                <template v-slot:prepend>
                  <v-img
                    :src="item.product_image || 'https://via.placeholder.com/80'"
                    width="80"
                    height="80"
                    cover
                    class="rounded mr-4"
                  ></v-img>
                </template>
                <v-list-item-title class="font-weight-medium">
                  {{ item.product_name }}
                </v-list-item-title>
                <v-list-item-subtitle>
                  Qty: {{ item.quantity }} × ₹{{ formatPrice(item.unit_price) }}
                </v-list-item-subtitle>
                <template v-slot:append>
                  <span class="font-weight-bold">₹{{ formatPrice(item.total_price) }}</span>
                </template>
              </v-list-item>
            </v-list>
            <v-divider></v-divider>
            <v-card-text>
              <div class="d-flex justify-space-between text-h6">
                <span>Total</span>
                <span class="font-weight-bold text-primary">₹{{ formatPrice(order.total) }}</span>
              </div>
            </v-card-text>
          </v-card>
        </v-col>

        <v-col cols="12" md="4">
          <!-- Shipping Info -->
          <v-card class="mb-4">
            <v-card-title>
              <v-icon class="mr-2">mdi-truck</v-icon>
              Shipping Address
            </v-card-title>
            <v-card-text>
              <p class="font-weight-medium mb-1">{{ order.first_name }} {{ order.last_name }}</p>
              <p class="text-body-2 mb-1">{{ order.shipping_address }}</p>
              <p class="text-body-2 mb-1">{{ order.shipping_city }}, {{ order.shipping_state }} {{ order.shipping_zip }}</p>
              <p class="text-body-2">{{ order.shipping_country }}</p>
            </v-card-text>
          </v-card>

          <!-- Payment Info -->
          <v-card>
            <v-card-title>
              <v-icon class="mr-2">mdi-credit-card</v-icon>
              Payment Info
            </v-card-title>
            <v-card-text>
              <v-chip :color="order.payment_method === 'razorpay' ? 'primary' : 'success'" class="mb-2">
                {{ order.payment_method === 'razorpay' ? 'Paid Online' : 'Cash on Delivery' }}
              </v-chip>
              <p class="text-body-2 text-grey mb-0">
                Order placed on {{ formatDate(order.created_at) }}
              </p>
            </v-card-text>
          </v-card>
        </v-col>
      </v-row>
    </template>
  </v-container>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import api from '@/services/api'
import { format } from 'date-fns'

const route = useRoute()

const searchOrderNumber = ref('')
const order = ref(null)
const loading = ref(false)
const error = ref('')
const searched = ref(false)

const statusSteps = [
  { status: 'pending', title: 'Order Placed', description: 'Your order has been received', icon: 'mdi-clipboard-check' },
  { status: 'confirmed', title: 'Confirmed', description: 'Your order has been confirmed', icon: 'mdi-check-circle' },
  { status: 'processing', title: 'Processing', description: 'Your order is being prepared', icon: 'mdi-cog' },
  { status: 'shipped', title: 'Shipped', description: 'Your order is on the way', icon: 'mdi-truck' },
  { status: 'out_for_delivery', title: 'Out for Delivery', description: 'Your order will be delivered today', icon: 'mdi-bike-fast' },
  { status: 'delivered', title: 'Delivered', description: 'Your order has been delivered', icon: 'mdi-package-variant-closed-check' },
]

const statusOrder = ['pending', 'confirmed', 'processing', 'shipped', 'out_for_delivery', 'delivered']

const formatPrice = (price) => parseFloat(price).toLocaleString('en-IN')
const formatDate = (date) => format(new Date(date), 'dd MMM yyyy, hh:mm a')

const formatStatus = (status) => {
  const statusMap = {
    pending: 'Pending',
    confirmed: 'Confirmed',
    processing: 'Processing',
    shipped: 'Shipped',
    out_for_delivery: 'Out for Delivery',
    delivered: 'Delivered',
    cancelled: 'Cancelled',
    returned: 'Returned'
  }
  return statusMap[status] || status
}

const getStatusColor = (status) => {
  const colors = {
    pending: 'warning',
    confirmed: 'info',
    processing: 'primary',
    shipped: 'secondary',
    out_for_delivery: 'orange',
    delivered: 'success',
    cancelled: 'error',
    returned: 'grey'
  }
  return colors[status] || 'grey'
}

const getTimelineColor = (stepStatus) => {
  if (!order.value) return 'grey-lighten-2'
  
  const currentIndex = statusOrder.indexOf(order.value.status)
  const stepIndex = statusOrder.indexOf(stepStatus)
  
  if (order.value.status === 'cancelled' || order.value.status === 'returned') {
    return stepIndex === 0 ? 'success' : 'grey-lighten-2'
  }
  
  if (stepIndex <= currentIndex) {
    return 'success'
  }
  return 'grey-lighten-2'
}

const isStepCompleted = (stepStatus) => {
  if (!order.value) return false
  
  const currentIndex = statusOrder.indexOf(order.value.status)
  const stepIndex = statusOrder.indexOf(stepStatus)
  
  if (order.value.status === 'cancelled' || order.value.status === 'returned') {
    return stepIndex === 0
  }
  
  return stepIndex <= currentIndex
}

const getStatusTime = (stepStatus) => {
  if (!order.value) return null
  
  // For simplicity, we just show the order creation time for completed steps
  // In a real app, you'd track each status change timestamp
  if (isStepCompleted(stepStatus) && stepStatus === order.value.status) {
    return formatDate(order.value.updated_at || order.value.created_at)
  }
  if (stepStatus === 'pending') {
    return formatDate(order.value.created_at)
  }
  return null
}

const searchOrder = async () => {
  if (!searchOrderNumber.value.trim()) {
    error.value = 'Please enter an order number'
    return
  }

  loading.value = true
  error.value = ''
  order.value = null
  searched.value = true

  try {
    const response = await api.get(`/orders/track/${searchOrderNumber.value.trim()}/`)
    order.value = response.data
  } catch (err) {
    if (err.response?.status === 404) {
      order.value = null
    } else {
      error.value = err.response?.data?.error || 'Failed to fetch order details'
    }
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  // Check if order number is passed in query params
  const queryOrder = route.query.order
  if (queryOrder) {
    searchOrderNumber.value = queryOrder
    searchOrder()
  }
})
</script>
