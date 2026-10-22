import { createSSRApp } from 'vue'
import type { RouterHistory } from 'vue-router'
import App from './App.vue'
import { createAppRouter } from './router'

export function createApp(history: RouterHistory) {
  const app = createSSRApp(App)
  const router = createAppRouter(history)
  app.use(router)
  return { app, router }
}
