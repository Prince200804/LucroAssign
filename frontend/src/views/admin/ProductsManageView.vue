<template>
  <v-container fluid class="pa-6">
    <!-- Header -->
    <div class="d-flex justify-space-between align-center mb-6">
      <div>
        <h1 class="text-h4 font-weight-bold">Product Management</h1>
        <p class="text-body-2 text-grey">Manage your product catalog</p>
      </div>
      <v-btn color="primary" prepend-icon="mdi-plus" @click="openProductDialog()">
        Add Product
      </v-btn>
    </div>

    <!-- Filters -->
    <v-card class="mb-6">
      <v-card-text>
        <v-row align="center">
          <v-col cols="12" sm="4">
            <v-text-field
              v-model="search"
              label="Search Products"
              prepend-inner-icon="mdi-magnify"
              variant="outlined"
              density="compact"
              hide-details
              clearable
            ></v-text-field>
          </v-col>
          <v-col cols="12" sm="3">
            <v-select
              v-model="filterCategory"
              :items="categories"
              label="Category"
              variant="outlined"
              density="compact"
              hide-details
              clearable
            ></v-select>
          </v-col>
          <v-col cols="12" sm="2">
            <v-select
              v-model="filterStock"
              :items="stockOptions"
              label="Stock Status"
              variant="outlined"
              density="compact"
              hide-details
              clearable
            ></v-select>
          </v-col>
          <v-col cols="12" sm="3" class="d-flex gap-2">
            <v-btn variant="outlined" @click="resetFilters">
              Reset
            </v-btn>
            <v-btn color="primary" @click="fetchProducts">
              Apply
            </v-btn>
          </v-col>
        </v-row>
      </v-card-text>
    </v-card>

    <!-- Products Table -->
    <v-card>
      <v-data-table-server
        v-model:items-per-page="itemsPerPage"
        v-model:page="page"
        :headers="headers"
        :items="products"
        :items-length="totalProducts"
        :loading="loading"
        class="elevation-0"
        @update:options="fetchProducts"
      >
        <template v-slot:item.product="{ item }">
          <div class="d-flex align-center py-2">
            <v-avatar size="48" rounded class="mr-3">
              <v-img :src="item.image || 'https://via.placeholder.com/100?text=No+Image'" />
            </v-avatar>
            <div>
              <div class="font-weight-medium">{{ item.name }}</div>
              <div class="text-caption text-grey">SKU: {{ item.sku }}</div>
            </div>
          </div>
        </template>

        <template v-slot:item.category="{ item }">
          <v-chip size="small" color="primary" variant="tonal">
            {{ item.category_name }}
          </v-chip>
        </template>

        <template v-slot:item.price="{ item }">
          <div>
            <span class="font-weight-bold">₹{{ item.price }}</span>
            <span v-if="item.discount_price" class="text-caption text-grey ml-2 text-decoration-line-through">
              ₹{{ item.discount_price }}
            </span>
          </div>
        </template>

        <template v-slot:item.stock="{ item }">
          <v-chip
            :color="getStockColor(item.stock)"
            size="small"
          >
            {{ item.stock }} units
          </v-chip>
        </template>

        <template v-slot:item.is_active="{ item }">
          <v-switch
            v-model="item.is_active"
            color="success"
            hide-details
            density="compact"
            @change="toggleProductStatus(item)"
          ></v-switch>
        </template>

        <template v-slot:item.actions="{ item }">
          <v-btn
            icon
            variant="text"
            size="small"
            color="info"
            @click="viewProduct(item)"
            title="View Product"
          >
            <v-icon>mdi-eye</v-icon>
          </v-btn>
          <v-btn
            icon
            variant="text"
            size="small"
            color="primary"
            @click="openProductDialog(item)"
            title="Edit Product"
          >
            <v-icon>mdi-pencil</v-icon>
          </v-btn>
          <v-btn
            icon
            variant="text"
            size="small"
            color="error"
            @click="confirmDelete(item)"
            title="Delete Product"
          >
            <v-icon>mdi-delete</v-icon>
          </v-btn>
        </template>
      </v-data-table-server>
    </v-card>

    <!-- Product Dialog -->
    <v-dialog v-model="productDialog" max-width="900" persistent scrollable>
      <v-card>
        <v-card-title class="d-flex justify-space-between align-center pa-4">
          <span class="text-h5">{{ editingProduct ? 'Edit Product' : 'Add New Product' }}</span>
          <v-btn icon variant="text" @click="productDialog = false">
            <v-icon>mdi-close</v-icon>
          </v-btn>
        </v-card-title>
        <v-divider></v-divider>
        <v-card-text class="pa-6">
          <v-form ref="productForm" @submit.prevent="saveProduct">
            <v-row>
              <!-- Basic Info -->
              <v-col cols="12">
                <h3 class="text-subtitle-1 font-weight-bold mb-3">Basic Information</h3>
              </v-col>
              <v-col cols="12" md="6">
                <v-text-field
                  v-model="productFormData.name"
                  label="Product Name *"
                  variant="outlined"
                  :rules="[v => !!v || 'Name is required']"
                ></v-text-field>
              </v-col>
              <v-col cols="12" md="6">
                <v-text-field
                  v-model="productFormData.sku"
                  label="SKU *"
                  variant="outlined"
                  :rules="[v => !!v || 'SKU is required']"
                ></v-text-field>
              </v-col>
              <v-col cols="12" md="6">
                <v-select
                  v-model="productFormData.category"
                  :items="categories"
                  label="Category *"
                  variant="outlined"
                  :rules="[v => !!v || 'Category is required']"
                ></v-select>
              </v-col>
              <v-col cols="12" md="6">
                <v-text-field
                  v-model="productFormData.brand"
                  label="Brand"
                  variant="outlined"
                ></v-text-field>
              </v-col>
              <v-col cols="12">
                <v-textarea
                  v-model="productFormData.short_description"
                  label="Short Description"
                  variant="outlined"
                  rows="2"
                  counter="200"
                ></v-textarea>
              </v-col>
              <v-col cols="12">
                <v-textarea
                  v-model="productFormData.description"
                  label="Full Description"
                  variant="outlined"
                  rows="4"
                ></v-textarea>
              </v-col>

              <!-- Pricing -->
              <v-col cols="12">
                <h3 class="text-subtitle-1 font-weight-bold mb-3">Pricing & Inventory</h3>
              </v-col>
              <v-col cols="12" md="4">
                <v-text-field
                  v-model.number="productFormData.price"
                  label="Price (₹) *"
                  variant="outlined"
                  type="number"
                  prefix="₹"
                  :rules="[v => v > 0 || 'Price must be positive']"
                ></v-text-field>
              </v-col>
              <v-col cols="12" md="4">
                <v-text-field
                  v-model.number="productFormData.discount_price"
                  label="Discount Price (₹)"
                  variant="outlined"
                  type="number"
                  prefix="₹"
                  hint="Leave empty for no discount"
                  persistent-hint
                ></v-text-field>
              </v-col>
              <v-col cols="12" md="4">
                <v-text-field
                  v-model.number="productFormData.stock"
                  label="Stock Quantity *"
                  variant="outlined"
                  type="number"
                  :rules="[v => v >= 0 || 'Stock cannot be negative']"
                ></v-text-field>
              </v-col>

              <!-- Image -->
              <v-col cols="12">
                <h3 class="text-subtitle-1 font-weight-bold mb-3">Product Image</h3>
              </v-col>
              <v-col cols="12" md="8">
                <v-text-field
                  v-model="productFormData.image_url"
                  label="Image URL"
                  variant="outlined"
                  placeholder="https://images.unsplash.com/..."
                  hint="Enter a valid image URL from Unsplash or other sources"
                  persistent-hint
                ></v-text-field>
              </v-col>
              <v-col cols="12" md="4">
                <div v-if="productFormData.image_url" class="preview-container">
                  <v-img
                    :src="productFormData.image_url"
                    height="120"
                    cover
                    class="rounded"
                  >
                    <template v-slot:error>
                      <div class="d-flex align-center justify-center fill-height bg-grey-darken-3">
                        <v-icon size="40" color="grey">mdi-image-broken</v-icon>
                      </div>
                    </template>
                  </v-img>
                  <span class="text-caption text-grey">Image Preview</span>
                </div>
              </v-col>

              <!-- Specifications -->
              <v-col cols="12">
                <h3 class="text-subtitle-1 font-weight-bold mb-3">Specifications</h3>
              </v-col>
              <v-col cols="12">
                <v-textarea
                  v-model="productFormData.specifications"
                  label="Specifications (JSON format)"
                  variant="outlined"
                  rows="4"
                  placeholder='{"Color": "Black", "Weight": "150g", "Material": "Plastic"}'
                  hint="Enter product specifications in JSON format"
                  persistent-hint
                ></v-textarea>
              </v-col>

              <!-- Status -->
              <v-col cols="12">
                <h3 class="text-subtitle-1 font-weight-bold mb-3">Status</h3>
              </v-col>
              <v-col cols="12" md="6">
                <v-switch
                  v-model="productFormData.is_active"
                  label="Active (Visible to customers)"
                  color="success"
                ></v-switch>
              </v-col>
              <v-col cols="12" md="6">
                <v-switch
                  v-model="productFormData.is_featured"
                  label="Featured (Show on homepage)"
                  color="primary"
                ></v-switch>
              </v-col>
            </v-row>
          </v-form>
        </v-card-text>
        <v-divider></v-divider>
        <v-card-actions class="pa-4">
          <v-spacer></v-spacer>
          <v-btn variant="text" @click="productDialog = false">Cancel</v-btn>
          <v-btn color="primary" variant="elevated" @click="saveProduct" :loading="saving">
            {{ editingProduct ? 'Update Product' : 'Create Product' }}
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>

    <!-- Delete Confirmation Dialog -->
    <v-dialog v-model="deleteDialog" max-width="450">
      <v-card>
        <v-card-title class="text-h6">
          <v-icon color="error" class="mr-2">mdi-alert-circle</v-icon>
          Confirm Delete
        </v-card-title>
        <v-card-text>
          Are you sure you want to delete <strong>{{ productToDelete?.name }}</strong>? 
          This action cannot be undone and will remove all associated data.
        </v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn variant="text" @click="deleteDialog = false">Cancel</v-btn>
          <v-btn color="error" variant="elevated" @click="deleteProduct" :loading="deleting">
            Delete Product
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
import { useRouter } from 'vue-router'
import api from '@/services/api'

