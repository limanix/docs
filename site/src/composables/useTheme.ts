import { computed, onMounted, ref } from 'vue'
import { useMediaQuery } from '@/composables/useMediaQuery'

export type Theme = 'light' | 'dark'

const KEY = 'theme'

function storedTheme(): Theme | null {
  try {
    const value = localStorage.getItem(KEY)
    return value === 'light' || value === 'dark' ? value : null
  } catch {
    return null
  }
}

const chosen = ref<Theme | null>(null)

export function useTheme() {
  const prefersLight = useMediaQuery('(prefers-color-scheme: light)')
  const theme = computed<Theme>(() => chosen.value ?? (prefersLight.value ? 'light' : 'dark'))

  onMounted(() => {
    chosen.value = storedTheme()
  })

  const toggle = () => {
    const next: Theme = theme.value === 'light' ? 'dark' : 'light'
    chosen.value = next
    const root = document.documentElement
    root.classList.add('u-instant')
    root.dataset.theme = next
    const page = getComputedStyle(root).getPropertyValue('--color-page').trim()
    window.setTimeout(() => root.classList.remove('u-instant'))
    for (const meta of document.querySelectorAll<HTMLMetaElement>('meta[name="theme-color"]')) {
      meta.content = page
    }
    try {
      localStorage.setItem(KEY, next)
    } catch {}
  }

  return { theme, toggle }
}
