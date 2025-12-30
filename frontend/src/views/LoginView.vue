<template>
  <div class="auth-page">
    <!-- Background Effects -->
    <div class="auth-bg">
      <div class="gradient-orb orb-1"></div>
      <div class="gradient-orb orb-2"></div>
      <div class="gradient-orb orb-3"></div>
    </div>

    <v-container class="auth-container">
      <div class="auth-card">
        <!-- Left Side - Branding -->
        <div class="auth-branding">
          <div class="brand-content">
            <div class="brand-logo">
              <v-icon size="48">mdi-shopping</v-icon>
            </div>
            <h2>Welcome Back!</h2>
            <p>Sign in to access your account and continue shopping</p>
            
            <div class="features-list">
              <div class="feature-item">
                <v-icon size="20">mdi-check-circle</v-icon>
                <span>Track your orders</span>
              </div>
              <div class="feature-item">
                <v-icon size="20">mdi-check-circle</v-icon>
                <span>Save your favorites</span>
              </div>
              <div class="feature-item">
                <v-icon size="20">mdi-check-circle</v-icon>
                <span>Exclusive deals</span>
              </div>
            </div>
          </div>
        </div>

        <!-- Right Side - Form -->
        <div class="auth-form-section">
          <div class="form-header">
            <h1>Sign In</h1>
            <p>Enter your credentials to continue</p>
          </div>

          <form @submit.prevent="handleLogin" class="auth-form">
            <div class="form-group">
              <label for="email">Email Address</label>
              <div class="input-wrapper">
                <v-icon class="input-icon">mdi-email-outline</v-icon>
                <input
                  id="email"
                  v-model="form.email"
                  type="email"
                  placeholder="Enter your email"
                  class="modern-input"
                  required
                />
              </div>
            </div>

            <div class="form-group">
              <label for="password">Password</label>
              <div class="input-wrapper">
                <v-icon class="input-icon">mdi-lock-outline</v-icon>
                <input
                  id="password"
                  v-model="form.password"
                  :type="showPassword ? 'text' : 'password'"
                  placeholder="Enter your password"
                  class="modern-input"
                  required
                />
                <button type="button" class="toggle-password" @click="showPassword = !showPassword">
                  <v-icon size="20">{{ showPassword ? 'mdi-eye-off' : 'mdi-eye' }}</v-icon>
                </button>
              </div>
            </div>

            <div class="form-options">
              <label class="remember-me">
                <input type="checkbox" v-model="rememberMe" />
                <span class="checkmark"></span>
                Remember me
              </label>
              <a href="#" class="forgot-link">Forgot password?</a>
            </div>

            <!-- Error Alert -->
            <div v-if="error" class="error-alert">
              <v-icon size="20">mdi-alert-circle</v-icon>
              <span>{{ error }}</span>
              <button type="button" @click="error = ''">
                <v-icon size="18">mdi-close</v-icon>
              </button>
            </div>

            <button type="submit" class="submit-btn" :disabled="loading">
              <span v-if="loading" class="loading-spinner"></span>
              <template v-else>
                <v-icon size="20" class="mr-2">mdi-login</v-icon>
                Sign In
              </template>
            </button>
          </form>

          <div class="auth-divider">
            <span>or</span>
          </div>

          <div class="social-login">
            <button class="social-btn google">
              <v-icon size="20">mdi-google</v-icon>
              Google
            </button>
            <button class="social-btn github">
              <v-icon size="20">mdi-github</v-icon>
              GitHub
            </button>
          </div>

          <div class="auth-footer">
            <p>Don't have an account? <router-link to="/register">Create one</router-link></p>
          </div>

          <!-- Demo Credentials -->
          <div class="demo-credentials">
            <div class="demo-header">
              <v-icon size="16">mdi-information</v-icon>
              <span>Demo Credentials</span>
            </div>
            <div class="demo-content">
              <p><strong>Admin:</strong> admin@example.com / admin123</p>
            </div>
          </div>
        </div>
      </div>
    </v-container>
  </div>
</template>

<script setup>
import { ref, inject } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { useCartStore } from '@/stores/cart'

const router = useRouter()
const route = useRoute()
const authStore = useAuthStore()
const cartStore = useCartStore()
const showSnackbar = inject('showSnackbar')

const loading = ref(false)
const error = ref('')
const showPassword = ref(false)
const rememberMe = ref(false)

const form = ref({
  email: '',
  password: '',
})

