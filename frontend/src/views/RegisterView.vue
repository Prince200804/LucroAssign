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
              <v-icon size="48">mdi-account-plus</v-icon>
            </div>
            <h2>Join Us Today!</h2>
            <p>Create an account and unlock exclusive benefits</p>
            
            <div class="features-list">
              <div class="feature-item">
                <v-icon size="20">mdi-check-circle</v-icon>
                <span>Personalized recommendations</span>
              </div>
              <div class="feature-item">
                <v-icon size="20">mdi-check-circle</v-icon>
                <span>Faster checkout</span>
              </div>
              <div class="feature-item">
                <v-icon size="20">mdi-check-circle</v-icon>
                <span>Order tracking</span>
              </div>
              <div class="feature-item">
                <v-icon size="20">mdi-check-circle</v-icon>
                <span>Exclusive offers</span>
              </div>
            </div>
          </div>
        </div>

        <!-- Right Side - Form -->
        <div class="auth-form-section">
          <div class="form-header">
            <h1>Create Account</h1>
            <p>Fill in your details to get started</p>
          </div>

          <form @submit.prevent="handleRegister" class="auth-form">
            <div class="form-row">
              <div class="form-group">
                <label for="firstName">First Name</label>
                <div class="input-wrapper">
                  <v-icon class="input-icon">mdi-account-outline</v-icon>
                  <input
                    id="firstName"
                    v-model="form.first_name"
                    type="text"
                    placeholder="John"
                    class="modern-input"
                    required
                  />
                </div>
              </div>
              <div class="form-group">
                <label for="lastName">Last Name</label>
                <div class="input-wrapper">
                  <v-icon class="input-icon">mdi-account-outline</v-icon>
                  <input
                    id="lastName"
                    v-model="form.last_name"
                    type="text"
                    placeholder="Doe"
                    class="modern-input"
                    required
                  />
                </div>
              </div>
            </div>

            <div class="form-group">
              <label for="username">Username</label>
              <div class="input-wrapper">
                <v-icon class="input-icon">mdi-at</v-icon>
                <input
                  id="username"
                  v-model="form.username"
                  type="text"
                  placeholder="Choose a username"
                  class="modern-input"
                  :class="{ error: errors.username }"
                  required
                />
              </div>
              <span v-if="errors.username" class="field-error">{{ errors.username }}</span>
            </div>

            <div class="form-group">
              <label for="email">Email Address</label>
              <div class="input-wrapper">
                <v-icon class="input-icon">mdi-email-outline</v-icon>
                <input
                  id="email"
                  v-model="form.email"
                  type="email"
                  placeholder="john@example.com"
                  class="modern-input"
                  :class="{ error: errors.email }"
                  required
                />
              </div>
              <span v-if="errors.email" class="field-error">{{ errors.email }}</span>
            </div>

            <div class="form-group">
              <label for="phone">Phone (Optional)</label>
              <div class="input-wrapper">
                <v-icon class="input-icon">mdi-phone-outline</v-icon>
                <input
                  id="phone"
                  v-model="form.phone"
                  type="tel"
                  placeholder="+1 (555) 000-0000"
                  class="modern-input"
                />
              </div>
            </div>

            <div class="form-row">
              <div class="form-group">
                <label for="password">Password</label>
                <div class="input-wrapper">
                  <v-icon class="input-icon">mdi-lock-outline</v-icon>
                  <input
                    id="password"
                    v-model="form.password"
                    :type="showPassword ? 'text' : 'password'"
                    placeholder="Min 8 characters"
                    class="modern-input"
                    :class="{ error: errors.password }"
                    required
                  />
                  <button type="button" class="toggle-password" @click="showPassword = !showPassword">
                    <v-icon size="20">{{ showPassword ? 'mdi-eye-off' : 'mdi-eye' }}</v-icon>
                  </button>
                </div>
                <span v-if="errors.password" class="field-error">{{ errors.password }}</span>
              </div>
              <div class="form-group">
                <label for="confirmPassword">Confirm Password</label>
                <div class="input-wrapper">
                  <v-icon class="input-icon">mdi-lock-check-outline</v-icon>
                  <input
                    id="confirmPassword"
                    v-model="form.password_confirm"
                    :type="showPassword ? 'text' : 'password'"
                    placeholder="Re-enter password"
                    class="modern-input"
                    required
                  />
                </div>
              </div>
            </div>

            <!-- Terms -->
            <div class="terms-checkbox">
              <label class="custom-checkbox">
                <input type="checkbox" v-model="agreeTerms" required />
                <span class="checkmark"></span>
                I agree to the <a href="#">Terms of Service</a> and <a href="#">Privacy Policy</a>
              </label>
            </div>

            <!-- Error Alert -->
            <div v-if="generalError" class="error-alert">
              <v-icon size="20">mdi-alert-circle</v-icon>
              <span>{{ generalError }}</span>
              <button type="button" @click="generalError = ''">
                <v-icon size="18">mdi-close</v-icon>
              </button>
            </div>

            <button type="submit" class="submit-btn" :disabled="loading || !agreeTerms">
              <span v-if="loading" class="loading-spinner"></span>
              <template v-else>
                <v-icon size="20" class="mr-2">mdi-account-plus</v-icon>
                Create Account
              </template>
            </button>
          </form>

          <div class="auth-divider">
            <span>or sign up with</span>
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
            <p>Already have an account? <router-link to="/login">Sign in</router-link></p>
          </div>
        </div>
      </div>
    </v-container>
  </div>
</template>

<script setup>
import { ref, inject } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const router = useRouter()
const authStore = useAuthStore()
const showSnackbar = inject('showSnackbar')

