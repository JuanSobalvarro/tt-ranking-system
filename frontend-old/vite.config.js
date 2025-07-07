import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// https://vite.dev/config/
export default defineConfig({
  plugins: [react()],
  server: {
    hmr: true,
    port: 8080,
    host: '0.0.0.0',
    proxy: {
      '/api': {
        target: 'http://backend:8000', // Django backend URL
        changeOrigin: true,
        secure: false,
      },
    },
    watch: {
        usePolling: true,
    }
  },
  resolve: {
    alias: {
      src: "/src",
      pages: "/src/pages",
      components: "/src/components",
      styles: "/src/styles",
      services: "/src/services",
      assets: "/src/assets",
      lib: "/src/lib",
    },
  },
});