const router = useRouter()

// State
const loading = ref(true)
const saving = ref(false)
const deleting = ref(false)
const products = ref([])
const totalProducts = ref(0)
const page = ref(1)
const itemsPerPage = ref(10)
const search = ref('')
const filterCategory = ref(null)
const filterStock = ref(null)
const categories = ref([])
const productDialog = ref(false)
const deleteDialog = ref(false)
const editingProduct = ref(null)
const productToDelete = ref(null)
const productForm = ref(null)

const stockOptions = [
  { title: 'In Stock (10+)', value: 'in_stock' },
  { title: 'Low Stock (1-9)', value: 'low_stock' },
  { title: 'Out of Stock (0)', value: 'out_of_stock' }
]

const productFormData = reactive({
  name: '',
  sku: '',
  short_description: '',
  description: '',
  category: null,
  brand: '',
  price: 0,
  discount_price: null,
  stock: 0,
  image_url: '',
  specifications: '',
  is_active: true,
  is_featured: false
})

const snackbar = reactive({
  show: false,
  message: '',
  color: 'success'
})

const headers = [
  { title: 'Product', key: 'product', sortable: false, width: '300px' },
  { title: 'Category', key: 'category', sortable: false },
  { title: 'Price', key: 'price' },
  { title: 'Stock', key: 'stock' },
  { title: 'Active', key: 'is_active', sortable: false },
  { title: 'Actions', key: 'actions', sortable: false, align: 'end', width: '150px' }
]

