<template>
  <v-container class="py-8 text-center">
    <v-icon size="120" color="error">mdi-alert-circle-outline</v-icon>
    <h1 class="text-h3 font-weight-bold mt-6 mb-4">404</h1>
    <h2 class="text-h5 mb-4">Page Not Found</h2>
    <p class="text-body-1 text-grey mb-6">
      The page you're looking for doesn't exist or has been moved.
    </p>
    <v-btn color="primary" size="large" to="/">
      <v-icon left>mdi-home</v-icon>
      Go to Home
    </v-btn>
  </v-container>
</template>
