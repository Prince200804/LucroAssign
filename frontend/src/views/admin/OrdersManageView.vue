<template>
  <v-container fluid class="pa-6">
    <!-- Header -->
    <div class="d-flex justify-space-between align-center mb-6">
      <div>
        <h1 class="text-h4 font-weight-bold">Order Management</h1>
        <p class="text-body-2 text-grey">View and process customer orders</p>
      </div>
      <div class="d-flex gap-2">
        <v-menu>
          <template v-slot:activator="{ props }">
            <v-btn variant="outlined" prepend-icon="mdi-download" v-bind="props" :loading="exporting">
              Export
              <v-icon end>mdi-chevron-down</v-icon>
            </v-btn>
          </template>
          <v-list>
            <v-list-item @click="exportOrders('excel')">
              <template v-slot:prepend>
                <v-icon color="success">mdi-file-excel</v-icon>
              </template>
              <v-list-item-title>Export to Excel</v-list-item-title>
              <v-list-item-subtitle>All orders with items</v-list-item-subtitle>
            </v-list-item>
            <v-list-item @click="exportOrders('pdf')">
              <template v-slot:prepend>
                <v-icon color="error">mdi-file-pdf-box</v-icon>
              </template>
              <v-list-item-title>Export to PDF</v-list-item-title>
              <v-list-item-subtitle>Orders summary report</v-list-item-subtitle>
            </v-list-item>
          </v-list>
        </v-menu>
        <v-btn variant="outlined" prepend-icon="mdi-refresh" @click="fetchOrders" :loading="loading">
          Refresh
        </v-btn>
      </div>
    </div>

    <!-- Stats Cards -->
    <v-row class="mb-6">
      <v-col cols="12" sm="6" md="2">
        <v-card class="pa-4" color="warning" variant="tonal">
          <div class="d-flex align-center">
            <v-avatar color="warning" size="48" class="mr-4">
              <v-icon color="white">mdi-clock</v-icon>
            </v-avatar>
            <div>
              <p class="text-body-2 text-grey">Pending</p>
              <h3 class="text-h5 font-weight-bold">{{ orderStats.pending }}</h3>
            </div>
          </div>
        </v-card>
      </v-col>
      <v-col cols="12" sm="6" md="2">
        <v-card class="pa-4" color="info" variant="tonal">
          <div class="d-flex align-center">
            <v-avatar color="info" size="48" class="mr-4">
              <v-icon color="white">mdi-check-circle</v-icon>
            </v-avatar>
            <div>
              <p class="text-body-2 text-grey">Confirmed</p>
              <h3 class="text-h5 font-weight-bold">{{ orderStats.confirmed }}</h3>
            </div>
          </div>
        </v-card>
      </v-col>
      <v-col cols="12" sm="6" md="2">
        <v-card class="pa-4" color="primary" variant="tonal">
          <div class="d-flex align-center">
            <v-avatar color="primary" size="48" class="mr-4">
              <v-icon color="white">mdi-cog</v-icon>
            </v-avatar>
            <div>
              <p class="text-body-2 text-grey">Processing</p>
              <h3 class="text-h5 font-weight-bold">{{ orderStats.processing }}</h3>
            </div>
          </div>
        </v-card>
      </v-col>
      <v-col cols="12" sm="6" md="2">
        <v-card class="pa-4" color="secondary" variant="tonal">
          <div class="d-flex align-center">
            <v-avatar color="secondary" size="48" class="mr-4">
              <v-icon color="white">mdi-truck</v-icon>
            </v-avatar>
            <div>
              <p class="text-body-2 text-grey">Shipped</p>
              <h3 class="text-h5 font-weight-bold">{{ orderStats.shipped }}</h3>
            </div>
          </div>
        </v-card>
      </v-col>
      <v-col cols="12" sm="6" md="2">
        <v-card class="pa-4" color="orange" variant="tonal">
          <div class="d-flex align-center">
            <v-avatar color="orange" size="48" class="mr-4">
              <v-icon color="white">mdi-bike-fast</v-icon>
            </v-avatar>
            <div>
              <p class="text-body-2 text-grey">Out for Delivery</p>
              <h3 class="text-h5 font-weight-bold">{{ orderStats.out_for_delivery }}</h3>
            </div>
          </div>
        </v-card>
      </v-col>
      <v-col cols="12" sm="6" md="2">
        <v-card class="pa-4" color="success" variant="tonal">
          <div class="d-flex align-center">
            <v-avatar color="success" size="48" class="mr-4">
              <v-icon color="white">mdi-check-all</v-icon>
            </v-avatar>
            <div>
              <p class="text-body-2 text-grey">Delivered</p>
              <h3 class="text-h5 font-weight-bold">{{ orderStats.delivered }}</h3>
            </div>
          </div>
        </v-card>
      </v-col>
    </v-row>

    <!-- Filters -->
    <v-card class="mb-6">
      <v-card-text>
        <v-row align="center">
          <v-col cols="12" sm="3">
            <v-text-field
              v-model="search"
              label="Search Orders"
              prepend-inner-icon="mdi-magnify"
              variant="outlined"
              density="compact"
              hide-details
              clearable
              placeholder="Order #, Customer, Email"
            ></v-text-field>
          </v-col>
          <v-col cols="12" sm="2">
            <v-select
              v-model="filterStatus"
              :items="statusOptions"
              label="Status"
              variant="outlined"
              density="compact"
              hide-details
              clearable
            ></v-select>
          </v-col>
          <v-col cols="12" sm="2">
            <v-select
              v-model="filterPayment"
              :items="paymentOptions"
              label="Payment"
              variant="outlined"
              density="compact"
              hide-details
              clearable
            ></v-select>
          </v-col>
          <v-col cols="12" sm="2">
            <v-text-field
              v-model="filterStartDate"
              label="From Date"
              type="date"
              variant="outlined"
              density="compact"
              hide-details
            ></v-text-field>
          </v-col>
          <v-col cols="12" sm="3" class="d-flex gap-2">
            <v-btn variant="outlined" @click="resetFilters">Reset</v-btn>
            <v-btn color="primary" @click="fetchOrders">Apply</v-btn>
          </v-col>
        </v-row>
      </v-card-text>
    </v-card>

    <!-- Orders Table -->
    <v-card>
      <v-data-table-server
        v-model:items-per-page="itemsPerPage"
        v-model:page="page"
        :headers="headers"
        :items="orders"
        :items-length="totalOrders"
        :loading="loading"
        class="elevation-0"
        @update:options="fetchOrders"
      >
        <template v-slot:item.order_number="{ item }">
          <span class="font-weight-medium text-primary">{{ item.order_number }}</span>
        </template>

        <template v-slot:item.customer="{ item }">
          <div>
            <div class="font-weight-medium">{{ item.first_name }} {{ item.last_name }}</div>
            <div class="text-caption text-grey">{{ item.email }}</div>
          </div>
        </template>

        <template v-slot:item.items="{ item }">
          <v-chip size="small" color="primary" variant="tonal">
            {{ item.items?.length || item.items_count || 0 }} items
          </v-chip>
        </template>

        <template v-slot:item.total="{ item }">
          <span class="font-weight-bold">₹{{ formatPrice(item.total) }}</span>
        </template>

        <template v-slot:item.payment="{ item }">
          <v-chip :color="item.payment_method === 'razorpay' ? 'primary' : 'success'" size="small" variant="tonal">
            {{ item.payment_method === 'razorpay' ? 'Online' : 'COD' }}
          </v-chip>
        </template>

        <template v-slot:item.status="{ item }">
          <v-chip :color="getStatusColor(item.status)" size="small">
            {{ formatStatus(item.status) }}
          </v-chip>
        </template>

        <template v-slot:item.date="{ item }">
          {{ formatDate(item.created_at) }}
        </template>

        <template v-slot:item.actions="{ item }">
          <v-btn icon variant="text" size="small" color="primary" @click="viewOrder(item)">
            <v-icon>mdi-eye</v-icon>
            <v-tooltip activator="parent" location="top">View Details</v-tooltip>
          </v-btn>
          <v-btn icon variant="text" size="small" color="info" @click="openUpdateDialog(item)">
            <v-icon>mdi-pencil</v-icon>
            <v-tooltip activator="parent" location="top">Update Order</v-tooltip>
          </v-btn>
        </template>
      </v-data-table-server>
    </v-card>

    <!-- Order Details Dialog -->
    <v-dialog v-model="orderDialog" max-width="900">
      <v-card v-if="selectedOrder">
        <v-card-title class="d-flex justify-space-between align-center pa-4 bg-primary">
          <span class="text-white">
            <v-icon class="mr-2">mdi-package-variant</v-icon>
            Order {{ selectedOrder.order_number }}
          </span>
          <v-btn icon variant="text" color="white" @click="orderDialog = false">
            <v-icon>mdi-close</v-icon>
          </v-btn>
        </v-card-title>
        <v-divider></v-divider>
        <v-card-text class="pa-4">
          <v-row>
            <v-col cols="12" md="6">
              <h4 class="text-subtitle-1 font-weight-bold mb-2">
                <v-icon class="mr-1" size="small">mdi-account</v-icon>
                Customer Information
              </h4>
              <v-list density="compact" class="bg-grey-lighten-4 rounded">
                <v-list-item>
                  <template v-slot:prepend><v-icon size="small">mdi-account</v-icon></template>
                  <v-list-item-title>{{ selectedOrder.first_name }} {{ selectedOrder.last_name }}</v-list-item-title>
                </v-list-item>
                <v-list-item>
                  <template v-slot:prepend><v-icon size="small">mdi-email</v-icon></template>
                  <v-list-item-title>{{ selectedOrder.email }}</v-list-item-title>
                </v-list-item>
                <v-list-item>
                  <template v-slot:prepend><v-icon size="small">mdi-phone</v-icon></template>
                  <v-list-item-title>{{ selectedOrder.phone || 'N/A' }}</v-list-item-title>
                </v-list-item>
              </v-list>
            </v-col>
            <v-col cols="12" md="6">
              <h4 class="text-subtitle-1 font-weight-bold mb-2">
                <v-icon class="mr-1" size="small">mdi-map-marker</v-icon>
                Shipping Address
              </h4>
              <div class="bg-grey-lighten-4 rounded pa-3">
                <p class="text-body-2 mb-1">{{ selectedOrder.shipping_address }}</p>
                <p class="text-body-2 mb-1">{{ selectedOrder.shipping_city }}, {{ selectedOrder.shipping_state }} {{ selectedOrder.shipping_zip }}</p>
                <p class="text-body-2 mb-0">{{ selectedOrder.shipping_country }}</p>
              </div>
              
              <div class="mt-4 d-flex gap-2">
                <v-chip :color="getStatusColor(selectedOrder.status)">
                  {{ formatStatus(selectedOrder.status) }}
                </v-chip>
                <v-chip :color="selectedOrder.payment_method === 'razorpay' ? 'primary' : 'success'" variant="outlined">
                  {{ selectedOrder.payment_method === 'razorpay' ? 'Paid Online' : 'Cash on Delivery' }}
                </v-chip>
              </div>
            </v-col>
          </v-row>

          <v-divider class="my-4"></v-divider>

          <h4 class="text-subtitle-1 font-weight-bold mb-4">
            <v-icon class="mr-1" size="small">mdi-shopping</v-icon>
            Order Items
          </h4>
          <v-table density="compact" class="rounded">
            <thead>
              <tr class="bg-grey-lighten-4">
                <th>Product</th>
                <th class="text-right">Price</th>
                <th class="text-right">Qty</th>
                <th class="text-right">Subtotal</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="item in selectedOrder.items" :key="item.id">
                <td>
                  <div class="d-flex align-center py-2">
                    <v-avatar size="40" rounded class="mr-2">
                      <v-img :src="item.product_image || 'https://via.placeholder.com/50'" />
                    </v-avatar>
                    {{ item.product_name }}
                  </div>
                </td>
                <td class="text-right">₹{{ formatPrice(item.unit_price) }}</td>
                <td class="text-right">{{ item.quantity }}</td>
                <td class="text-right font-weight-bold">₹{{ formatPrice(item.total_price) }}</td>
              </tr>
            </tbody>
            <tfoot>
              <tr class="bg-grey-lighten-4">
                <td colspan="3" class="text-right font-weight-bold">Total:</td>
                <td class="text-right font-weight-bold text-primary">₹{{ formatPrice(selectedOrder.total) }}</td>
              </tr>
            </tfoot>
          </v-table>

          <!-- Order Notes -->
          <div v-if="selectedOrder.notes" class="mt-4">
            <h4 class="text-subtitle-1 font-weight-bold mb-2">
              <v-icon class="mr-1" size="small">mdi-note</v-icon>
              Customer Notes
            </h4>
            <v-alert type="info" variant="tonal">{{ selectedOrder.notes }}</v-alert>
          </div>

          <!-- Tracking Info -->
          <div v-if="selectedOrder.tracking_number" class="mt-4">
            <v-alert type="success" variant="tonal">
              <strong>Tracking Number:</strong> {{ selectedOrder.tracking_number }}
            </v-alert>
          </div>
        </v-card-text>
        <v-divider></v-divider>
        <v-card-actions class="pa-4">
          <v-spacer></v-spacer>
          <v-btn variant="outlined" @click="orderDialog = false">Close</v-btn>
          <v-btn color="primary" @click="openUpdateDialog(selectedOrder)">
            <v-icon left>mdi-pencil</v-icon>
            Update Order
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>

    <!-- Update Order Dialog -->
    <v-dialog v-model="updateDialog" max-width="500">
      <v-card>
        <v-card-title class="pa-4 bg-primary">
          <span class="text-white">
            <v-icon class="mr-2">mdi-pencil</v-icon>
            Update Order {{ editingOrder?.order_number }}
          </span>
        </v-card-title>
        <v-card-text class="pa-4">
          <v-form ref="updateForm">
            <v-select
              v-model="updateData.status"
              :items="allStatusOptions"
              label="Order Status"
              variant="outlined"
              prepend-inner-icon="mdi-flag"
              class="mb-4"
            ></v-select>

            <v-text-field
              v-model="updateData.tracking_number"
              label="Tracking Number"
              variant="outlined"
              prepend-inner-icon="mdi-barcode"
              placeholder="Enter tracking number"
              class="mb-4"
            ></v-text-field>

            <v-text-field
              v-model="updateData.estimated_delivery"
              label="Estimated Delivery Date"
              type="date"
              variant="outlined"
              prepend-inner-icon="mdi-calendar"
              class="mb-4"
            ></v-text-field>

            <v-textarea
              v-model="updateData.admin_notes"
              label="Admin Notes (Internal)"
              variant="outlined"
              prepend-inner-icon="mdi-note"
              rows="3"
              placeholder="Add internal notes about this order"
            ></v-textarea>
          </v-form>
        </v-card-text>
        <v-divider></v-divider>
        <v-card-actions class="pa-4">
          <v-spacer></v-spacer>
          <v-btn variant="outlined" @click="updateDialog = false">Cancel</v-btn>
          <v-btn color="primary" :loading="updating" @click="saveOrderUpdate">
            <v-icon left>mdi-check</v-icon>
            Save Changes
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>

    <!-- Snackbar -->
    <v-snackbar v-model="snackbar.show" :color="snackbar.color" :timeout="3000">
      {{ snackbar.message }}
    </v-snackbar>
  </v-container>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import api from '@/services/api'

