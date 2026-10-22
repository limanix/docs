import '@fontsource-variable/inter'
import '@fontsource-variable/jetbrains-mono'
import '@/styles/main.scss'

import { createWebHistory } from 'vue-router'
import { createApp } from './app'

const { app, router } = createApp(createWebHistory(import.meta.env.BASE_URL))

router.isReady().then(() => app.mount('#app'))
