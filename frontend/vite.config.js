import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';

export default defineConfig({
  plugins: [react()],
  server: {
    port: 5173,
    proxy: {
      '/api': 'http://localhost:8000',
    },
    // Correct way for Vite 4+ to fix SPA reload black screen
    fs: { allow: ['..'] },
    middlewareMode: false,
  },
  preview: {
    port: 4173,
  },
  // Use this for SPA fallback
  build: {
    rollupOptions: {
      output: {
        manualChunks: undefined,
      },
    },
  },
  resolve: {
    alias: {
      '@': '/src',
    },
  },
  // Vite 4+ SPA fallback
  appType: 'spa',
});
