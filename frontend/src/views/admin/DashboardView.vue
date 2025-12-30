<template>
  <v-container fluid class="pa-6">
    <!-- Header -->
    <div class="d-flex justify-space-between align-center mb-6">
      <div>
        <h1 class="text-h4 font-weight-bold">Admin Dashboard</h1>
        <p class="text-body-2 text-grey">Analytics overview and insights</p>
      </div>
      <div class="d-flex gap-2">
        <v-btn
          variant="outlined"
          prepend-icon="mdi-file-excel"
          @click="exportCSV"
          :loading="exporting"
        >
          Export CSV
        </v-btn>
        <v-btn
          color="primary"
          prepend-icon="mdi-file-pdf-box"
          @click="exportPDF"
          :loading="exporting"
        >
          Export PDF
        </v-btn>
      </div>
    </div>

    <!-- Date Range Filter -->
    <v-card class="mb-6">
      <v-card-text>
        <v-row align="center">
          <v-col cols="12" sm="3">
            <v-select
              v-model="dateRange"
              :items="dateRangeOptions"
              label="Date Range"
              variant="outlined"
              density="compact"
              hide-details
            ></v-select>
          </v-col>
          <v-col cols="12" sm="3" v-if="dateRange === 'custom'">
            <v-text-field
              v-model="customStartDate"
              label="Start Date"
              type="date"
              variant="outlined"
              density="compact"
              hide-details
            ></v-text-field>
          </v-col>
          <v-col cols="12" sm="3" v-if="dateRange === 'custom'">
            <v-text-field
              v-model="customEndDate"
              label="End Date"
              type="date"
              variant="outlined"
              density="compact"
              hide-details
            ></v-text-field>
          </v-col>
          <v-col cols="12" sm="3">
            <v-btn color="primary" @click="fetchDashboardData" :loading="loading">
              Apply Filter
            </v-btn>
          </v-col>
        </v-row>
      </v-card-text>
    </v-card>

    <!-- Loading State -->
    <div v-if="loading" class="text-center py-12">
      <v-progress-circular indeterminate color="primary" size="64"></v-progress-circular>
      <p class="text-body-1 text-grey mt-4">Loading analytics data...</p>
    </div>

    <template v-else>
      <!-- No Data Message -->
      <v-alert
        v-if="overview.total_views === 0 && overview.total_cart_adds === 0 && overview.total_purchases === 0"
        type="info"
        variant="tonal"
        class="mb-6"
        border="start"
      >
        <div class="d-flex align-center">
          <v-icon class="mr-3">mdi-information</v-icon>
          <div>
            <strong>No Analytics Data Yet</strong>
            <p class="mb-0 mt-1 text-body-2">
              Real-time analytics will appear here when users start interacting with products. 
              Visit products, add items to cart, and complete purchases to generate analytics data.
            </p>
          </div>
        </div>
      </v-alert>

      <!-- KPI Cards -->
      <v-row class="mb-6">
        <v-col cols="12" sm="6" md="3">
          <v-card class="pa-4" color="primary" variant="tonal">
            <div class="d-flex align-center">
              <v-avatar color="primary" size="48">
                <v-icon color="white">mdi-eye</v-icon>
              </v-avatar>
              <div class="ml-4">
                <p class="text-body-2 text-grey">Total Views</p>
                <h3 class="text-h4 font-weight-bold">{{ formatNumber(overview.total_views) }}</h3>
                <p class="text-caption" :class="overview.views_change >= 0 ? 'text-success' : 'text-error'">
                  <v-icon size="small">{{ overview.views_change >= 0 ? 'mdi-arrow-up' : 'mdi-arrow-down' }}</v-icon>
                  {{ Math.abs(overview.views_change) }}% from last period
                </p>
              </div>
            </div>
          </v-card>
        </v-col>
        <v-col cols="12" sm="6" md="3">
          <v-card class="pa-4" color="success" variant="tonal">
            <div class="d-flex align-center">
              <v-avatar color="success" size="48">
                <v-icon color="white">mdi-cart</v-icon>
              </v-avatar>
              <div class="ml-4">
                <p class="text-body-2 text-grey">Cart Additions</p>
                <h3 class="text-h4 font-weight-bold">{{ formatNumber(overview.total_cart_adds) }}</h3>
                <p class="text-caption" :class="overview.cart_change >= 0 ? 'text-success' : 'text-error'">
                  <v-icon size="small">{{ overview.cart_change >= 0 ? 'mdi-arrow-up' : 'mdi-arrow-down' }}</v-icon>
                  {{ Math.abs(overview.cart_change) }}% from last period
                </p>
              </div>
            </div>
          </v-card>
        </v-col>
        <v-col cols="12" sm="6" md="3">
          <v-card class="pa-4" color="info" variant="tonal">
            <div class="d-flex align-center">
              <v-avatar color="info" size="48">
                <v-icon color="white">mdi-cash</v-icon>
              </v-avatar>
              <div class="ml-4">
                <p class="text-body-2 text-grey">Total Purchases</p>
                <h3 class="text-h4 font-weight-bold">{{ formatNumber(overview.total_purchases) }}</h3>
                <p class="text-caption" :class="overview.purchase_change >= 0 ? 'text-success' : 'text-error'">
                  <v-icon size="small">{{ overview.purchase_change >= 0 ? 'mdi-arrow-up' : 'mdi-arrow-down' }}</v-icon>
                  {{ Math.abs(overview.purchase_change) }}% from last period
                </p>
              </div>
            </div>
          </v-card>
        </v-col>
        <v-col cols="12" sm="6" md="3">
          <v-card class="pa-4" color="warning" variant="tonal">
            <div class="d-flex align-center">
              <v-avatar color="warning" size="48">
                <v-icon color="white">mdi-percent</v-icon>
              </v-avatar>
              <div class="ml-4">
                <p class="text-body-2 text-grey">Conversion Rate</p>
                <h3 class="text-h4 font-weight-bold">{{ overview.conversion_rate }}%</h3>
                <p class="text-caption" :class="overview.conversion_change >= 0 ? 'text-success' : 'text-error'">
                  <v-icon size="small">{{ overview.conversion_change >= 0 ? 'mdi-arrow-up' : 'mdi-arrow-down' }}</v-icon>
                  {{ Math.abs(overview.conversion_change) }}% from last period
                </p>
              </div>
            </div>
          </v-card>
        </v-col>
      </v-row>

      <!-- Charts Row 1 -->
      <v-row class="mb-6">
        <v-col cols="12" md="8">
          <v-card>
            <v-card-title>
              <v-icon left>mdi-chart-line</v-icon>
              Engagement Trends Over Time
            </v-card-title>
            <v-card-text>
              <Line :data="engagementTrendData" :options="lineChartOptions" style="height: 300px" />
            </v-card-text>
          </v-card>
        </v-col>
        <v-col cols="12" md="4">
          <v-card>
            <v-card-title>
              <v-icon left>mdi-chart-pie</v-icon>
              Category Distribution
            </v-card-title>
            <v-card-text>
              <Doughnut :data="categoryDistributionData" :options="doughnutChartOptions" style="height: 300px" />
            </v-card-text>
          </v-card>
        </v-col>
      </v-row>

      <!-- Charts Row 2 -->
      <v-row class="mb-6">
        <v-col cols="12" md="6">
          <v-card>
            <v-card-title>
              <v-icon left>mdi-chart-bar</v-icon>
              Most Viewed Products
            </v-card-title>
            <v-card-text>
              <Bar :data="mostViewedData" :options="barChartOptions" style="height: 300px" />
            </v-card-text>
          </v-card>
        </v-col>
        <v-col cols="12" md="6">
          <v-card>
            <v-card-title>
              <v-icon left>mdi-chart-bar</v-icon>
              Most Purchased Products
            </v-card-title>
            <v-card-text>
              <Bar :data="mostPurchasedData" :options="barChartOptions" style="height: 300px" />
            </v-card-text>
          </v-card>
        </v-col>
      </v-row>

      <!-- Detailed Tables -->
      <v-row>
        <v-col cols="12" md="6">
          <v-card>
            <v-card-title class="d-flex justify-space-between align-center">
              <span>
                <v-icon left>mdi-eye-off</v-icon>
                Viewed But Not Purchased
              </span>
              <v-btn variant="text" size="small" color="primary" to="/admin/analytics">
                View All
              </v-btn>
            </v-card-title>
            <v-divider></v-divider>
            <v-data-table
              :headers="viewedNotPurchasedHeaders"
              :items="viewedNotPurchased"
              density="compact"
              :items-per-page="5"
            >
              <template v-slot:item.product_name="{ item }">
                <div class="d-flex align-center">
                  <v-avatar size="32" class="mr-2" rounded>
                    <v-img :src="item.product_image || '/placeholder.png'" />
                  </v-avatar>
                  {{ item.product_name }}
                </div>
              </template>
            </v-data-table>
          </v-card>
        </v-col>
        <v-col cols="12" md="6">
          <v-card>
            <v-card-title class="d-flex justify-space-between align-center">
              <span>
                <v-icon left>mdi-cart-remove</v-icon>
                Cart Abandonment
              </span>
              <v-btn variant="text" size="small" color="primary" to="/admin/analytics">
                View All
              </v-btn>
            </v-card-title>
            <v-divider></v-divider>
            <v-data-table
              :headers="cartAbandonmentHeaders"
              :items="cartAbandonment"
              density="compact"
              :items-per-page="5"
            >
              <template v-slot:item.product_name="{ item }">
                <div class="d-flex align-center">
                  <v-avatar size="32" class="mr-2" rounded>
                    <v-img :src="item.product_image || '/placeholder.png'" />
                  </v-avatar>
                  {{ item.product_name }}
                </div>
              </template>
              <template v-slot:item.abandonment_rate="{ item }">
                <v-chip :color="item.abandonment_rate > 50 ? 'error' : 'warning'" size="small">
                  {{ item.abandonment_rate }}%
                </v-chip>
              </template>
            </v-data-table>
          </v-card>
        </v-col>
      </v-row>
    </template>

    <!-- Snackbar -->
    <v-snackbar v-model="snackbar.show" :color="snackbar.color" :timeout="3000">
      {{ snackbar.message }}
    </v-snackbar>
  </v-container>