const loading = ref(false)
const showPassword = ref(false)
const generalError = ref('')
const errors = ref({})
const agreeTerms = ref(false)

const form = ref({
  first_name: '',
  last_name: '',
  username: '',
  email: '',
  phone: '',
  password: '',
  password_confirm: '',
})

const handleRegister = async () => {
  if (!form.value.first_name || !form.value.last_name || !form.value.username || 
      !form.value.email || !form.value.password || !form.value.password_confirm) {
    generalError.value = 'Please fill in all required fields'
    return
  }

  if (form.value.password.length < 8) {
    errors.value = { password: 'Password must be at least 8 characters' }
    return
  }

  if (form.value.password !== form.value.password_confirm) {
    generalError.value = 'Passwords do not match'
    return
  }

  loading.value = true
  errors.value = {}
  generalError.value = ''

  const result = await authStore.register(form.value)

  if (result.success) {
    showSnackbar('Account created successfully!', 'success')
    router.push('/')
  } else {
    if (result.errors.general) {
      generalError.value = result.errors.general
    } else {
      errors.value = result.errors
    }
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
  background: linear-gradient(135deg, #8B5CF6, #EC4899);
  top: -100px;
  left: -100px;
  animation: float 8s ease-in-out infinite;
}

.orb-2 {
  width: 300px;
  height: 300px;
  background: linear-gradient(135deg, #6366F1, #10B981);
  bottom: -50px;
  right: -50px;
  animation: float 10s ease-in-out infinite reverse;
}

.orb-3 {
  width: 200px;
  height: 200px;
  background: linear-gradient(135deg, #EC4899, #6366F1);
  top: 40%;
  right: 20%;
  animation: float 12s ease-in-out infinite;
}

@keyframes float {
  0%, 100% { transform: translate(0, 0); }
  50% { transform: translate(30px, -30px); }
}

.auth-container {
  position: relative;
  z-index: 1;
  max-width: 1100px;
}

/* Auth Card */
.auth-card {
  display: grid;
  grid-template-columns: 1fr 1.3fr;
  background: rgba(30, 30, 46, 0.8);
  backdrop-filter: blur(20px);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 24px;
  overflow: hidden;
  box-shadow: 0 25px 50px rgba(0, 0, 0, 0.3);
}

@media (max-width: 960px) {
  .auth-card {
    grid-template-columns: 1fr;
  }
  .auth-branding {
    display: none;
  }
}

/* Branding Side */
.auth-branding {
  background: linear-gradient(135deg, rgba(139, 92, 246, 0.2), rgba(236, 72, 153, 0.2));
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
  background: radial-gradient(circle, rgba(139, 92, 246, 0.1) 0%, transparent 70%);
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
  background: linear-gradient(135deg, #8B5CF6, #EC4899);
  border-radius: 20px;
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 0 auto 24px;
  color: white;
  box-shadow: 0 10px 30px rgba(139, 92, 246, 0.4);
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
  padding: 40px 48px;
  max-height: 90vh;
  overflow-y: auto;
}

.form-header {
  margin-bottom: 28px;
}

.form-header h1 {
  font-size: 1.8rem;
  font-weight: 700;
  color: #ffffff;
  margin-bottom: 8px;
}

.form-header p {
  color: rgba(255, 255, 255, 0.6);
}

/* Form Styles */
.form-row {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 16px;
}

@media (max-width: 600px) {
  .form-row {
    grid-template-columns: 1fr;
  }
}

.form-group {
  margin-bottom: 20px;
}

.form-group label {
  display: block;
  font-size: 13px;
  font-weight: 500;
  color: rgba(255, 255, 255, 0.8);
  margin-bottom: 8px;
}

.input-wrapper {
  position: relative;
}

.input-icon {
  position: absolute;
  left: 14px;
  top: 50%;
  transform: translateY(-50%);
  color: rgba(255, 255, 255, 0.4);
  font-size: 18px;
}

.modern-input {
  width: 100%;
  padding: 14px 44px;
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 12px;
  color: #ffffff;
  font-size: 14px;
  transition: all 0.3s ease;
}

.modern-input:focus {
  outline: none;
  border-color: #8B5CF6;
  background: rgba(139, 92, 246, 0.1);
}

.modern-input.error {
  border-color: #EF4444;
}

.modern-input::placeholder {
  color: rgba(255, 255, 255, 0.4);
}

.toggle-password {
  position: absolute;
  right: 14px;
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

.field-error {
  display: block;
  font-size: 12px;
  color: #EF4444;
  margin-top: 6px;
}

/* Terms Checkbox */
.terms-checkbox {
  margin-bottom: 24px;
}

.custom-checkbox {
  display: flex;
  align-items: flex-start;
  gap: 10px;
  font-size: 13px;
  color: rgba(255, 255, 255, 0.7);
  cursor: pointer;
  line-height: 1.4;
}

.custom-checkbox input {
  display: none;
}

.custom-checkbox .checkmark {
  min-width: 18px;
  height: 18px;
  border: 2px solid rgba(255, 255, 255, 0.3);
  border-radius: 4px;
  position: relative;
  transition: all 0.3s ease;
  margin-top: 2px;
}

.custom-checkbox input:checked + .checkmark {
  background: linear-gradient(135deg, #8B5CF6, #EC4899);
  border-color: transparent;
}

.custom-checkbox input:checked + .checkmark::after {
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

.custom-checkbox a {
  color: #8B5CF6;
  text-decoration: none;
}

.custom-checkbox a:hover {
  text-decoration: underline;
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
  background: linear-gradient(135deg, #8B5CF6, #EC4899);
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
  box-shadow: 0 10px 30px rgba(139, 92, 246, 0.4);
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
  font-size: 13px;
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
  color: #EC4899;
}
</style>