// Methods
const showMessage = (message, color = 'success') => {
  snackbar.message = message
  snackbar.color = color
  snackbar.show = true
}

const getStockColor = (stock) => {
  if (stock === 0) return 'error'
  if (stock < 10) return 'warning'
  return 'success'
}

const fetchCategories = async () => {
  try {
    const response = await api.get('/products/categories/')
    categories.value = response.data.map(c => ({ title: c.name, value: c.id }))
  } catch (error) {
    console.error('Error fetching categories:', error)
  }
}

const fetchProducts = async () => {
  loading.value = true
  try {
    const params = {
      page: page.value,
      page_size: itemsPerPage.value,
      search: search.value || undefined,
      category: filterCategory.value || undefined
    }

    if (filterStock.value === 'in_stock') params.stock_min = 10
    else if (filterStock.value === 'low_stock') {
      params.stock_min = 1
      params.stock_max = 9
    } else if (filterStock.value === 'out_of_stock') {
      params.stock_max = 0
    }

    const response = await api.get('/products/', { params })
    products.value = response.data.results || response.data
    totalProducts.value = response.data.count || products.value.length
  } catch (error) {
    console.error('Error fetching products:', error)
    showMessage('Failed to load products', 'error')
  } finally {
    loading.value = false
  }
}

const resetFilters = () => {
  search.value = ''
  filterCategory.value = null
  filterStock.value = null
  page.value = 1
  fetchProducts()
}