// State
const loading = ref(true)
const updating = ref(false)
const exporting = ref(false)
const orders = ref([])
const totalOrders = ref(0)
const page = ref(1)
const itemsPerPage = ref(10)
const search = ref('')
const filterStatus = ref(null)
const filterPayment = ref(null)
const filterStartDate = ref('')
const orderDialog = ref(false)
const updateDialog = ref(false)
const selectedOrder = ref(null)
const editingOrder = ref(null)

const updateData = ref({
  status: '',
  tracking_number: '',
  estimated_delivery: '',
  admin_notes: ''
})

const orderStats = reactive({
  pending: 0,
  confirmed: 0,
  processing: 0,
  shipped: 0,
  out_for_delivery: 0,
  delivered: 0
})

const snackbar = reactive({
  show: false,
  message: '',
  color: 'success'
})

const statusOptions = [
  { title: 'Pending', value: 'pending' },
  { title: 'Confirmed', value: 'confirmed' },
  { title: 'Processing', value: 'processing' },
  { title: 'Shipped', value: 'shipped' },
  { title: 'Out for Delivery', value: 'out_for_delivery' },
  { title: 'Delivered', value: 'delivered' },
  { title: 'Cancelled', value: 'cancelled' },
  { title: 'Returned', value: 'returned' }
]