const handleLogin = async () => {
  if (!form.value.email || !form.value.password) {
    error.value = 'Please fill in all fields'
    return
  }

  loading.value = true
  error.value = ''

  const result = await authStore.login(form.value.email, form.value.password)

  if (result.success) {
    showSnackbar('Login successful!', 'success')
    
    // Merge anonymous cart with user cart
    await cartStore.fetchCart()
    
    // Redirect to intended page or home
    const redirect = route.query.redirect || '/'
    router.push(redirect)
  } else {
    error.value = result.error
  }

  loading.value = false
}
</script>

<style scoped>
.auth-page {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  position: relative;
  padding: 40px 0;
}

/* Background Effects */
.auth-bg {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  overflow: hidden;
  z-index: 0;
}

.gradient-orb {
  position: absolute;
  border-radius: 50%;
  filter: blur(80px);
  opacity: 0.5;
}

.orb-1 {
  width: 400px;
  height: 400px;
  background: linear-gradient(135deg, #6366F1, #8B5CF6);
  top: -100px;
  right: -100px;
  animation: float 8s ease-in-out infinite;
}

.orb-2 {
  width: 300px;
  height: 300px;
  background: linear-gradient(135deg, #EC4899, #8B5CF6);
  bottom: -50px;
  left: -50px;
  animation: float 10s ease-in-out infinite reverse;
}

.orb-3 {
  width: 200px;
  height: 200px;
  background: linear-gradient(135deg, #10B981, #6366F1);
  top: 50%;
  left: 30%;
  animation: float 12s ease-in-out infinite;
}

@keyframes float {
  0%, 100% { transform: translate(0, 0); }
  50% { transform: translate(30px, -30px); }
}

.auth-container {
  position: relative;
  z-index: 1;
  max-width: 1000px;
}

/* Auth Card */
.auth-card {
  display: grid;
  grid-template-columns: 1fr 1fr;
  background: rgba(30, 30, 46, 0.8);
  backdrop-filter: blur(20px);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 24px;
  overflow: hidden;
  box-shadow: 0 25px 50px rgba(0, 0, 0, 0.3);
}

@media (max-width: 900px) {
  .auth-card {
    grid-template-columns: 1fr;
  }
  .auth-branding {
    display: none;
  }
}

/* Branding Side */
.auth-branding {
  background: linear-gradient(135deg, rgba(99, 102, 241, 0.2), rgba(139, 92, 246, 0.2));
  padding: 48px;
  display: flex;
  align-items: center;
  justify-content: center;
  position: relative;
  overflow: hidden;
}

.auth-branding::before {
  content: '';
  position: absolute;
  top: -50%;
  left: -50%;
  width: 200%;
  height: 200%;
  background: radial-gradient(circle, rgba(99, 102, 241, 0.1) 0%, transparent 70%);
  animation: rotate 20s linear infinite;
}

@keyframes rotate {
  from { transform: rotate(0deg); }
  to { transform: rotate(360deg); }
}

.brand-content {
  position: relative;
  z-index: 1;
  text-align: center;
}

.brand-logo {
  width: 80px;
  height: 80px;
  background: linear-gradient(135deg, #6366F1, #8B5CF6);
  border-radius: 20px;
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 0 auto 24px;
  color: white;
  box-shadow: 0 10px 30px rgba(99, 102, 241, 0.4);
}

.brand-content h2 {
  font-size: 2rem;
  font-weight: 700;
  color: #ffffff;
  margin-bottom: 12px;
}

.brand-content p {
  color: rgba(255, 255, 255, 0.7);
  margin-bottom: 32px;
}

.features-list {
  text-align: left;
}

.feature-item {
  display: flex;
  align-items: center;
  gap: 12px;
  color: rgba(255, 255, 255, 0.8);
  margin-bottom: 16px;
}

.feature-item .v-icon {
  color: #10B981;
}

/* Form Side */
.auth-form-section {
  padding: 48px;
}

.form-header {
  margin-bottom: 32px;
}

.form-header h1 {
  font-size: 2rem;
  font-weight: 700;
  color: #ffffff;
  margin-bottom: 8px;
}

.form-header p {
  color: rgba(255, 255, 255, 0.6);
}

/* Form Styles */
.form-group {
  margin-bottom: 24px;
}

.form-group label {
  display: block;
  font-size: 14px;
  font-weight: 500;
  color: rgba(255, 255, 255, 0.8);
  margin-bottom: 8px;
}

.input-wrapper {
  position: relative;
}

.input-icon {
  position: absolute;
  left: 16px;
  top: 50%;
  transform: translateY(-50%);
  color: rgba(255, 255, 255, 0.4);
}

.modern-input {
  width: 100%;
  padding: 16px 48px;
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 12px;
  color: #ffffff;
  font-size: 15px;
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

.toggle-password {
  position: absolute;
  right: 16px;
  top: 50%;
  transform: translateY(-50%);
  background: none;
  border: none;
  color: rgba(255, 255, 255, 0.4);
  cursor: pointer;
  padding: 0;
}

.toggle-password:hover {
  color: rgba(255, 255, 255, 0.7);
}

/* Form Options */
.form-options {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 24px;
}

.remember-me {
  display: flex;
  align-items: center;
  gap: 8px;
  color: rgba(255, 255, 255, 0.7);
  font-size: 14px;
  cursor: pointer;
}

.remember-me input {
  display: none;
}

.checkmark {
  width: 18px;
  height: 18px;
  border: 2px solid rgba(255, 255, 255, 0.3);
  border-radius: 4px;
  position: relative;
  transition: all 0.3s ease;
}

.remember-me input:checked + .checkmark {
  background: linear-gradient(135deg, #6366F1, #8B5CF6);
  border-color: transparent;
}

.remember-me input:checked + .checkmark::after {
  content: '';
  position: absolute;
  left: 5px;
  top: 2px;
  width: 5px;
  height: 9px;
  border: solid white;
  border-width: 0 2px 2px 0;
  transform: rotate(45deg);
}

.forgot-link {
  color: #8B5CF6;
  text-decoration: none;
  font-size: 14px;
  transition: color 0.3s ease;
}

.forgot-link:hover {
  color: #6366F1;
}

/* Error Alert */
.error-alert {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 14px 16px;
  background: rgba(239, 68, 68, 0.1);
  border: 1px solid rgba(239, 68, 68, 0.3);
  border-radius: 12px;
  color: #EF4444;
  margin-bottom: 24px;
}

.error-alert span {
  flex: 1;
  font-size: 14px;
}

.error-alert button {
  background: none;
  border: none;
  color: inherit;
  cursor: pointer;
  padding: 0;
}

/* Submit Button */
.submit-btn {
  width: 100%;
  padding: 16px;
  background: linear-gradient(135deg, #6366F1, #8B5CF6);
  border: none;
  border-radius: 12px;
  color: white;
  font-size: 16px;
  font-weight: 600;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.3s ease;
}

.submit-btn:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 10px 30px rgba(99, 102, 241, 0.4);
}

.submit-btn:disabled {
  opacity: 0.7;
  cursor: not-allowed;
}

.loading-spinner {
  width: 24px;
  height: 24px;
  border: 3px solid rgba(255, 255, 255, 0.3);
  border-top-color: white;
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

/* Divider */
.auth-divider {
  display: flex;
  align-items: center;
  margin: 24px 0;
  color: rgba(255, 255, 255, 0.4);
  font-size: 14px;
}

.auth-divider::before,
.auth-divider::after {
  content: '';
  flex: 1;
  height: 1px;
  background: rgba(255, 255, 255, 0.1);
}

.auth-divider span {
  padding: 0 16px;
}

/* Social Login */
.social-login {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 12px;
}

.social-btn {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  padding: 14px;
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 12px;
  color: rgba(255, 255, 255, 0.8);
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.3s ease;
}

.social-btn:hover {
  background: rgba(255, 255, 255, 0.1);
  border-color: rgba(255, 255, 255, 0.2);
}

/* Auth Footer */
.auth-footer {
  text-align: center;
  margin-top: 24px;
  color: rgba(255, 255, 255, 0.6);
  font-size: 14px;
}

.auth-footer a {
  color: #8B5CF6;
  text-decoration: none;
  font-weight: 500;
}

.auth-footer a:hover {
  color: #6366F1;
}

/* Demo Credentials */
.demo-credentials {
  margin-top: 24px;
  background: rgba(99, 102, 241, 0.1);
  border: 1px solid rgba(99, 102, 241, 0.2);
  border-radius: 12px;
  overflow: hidden;
}

.demo-header {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 12px 16px;
  background: rgba(99, 102, 241, 0.1);
  color: #8B5CF6;
  font-size: 13px;
  font-weight: 600;
}

.demo-content {
  padding: 12px 16px;
}

.demo-content p {
  font-size: 13px;
  color: rgba(255, 255, 255, 0.7);
  margin: 0;
}
</style>
