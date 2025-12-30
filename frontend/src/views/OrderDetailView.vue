<template>
  <v-container class="py-8">
    <v-btn variant="text" to="/orders" class="mb-4">
      <v-icon left>mdi-arrow-left</v-icon>
      Back to Orders
    </v-btn>

    <v-skeleton-loader v-if="loading" type="article"></v-skeleton-loader>

    <v-card v-else-if="!order" class="pa-8 text-center">
      <v-icon size="64" color="error">mdi-alert-circle</v-icon>
      <h2 class="text-h5 mt-4">Order not found</h2>
      <v-btn color="primary" class="mt-4" to="/orders">View All Orders</v-btn>
    </v-card>

    <template v-else>
      <v-row>
        <v-col cols="12" md="8">
          <v-card class="mb-4">
            <v-card-title class="d-flex justify-space-between align-center">
              <span>Order #{{ order.order_number }}</span>
              <div>
                <v-chip :color="getStatusColor(order.status)" class="mr-2">
                  {{ order.status }}
                </v-chip>
                <v-chip :color="order.payment_status === 'paid' ? 'success' : 'warning'">
                  {{ order.payment_status }}
                </v-chip>
              </div>
            </v-card-title>

            <v-divider></v-divider>

            <v-list>
              <v-list-item v-for="item in order.items" :key="item.id">
                <template v-slot:prepend>
                  <v-avatar size="60" rounded>
                    <v-img src="https://via.placeholder.com/60"></v-img>
                  </v-avatar>
                </template>
                <v-list-item-title class="font-weight-medium">
                  {{ item.product_name }}
                </v-list-item-title>
                <v-list-item-subtitle>
                  SKU: {{ item.product_sku }} | Qty: {{ item.quantity }}
                </v-list-item-subtitle>
                <template v-slot:append>
                  <span class="font-weight-bold">₹{{ formatPrice(item.total_price) }}</span>
                </template>
              </v-list-item>
            </v-list>
          </v-card>

          <v-card>
            <v-card-title>Shipping Address</v-card-title>
            <v-card-text>
              <p class="font-weight-medium">{{ order.first_name }} {{ order.last_name }}</p>
              <p>{{ order.shipping_address }}</p>
              <p>{{ order.shipping_city }}, {{ order.shipping_state }} - {{ order.shipping_zip }}</p>
              <p>{{ order.shipping_country }}</p>
              <p class="mt-2">
                <v-icon size="small" class="mr-1">mdi-email</v-icon>
                {{ order.email }}
              </p>
              <p v-if="order.phone">
                <v-icon size="small" class="mr-1">mdi-phone</v-icon>
                {{ order.phone }}
              </p>
            </v-card-text>
          </v-card>
        </v-col>

        <v-col cols="12" md="4">
          <v-card>
            <v-card-title>Order Summary</v-card-title>
            <v-card-text>
              <div class="d-flex justify-space-between mb-2">
                <span>Subtotal</span>
                <span>₹{{ formatPrice(order.subtotal) }}</span>
              </div>
              <div class="d-flex justify-space-between mb-2">
                <span>Shipping</span>
                <span>₹{{ formatPrice(order.shipping_cost) }}</span>
              </div>
              <div class="d-flex justify-space-between mb-2">
                <span>Tax</span>
                <span>₹{{ formatPrice(order.tax) }}</span>
              </div>
              <v-divider class="my-4"></v-divider>
              <div class="d-flex justify-space-between">
                <span class="text-h6 font-weight-bold">Total</span>
                <span class="text-h6 font-weight-bold text-primary">
                  ₹{{ formatPrice(order.total) }}
                </span>
              </div>
            </v-card-text>
          </v-card>

          <v-card class="mt-4">
            <v-card-title>Order Timeline</v-card-title>
            <v-card-text>
              <v-timeline density="compact" side="end">
                <v-timeline-item dot-color="success" size="small">
                  <div class="text-caption">Order Placed</div>
                  <div class="text-body-2">{{ formatDate(order.created_at) }}</div>
                </v-timeline-item>
                <v-timeline-item
                  v-if="order.status !== 'cancelled'"
                  :dot-color="order.status === 'confirmed' ? 'success' : 'grey'"
                  size="small"
                >
                  <div class="text-caption">Confirmed</div>
                </v-timeline-item>
                <v-timeline-item
                  v-if="order.status !== 'cancelled'"
                  :dot-color="['processing', 'shipped', 'delivered'].includes(order.status) ? 'success' : 'grey'"
                  size="small"
                >
                  <div class="text-caption">Processing</div>
                </v-timeline-item>
                <v-timeline-item
                  v-if="order.status !== 'cancelled'"
                  :dot-color="['shipped', 'delivered'].includes(order.status) ? 'success' : 'grey'"
                  size="small"
                >
                  <div class="text-caption">Shipped</div>
                </v-timeline-item>
                <v-timeline-item
                  v-if="order.status !== 'cancelled'"
                  :dot-color="order.status === 'delivered' ? 'success' : 'grey'"
                  size="small"
                >
                  <div class="text-caption">Delivered</div>
                </v-timeline-item>
                <v-timeline-item
                  v-if="order.status === 'cancelled'"
                  dot-color="error"
                  size="small"
                >
                  <div class="text-caption">Cancelled</div>
                </v-timeline-item>
              </v-timeline>
            </v-card-text>
          </v-card>
        </v-col>
      </v-row>
    </template>
  </v-container>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import api from '@/services/api'
import { format } from 'date-fns'

const route = useRoute()
const loading = ref(true)
const order = ref(null)

const formatPrice = (price) => parseFloat(price || 0).toLocaleString('en-IN')
const formatDate = (date) => format(new Date(date), 'dd MMM yyyy, hh:mm a')

const getStatusColor = (status) => {
  const colors = {
    pending: 'warning',
    confirmed: 'info',
    processing: 'primary',
    shipped: 'secondary',
    delivered: 'success',
    cancelled: 'error',
  }
  return colors[status] || 'grey'
}

onMounted(async () => {
  try {
    const response = await api.get(`/orders/${route.params.id}/`)
    order.value = response.data
  } catch (error) {
    console.error('Error fetching order:', error)
  } finally {
    loading.value = false
  }
})
</script>
