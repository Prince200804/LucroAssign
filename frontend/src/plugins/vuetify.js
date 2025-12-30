import 'vuetify/styles'
import { createVuetify } from 'vuetify'
import * as components from 'vuetify/components'
import * as directives from 'vuetify/directives'
import '@mdi/font/css/materialdesignicons.css'

const vuetify = createVuetify({
  components,
  directives,
  theme: {
    defaultTheme: 'dark',
    themes: {
      light: {
        dark: false,
        colors: {
          primary: '#6366f1',
          'primary-darken-1': '#4f46e5',
          secondary: '#8b5cf6',
          accent: '#06b6d4',
          error: '#ef4444',
          info: '#3b82f6',
          success: '#22c55e',
          warning: '#f59e0b',
          background: '#fafafa',
          surface: '#ffffff',
        }
      },
      dark: {
        dark: true,
        colors: {
          primary: '#6366f1',
          'primary-darken-1': '#4f46e5',
          secondary: '#8b5cf6',
          accent: '#06b6d4',
          error: '#ef4444',
          info: '#3b82f6',
          success: '#22c55e',
          warning: '#f59e0b',
          background: '#0a0a0a',
          surface: '#141414',
          'surface-variant': '#1a1a1a',
          'on-background': '#ffffff',
          'on-surface': '#e5e5e5',
        }
      }
    }
  },
  defaults: {
    VBtn: {
      variant: 'flat',
      rounded: 'xl',
    },
    VCard: {
      rounded: 'xl',
      elevation: 0,
    },
    VTextField: {
      variant: 'outlined',
      density: 'comfortable',
      rounded: 'lg',
    },
    VSelect: {
      variant: 'outlined',
      density: 'comfortable',
      rounded: 'lg',
    },
    VChip: {
      rounded: 'lg',
    },
  }
})

export default vuetify
