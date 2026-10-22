import { renderToString } from 'vue/server-renderer'
import { createMemoryHistory } from 'vue-router'
import { createApp } from './app'

export async function render(url: string) {
  const { app, router } = createApp(createMemoryHistory())
  await router.push(url)
  await router.isReady()
  return renderToString(app)
}
