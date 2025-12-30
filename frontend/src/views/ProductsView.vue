<template>
  <div class="products-page">
    <!-- Hero Banner -->
    <div class="page-hero">
      <div class="hero-bg"></div>
      <v-container>
        <div class="hero-content text-center">
          <h1 class="page-title">
            <span class="gradient-text">Explore</span> Products
          </h1>
          <p class="page-subtitle">
            Discover amazing products curated just for you
          </p>
          <div class="products-count">
            <v-icon class="mr-2">mdi-package-variant</v-icon>
            {{ pagination.count || 0 }} products found
          </div>
        </div>
      </v-container>
    </div>

    <v-container class="py-8">
      <v-row>
        <!-- Filters Sidebar -->
        <v-col cols="12" md="3">
          <div class="filter-sidebar">
            <div class="filter-header">
              <v-icon class="mr-2" color="primary">mdi-filter-variant</v-icon>
              <span>Filters</span>
            </div>
            
            <!-- Search -->
            <div class="filter-section">
              <label class="filter-label">Search</label>
              <div class="search-input-wrapper">
                <v-icon class="search-icon">mdi-magnify</v-icon>
                <input
                  v-model="searchQuery"
                  type="text"
                  placeholder="Search products..."
                  class="modern-input"
                  @input="handleSearch"
                />
                <button v-if="searchQuery" class="clear-btn" @click="searchQuery = ''; handleSearch()">
                  <v-icon size="16">mdi-close</v-icon>
                </button>
              </div>
            </div>

            <!-- Categories -->
            <div class="filter-section">
              <label class="filter-label">Categories</label>
              <div class="category-list">
                <button
                  class="category-item"
                  :class="{ active: !selectedCategory }"
                  @click="selectCategory(null)"
                >
                  <v-icon size="18" class="mr-2">mdi-view-grid</v-icon>
                  All Categories
                </button>
                <button
                  v-for="category in categories"
                  :key="category.id"
                  class="category-item"
                  :class="{ active: selectedCategory === category.id }"
                  @click="selectCategory(category.id)"
                >
                  <v-icon size="18" class="mr-2">mdi-tag</v-icon>
                  {{ category.name }}
                  <span class="category-count">{{ category.product_count }}</span>
                </button>
              </div>
            </div>

            <!-- Sort By -->
            <div class="filter-section">
              <label class="filter-label">Sort By</label>
              <select v-model="sortBy" class="modern-select" @change="handleSort">
                <option v-for="option in sortOptions" :key="option.value" :value="option.value">
                  {{ option.label }}
                </option>
              </select>
            </div>

            <!-- Clear Filters -->
            <button class="clear-filters-btn" @click="clearFilters">
              <v-icon size="18" class="mr-2">mdi-refresh</v-icon>
              Clear All Filters
            </button>
          </div>
        </v-col>

        <!-- Products Grid -->
        <v-col cols="12" md="9">
          <!-- Loading State -->
          <div v-if="loading" class="products-grid">
            <div v-for="n in 9" :key="n" class="skeleton-card">
              <div class="skeleton-image"></div>
              <div class="skeleton-content">
                <div class="skeleton-line short"></div>
                <div class="skeleton-line"></div>
                <div class="skeleton-line medium"></div>
              </div>
            </div>
          </div>

          <!-- Empty State -->
          <div v-else-if="products.length === 0" class="empty-state">
            <div class="empty-icon">
              <v-icon size="80">mdi-package-variant-remove</v-icon>
            </div>
            <h3>No Products Found</h3>
            <p>Try adjusting your filters or search query</p>
            <button class="primary-btn" @click="clearFilters">
              <v-icon size="18" class="mr-2">mdi-refresh</v-icon>
              Clear Filters
            </button>
          </div>

          <!-- Products Grid -->
          <div v-else class="products-grid">
            <div
              v-for="product in products"
              :key="product.id"
              class="product-grid-item"
            >
              <ProductCard :product="product" />
            </div>
          </div>

          <!-- Pagination -->
          <div v-if="totalPages > 1" class="pagination-wrapper">
            <button
              class="page-btn"
              :disabled="currentPage === 1"
              @click="currentPage--; handlePageChange()"
            >
              <v-icon>mdi-chevron-left</v-icon>
            </button>
            
            <div class="page-numbers">
              <button
                v-for="page in visiblePages"
                :key="page"
                class="page-num"
                :class="{ active: page === currentPage }"
                @click="currentPage = page; handlePageChange()"
              >
                {{ page }}
              </button>
            </div>
            
            <button
              class="page-btn"
              :disabled="currentPage === totalPages"
              @click="currentPage++; handlePageChange()"
            >
              <v-icon>mdi-chevron-right</v-icon>
            </button>
          </div>
        </v-col>
      </v-row>
    </v-container>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useProductStore } from '@/stores/products'
import ProductCard from '@/components/ProductCard.vue'

const route = useRoute()
const router = useRouter()
const productStore = useProductStore()

const searchQuery = ref('')
const selectedCategory = ref(null)
const sortBy = ref('-created_at')
const currentPage = ref(1)

