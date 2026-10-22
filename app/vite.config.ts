import { fileURLToPath, URL } from 'node:url'
import vue from '@vitejs/plugin-vue'
import { defineConfig } from 'vite'

const page = (name: string) => fileURLToPath(new URL(`./${name}.html`, import.meta.url))

export default defineConfig({
  plugins: [vue()],
  resolve: {
    alias: {
      '@': fileURLToPath(new URL('./src', import.meta.url)),
    },
  },
  build: {
    rolldownOptions: {
      input: { index: page('index'), download: page('download') },
      output: {
        codeSplitting: {
          groups: [{ name: 'vue', test: /node_modules[\\/](?:@vue|vue|vue-router)[\\/]/ }],
        },
      },
    },
  },
})