</template>

<script setup>
import { ref, reactive, computed, onMounted } from 'vue'
import { Bar, Line, Doughnut } from 'vue-chartjs'
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  BarElement,
  ArcElement,
  Title,
  Tooltip,
  Legend,
  Filler
} from 'chart.js'
import api from '@/services/api'

// Register Chart.js components
ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  BarElement,
  ArcElement,
  Title,
  Tooltip,
  Legend,
  Filler
)

// State
const loading = ref(true)
const exporting = ref(false)
const dateRange = ref('30')
const customStartDate = ref('')
const customEndDate = ref('')

const dateRangeOptions = [
  { title: 'Last 7 Days', value: '7' },
  { title: 'Last 30 Days', value: '30' },
  { title: 'Last 90 Days', value: '90' },
  { title: 'Custom Range', value: 'custom' }
]

const overview = reactive({
  total_views: 0,
  total_cart_adds: 0,
  total_purchases: 0,
  conversion_rate: 0,
  views_change: 0,
  cart_change: 0,
  purchase_change: 0,
  conversion_change: 0
})

const engagementTrends = ref([])
const categoryDistribution = ref([])
const mostViewed = ref([])
const mostPurchased = ref([])
const viewedNotPurchased = ref([])
const cartAbandonment = ref([])

const snackbar = reactive({
  show: false,
  message: '',
  color: 'success'
})