const sortOptions = [
  { label: 'Newest First', value: '-created_at' },
  { label: 'Oldest First', value: 'created_at' },
  { label: 'Price: Low to High', value: 'price' },
  { label: 'Price: High to Low', value: '-price' },
  { label: 'Name: A-Z', value: 'name' },
  { label: 'Name: Z-A', value: '-name' },
]

const loading = computed(() => productStore.loading)
const products = computed(() => productStore.products)
const categories = computed(() => productStore.categories)
const pagination = computed(() => productStore.pagination)
const totalPages = computed(() => Math.ceil(pagination.value.count / 12))

const visiblePages = computed(() => {
  const pages = []
  const start = Math.max(1, currentPage.value - 2)
  const end = Math.min(totalPages.value, currentPage.value + 2)
  for (let i = start; i <= end; i++) {
    pages.push(i)
  }
  return pages
})

const fetchProducts = async () => {
  await productStore.fetchProducts({
    page: currentPage.value,
    search: searchQuery.value || undefined,
    category: selectedCategory.value || undefined,
    ordering: sortBy.value,
  })
}

const handleSearch = () => {
  currentPage.value = 1
  fetchProducts()
}

const selectCategory = (categoryId) => {
  selectedCategory.value = categoryId
  currentPage.value = 1
  fetchProducts()
}

const handleSort = () => {
  currentPage.value = 1
  fetchProducts()
}

const handlePageChange = () => {
  fetchProducts()
  window.scrollTo({ top: 0, behavior: 'smooth' })
}

const clearFilters = () => {
  searchQuery.value = ''
  selectedCategory.value = null
  sortBy.value = '-created_at'
  currentPage.value = 1
  fetchProducts()
}

onMounted(async () => {
  await productStore.fetchCategories()
  
  // Check for query params
  if (route.query.search) {
    searchQuery.value = route.query.search
  }
  if (route.query.category) {
    selectedCategory.value = route.query.category
  }
  
  await fetchProducts()
})
</script>

<style scoped>
.products-page {
  min-height: 100vh;
}

/* Hero Banner */
.page-hero {
  position: relative;
  padding: 80px 0 60px;
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
  font-size: 3rem;
  font-weight: 800;
  color: #ffffff;
  margin-bottom: 16px;
}

.gradient-text {
  background: linear-gradient(135deg, #6366F1, #8B5CF6, #EC4899);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.page-subtitle {
  font-size: 1.1rem;
  color: rgba(255, 255, 255, 0.7);
  margin-bottom: 24px;
}

.products-count {
  display: inline-flex;
  align-items: center;
  background: rgba(99, 102, 241, 0.1);
  border: 1px solid rgba(99, 102, 241, 0.3);
  padding: 10px 20px;
  border-radius: 30px;
  color: #8B5CF6;
  font-weight: 500;
}

/* Filter Sidebar */
.filter-sidebar {
  background: rgba(30, 30, 46, 0.6);
  backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.05);
  border-radius: 20px;
  padding: 24px;
  position: sticky;
  top: 100px;
}

.filter-header {
  display: flex;
  align-items: center;
  font-size: 1.2rem;
  font-weight: 700;
  color: #ffffff;
  margin-bottom: 24px;
  padding-bottom: 16px;
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
}

.filter-section {
  margin-bottom: 24px;
}

.filter-label {
  display: block;
  font-size: 13px;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 1px;
  color: rgba(255, 255, 255, 0.6);
  margin-bottom: 12px;
}

/* Search Input */
.search-input-wrapper {
  position: relative;
}

.search-icon {
  position: absolute;
  left: 14px;
  top: 50%;
  transform: translateY(-50%);
  color: rgba(255, 255, 255, 0.4);
}

.modern-input {
  width: 100%;
  padding: 12px 40px 12px 44px;
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 12px;
  color: #ffffff;
  font-size: 14px;
  transition: all 0.3s ease;
}

.modern-input:focus {
  outline: none;
  border-color: #6366F1;
  background: rgba(99, 102, 241, 0.1);
}

.modern-input::placeholder {
  color: rgba(255, 255, 255, 0.4);
}

.clear-btn {
  position: absolute;
  right: 10px;
  top: 50%;
  transform: translateY(-50%);
  background: rgba(255, 255, 255, 0.1);
  border: none;
  border-radius: 50%;
  width: 24px;
  height: 24px;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  color: rgba(255, 255, 255, 0.6);
}