const viewProduct = (product) => {
  router.push(`/products/${product.slug}`)
}

const openProductDialog = (product = null) => {
  editingProduct.value = product
  if (product) {
    Object.assign(productFormData, {
      name: product.name,
      sku: product.sku,
      short_description: product.short_description || '',
      description: product.description || '',
      category: product.category,
      brand: product.brand || '',
      price: product.price,
      discount_price: product.discount_price || null,
      stock: product.stock,
      image_url: product.image || '',
      specifications: product.specifications ? JSON.stringify(product.specifications, null, 2) : '',
      is_active: product.is_active,
      is_featured: product.is_featured
    })
  } else {
    // Generate a unique SKU for new products
    const timestamp = Date.now().toString(36).toUpperCase()
    Object.assign(productFormData, {
      name: '',
      sku: `SKU-${timestamp}`,
      short_description: '',
      description: '',
      category: null,
      brand: '',
      price: 0,
      discount_price: null,
      stock: 0,
      image_url: '',
      specifications: '',
      is_active: true,
      is_featured: false
    })
  }
  productDialog.value = true
}

const saveProduct = async () => {
  const { valid } = await productForm.value.validate()
  if (!valid) return

  saving.value = true
  try {
    // Parse specifications JSON
    let specs = {}
    if (productFormData.specifications) {
      try {
        specs = JSON.parse(productFormData.specifications)
      } catch (e) {
        showMessage('Invalid JSON format in specifications', 'error')
        saving.value = false
        return
      }
    }

    const data = {
      name: productFormData.name,
      sku: productFormData.sku,
      short_description: productFormData.short_description,
      description: productFormData.description,
      category: productFormData.category,
      brand: productFormData.brand,
      price: productFormData.price,
      discount_price: productFormData.discount_price || null,
      stock: productFormData.stock,
      image_url: productFormData.image_url,
      specifications: specs,
      is_active: productFormData.is_active,
      is_featured: productFormData.is_featured
    }

    if (editingProduct.value) {
      await api.patch(`/products/${editingProduct.value.id}/`, data)
      showMessage('Product updated successfully')
    } else {
      await api.post('/products/', data)
      showMessage('Product created successfully')
    }
    
    productDialog.value = false
    fetchProducts()
  } catch (error) {
    console.error('Error saving product:', error)
    const errorMsg = error.response?.data?.detail || 
                     error.response?.data?.error ||
                     Object.values(error.response?.data || {})[0]?.[0] ||
                     'Failed to save product'
    showMessage(errorMsg, 'error')
  } finally {
    saving.value = false
  }
}

const toggleProductStatus = async (product) => {
  try {
    await api.patch(`/products/${product.id}/`, { is_active: product.is_active })
    showMessage(`Product ${product.is_active ? 'activated' : 'deactivated'}`)
  } catch (error) {
    product.is_active = !product.is_active
    showMessage('Failed to update product status', 'error')
  }
}

const confirmDelete = (product) => {
  productToDelete.value = product
  deleteDialog.value = true
}

const deleteProduct = async () => {
  deleting.value = true
  try {
    await api.delete(`/products/${productToDelete.value.id}/`)
    showMessage('Product deleted successfully')
    deleteDialog.value = false
    fetchProducts()
  } catch (error) {
    showMessage('Failed to delete product', 'error')
  } finally {
    deleting.value = false
  }
}

onMounted(() => {
  fetchCategories()
  fetchProducts()
})
</script>

<style scoped>
.preview-container {
  text-align: center;
}

.preview-container .text-caption {
  display: block;
  margin-top: 4px;
}
</style>
