import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [react()],
  build: {
    rollupOptions: {
      output: {
        manualChunks: {
          plotly: ['plotly.js-dist-min', 'react-plotly.js'],
          leaflet: ['leaflet', 'react-leaflet'],
          vendor: ['react', 'react-dom', 'axios', 'lucide-react']
        }
      }
    },
    chunkSizeWarningLimit: 3500
  },
  server: {
    port: 5173,
    proxy: {
      '/api': {
        target: 'http://127.0.0.1:8000',
        changeOrigin: true,
        secure: false,
      }
    }
  }
})
