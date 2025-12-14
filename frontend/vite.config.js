import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

export default defineConfig({
  plugins: [vue()],
  server: {
    host: '0.0.0.0', // Allow external access
    port: 5173,
    proxy: {
      '/api': {
        target: 'http://192.168.1.18:8000',
        changeOrigin: true,
      }
    }
  }
})
