import { onBeforeUnmount, onMounted, ref } from 'vue'

export function useScrolled(offset: number) {
  const scrolled = ref(false)

  const update = () => {
    scrolled.value = window.scrollY > offset
  }

  onMounted(() => {
    update()
    window.addEventListener('scroll', update, { passive: true })
  })

  onBeforeUnmount(() => window.removeEventListener('scroll', update))

  return scrolled
}