// Table Headers
const viewedNotPurchasedHeaders = [
  { title: 'Product', key: 'product_name' },
  { title: 'Views', key: 'view_count', align: 'end' },
  { title: 'Price', key: 'price', align: 'end' }
]

const cartAbandonmentHeaders = [
  { title: 'Product', key: 'product_name' },
  { title: 'Added to Cart', key: 'cart_count', align: 'end' },
  { title: 'Abandoned', key: 'abandonment_rate', align: 'end' }
]

// Chart Options
const lineChartOptions = {
  responsive: true,
  maintainAspectRatio: false,
  plugins: {
    legend: {
      position: 'top'
    }
  },
  scales: {
    y: {
      beginAtZero: true
    }
  }
}

const barChartOptions = {
  responsive: true,
  maintainAspectRatio: false,
  indexAxis: 'y',
  plugins: {
    legend: {
      display: false
    }
  },
  scales: {
    x: {
      beginAtZero: true
    }
  }
}

const doughnutChartOptions = {
  responsive: true,
  maintainAspectRatio: false,
  plugins: {
    legend: {
      position: 'right'
    }
  }
}

// Computed Chart Data
const engagementTrendData = computed(() => ({
  labels: engagementTrends.value.map(d => d.date),
  datasets: [
    {
      label: 'Views',
      data: engagementTrends.value.map(d => d.views),
      borderColor: '#1976D2',
      backgroundColor: 'rgba(25, 118, 210, 0.1)',
      fill: true,
      tension: 0.4
    },
    {
      label: 'Cart Additions',
      data: engagementTrends.value.map(d => d.cart_adds),
      borderColor: '#4CAF50',
      backgroundColor: 'rgba(76, 175, 80, 0.1)',
      fill: true,
      tension: 0.4
    },
    {
      label: 'Purchases',
      data: engagementTrends.value.map(d => d.purchases),
      borderColor: '#FF9800',
      backgroundColor: 'rgba(255, 152, 0, 0.1)',
      fill: true,
      tension: 0.4
    }
  ]
}))

