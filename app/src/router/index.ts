import { createRouter, type RouterHistory } from 'vue-router'
import DownloadView from '@/views/DownloadView.vue'
import HomeView from '@/views/HomeView.vue'

export function createAppRouter(history: RouterHistory) {
  return createRouter({
    history,
    scrollBehavior: (to, _from, saved) => {
      if (saved) return { ...saved, behavior: 'instant' }
      return to.hash ? { el: to.hash } : { top: 0, behavior: 'instant' }
    },
    routes: [
      {
        path: '/',
        name: 'home',
        component: HomeView,
      },
      {
        path: '/download',
        name: 'download',
        component: DownloadView,
      },
      {
        path: '/:pathMatch(.*)*',
        component: HomeView,
      },
    ],
  })
}