/* Category List */
.category-list {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.category-item {
  display: flex;
  align-items: center;
  padding: 12px 16px;
  background: rgba(255, 255, 255, 0.03);
  border: 1px solid transparent;
  border-radius: 12px;
  color: rgba(255, 255, 255, 0.7);
  font-size: 14px;
  cursor: pointer;
  transition: all 0.3s ease;
  text-align: left;
}

.category-item:hover {
  background: rgba(99, 102, 241, 0.1);
  color: #ffffff;
}

.category-item.active {
  background: linear-gradient(135deg, rgba(99, 102, 241, 0.2), rgba(139, 92, 246, 0.2));
  border-color: rgba(99, 102, 241, 0.3);
  color: #8B5CF6;
}

.category-count {
  margin-left: auto;
  background: rgba(255, 255, 255, 0.1);
  padding: 2px 8px;
  border-radius: 10px;
  font-size: 12px;
}

/* Modern Select */
.modern-select {
  width: 100%;
  padding: 12px 16px;
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 12px;
  color: #ffffff;
  font-size: 14px;
  cursor: pointer;
  appearance: none;
  background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='24' height='24' viewBox='0 0 24 24' fill='none' stroke='%23888' stroke-width='2'%3E%3Cpath d='M6 9l6 6 6-6'/%3E%3C/svg%3E");
  background-repeat: no-repeat;
  background-position: right 12px center;
}

.modern-select:focus {
  outline: none;
  border-color: #6366F1;
}

.modern-select option {
  background: #1e1e2e;
  color: #ffffff;
}

/* Clear Filters Button */
.clear-filters-btn {
  width: 100%;
  padding: 14px;
  background: transparent;
  border: 1px solid rgba(255, 255, 255, 0.2);
  border-radius: 12px;
  color: rgba(255, 255, 255, 0.7);
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.3s ease;
}

.clear-filters-btn:hover {
  border-color: #EF4444;
  color: #EF4444;
  background: rgba(239, 68, 68, 0.1);
}

/* Products Grid */
.products-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 24px;
}

@media (max-width: 1200px) {
  .products-grid {
    grid-template-columns: repeat(2, 1fr);
  }
}

@media (max-width: 768px) {
  .products-grid {
    grid-template-columns: 1fr;
  }
}

.product-grid-item {
  height: 100%;
}

/* Skeleton Loading */
.skeleton-card {
  background: rgba(30, 30, 46, 0.6);
  border-radius: 20px;
  overflow: hidden;
}

.skeleton-image {
  height: 220px;
  background: linear-gradient(90deg, rgba(255, 255, 255, 0.05), rgba(255, 255, 255, 0.1), rgba(255, 255, 255, 0.05));
  background-size: 200% 100%;
  animation: shimmer 1.5s infinite;
}

.skeleton-content {
  padding: 20px;
}

.skeleton-line {
  height: 16px;
  background: linear-gradient(90deg, rgba(255, 255, 255, 0.05), rgba(255, 255, 255, 0.1), rgba(255, 255, 255, 0.05));
  background-size: 200% 100%;
  animation: shimmer 1.5s infinite;
  border-radius: 8px;
  margin-bottom: 12px;
}

.skeleton-line.short {
  width: 40%;
}

.skeleton-line.medium {
  width: 60%;
}

@keyframes shimmer {
  0% { background-position: 200% 0; }
  100% { background-position: -200% 0; }
}

/* Empty State */
.empty-state {
  text-align: center;
  padding: 80px 40px;
  background: rgba(30, 30, 46, 0.6);
  border-radius: 24px;
  border: 1px solid rgba(255, 255, 255, 0.05);
}

.empty-icon {
  width: 120px;
  height: 120px;
  margin: 0 auto 24px;
  background: rgba(99, 102, 241, 0.1);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #6366F1;
}

.empty-state h3 {
  font-size: 1.5rem;
  font-weight: 700;
  color: #ffffff;
  margin-bottom: 8px;
}

.empty-state p {
  color: rgba(255, 255, 255, 0.6);
  margin-bottom: 24px;
}

.primary-btn {
  display: inline-flex;
  align-items: center;
  padding: 14px 28px;
  background: linear-gradient(135deg, #6366F1, #8B5CF6);
  border: none;
  border-radius: 12px;
  color: white;
  font-size: 14px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
}

.primary-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 10px 30px rgba(99, 102, 241, 0.4);
}

/* Pagination */
.pagination-wrapper {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  margin-top: 48px;
}

.page-btn {
  width: 44px;
  height: 44px;
  border-radius: 12px;
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid rgba(255, 255, 255, 0.1);
  color: #ffffff;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.3s ease;
}

.page-btn:hover:not(:disabled) {
  background: rgba(99, 102, 241, 0.2);
  border-color: #6366F1;
}

.page-btn:disabled {
  opacity: 0.4;
  cursor: not-allowed;
}

.page-numbers {
  display: flex;
  gap: 8px;
}

.page-num {
  width: 44px;
  height: 44px;
  border-radius: 12px;
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid rgba(255, 255, 255, 0.1);
  color: rgba(255, 255, 255, 0.7);
  font-weight: 500;
  cursor: pointer;
  transition: all 0.3s ease;
}

.page-num:hover {
  background: rgba(99, 102, 241, 0.2);
  color: #ffffff;
}

.page-num.active {
  background: linear-gradient(135deg, #6366F1, #8B5CF6);
  border-color: transparent;
  color: #ffffff;
}

/* Responsive */
@media (max-width: 960px) {
  .page-title {
    font-size: 2rem;
  }
  
  .filter-sidebar {
    position: relative;
    top: 0;
    margin-bottom: 24px;
  }
}
</style>