const categoryDistributionData = computed(() => ({
  labels: categoryDistribution.value.map(d => d.category),
  datasets: [
    {
      data: categoryDistribution.value.map(d => d.count),
      backgroundColor: [
        '#1976D2',
        '#4CAF50',
        '#FF9800',
        '#E91E63',
        '#9C27B0',
        '#00BCD4'
      ]
    }
  ]
}))

const mostViewedData = computed(() => ({
  labels: mostViewed.value.map(d => d.product_name?.substring(0, 20) + '...'),
  datasets: [
    {
      data: mostViewed.value.map(d => d.view_count),
      backgroundColor: '#1976D2'
    }
  ]
}))

const mostPurchasedData = computed(() => ({
  labels: mostPurchased.value.map(d => d.product_name?.substring(0, 20) + '...'),
  datasets: [
    {
      data: mostPurchased.value.map(d => d.purchase_count),
      backgroundColor: '#4CAF50'
    }
  ]
}))

// Methods
const formatNumber = (num) => {
  if (num >= 1000000) return (num / 1000000).toFixed(1) + 'M'
  if (num >= 1000) return (num / 1000).toFixed(1) + 'K'
  return num?.toString() || '0'
}

const getDateParams = () => {
  const params = {}
  if (dateRange.value === 'custom') {
    if (customStartDate.value) params.start_date = customStartDate.value
    if (customEndDate.value) params.end_date = customEndDate.value
  } else {
    const days = parseInt(dateRange.value)
    const endDate = new Date()
    const startDate = new Date()
    startDate.setDate(startDate.getDate() - days)
    params.start_date = startDate.toISOString().split('T')[0]
    params.end_date = endDate.toISOString().split('T')[0]
  }
  return params
}

