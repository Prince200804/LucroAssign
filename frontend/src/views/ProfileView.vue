<template>
  <v-container class="py-8">
    <h1 class="text-h4 font-weight-bold mb-6">My Profile</h1>

    <v-row>
      <v-col cols="12" md="4">
        <v-card class="pa-6 text-center">
          <v-avatar size="120" color="primary">
            <span class="text-h3 text-white">{{ initials }}</span>
          </v-avatar>
          <h2 class="text-h5 font-weight-bold mt-4">{{ fullName }}</h2>
          <p class="text-body-2 text-grey">{{ user?.email }}</p>
          <v-chip
            v-if="isAdmin"
            color="warning"
            class="mt-2"
            prepend-icon="mdi-shield-crown"
          >
            Admin
          </v-chip>
        </v-card>
      </v-col>

      <v-col cols="12" md="8">
        <v-card class="pa-6">
          <v-tabs v-model="tab" color="primary">
            <v-tab value="profile">Profile Info</v-tab>
            <v-tab value="password">Change Password</v-tab>
          </v-tabs>

          <v-window v-model="tab" class="mt-6">
            <!-- Profile Tab -->
            <v-window-item value="profile">
              <v-form ref="profileFormRef" @submit.prevent="updateProfile">
                <v-row>
                  <v-col cols="12" sm="6">
                    <v-text-field
                      v-model="profileForm.first_name"
                      label="First Name"
                      prepend-inner-icon="mdi-account"
                    ></v-text-field>
                  </v-col>
                  <v-col cols="12" sm="6">
                    <v-text-field
                      v-model="profileForm.last_name"
                      label="Last Name"
                      prepend-inner-icon="mdi-account"
                    ></v-text-field>
                  </v-col>
                  <v-col cols="12" sm="6">
                    <v-text-field
                      v-model="profileForm.phone"
                      label="Phone"
                      prepend-inner-icon="mdi-phone"
                    ></v-text-field>
                  </v-col>
                  <v-col cols="12">
                    <v-textarea
                      v-model="profileForm.address"
                      label="Address"
                      rows="2"
                      prepend-inner-icon="mdi-map-marker"
                    ></v-textarea>
                  </v-col>
                  <v-col cols="12" sm="6">
                    <v-text-field
                      v-model="profileForm.city"
                      label="City"
                      prepend-inner-icon="mdi-city"
                    ></v-text-field>
                  </v-col>
                  <v-col cols="12" sm="6">
                    <v-text-field
                      v-model="profileForm.state"
                      label="State"
                      prepend-inner-icon="mdi-map"
                    ></v-text-field>
                  </v-col>
                  <v-col cols="12" sm="6">
                    <v-text-field
                      v-model="profileForm.zip_code"
                      label="ZIP Code"
                      prepend-inner-icon="mdi-mailbox"
                    ></v-text-field>
                  </v-col>
                  <v-col cols="12" sm="6">
                    <v-text-field
                      v-model="profileForm.country"
                      label="Country"
                      prepend-inner-icon="mdi-earth"
                    ></v-text-field>
                  </v-col>
                </v-row>

                <v-btn
                  color="primary"
                  type="submit"
                  :loading="profileLoading"
                  class="mt-4"
                >
                  Update Profile
                </v-btn>
              </v-form>
            </v-window-item>

            <!-- Password Tab -->
            <v-window-item value="password">
              <v-form ref="passwordFormRef" v-model="passwordValid" @submit.prevent="changePassword">
                <v-text-field
                  v-model="passwordForm.old_password"
                  label="Current Password"
                  type="password"
                  :rules="[rules.required]"
                  prepend-inner-icon="mdi-lock"
                  class="mb-4"
                ></v-text-field>

                <v-text-field
                  v-model="passwordForm.new_password"
                  label="New Password"
                  type="password"
                  :rules="[rules.required, rules.minLength(8)]"
                  prepend-inner-icon="mdi-lock-plus"
                  class="mb-4"
                ></v-text-field>

                <v-text-field
                  v-model="passwordForm.new_password_confirm"
                  label="Confirm New Password"
                  type="password"
                  :rules="[rules.required, rules.match(passwordForm.new_password)]"
                  prepend-inner-icon="mdi-lock-check"
                  class="mb-4"
                ></v-text-field>

                <v-alert
                  v-if="passwordError"
                  type="error"
                  variant="tonal"
                  class="mb-4"
                  closable
                  @click:close="passwordError = ''"
                >
                  {{ passwordError }}
                </v-alert>

                <v-btn
                  color="primary"
                  type="submit"
                  :loading="passwordLoading"
                  :disabled="!passwordValid"
                >
                  Change Password
                </v-btn>
              </v-form>
            </v-window-item>
          </v-window>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script setup>
import { ref, computed, inject, onMounted } from 'vue'
import { useAuthStore } from '@/stores/auth'

const authStore = useAuthStore()
const showSnackbar = inject('showSnackbar')

const tab = ref('profile')
const profileFormRef = ref(null)
const passwordFormRef = ref(null)
const passwordValid = ref(false)
const profileLoading = ref(false)
const passwordLoading = ref(false)
const passwordError = ref('')

const user = computed(() => authStore.user)
const isAdmin = computed(() => authStore.isAdmin)
const fullName = computed(() => `${user.value?.first_name || ''} ${user.value?.last_name || ''}`.trim() || 'User')
const initials = computed(() => {
  const first = user.value?.first_name?.[0] || ''
  const last = user.value?.last_name?.[0] || ''
  return (first + last).toUpperCase() || 'U'
})

const profileForm = ref({
  first_name: '',
  last_name: '',
  phone: '',
  address: '',
  city: '',
  state: '',
  zip_code: '',
  country: '',
})

const passwordForm = ref({
  old_password: '',
  new_password: '',
  new_password_confirm: '',
})

const rules = {
  required: v => !!v || 'This field is required',
  minLength: (len) => v => (v && v.length >= len) || `Minimum ${len} characters required`,
  match: (val) => v => v === val || 'Passwords do not match',
}

const updateProfile = async () => {
  profileLoading.value = true
  const result = await authStore.updateProfile(profileForm.value)
  
  if (result.success) {
    showSnackbar('Profile updated successfully!', 'success')
  } else {
    showSnackbar('Failed to update profile', 'error')
  }
  
  profileLoading.value = false
}

const changePassword = async () => {
  passwordLoading.value = true
  passwordError.value = ''
  
  const result = await authStore.changePassword(passwordForm.value)
  
  if (result.success) {
    showSnackbar('Password changed successfully!', 'success')
    passwordForm.value = {
      old_password: '',
      new_password: '',
      new_password_confirm: '',
    }
    passwordFormRef.value?.reset()
  } else {
    passwordError.value = result.error
  }
  
  passwordLoading.value = false
}

onMounted(() => {
  if (user.value) {
    profileForm.value = {
      first_name: user.value.first_name || '',
      last_name: user.value.last_name || '',
      phone: user.value.phone || '',
      address: user.value.address || '',
      city: user.value.city || '',
      state: user.value.state || '',
      zip_code: user.value.zip_code || '',
      country: user.value.country || '',
    }
  }
})
</script>
