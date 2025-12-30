<template>
  <v-container class="py-8">
    <div class="d-flex justify-space-between align-center mb-6">
      <h1 class="text-h4 font-weight-bold">My Orders</h1>
      <v-btn variant="outlined" to="/track-order" prepend-icon="mdi-truck-delivery">
        Track Order
      </v-btn>
    </div>

    <v-skeleton-loader v-if="loading" type="table"></v-skeleton-loader>

    <v-card v-else-if="orders.length === 0" class="pa-8 text-center">
      <v-icon size="64" color="grey">mdi-package-variant</v-icon>
      <h2 class="text-h5 mt-4 mb-2">No orders yet</h2>
      <p class="text-body-2 text-grey mb-4">Start shopping to see your orders here.</p>
      <v-btn color="primary" to="/products">Browse Products</v-btn>
    </v-card>

    <v-card v-else>
      <v-table>
        <thead>
          <tr>
            <th>Order #</th>
            <th>Date</th>
            <th>Items</th>
            <th>Total</th>
            <th>Payment</th>
            <th>Status</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="order in orders" :key="order.id">
            <td class="font-weight-medium text-primary">{{ order.order_number }}</td>
            <td>{{ formatDate(order.created_at) }}</td>
            <td>{{ order.items_count || order.items?.length }} items</td>
            <td class="font-weight-bold">₹{{ formatPrice(order.total) }}</td>
            <td>
              <v-chip :color="order.payment_method === 'razorpay' ? 'primary' : 'success'" size="small" variant="tonal">
                {{ order.payment_method === 'razorpay' ? 'Online' : 'COD' }}
              </v-chip>
            </td>
            <td>
              <v-chip :color="getStatusColor(order.status)" size="small">
                {{ formatStatus(order.status) }}
              </v-chip>
            </td>
            <td>
              <v-btn
                variant="text"
                color="primary"
                size="small"
                :to="`/order/${order.id}`"
              >
                View
              </v-btn>
              <v-btn
                variant="text"
                color="info"
                size="small"
                :to="`/track-order?order=${order.order_number}`"
              >
                Track
              </v-btn>
            </td>
          </tr>
        </tbody>
      </v-table>
    </v-card>
  </v-container>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import api from '@/services/api'
import { format } from 'date-fns'

const loading = ref(true)
const orders = ref([])

const formatPrice = (price) => parseFloat(price).toLocaleString('en-IN')
const formatDate = (date) => format(new Date(date), 'dd MMM yyyy')

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

onMounted(async () => {
  try {
    const response = await api.get('/orders/')
    orders.value = response.data.results || response.data
  } catch (error) {
    console.error('Error fetching orders:', error)
  } finally {
    loading.value = false
  }
})
</script>
