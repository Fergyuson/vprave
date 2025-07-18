import { fileURLToPath, URL } from 'node:url'

import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import vueDevTools from 'vite-plugin-vue-devtools'


// https://vite.dev/config/
export default defineConfig({
  plugins: [
    vue(),
    vueDevTools(),
  ],
  resolve: {
    alias: {
      '@': fileURLToPath(new URL('./src', import.meta.url))
    },
  },
  build: {
    outDir: 'dist',
    assetsDir: 'assets',
    // Генерирует manifest.json для лучшего кэширования
    manifest: false,
    // Минимальный размер чанка
    rollupOptions: {
      output: {
        // Группируем CSS и JS файлы
        manualChunks: undefined,
      }
    }
  },
  // Base URL для production - оставляем пустым так как раздаем с корня
  base: '/',
})
