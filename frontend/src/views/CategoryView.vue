<template>
  <v-container class="py-8">
    <h1 class="text-h4 font-weight-bold mb-6">{{ categoryName }}</h1>
    
    <v-row v-if="loading">
      <v-col v-for="n in 8" :key="n" cols="12" sm="6" md="4" lg="3">
        <v-skeleton-loader type="card"></v-skeleton-loader>
      </v-col>
    </v-row>

    <v-row v-else-if="products.length === 0">
      <v-col cols="12">
        <v-card class="pa-8 text-center">
          <v-icon size="64" color="grey">mdi-package-variant-remove</v-icon>
          <h3 class="text-h5 mt-4 mb-2">No products in this category</h3>
          <v-btn color="primary" class="mt-4" to="/products">Browse All Products</v-btn>
        </v-card>
      </v-col>
    </v-row>

    <v-row v-else>
      <v-col v-for="product in products" :key="product.id" cols="12" sm="6" md="4" lg="3">
        <ProductCard :product="product" />
      </v-col>
    </v-row>

    <v-pagination
      v-if="totalPages > 1"
      v-model="currentPage"
      :length="totalPages"
      class="mt-8"
      @update:modelValue="handlePageChange"
    ></v-pagination>
  </v-container>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import { useRoute } from 'vue-router'
import { useProductStore } from '@/stores/products'
import ProductCard from '@/components/ProductCard.vue'

const route = useRoute()
const productStore = useProductStore()

const currentPage = ref(1)
const categoryName = ref('')

const loading = computed(() => productStore.loading)
const products = computed(() => productStore.products)
const pagination = computed(() => productStore.pagination)
const totalPages = computed(() => Math.ceil(pagination.value.count / 12))

const fetchProducts = async () => {
  const slug = route.params.slug
  await productStore.fetchProductsByCategory(slug, { page: currentPage.value })
  
  const category = productStore.categories.find(c => c.slug === slug)
  categoryName.value = category?.name || 'Category'
}

const handlePageChange = () => {
  fetchProducts()
  window.scrollTo({ top: 0, behavior: 'smooth' })
}

watch(() => route.params.slug, () => {
  currentPage.value = 1
  fetchProducts()
})

onMounted(async () => {
  await productStore.fetchCategories()
  await fetchProducts()
})
</script>
