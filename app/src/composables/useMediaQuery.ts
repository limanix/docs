import { onBeforeUnmount, onMounted, readonly, ref } from 'vue'

export function useMediaQuery(query: string) {
  const matches = ref(false)
  let list: MediaQueryList | undefined

  const update = () => {
    matches.value = list?.matches ?? false
  }

  onMounted(() => {
    list = window.matchMedia(query)
    update()
    list.addEventListener('change', update)
  })

  onBeforeUnmount(() => list?.removeEventListener('change', update))

  return readonly(matches)
}