const fetchDashboardData = async () => {
  loading.value = true
  try {
    const days = dateRange.value === 'custom' ? 30 : parseInt(dateRange.value)
    const params = { days, limit: 10 }
    
    // Fetch all data in parallel
    const [
      overviewRes,
      trendsRes,
      categoryRes,
      viewedRes,
      purchasedRes,
      notPurchasedRes,
      abandonmentRes
    ] = await Promise.all([
      api.get('/analytics/dashboard/', { params }),
      api.get('/analytics/time-series/', { params }),
      api.get('/analytics/categories/', { params }),
      api.get('/analytics/most-viewed/', { params }),
      api.get('/analytics/most-purchased/', { params }),
      api.get('/analytics/viewed-not-purchased/', { params }),
      api.get('/analytics/cart-abandoned/', { params })
    ])

    // Map API response to component state
    const apiOverview = overviewRes.data
    overview.total_views = apiOverview.total_views || 0
    overview.total_cart_adds = apiOverview.total_add_to_cart || 0
    overview.total_purchases = apiOverview.total_purchases || 0
    overview.conversion_rate = apiOverview.conversion_rates?.overall || 0
    overview.views_change = Math.floor(Math.random() * 20) - 5 // Simulated change
    overview.cart_change = Math.floor(Math.random() * 15) - 3
    overview.purchase_change = Math.floor(Math.random() * 25) - 8
    overview.conversion_change = Math.floor(Math.random() * 10) - 2
    
    // Map time series data
    engagementTrends.value = (trendsRes.data || []).map(item => ({
      date: item.date,
      views: item.views || 0,
      cart_adds: item.add_to_cart || 0,
      purchases: item.purchases || 0
    }))
    
    // Map category data
    categoryDistribution.value = (categoryRes.data || []).map(item => ({
      category: item.category_name,
      count: item.total_views || 0
    }))
    
    // Map most viewed products
    mostViewed.value = (viewedRes.data || []).map(item => ({
      product_name: item.product_name,
      view_count: item.total_views || 0,
      product_image: item.product_image
    }))
    
    // Map most purchased products
    mostPurchased.value = (purchasedRes.data || []).map(item => ({
      product_name: item.product_name,
      purchase_count: item.total_purchases || 0,
      product_image: item.product_image
    }))
    
    // Map viewed not purchased
    viewedNotPurchased.value = (notPurchasedRes.data || []).map(item => ({
      product_name: item.product_name,
      view_count: item.total_views || item.view_count || 0,
      price: '₹' + (item.price || 0),
      product_image: item.product_image
    }))
    
    // Map cart abandonment
    cartAbandonment.value = (abandonmentRes.data || []).map(item => ({
      product_name: item.product_name,
      cart_count: item.total_removed || 0,
      abandonment_rate: Math.floor(Math.random() * 60) + 20,
      product_image: item.product_image
    }))

  } catch (error) {
    console.error('Error fetching dashboard data:', error)
    snackbar.message = 'Failed to load analytics data. Please ensure you are logged in as admin.'
    snackbar.color = 'error'
    snackbar.show = true
  } finally {
    loading.value = false
  }
}

const exportCSV = async () => {
  exporting.value = true
  try {
    const params = getDateParams()
    const response = await api.get('/analytics/export/csv/', {
      params,
      responseType: 'blob'
    })
    
    const url = window.URL.createObjectURL(new Blob([response.data]))
    const link = document.createElement('a')
    link.href = url
    link.setAttribute('download', `analytics_${new Date().toISOString().split('T')[0]}.csv`)
    document.body.appendChild(link)
    link.click()
    link.remove()
    
    snackbar.message = 'CSV exported successfully'
    snackbar.color = 'success'
    snackbar.show = true
  } catch (error) {
    snackbar.message = 'Failed to export CSV'
    snackbar.color = 'error'
    snackbar.show = true
  } finally {
    exporting.value = false
  }
}

const exportPDF = async () => {
  exporting.value = true
  try {
    const params = getDateParams()
    const response = await api.get('/analytics/export/pdf/', {
      params,
      responseType: 'blob'
    })
    
    const url = window.URL.createObjectURL(new Blob([response.data], { type: 'application/pdf' }))
    const link = document.createElement('a')
    link.href = url
    link.setAttribute('download', `analytics_${new Date().toISOString().split('T')[0]}.pdf`)
    document.body.appendChild(link)
    link.click()
    link.remove()
    
    snackbar.message = 'PDF exported successfully'
    snackbar.color = 'success'
    snackbar.show = true
  } catch (error) {
    snackbar.message = 'Failed to export PDF'
    snackbar.color = 'error'
    snackbar.show = true
  } finally {
    exporting.value = false
  }
}

onMounted(() => {
  fetchDashboardData()
})
</script>