const allStatusOptions = statusOptions

const paymentOptions = [
  { title: 'Online (Stripe)', value: 'stripe' },
  { title: 'Cash on Delivery', value: 'cod' }
]

const headers = [
  { title: 'Order #', key: 'order_number', sortable: false },
  { title: 'Customer', key: 'customer', sortable: false },
  { title: 'Items', key: 'items', sortable: false },
  { title: 'Total', key: 'total' },
  { title: 'Payment', key: 'payment', sortable: false },
  { title: 'Status', key: 'status' },
  { title: 'Date', key: 'date' },
  { title: 'Actions', key: 'actions', sortable: false, align: 'end' }
]

// Methods
const showMessage = (message, color = 'success') => {
  snackbar.message = message
  snackbar.color = color
  snackbar.show = true
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

const formatPrice = (price) => parseFloat(price).toLocaleString('en-IN')

const formatDate = (dateString) => {
  return new Date(dateString).toLocaleDateString('en-US', {
    year: 'numeric',
    month: 'short',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  })
}

const fetchOrders = async () => {
  loading.value = true
  try {
    const params = {
      page: page.value,
      page_size: itemsPerPage.value,
      search: search.value || undefined,
      status: filterStatus.value || undefined,
      payment_method: filterPayment.value || undefined,
      start_date: filterStartDate.value || undefined
    }

    const response = await api.get('/orders/', { params })
    orders.value = response.data.results || response.data
    totalOrders.value = response.data.count || orders.value.length

    // Fetch stats
    await fetchOrderStats()
  } catch (error) {
    console.error('Error fetching orders:', error)
    showMessage('Failed to load orders', 'error')
  } finally {
    loading.value = false
  }
}

const fetchOrderStats = async () => {
  try {
    const response = await api.get('/orders/admin/stats/')
    Object.assign(orderStats, response.data)
  } catch (error) {
    // Calculate from current orders as fallback
    orderStats.pending = orders.value.filter(o => o.status === 'pending').length
    orderStats.confirmed = orders.value.filter(o => o.status === 'confirmed').length
    orderStats.processing = orders.value.filter(o => o.status === 'processing').length
    orderStats.shipped = orders.value.filter(o => o.status === 'shipped').length
    orderStats.out_for_delivery = orders.value.filter(o => o.status === 'out_for_delivery').length
    orderStats.delivered = orders.value.filter(o => o.status === 'delivered').length
  }
}

const resetFilters = () => {
  search.value = ''
  filterStatus.value = null
  filterPayment.value = null
  filterStartDate.value = ''
  page.value = 1
  fetchOrders()
}

const viewOrder = async (order) => {
  try {
    // Fetch full order details
    const response = await api.get(`/orders/${order.id}/`)
    selectedOrder.value = response.data
    orderDialog.value = true
  } catch (error) {
    selectedOrder.value = order
    orderDialog.value = true
  }
}

const openUpdateDialog = (order) => {
  editingOrder.value = order
  updateData.value = {
    status: order.status,
    tracking_number: order.tracking_number || '',
    estimated_delivery: order.estimated_delivery ? order.estimated_delivery.split('T')[0] : '',
    admin_notes: order.admin_notes || ''
  }
  orderDialog.value = false
  updateDialog.value = true
}

const saveOrderUpdate = async () => {
  if (!editingOrder.value) return
  
  updating.value = true
  try {
    await api.patch(`/orders/admin/${editingOrder.value.id}/update-status/`, updateData.value)
    showMessage('Order updated successfully')
    updateDialog.value = false
    fetchOrders()
  } catch (error) {
    showMessage(error.response?.data?.error || 'Failed to update order', 'error')
  } finally {
    updating.value = false
  }
}

const exportOrders = async (format) => {
  exporting.value = true
  try {
    let url = `/orders/admin/export/orders/${format === 'excel' ? 'excel' : 'pdf'}/`
    
    // Build query params from current filters
    const params = new URLSearchParams()
    if (filterStatus.value) params.append('status', filterStatus.value)
    if (filterPayment.value) params.append('payment_status', filterPayment.value)
    if (filterStartDate.value) params.append('start_date', filterStartDate.value)
    
    if (params.toString()) {
      url += '?' + params.toString()
    }
    
    const response = await api.get(url, {
      responseType: 'blob'
    })
    
    // Create download link
    const blob = new Blob([response.data], {
      type: format === 'excel' 
        ? 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        : 'application/pdf'
    })
    const downloadUrl = window.URL.createObjectURL(blob)
    const link = document.createElement('a')
    link.href = downloadUrl
    link.download = `orders_export.${format === 'excel' ? 'xlsx' : 'pdf'}`
    document.body.appendChild(link)
    link.click()
    document.body.removeChild(link)
    window.URL.revokeObjectURL(downloadUrl)
    
    showMessage(`Orders exported to ${format.toUpperCase()} successfully`)
  } catch (error) {
    showMessage('Failed to export orders', 'error')
    console.error(error)
  } finally {
    exporting.value = false
  }
}

onMounted(() => {
  fetchOrders()
})
</script>
